# MiroFish-BioReviewer — Google Colab

Run MiroFish-BioReviewer directly in Google Colab without any local installation.

## Quick Start

1. Click the badge below to open the notebook in Colab:
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kouroshSA/MiroFish-BioReviewer/blob/main/colab/MiroFish_BioReviewer.ipynb)

2. When the notebook opens, run Cell 1 (Setup). You will be prompted to enter:
   - Your LLM API key (OpenAI, Anthropic, Gemini, DeepSeek, or Ollama endpoint)
   - Your ZEP Cloud API key
   - Your preferred model name

3. Upload your grant pre-proposal PDF when prompted in Cell 3.

4. Run all cells in order. The review report will be displayed inline and available
   for download as a Markdown file.

## Notes
- The Colab environment does not persist between sessions — you will be prompted
  for API keys each time you start a new session.
- API keys are stored only in Colab's in-session memory using `getpass` — they are
  never written to disk or logged.
- The default simulation length is **40 rounds**. For longer simulations (>40 rounds),
  use a Colab Pro runtime to avoid session timeouts.
- The frontend UI is not available in Colab — the notebook runs the backend
  pipeline directly and renders the report inline.

## Colab-only — do not run locally

The notebook is hard-gated to Google Colab. Cell 2 will refuse to proceed on
Windows/macOS/local Linux Jupyter and tell you why.

The reason: `camel-oasis` and `camel-ai` (the swarm simulation engines) only
ship pre-built wheels for Linux x86_64 / Python ≥3.10. On Windows or macOS,
pip falls back to compiling from source, which is what produces the
`Microsoft Visual C++ 14.0 or greater is required` error. We do not support
that path because students should not need to install a 6 GB C++ toolchain.

If you want to develop locally, use a Linux container or WSL2 — and then `pip
install -r backend/requirements.txt` works normally.

## Troubleshooting

### "Microsoft Visual C++ 14.0 or greater is required"
You opened the notebook in **VS Code**, **local Jupyter**, or **Anaconda
Jupyter** on Windows — not in Google Colab. Open it via the Colab badge at
the top of the README, or click here directly:
[Open in Colab](https://colab.research.google.com/github/kouroshSA/MiroFish-BioReviewer/blob/main/colab/MiroFish_BioReviewer.ipynb).
The URL bar must say `colab.research.google.com`.

### Cell 2 takes ~5 minutes the first time
That's expected. Cell 2 has to:
1. Clone the repo (~5 sec)
2. `apt-get install python3.11` if Colab's runtime is Python 3.12+ (~30 sec)
3. Create a venv at `/opt/mirofish_venv` (~5 sec)
4. `pip install -r backend/requirements.txt` into the venv (~3 minutes)

If it stalls past 6–7 minutes: **Runtime → Restart runtime**, then re-run Cell 2.

### Why does Cell 2 print "Installing Python 3.11..."?
Every released version of `camel-oasis` declares `requires_python = "<3.12,>=3.10"`. When Colab's default runtime is Python 3.12+ (current default since 2025), pip can't install camel-oasis directly — so Cell 2 transparently provisions a Python 3.11 venv at `/opt/mirofish_venv` and installs the dependencies there. Cell 6 then runs the pipeline through that venv via the `MIROFISH_PYTHON` env var. No action needed on your end.

### `Cell 6` raises `ModuleNotFoundError`
Cell 2 finished but a package didn't actually install. **Runtime → Restart
runtime**, then re-run Cell 2 — its smoke-import step at the end will tell
you which package is missing.

### `Cell 6` exits with non-zero status mid-pipeline
Most common cause is an exhausted ZEP free-tier quota or an LLM API rate
limit. Check the printed traceback. The pipeline writes partial state under
`backend/uploads/` so you can resume by lowering the round count in Cell 5
and re-running Cell 6.
