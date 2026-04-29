# How to run MiroFish-BioReviewer

There are two supported ways to run this tool. Pick whichever matches what you want to do.

| Path | Audience | Setup time | When to use |
|---|---|---|---|
| **A. Google Colab + Live UI** | Anyone with a browser | ~5 minutes | First-time use, classroom, demos, quick proposal reviews. **Recommended.** |
| **B. Local development** | Engineers who want to modify the code | ~30 minutes | Hacking on the backend/frontend, running headless batch jobs, integrating with other systems |

---

## Path A — Google Colab + Live UI (recommended)

This is the easiest path: no installation, runs in your browser, all the tool's pieces (backend, frontend, GraphRAG, simulation, reviewer panel) are provisioned automatically.

**Quick start.** Click the badge in the [README](README-EN.md), or open this URL directly:

```
https://colab.research.google.com/github/kouroshSA/MiroFish-BioReviewer/blob/main/colab/MiroFish_BioReviewer.ipynb
```

Then run **Cell 2 → Cell 3 → Cell 4** in order, click the orange "Open MiroFish-BioReviewer UI" button that appears, upload your pre-proposal PDF in the new tab, and let the pipeline run. ~8–15 minutes per proposal.

**Walkthroughs.** The full step-by-step guides for the Colab path live in two places. Start with whichever fits you:

- [`Easy-start_in_Colab.md`](Easy-start_in_Colab.md) — non-technical guide for individual users (researchers, PIs).
- [`colab/README_colab.md`](colab/README_colab.md) — Colab-specific README with troubleshooting and the auto-Python-3.11-venv explanation.

If you are running this in a class, your instructor may provide their own lab handout.

---

## Path B — Local development

Use this path if you need to modify the backend or frontend code, run headless batch jobs across many proposals, or integrate MiroFish-BioReviewer into another system.

### B.1 Prerequisites

| Tool | Version | Install Check |
|---|---|---|
| Node.js | ≥18 | `node -v` |
| Python | 3.10 or 3.11 (NOT 3.12 — `camel-oasis` does not support 3.12) | `python --version` |
| Git | any modern | `git --version` |
| Linux or macOS | — | (Windows works only via WSL2; native Windows hits MSVC build-tool issues) |

> **Why Python 3.11 specifically?** Every released version of `camel-oasis` (the social-media simulation library) declares `requires_python = "<3.12,>=3.10"`. Newer Python versions will fail at `pip install`. The Colab notebook works around this automatically by provisioning a 3.11 venv; on local machines you should pick 3.10/3.11 yourself (e.g. `pyenv install 3.11.9 && pyenv local 3.11.9`).

### B.2 Clone and configure

```bash
git clone https://github.com/kouroshSA/MiroFish-BioReviewer.git
cd MiroFish-BioReviewer
cp .env.example .env
```

Edit `.env` and fill in two keys (see B.3 for how to get them):

```env
# === LLM (pick ONE provider) ===

# Anthropic Claude — recommended; uses native OpenAI-compat, no proxy.
LLM_API_KEY=sk-ant-...
LLM_BASE_URL=https://api.anthropic.com/v1/
LLM_MODEL_NAME=claude-haiku-4-5

# OpenAI
# LLM_API_KEY=sk-...
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL_NAME=gpt-4o-mini

# Google Gemini
# LLM_API_KEY=AIza...
# LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
# LLM_MODEL_NAME=gemini-2.5-flash

# DeepSeek
# LLM_API_KEY=sk-...
# LLM_BASE_URL=https://api.deepseek.com/v1
# LLM_MODEL_NAME=deepseek-chat

# Ollama (local, free)
# LLM_API_KEY=ollama
# LLM_BASE_URL=http://localhost:11434/v1
# LLM_MODEL_NAME=qwen2.5:7b

# === ZEP knowledge graph (required) ===
ZEP_API_KEY=z_...

# === Simulation mode for grant review ===
SIMULATION_MODE=grant_review
REVIEWER_PANEL_ENABLED=true
```

### B.3 Get API keys

**Zep Cloud (free tier, no credit card).** Sign up at <https://app.getzep.com>, open *API Keys* in the sidebar, click *Create New Key*, copy it (shown only once).

**Anthropic Claude (recommended LLM).** Sign up at <https://console.anthropic.com>, go to *API Keys*, click *Create Key*. New accounts get a small free credit; for ongoing use add a payment method and set a monthly spending cap (`Settings → Limits`). Default model `claude-haiku-4-5` is the cheapest; switch to `claude-sonnet-4-6` or `claude-opus-4-7` for higher-quality output.

