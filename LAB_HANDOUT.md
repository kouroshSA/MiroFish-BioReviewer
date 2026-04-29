# Lab Handout — MiroFish-BioReviewer

> **Course:** _(fill in)_  
> **Date:** _(fill in)_  
> **Instructor:** _(fill in)_  
> **Time required:** ~60–90 minutes (most of which is automated)

You will use **MiroFish-BioReviewer** — an AI-assisted reviewer for systems-biology grant pre-proposals — to put a real pre-proposal through a multi-agent simulation and produce a structured review report. You will run everything in your web browser. No local installation. No coding.

---

## Learning Objectives

By the end of the lab you will be able to:

1. Explain what a knowledge graph is and how a GraphRAG pipeline differs from a plain RAG.
2. Describe the three reviewer-agent personas (Mechanist, Visionary, Realist) and what each one is responsible for.
3. Read a structured grant review and identify which findings are *evidence from the simulation* vs. *judgments from the reviewer panel*.
4. Critically discuss where AI-assisted review is reliable and where a human reviewer is still required.

---

## What You Will Need

- A Google account (any personal Gmail works; you'll use Google Colab).
- An LLM API key + a Zep Cloud API key. **The instructor will provide these in class.** Do not paste them anywhere except into the notebook prompts described below.
- A grant pre-proposal PDF (provided in class, or use your own 2–3 page draft).

---

## Procedure

### Part 1 — Open the notebook in Google Colab

1. Open the notebook in Colab via this link (it's the orange "Open In Colab" button at the top of the project README):

   `https://colab.research.google.com/github/kouroshSA/MiroFish-BioReviewer/blob/main/colab/MiroFish_BioReviewer.ipynb`

2. **Important.** Confirm the URL bar reads `colab.research.google.com`. If it reads anything else (e.g. you opened it in VS Code or local Jupyter), close the tab and use the link above. The notebook will refuse to run anywhere except Colab.

3. From the menu, choose **Runtime → Disconnect and delete runtime**, then confirm. (This wipes any leftover state from a previous student.) Your runtime is fresh.

### Part 2 — Run **Cell 2: Environment Setup**

This cell installs everything the notebook needs (~3–5 minutes the first time).

- Click the play button on Cell 2.
- You will see messages like:
  - `Running in Colab on Linux (system Python 3.12)`
  - `Installing Python 3.11 and creating a venv at /opt/mirofish_venv ...`
  - `Installing MiroFish-BioReviewer Python dependencies (2-4 minutes)...`
- Wait for it to finish with `Setup complete.` Do not interrupt.

> **What's happening:** Colab's default Python is 3.12, but one of our dependencies only ships for 3.11. The cell quietly creates a Python 3.11 sandbox and installs everything inside it. You don't need to do anything.

### Part 3 — Run **Cell 3: API Key Configuration**

The cell asks four short questions. Follow these answers:

| Prompt | Your answer |
|--------|-------------|
| `Enter choice (1-5)` | Type the number the instructor tells you (likely `2` for Anthropic Claude). |
| `Model name [...]` | Press **Enter** to accept the default. |
| `Enter your LLM API key (hidden)` | Paste the LLM key from the instructor. The cell hides what you type — that is normal. |
| `Enter your ZEP Cloud API key (hidden)` | Paste the Zep key from the instructor. Also hidden. |
| `Use a stronger model for final report synthesis?` | Press **Enter** to reuse the same model. |

Confirm the green `Configuration complete.` line at the end shows the right provider and model.

> **Privacy note.** Your keys are read with `getpass`, stored only in this Colab session's memory, never written to disk, and lost the moment you close the tab. Don't paste keys anywhere else.

### Part 4 — Run **Cell 4: Live UI Mode**

This cell builds the web interface, starts the backend, and opens a tunnel to your browser.

- Click play on Cell 4. Wait ~3 minutes the first time. You will see:
  - `Building Vue frontend...`
  - `Starting Flask backend ...`
  - `Backend healthy on port 5001`
  - `LLM endpoint smoke-test: ✓ ... responds`
  - A big orange **"Open MiroFish-BioReviewer UI"** button.
- Click the button. A new browser tab opens with the MiroFish-BioReviewer interface.

> **Leave the Colab tab open** in the background. Cell 4 keeps running on purpose — it's streaming the backend's log so any error is visible. If you close Colab, the backend dies and your UI tab stops working.

### Part 5 — Run the review in the UI tab

You are now in the web interface. The page has an upload area and a prompt area.

1. **Upload your pre-proposal PDF** (drag-and-drop or click to browse).
2. **Paste this prompt** into the simulation requirement box (it is also in the appendix):

   > Review this systems biology grant pre-proposal. Simulate how the key biological tools, systems, and molecular targets described in the proposal would react to and debate the scientific plan. Focus on entities central to the proposed biology: CRISPR or other editing tools, target genes/loci/pathways, host systems and model organisms, delivery vectors, and synthetic circuits. Do NOT create agents for researchers, institutions, or journals.
   >
   > Have the swarm address: (1) Do the proposed tools and systems "believe" the plan is feasible? (2) Where is the tension between what is designed and what biological reality will tolerate? (3) What is the single most compelling scientific claim?

3. Click **Launch Engine**. The UI walks through five workflow steps. Each step takes a few minutes; the whole pipeline is roughly **8–15 minutes** depending on the model.

4. Watch the steps progress:
   - **Step 01 — Ontology Generation:** the LLM reads your proposal and decides what kinds of things matter (e.g. "EditingTool", "TargetLocus").
   - **Step 02 — GraphRAG Build:** Zep ingests the proposal and builds a knowledge graph node-by-node. You can watch the graph fill in.
   - **Step 03 — Environment Setup & Simulation:** each entity from the proposal is given a personality and starts interacting with the others.
   - **Step 04 — Reviewer Panel + Report:** the three reviewer agents (Mechanist, Visionary, Realist) deliberate, then the Reporter Agent assembles the final document.
   - **Step 05 — Deep Interaction (optional):** chat with any agent or with the report after it's done.

### Part 6 — Read and download the results

When the pipeline completes you'll see action buttons at the bottom of Step 4:

- **Enter Deep Interaction** — chat with the agents (optional).
- **Program Manager Final Report** (orange) — downloads the senior-model synthesis. **This is the file your instructor wants you to submit.**
- **Export Report** — full report in Markdown / Word / PDF format, useful for your own notes.

When you're done, return to the Colab tab and click the stop button on Cell 4 to free the backend.

---

## What to submit

By _(date / time)_:

1. The downloaded **`program_manager_final_report.md`** file.
2. A short (≤300 word) reflection answering:
   - Did the panel reach a consensus recommendation? Where did the three reviewers most strongly disagree, and which one did you find most convincing?
   - Find one finding the simulation surfaced that you believe is correct, and one that you believe is wrong or misleading. Explain why for each.
   - Would you trust this tool to *replace* a human review at full-proposal stage? Why or why not? (See Appendix B before answering.)

---

## Quick troubleshooting

| Symptom | Most likely cause | Fix |
|---------|-------------------|-----|
| Cell 2 errors with `Microsoft Visual C++ ...` | You're not actually in Colab | Open the notebook via the URL in Part 1, not VS Code or local Jupyter |
| Cell 4 errors with `LLM endpoint smoke-test failed` | Wrong API key or model name | Re-run Cell 3 and double-check the key |
| The UI button opens a page that says "this site can't be reached" | Cell 4 was stopped or the runtime disconnected | Re-run Cell 4 |
| The graph build is stuck at 0% | Zep monthly quota exhausted | Tell the instructor; they can rotate the key |
| The Program Manager Final Report button gives a 404 | The senior-model step failed silently | Scroll Cell 4's log for an `ERROR:` line and show it to the instructor |
| You hit Colab's "session timeout" | Free Colab idles after ~90 min of inactivity | Click into the Colab tab every ~15 min during long runs |

---

## Appendix A — How the tool works (non-technical)

MiroFish-BioReviewer treats your pre-proposal not as a document, but as a **cast of characters**. Specifically:

1. The proposal is fed to a language model (the **Ontology Generator**), which decides what *kinds* of things matter — for SynBio this usually means CRISPR tools, guide RNAs, target genes, delivery vectors, host cells, repair pathways, and so on.
2. Each thing in the proposal becomes an **agent** with a personality based on its biological role. Then those agents *talk to each other* in a simulated environment for hundreds of rounds, like a Twitter/Reddit feed populated by molecules and cells. The point is to surface tensions: *does the host cell "believe" the editor will reach its target? Does NHEJ cooperate with HDR the way the proposal needs?*
3. Once the simulation is done, **three human-style reviewer agents** read the proposal and the simulation transcript and write structured assessments. They have very different jobs:

| Agent | Role | What they look at |
|-------|------|-------------------|
| **The Mechanist** | The hardcore experimentalist who reads methods first | Mechanistic logic, controls, statistical/quantitative design, specificity of CRISPR/vector choices |
| **The Visionary** | The trend-watcher who sits on study sections | Significance, novelty, conceptual clarity, transformative potential, where the field is heading |
| **The Realist** | The pragmatic program manager | Feasibility, preliminary data strength, team expertise, scope-for-a-pre-proposal, communication quality |

Each reviewer outputs a structured JSON record with scored dimensions, concerns, strengths, a recommendation (Fund / Revise and Resubmit / Do Not Fund), and a confidence level.

4. A **Reporter Agent** then writes the actual review report, section by section. It uses the simulation evidence as *secondary support* and the reviewer panel verdicts as *primary evidence*. The report has six fixed sections: Executive Summary, Scored Dimensions, Reviewer Panel Synthesis, Field Resonance from Simulation, Top 3 Recommendations, and Overall Recommendation.

5. Finally, a **senior-model polish pass** (the "Program Manager Final Report") takes everything and produces a tightened, publication-ready summary. This is the file with the orange download button.

The other agents are mostly invisible plumbing: a **Persona Generator** that gives each entity its character, a **Simulation Config Generator** that decides how often each agent acts, and the **Graph Builder** that turns your proposal text into a queryable knowledge graph (see Appendix C).

---

## Appendix B — Limitations and recommended use

This tool is genuinely useful for a class of problems, and genuinely useless or worse for others. Be honest with yourself about which.

**The tool is good at:**
- Catching *missing controls*, *unstated assumptions*, and *vague specificity claims* that a busy reviewer might gloss over.
- Surfacing *tensions between intent and biology* — e.g. "you say you'll deliver this with AAV but your transgene is 6 kb."
- Producing a *first-draft critique* that a human reviewer can then sharpen, agree with, or push back against.
- Forcing structure on an early-stage proposal: by the time the report is written, the proposal's claims have been pinned to scored dimensions.

**The tool is not good at — and should not be used for:**
- **Replacing a human review at full-proposal stage.** Treat its output as a stress-test for the proposal's logic, not as a verdict.
- **Detecting fraud or fabrication.** It treats the proposal at face value.
- **Judging novelty against the actual literature.** Its sense of "what's new" comes only from the proposal text, not from a current PubMed search.
- **Assessing the team's track record.** It can only infer expertise from what the proposal says.
- **Highly sensitive or confidential content.** API keys are scoped to the instructor's accounts; assume the LLM provider sees the proposal text.

**How we recommend using it:**

1. As a *first pass* on your own draft pre-proposal, before showing it to a colleague.
2. As a *teaching tool* to make the structure of grant review concrete (which is what this lab is about).
3. As a *brainstorming partner* — interrogate the agents in Deep Interaction mode and see what objections they raise.

Do **not** copy its output verbatim into anything you submit. The polished section reads convincingly enough to be tempting; resist.

---

## Appendix C — Knowledge graphs, RAG, and GraphRAG (in plain language)

**What is a knowledge graph?** Imagine a Wikipedia where every article is a dot on a giant pinboard and every link between articles is a piece of string. The dots are **entities** (people, places, genes, drugs, papers); the strings are **relationships** (binds-to, regulates, is-a-citizen-of). A knowledge graph is exactly this — but built and queried by software, not by hand.

**What is RAG (Retrieval-Augmented Generation)?** Language models like Claude or GPT-4 are smart about general topics but can't read a 50-page document fresh every time you ask them a question. RAG is the workaround: you chop your document into pieces, store them in a database, and when you ask a question the system *first* fetches the most relevant pieces and *then* passes them to the model along with your question. The model only has to read the relevant bits, not the whole document.

**What is GraphRAG?** Plain RAG retrieves text chunks. **GraphRAG** retrieves text chunks **plus the graph structure connecting them.** Instead of getting back five paragraphs that mention "Cas9", you get back the *Cas9 node* and everything it's connected to: the guide RNAs that ride with it, the target loci it cuts, the off-target sites people worry about, the delivery vectors that carry it. This makes the model's answers sharper because the model can reason about *relationships*, not just keywords.

In MiroFish-BioReviewer:
- We use a service called **Zep Cloud** to do the GraphRAG.
- Zep ingests your proposal, builds the graph, and exposes search APIs that the simulation agents and the reviewer agents query repeatedly.
- The graph is what the reviewer agents *read* when they say things like "the proposal connects this base editor to this disease allele but says nothing about the repair pathway" — they're reading the graph's edges, not searching for a string.

That's why your free Zep tier matters: every time an agent asks the graph a question, it consumes a small amount of Zep quota.

---

## Appendix D — Using MiroFish-BioReviewer after the class

The keys you used today are the instructor's. To use the tool after the class you need your own. Both providers offer free tiers that comfortably cover several full runs.

### 1. Zep Cloud (knowledge graph)

1. Go to <https://app.getzep.com> and sign up. The free tier needs no credit card.
2. After signup you'll land on a Project dashboard. Either use the default project or create one named anything.
3. Open **API Keys** in the left sidebar (or **Project Settings → API Keys**).
4. Click **Create New Key**, name it something like "MiroFish", and copy the key. **It is shown only once** — paste it into a password manager immediately.

### 2. Anthropic Claude (recommended LLM)

1. Go to <https://console.anthropic.com>, sign up, and verify your email.
2. New accounts get a small amount of free credit; for heavier use add a payment method and **set a monthly spending cap** (`Settings → Limits`). $10 is plenty for a few full reviews.
3. Open **API Keys**, click **Create Key**, copy the key. (Again, shown once.)

### 3. Run the notebook with your own keys

The procedure is identical to today — paste your keys into Cell 3 instead of the instructor's. The default model `claude-haiku-4-5` is the cheapest and works fine for the lab; switch to `claude-sonnet-4-6` or `claude-opus-4-7` if you want a more eloquent report (proportionally more expensive).

### 4. Other providers

If you'd rather not give Anthropic a credit card, the same notebook works with:

- **OpenAI** (`gpt-4o-mini`, `gpt-4o`, `gpt-4.1`) — sign up at <https://platform.openai.com>; new accounts get a small free credit.
- **Google Gemini** (`gemini-2.5-flash`) — get a free key at <https://aistudio.google.com/app/apikey>.
- **DeepSeek** (`deepseek-chat`) — sign up at <https://platform.deepseek.com>; cheapest of the three.

Pick option 1, 3, or 4 in Cell 3, paste the corresponding key, and run as normal.

### 5. Where to look if something stops working

- The repository: <https://github.com/kouroshSA/MiroFish-BioReviewer>
- The Colab notebook (always tracks the latest commit): <https://colab.research.google.com/github/kouroshSA/MiroFish-BioReviewer/blob/main/colab/MiroFish_BioReviewer.ipynb>
- The Colab-specific README: <https://github.com/kouroshSA/MiroFish-BioReviewer/blob/main/colab/README_colab.md>

---

*This handout is part of the MiroFish-BioReviewer project. Comments, corrections, and student feedback are welcome via GitHub Issues.*
