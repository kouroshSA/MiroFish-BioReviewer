"""
Orchestrates the reviewer panel and serializes results to disk
for the Reporter agent to consume.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

from .reviewer_agents import run_reviewer_panel


def run_and_save_panel(
    proposal_text: str,
    simulation_posts: List[Dict[str, Any]],
    llm_client,
    model_name: str,
    output_dir: str,
) -> Dict[str, Any]:
    """
    Run reviewer panel and save results to output_dir/reviewer_panel.json.
    Returns the panel results dict.
    """
    results = run_reviewer_panel(
        proposal_text=proposal_text,
        simulation_posts=simulation_posts,
        llm_client=llm_client,
        model_name=model_name,
    )

    panel_output = {
        "timestamp": datetime.utcnow().isoformat(),
        "reviewer_count": len(results),
        "reviews": results,
        "panel_consensus": _compute_consensus(results),
    }

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / "reviewer_panel.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(panel_output, f, indent=2, ensure_ascii=False)

    return panel_output


def _compute_consensus(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute simple consensus metrics across reviewer outputs.
    Used by the Reporter agent for at-a-glance orientation.
    """
    recommendations = [r.get("recommendation", "N/A") for r in results if "error" not in r]

    rec_counts: Dict[str, int] = {}
    for r in recommendations:
        rec_counts[r] = rec_counts.get(r, 0) + 1

    majority = max(rec_counts, key=rec_counts.get) if rec_counts else "N/A"
    unanimous = len(set(recommendations)) == 1 and len(recommendations) == 3

    # Collect all dimension scores for averaging
    all_scores: Dict[str, List[float]] = {}
    for review in results:
        if "error" in review:
            continue
        for dim, score in review.get("dimension_scores", {}).items():
            try:
                score_val = float(score)
            except (TypeError, ValueError):
                continue
            all_scores.setdefault(dim, []).append(score_val)

    avg_scores = {dim: round(sum(v) / len(v), 1) for dim, v in all_scores.items()}

    return {
        "majority_recommendation": majority,
        "unanimous": unanimous,
        "recommendation_breakdown": rec_counts,
        "average_dimension_scores": avg_scores,
        "panel_complete": len([r for r in results if "error" not in r]) == 3,
    }
