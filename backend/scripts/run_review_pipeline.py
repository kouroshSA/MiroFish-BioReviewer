"""
MiroFish-BioReviewer end-to-end review pipeline driver.

Designed to be called from the Google Colab notebook (or any non-UI context):
takes a proposal file path + simulation_request + max_rounds, and runs:

  1. Project bootstrap + text extraction
  2. Ontology generation
  3. ZEP graph build (synchronous wait)
  4. Simulation create + prepare
  5. Simulation run (parallel Twitter+Reddit) with max_rounds cap
  6. Reviewer panel (when SIMULATION_MODE=grant_review) + Report generation

Exits 0 on success and prints a summary block with the report path; exits non-zero
on any unrecoverable failure.

Usage:
  python backend/scripts/run_review_pipeline.py \
      --proposal /path/to/proposal.pdf \
      --request  "Review this systems biology grant pre-proposal..." \
      --max-rounds 40 \
      --output-dir colab_output \
      --mode grant_review
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Resolve repo paths
_scripts_dir = os.path.dirname(os.path.abspath(__file__))
_backend_dir = os.path.abspath(os.path.join(_scripts_dir, ".."))
_project_root = os.path.abspath(os.path.join(_backend_dir, ".."))
sys.path.insert(0, _backend_dir)

from dotenv import load_dotenv  # noqa: E402

_env_file = os.path.join(_project_root, ".env")
if os.path.exists(_env_file):
    load_dotenv(_env_file)

# These imports require backend/ to be on sys.path
from app.config import Config  # noqa: E402
from app.models.project import ProjectManager  # noqa: E402
from app.models.task import TaskStatus  # noqa: E402
from app.utils.file_parser import FileParser  # noqa: E402
from app.services.ontology_generator import OntologyGenerator  # noqa: E402
from app.services.graph_builder import GraphBuilderService  # noqa: E402
from app.services.simulation_manager import SimulationManager  # noqa: E402
from app.services.simulation_runner import SimulationRunner, RunnerStatus  # noqa: E402
from app.services.report_agent import ReportAgent  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MiroFish-BioReviewer end-to-end pipeline")
    p.add_argument("--proposal", required=True, help="Path to the proposal file (PDF/MD/TXT)")
    p.add_argument(
        "--request",
        required=True,
        help="Simulation request — what the swarm should debate/evaluate",
    )
    p.add_argument(
        "--max-rounds",
        type=int,
        default=40,
        help="Maximum simulation rounds (default: 40 — Colab default)",
    )
    p.add_argument(
        "--output-dir",
        default=None,
        help="Directory the final report will be copied into (optional)",
    )
    p.add_argument(
        "--mode",
        default=None,
        help="Override SIMULATION_MODE for this run (e.g. grant_review)",
    )
    p.add_argument(
        "--name",
        default="Colab BioReviewer Run",
        help="Project display name",
    )
    p.add_argument(
        "--graph-build-timeout",
        type=int,
        default=900,
        help="Seconds to wait for graph build to finish (default 900)",
    )
    p.add_argument(
        "--sim-timeout",
        type=int,
        default=3600,
        help="Seconds to wait for simulation to finish (default 3600)",
    )
    return p.parse_args()


def _validate_env() -> None:
    errors = Config.validate()
    if errors:
        for err in errors:
            print(f"[FATAL] Missing config: {err}", file=sys.stderr)
        sys.exit(2)


def _bootstrap_project(proposal_path: str, name: str) -> tuple:
    """Create project, save the uploaded file, extract text, persist it.
    Returns (project, document_text)."""
    project = ProjectManager.create_project(name=name)
    print(f"[1/6] Project created: {project.project_id}")

    with open(proposal_path, "rb") as f:
        file_bytes = f.read()
    file_info = ProjectManager.save_file_to_project(
        project.project_id,
        os.path.basename(proposal_path),
        file_bytes,
    )
    print(f"      → saved file: {file_info['path']} ({file_info['size']:,} bytes)")

    text = FileParser.extract_text(file_info["path"])
    if not text or len(text.strip()) < 50:
        raise RuntimeError(
            f"Extracted text is empty or too short ({len(text or '')} chars) — "
            f"cannot build a useful review."
        )
    ProjectManager.save_extracted_text(project.project_id, text)
    print(f"      → extracted text: {len(text):,} chars")
    return project, text


def _generate_ontology_and_graph(
    project, document_text: str, simulation_request: str, build_timeout: int
) -> str:
    """Run ontology generator + ZEP graph build (sync wait)."""
    print(f"[2/6] Generating ontology...")
    ontology = OntologyGenerator().generate(
        document_texts=[document_text],
        simulation_requirement=simulation_request,
    )
    project.ontology = ontology
    ProjectManager.save_project(project)
    print(
        f"      → entity_types={len(ontology.get('entity_types', []))}, "
        f"edge_types={len(ontology.get('edge_types', []))}"
    )

    print(f"[3/6] Building ZEP graph (this can take several minutes)...")
    gb = GraphBuilderService()
    task_id = gb.build_graph_async(
        text=document_text,
        ontology=ontology,
        graph_name=f"BioReviewer-{project.project_id}",
    )

    deadline = time.time() + build_timeout
    last_msg = ""
    while time.time() < deadline:
        task = gb.task_manager.get_task(task_id)
        if task is None:
            time.sleep(2)
            continue
        if task.message and task.message != last_msg:
            print(f"      [{task.progress:>3}%] {task.message}")
            last_msg = task.message
        if task.status == TaskStatus.COMPLETED:
            graph_id = task.result.get("graph_id")
            project.graph_id = graph_id
            ProjectManager.save_project(project)
            print(f"      → graph_id: {graph_id}")
            return graph_id
        if task.status == TaskStatus.FAILED:
            raise RuntimeError(f"Graph build failed: {task.error}")
        time.sleep(3)
    raise TimeoutError(f"Graph build did not finish within {build_timeout}s")


def _run_simulation(
    graph_id: str,
    project_id: str,
    document_text: str,
    simulation_request: str,
    max_rounds: int,
    sim_timeout: int,
) -> str:
    """Create + prepare + run simulation, blocking until COMPLETED. Returns simulation_id."""
    sm = SimulationManager()
    sim_state = sm.create_simulation(
        project_id=project_id,
        graph_id=graph_id,
        enable_twitter=True,
        enable_reddit=True,
    )
    print(f"[4/6] Simulation created: {sim_state.simulation_id}")

    print(f"      → preparing (entity read, profile gen, config gen)...")
    sm.prepare_simulation(
        simulation_id=sim_state.simulation_id,
        simulation_requirement=simulation_request,
        document_text=document_text,
    )
    print(f"      → prepare complete: {sim_state.entities_count} entities, "
          f"{sim_state.profiles_count} profiles")

    print(f"[5/6] Starting simulation (max_rounds={max_rounds})...")
    SimulationRunner.start_simulation(
        simulation_id=sim_state.simulation_id,
        platform="parallel",
        max_rounds=max_rounds,
    )

    deadline = time.time() + sim_timeout
    last_round = -1
    while time.time() < deadline:
        run_state = SimulationRunner.get_run_state(sim_state.simulation_id)
        if run_state is None:
            time.sleep(2)
            continue
        if run_state.current_round != last_round:
            print(
                f"      round {run_state.current_round}/{run_state.total_rounds} "
                f"(twitter={run_state.twitter_actions_count} reddit={run_state.reddit_actions_count}) "
                f"status={run_state.runner_status}"
            )
            last_round = run_state.current_round
        if run_state.runner_status == RunnerStatus.COMPLETED:
            print(f"      → simulation complete")
            try:
                SimulationRunner.close_simulation_env(sim_state.simulation_id)
            except Exception:
                pass
            return sim_state.simulation_id
        if run_state.runner_status == RunnerStatus.FAILED:
            raise RuntimeError(f"Simulation failed: {run_state.error}")
        time.sleep(5)
    raise TimeoutError(f"Simulation did not finish within {sim_timeout}s")


def _generate_report(graph_id: str, simulation_id: str, simulation_request: str) -> str:
    """Drive ReportAgent.generate_report and return the report folder."""
    print(f"[6/6] Generating report (with reviewer panel if grant_review mode)...")
    agent = ReportAgent(
        graph_id=graph_id,
        simulation_id=simulation_id,
        simulation_requirement=simulation_request,
    )

    def _cb(stage: str, prog: int, msg: str) -> None:
        print(f"      [{stage:<10}] {prog:>3}%  {msg}")

    report = agent.generate_report(progress_callback=_cb)
    if report.status.value != "completed":
        raise RuntimeError(f"Report generation failed: {report.error}")

    report_folder = os.path.join(Config.UPLOAD_FOLDER, "reports", report.report_id)
    print(f"      → report folder: {report_folder}")
    return report_folder


def _copy_output(report_folder: str, output_dir: str) -> None:
    if not output_dir:
        return
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    src = os.path.join(report_folder, "full_report.md")
    if os.path.exists(src):
        dst = os.path.join(output_dir, "full_report.md")
        with open(src, "r", encoding="utf-8") as fr, open(dst, "w", encoding="utf-8") as fw:
            fw.write(fr.read())
        print(f"      → copied full_report.md → {dst}")
    panel = os.path.join(report_folder, "reviewer_panel.json")
    if os.path.exists(panel):
        dst = os.path.join(output_dir, "reviewer_panel.json")
        with open(panel, "r", encoding="utf-8") as fr, open(dst, "w", encoding="utf-8") as fw:
            fw.write(fr.read())
        print(f"      → copied reviewer_panel.json → {dst}")


def main() -> int:
    args = _parse_args()
    if args.mode:
        os.environ["SIMULATION_MODE"] = args.mode
    if not os.path.exists(args.proposal):
        print(f"[FATAL] Proposal file not found: {args.proposal}", file=sys.stderr)
        return 2

    _validate_env()
    print(f"=== MiroFish-BioReviewer pipeline (mode={Config.SIMULATION_MODE}) ===")

    project, text = _bootstrap_project(args.proposal, args.name)
    graph_id = _generate_ontology_and_graph(
        project, text, args.request, args.graph_build_timeout
    )
    sim_id = _run_simulation(
        graph_id=graph_id,
        project_id=project.project_id,
        document_text=text,
        simulation_request=args.request,
        max_rounds=args.max_rounds,
        sim_timeout=args.sim_timeout,
    )
    report_folder = _generate_report(graph_id, sim_id, args.request)
    _copy_output(report_folder, args.output_dir or "")

    print("\n=== DONE ===")
    summary = {
        "project_id": project.project_id,
        "graph_id": graph_id,
        "simulation_id": sim_id,
        "report_folder": report_folder,
        "mode": Config.SIMULATION_MODE,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