**Other providers:** see B.2 for base URLs. OpenAI: <https://platform.openai.com>. Gemini: <https://aistudio.google.com/app/apikey>. DeepSeek: <https://platform.deepseek.com>.

> **Note: no LiteLLM proxy needed.** Earlier versions of MiroFish required a separately-running LiteLLM proxy for Anthropic. MiroFish-BioReviewer uses Anthropic's native OpenAI-compatibility endpoint (`https://api.anthropic.com/v1/`), so the OpenAI SDK in the backend talks to it directly with no extra process.

### B.4 Install dependencies

```bash
# Node deps (root + frontend)
npm run setup

# Python deps (creates backend venv if needed)
npm run setup:backend
```

If you prefer an explicit conda or pyenv environment:

```bash
# pyenv example
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt

# conda example
conda create -n mirofish python=3.11 -y
conda activate mirofish
pip install -r backend/requirements.txt
```

### B.5 Run

```bash
npm run dev
```

This launches both services:
- **Frontend:** <http://localhost:3000> (Vite dev server with hot reload)
- **Backend API:** <http://localhost:5001> (Flask)

Open <http://localhost:3000> in your browser. The Vite dev server proxies `/api/*` calls to the Flask backend, so you can hit `localhost:3000` for everything.

To run them separately:
```bash
npm run backend    # Flask only, on :5001
npm run frontend   # Vite only, on :3000
```

### B.6 Headless batch runs

For automated review of multiple proposals, use the headless pipeline driver:

```bash
python backend/scripts/run_review_pipeline.py \
    --proposal /path/to/proposal.pdf \
    --request "Review this systems biology grant pre-proposal..." \
    --max-rounds 40 \
    --output-dir output/proposal_001 \
    --mode grant_review
```

The driver creates a project, runs ontology generation → graph build → simulation → reviewer panel → report → polished summary, and writes `full_report.md`, `reviewer_panel.json`, and `program_manager_final_report.md` to the output directory.

---

## Environment variables

All variables read from `.env` at the repo root.

### Core (required)

| Variable | Default | Description |
|---|---|---|
| `LLM_API_KEY` | — | Provider API key |
| `LLM_BASE_URL` | `https://api.openai.com/v1` | Provider base URL |
| `LLM_MODEL_NAME` | `gpt-4o-mini` | Model name |
| `ZEP_API_KEY` | — | Zep Cloud API key (required) |

### Simulation mode

| Variable | Default | Description |
|---|---|---|
| `SIMULATION_MODE` | `social` | One of: `social`, `biological`, `custom`, `grant_review`. |
| `AGENT_SOUL_PATH` | `./agent-soul.md` | Used only when `SIMULATION_MODE=custom` |
| `GRANT_REVIEW_SOUL_PATH` | `./grant-review-soul.md` | Soul config for grant_review mode |

### Reviewer panel (grant_review mode only)

| Variable | Default | Description |
|---|---|---|
| `REVIEWER_PANEL_ENABLED` | `true` | Run the 3-agent reviewer panel after the simulation |
| `REVIEWER_MECHANIST_TEMPERATURE` | `0.3` | Mechanist reviewer temperature |
| `REVIEWER_VISIONARY_TEMPERATURE` | `0.7` | Visionary reviewer temperature |
| `REVIEWER_REALIST_TEMPERATURE` | `0.4` | Realist reviewer temperature |
| `REVIEWER_MAX_TOKENS` | `800` | Max tokens per reviewer JSON response |

### Tuning

| Variable | Default | Description |
|---|---|---|
| `FLASK_HOST` | `0.0.0.0` | Backend bind address |
| `FLASK_PORT` | `5001` | Backend port |
| `FLASK_DEBUG` | `True` | Flask debug + auto-reload |
| `OASIS_DEFAULT_MAX_ROUNDS` | `90` | Default simulation rounds (Colab overrides to 40) |
| `MAX_CONCURRENT_LLM_REQUESTS` | `2` | Throttle for parallel LLM calls |
| `REPORT_AGENT_MAX_TOOL_CALLS` | `5` | Max tool calls per report section |
| `REPORT_AGENT_MAX_REFLECTION_ROUNDS` | `2` | Reporter self-reflection rounds |
| `REPORT_AGENT_TEMPERATURE` | `0.5` | Reporter temperature |
| `DISCUSSION_LLM_MODEL_NAME` | (same as `LLM_MODEL_NAME`) | Stronger model for the Program Manager Final Report polish |

---

## Simulation modes

MiroFish-BioReviewer ships four `SIMULATION_MODE` values. The repo's primary use case is `grant_review`; the others are inherited from upstream.

