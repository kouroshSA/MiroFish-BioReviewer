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