### `grant_review` (the BioReviewer default)

Tuned for systems-biology grant pre-proposals. Activates:
- A SynBio entity ontology (CRISPR effectors, guide RNAs, target loci, host systems, delivery vectors, synthetic circuits, regulatory elements, pathways, off-target risks).
- Persona generation that maps biological role to character — a *base editor* gets the persona of a precision-obsessed minimalist, etc.
- A 24-hour simulation with 30-minute rounds and uniform activity (no circadian bias).
- A 3-agent reviewer panel (Mechanist / Visionary / Realist) that runs after the simulation.
- A grant-review report template (Executive Summary → Scored Dimensions → Reviewer Panel Synthesis → Field Resonance → Top 3 Recommendations → Overall Recommendation).
- A senior-model polish pass producing the standalone "Program Manager Final Report" file.

See [`grant-review-soul.md`](grant-review-soul.md) for the full soul configuration.

### `biological` (inherited)

Treats entities as molecules/proteins/genes. Personalities reflect biological function; the simulation models molecular interactions framed as social-media posts. Output is a biological-network analysis report. See [`agent-soul.md`](agent-soul.md).

### `social` (inherited)

The original general-purpose mode. Entities are people and organizations; personalities reflect public roles; output is a public-opinion / future-prediction report.

### `custom`

For domain experimentation. Set `SIMULATION_MODE=custom` and `AGENT_SOUL_PATH` to a custom soul-config file. See [`agent-soul.md`](agent-soul.md) and [`AI-Guidelines-Agent-Soul.md`](AI-Guidelines-Agent-Soul.md).

---

## How the pipeline works (one-page summary)

![MiroFish-BioReviewer workflow](static/image/workflow.png)

In sequence:

1. **Ontology Generator** (LLM) reads the proposal and decides what entity types matter.
2. **Graph Builder** + **Zep Cloud** ingest the proposal and build a knowledge graph (GraphRAG).
3. **Persona Generator** (LLM) gives each entity a personality based on its biological role.
4. **OASIS Simulation Engine** (`camel-oasis`, from CAMEL-AI) runs ~40 rounds of agent posts/replies/follows.
5. **Reviewer Panel** — three independent LLM calls (Mechanist / Visionary / Realist) produce structured JSON assessments.
6. **Reporter Agent** writes a 6-section grant review using simulation evidence + reviewer panel verdicts.
7. **Program Manager Final Report** — a senior-model polish pass produces a publication-ready Markdown file with three subheadings (Synthesis & Discussion, Broader Implications, Polished Executive Summary). Saved to `program_manager_final_report.md` for direct download.

For non-technical detail on each agent, see [`Easy-start_in_Colab.md`](Easy-start_in_Colab.md). For the soul configurations, see [`grant-review-soul.md`](grant-review-soul.md), [`agent-soul.md`](agent-soul.md), and [`AI-Guidelines-Agent-Soul.md`](AI-Guidelines-Agent-Soul.md).

---

## Limitations

This tool is genuinely useful for some things and genuinely not useful for others. Be honest about which.

**Use it for:** first-pass critique of your own draft pre-proposal; catching missing controls, unstated assumptions, and vague specificity claims; surfacing tensions between proposal intent and biological reality; teaching the structure of grant review.

**Do not use it for:** replacing a human reviewer at full-proposal stage; detecting fraud or fabrication (it takes the proposal at face value); judging novelty against the literature (it doesn't search PubMed); assessing the team's track record (it can only read what's in the proposal); highly sensitive or confidential content (assume the LLM provider sees the proposal text).

Do not copy the polished output verbatim into a real submission. The Program Manager Final Report reads convincingly enough to be tempting; resist.

---

## Docker (optional)

A `Dockerfile` and `docker-compose.yml` are included for production-style deployment:

```bash
# Build and run
docker compose up --build

# In another terminal
docker compose logs -f
```

The container exposes the frontend on `:3000` and the backend on `:5001`. Set the same environment variables via `docker-compose.yml` or an `.env` file in the repo root.

---

## Where to look if something stops working

- **Colab path:** the streamed Flask log in Cell 4 shows every API call and any errors. See [`colab/README_colab.md`](colab/README_colab.md) → Troubleshooting.
- **Local path:** Flask logs go to `backend/logs/<date>.log` and the console; Vite logs to the terminal where you ran `npm run dev`.
- **GitHub Issues:** <https://github.com/kouroshSA/MiroFish-BioReviewer/issues>
- **Original MiroFish project** (general-purpose social simulation, useful background): <https://github.com/666ghj/MiroFish>
