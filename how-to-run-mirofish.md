# How to Run MiroFish

MiroFish is a multi-agent swarm intelligence engine that simulates digital worlds from seed materials (reports, documents, stories) and generates prediction reports through agent interactions.

---

## First-Time Setup

### Prerequisites

| Tool | Version | Install Check |
|------|---------|---------------|
| Node.js | 18+ | `node -v` |
| Python | 3.11–3.12 | `python --version` |
| uv | latest | `uv --version` |
| Ollama (optional) | latest | `ollama --version` |

### 1. Clone the Repository

```bash
git clone https://github.com/kouroshSA/MiroFish-Bio.git
cd MiroFish
```

### 2. Get API Keys

You need two API keys before running MiroFish:

#### LLM API Key

MiroFish supports any LLM with an OpenAI-compatible API. Choose one:

- **Ollama (local, free):** Install from https://ollama.com, then pull a model:
  ```bash
  ollama pull qwen2.5:7b
  ```
  No API key needed — use `ollama` as the key value.

- **Alibaba Bailian (recommended by MiroFish):** Sign up at https://bailian.console.aliyun.com/ and get an API key. Use model `qwen-plus`.

- **OpenAI:** Sign up at https://platform.openai.com/, create an API key under API Keys. Models: `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, etc.

- **Anthropic (Claude):** Sign up at https://console.anthropic.com/, create an API key. Claude does not natively expose an OpenAI-compatible endpoint, so you need a proxy such as [LiteLLM](https://github.com/BerriAI/litellm):
  ```bash
  pip install litellm
  litellm --model claude-sonnet-4-20250514 --port 8000
  ```
  Then set `LLM_BASE_URL=http://localhost:8000/v1` and `LLM_API_KEY=your_anthropic_key`.

- **Google Gemini:** Sign up at https://aistudio.google.com/, get an API key. Gemini provides an OpenAI-compatible endpoint:
  ```
  LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
  LLM_MODEL_NAME=gemini-2.5-flash
  ```

- **DeepSeek:** Sign up at https://platform.deepseek.com/, create an API key. Natively OpenAI-compatible:
  ```
  LLM_BASE_URL=https://api.deepseek.com/v1
  LLM_MODEL_NAME=deepseek-chat
  ```

- **Any OpenAI-compatible provider:** MiroFish uses the OpenAI SDK internally, so any provider with a compatible `/v1/chat/completions` endpoint will work (e.g., Together AI, Groq, Mistral, OpenRouter). Just set the appropriate `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL_NAME`.

#### ZEP API Key (required)

ZEP Cloud provides the memory graph that MiroFish uses for agent knowledge and entity relationships.

1. Go to https://app.getzep.com/
2. Create a free account (free tier is sufficient for basic use)
3. Navigate to your project → API Keys
4. Generate and copy your API key

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```env
# === LLM Configuration ===

# Option A: Ollama (local)
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:7b

# Option B: Alibaba Bailian
# LLM_API_KEY=your_bailian_api_key
# LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
# LLM_MODEL_NAME=qwen-plus

# Option C: OpenAI
# LLM_API_KEY=sk-...
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL_NAME=gpt-4o-mini

# Option D: Claude (via LiteLLM proxy)
# LLM_API_KEY=your_anthropic_key
# LLM_BASE_URL=http://localhost:8000/v1
# LLM_MODEL_NAME=claude-sonnet-4-20250514

# Option E: Google Gemini
# LLM_API_KEY=your_gemini_key
# LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
# LLM_MODEL_NAME=gemini-2.5-flash

# Option F: DeepSeek
# LLM_API_KEY=your_deepseek_key
# LLM_BASE_URL=https://api.deepseek.com/v1
# LLM_MODEL_NAME=deepseek-chat

# === ZEP Memory Graph (required) ===
ZEP_API_KEY=your_zep_api_key_here

# === Boost LLM (optional, for faster processing) ===
# LLM_BOOST_API_KEY=your_api_key_here
# LLM_BOOST_BASE_URL=your_base_url_here
# LLM_BOOST_MODEL_NAME=your_model_name_here
```

### 4. Install Dependencies

All at once:
```bash
npm run setup:all
```

Or step by step:
```bash
# Node dependencies (root + frontend)
npm run setup

# Python dependencies (backend, creates virtual env)
npm run setup:backend
```

### 5. (Optional) Conda Environment

If you prefer using conda:
```bash
conda create -n mirofish python=3.12 -y
conda activate mirofish
npm run setup:all
```

---

## Basic Usage

### Start the Application

```bash
npm run dev
```

This launches both services:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5001

### Start Services Individually

```bash
npm run backend    # Backend only
npm run frontend   # Frontend only
```

### Using the Web UI

1. Open http://localhost:3000 in your browser
2. Upload a seed document (PDF, MD, or TXT — max 50 MB)
3. Enter your prediction/simulation request in natural language
4. MiroFish will proceed through 5 stages:
   - **Graph Construction** — Extracts entities and relationships from your document
   - **Environment Setup** — Generates agent personas and injects simulation parameters
   - **Simulation** — Agents interact across dual platforms (Twitter + Reddit style)
   - **Report Generation** — ReportAgent analyzes simulation results
   - **Deep Interaction** — Chat with any agent or the ReportAgent

### Browser Translation

The UI is in Chinese. Use your browser's built-in translation:
- **Chrome/Edge:** Right-click the page → "Translate to English"
- **Firefox:** Install a translation extension

---

## Advanced Usage

### Environment Variable Tuning

Add these to your `.env` file to customize behavior:

| Variable | Default | Description |
|---|---|---|
| `FLASK_HOST` | `0.0.0.0` | Backend bind address |
| `FLASK_PORT` | `5001` | Backend port |
| `FLASK_DEBUG` | `True` | Enable debug mode |
| `OASIS_DEFAULT_MAX_ROUNDS` | `10` | Default number of simulation rounds |
| `REPORT_AGENT_MAX_TOOL_CALLS` | `5` | Max tool calls per report generation |
| `REPORT_AGENT_MAX_REFLECTION_ROUNDS` | `2` | Report agent self-reflection rounds |
| `REPORT_AGENT_TEMPERATURE` | `0.5` | LLM temperature for report generation |

### Switching Ollama Models

```bash
# List available models
ollama list

# Pull a new model
ollama pull qwen2.5:32b

# Update .env
# LLM_MODEL_NAME=qwen2.5:32b
```

Restart the app after changing the model.

### CLI Simulation Scripts

For running simulations directly from the command line without the web UI. Run from the `backend/` directory.

**Parallel simulation (both platforms):**
```bash
uv run python scripts/run_parallel_simulation.py \
  --config path/to/simulation_config.json \
  --max-rounds 20
```

**Twitter simulation only:**
```bash
uv run python scripts/run_twitter_simulation.py \
  --config path/to/simulation_config.json \
  --max-rounds 20
```

**Reddit simulation only:**
```bash
uv run python scripts/run_reddit_simulation.py \
  --config path/to/simulation_config.json \
  --max-rounds 20
```

**CLI flags:**

| Flag | Description |
|---|---|
| `--config` | **(Required)** Path to `simulation_config.json` |
| `--max-rounds` | Max simulation rounds (overrides config) |
| `--twitter-only` | Run only Twitter simulation (parallel script only) |
| `--reddit-only` | Run only Reddit simulation (parallel script only) |
| `--no-wait` | Exit immediately after simulation completes instead of entering interactive mode |

### Agents and Simulation Parameters

#### How agent count is determined

The number of agents is **not set manually** — it is automatically determined by the entities (people, organizations, groups, etc.) that MiroFish extracts from your uploaded document via the ZEP knowledge graph. Each extracted entity becomes a simulated agent. The ontology is capped at a maximum of 10 entity types.

For example, if you upload a report mentioning 50 distinct people and organizations, MiroFish will create approximately 50 agents for the simulation.

#### Simulation parameters (LLM-generated)

During the "Environment Setup" stage, the LLM automatically generates simulation parameters tailored to your scenario. These are not exposed in the UI but can be understood as:

| Parameter | Default | Range | Description |
|---|---|---|---|
| `total_simulation_hours` | 72 | 24–168 | Total simulated time span |
| `minutes_per_round` | 60 | 30–120 | Simulated minutes per round |
| `agents_per_hour_min` | entities/15 | 1 – 90% of agents | Min agents active per simulated hour |
| `agents_per_hour_max` | entities/5 | 1 – 90% of agents | Max agents active per simulated hour |
| `peak_hours` | 19–22 | 0–23 | High-activity hours (simulated time) |
| `off_peak_hours` | 0–5 | 0–23 | Low-activity hours (simulated time) |

#### What you CAN control

- **`max_rounds`** — Limit simulation length via the CLI (`--max-rounds`) or the start simulation API. This truncates the simulation if it would otherwise run too long.
- **`OASIS_DEFAULT_MAX_ROUNDS`** — Set in `.env` to change the default max rounds (default: 10).
- **`platform`** — Choose to simulate on Twitter only, Reddit only, or both in parallel (via CLI flags `--twitter-only` / `--reddit-only`, or the API `platform` parameter).
- **`force`** — Force restart a simulation via the API (stops any running simulation and clears logs, but preserves config and profiles).
- **`enable_graph_memory_update`** — When enabled via the API, agent activity (posts, comments, likes) is written back to the ZEP graph in real time for post-simulation analysis.

### Docker Deployment

```bash
cp .env.example .env
# Edit .env with your API keys (same as above)
docker compose up -d
```

Ports `3000` (frontend) and `5001` (backend) are mapped by default. Accelerated mirror addresses are provided in `docker-compose.yml` as comments.

---

## Understanding ZEP's Role

ZEP Cloud is the **persistent knowledge graph backend** that powers MiroFish's memory and retrieval. It is involved in every stage of the pipeline:

### Stage 1: Graph Building (from your uploaded document)

When you upload a document, MiroFish chunks the text (~500-character segments) and sends it to ZEP. ZEP automatically extracts **entities** (people, organizations, concepts) and **relationships** between them. An ontology defining entity and edge types is set on the graph so ZEP knows what to look for. The result is a structured knowledge graph with nodes and edges representing the world described in your document.

### Stage 2: Agent Creation

The `ZepEntityReader` reads all extracted entities from the ZEP graph. Each entity becomes a simulated agent whose persona is generated from its graph context — its attributes, relationships, and summary.

### Stage 3: Simulation (optional real-time memory updates)

If `enable_graph_memory_update` is turned on, agent activities during simulation (posts, likes, comments, follows, reposts) are **written back to ZEP** as natural language narrative episodes, batched 5 at a time. This makes the graph "remember" what happened during the simulation, enriching it with dynamic data.

### Stage 4: Report Generation

This is where ZEP pays off most. The ReportAgent queries ZEP extensively using three retrieval strategies:

- **InsightForge** — Deep multi-angle analysis that auto-generates sub-questions and retrieves facts, entities, and relationship chains
- **PanoramaSearch** — Full graph view including historical and expired facts, showing how the situation evolved
- **QuickSearch** — Fast semantic search for verifying specific claims

The ReportAgent also uses **InterviewAgents** to "interview" simulated agents using their graph context, adding qualitative perspectives to the report.

### Stage 5: Deep Interaction

When you chat with individual agents or the ReportAgent after the simulation, ZEP provides the contextual knowledge that informs their responses.

### In summary

Without ZEP, MiroFish has no way to persist or query the knowledge graph extracted from your document. ZEP stores what MiroFish knows about your document's world, records what happens during simulation, and serves as the retrieval backend for generating reports and powering interactive conversations.

---

## Limitations: Scientific and Non-Social Data

MiroFish is purpose-built for **social media opinion simulation**. Its entire pipeline — from entity extraction to agent personas to simulation actions — assumes entities are human actors or organizations that interact on social media platforms. This has important implications if you want to use it for scientific data analysis.

### What works: Uploading a scientific manuscript as text

You can upload a research paper (e.g., a protein interactome study) as a PDF. MiroFish will:
- Extract people, institutions, and concepts mentioned in the paper
- Generate social media personas for those entities
- Simulate public discourse *about* the research (e.g., how scientists, media, or the public might react to the findings)
- Produce a prediction report on the societal or scientific community response

This is a valid and interesting use case — simulating how a scientific discovery might play out in public discourse.

### What does NOT work: Uploading raw scientific interaction data

If you upload data where the entities are **not human** (e.g., protein-protein interaction networks, gene regulatory networks, chemical compound interactions), the system will fail or produce nonsensical results. Here's why:

#### 1. Ontology generator rejects non-social entities
The ontology system prompt explicitly requires entities that "can speak and interact on social media" — people, organizations, media outlets. It rejects abstract concepts. Proteins, genes, or chemical compounds would be rejected or misclassified.

#### 2. Persona generator assumes human attributes
Each agent profile requires: `age`, `gender`, `MBTI type`, `country`, `profession`, social media `bio`, `karma`, `follower_count`, and a 2000-word persona describing posting style, emotional triggers, and social media behavior. Entity types are hardcoded into two categories:
- **Individuals:** student, alumni, professor, person, publicfigure, expert, etc.
- **Groups/Institutions:** university, government agency, organization, NGO, media outlet, etc.

A protein like "CAE19578 (outer membrane porin)" would fall into a generic fallback and be assigned a random age, gender, and MBTI type.

#### 3. Simulation actions are social-media-only
Agents can only perform: `CREATE_POST`, `LIKE_POST`, `REPOST`, `FOLLOW`, `CREATE_COMMENT`, `DISLIKE_POST`, `MUTE`, `SEARCH_POSTS`, etc. These are Twitter/Reddit actions — meaningless for molecular interactions like binding, phosphorylation, or transport.

#### 4. Time and behavior models assume human patterns
Simulation timing is configured around Beijing-timezone human activity patterns (peak hours 19–22, off-peak 0–5, etc.). Agent activation follows social media usage rhythms, not biological processes.

### What would need to change for non-social data

Adapting MiroFish for scientific interaction networks (e.g., protein-protein interactions) would require fundamental changes:

| Component | Current (Social) | Needed (Scientific) |
|---|---|---|
| Ontology prompt | People, orgs, media | Proteins, domains, complexes, pathways |
| Agent persona | Age, gender, MBTI, posting style | Functional domains, GO terms, subcellular localization |
| Action space | Post, like, repost, follow | Bind, phosphorylate, inhibit, transport, catalyze |
| Simulation engine | OASIS (Twitter/Reddit) | Molecular interaction simulator |
| Time model | Beijing-timezone activity | Reaction kinetics, cellular timescales |
| Report prompts | Public opinion analysis | Scientific hypothesis generation |

This would essentially be building a different tool on top of MiroFish's architecture.

### Agent Soul: Experimental biological mode (new)

We have implemented an experimental `agent-soul.md` system that partially addresses these limitations. It modifies the ontology generator, persona generator, and time configuration to support biological entities — **without changing the OASIS simulation engine itself**.

#### How to activate biological mode

Set in your `.env` file:

```env
SIMULATION_MODE=biological
```

Then restart the app. The following components change:

| Component | Social Mode (default) | Biological Mode |
|---|---|---|
| Entity types | Person, Organization, Student, etc. | Protein, Enzyme, Transporter, Complex, etc. |
| Fallback types | Person + Organization | Molecule + BiologicalSystem |
| Persona attributes | Age, gender, MBTI, posting style | Molecular weight, domains, GO terms, localization |
| System prompt | "Social media user profile expert" | "Molecular biology expert" |
| Time config | Beijing-timezone circadian rhythm | Uniform 24h activity (no circadian bias) |
| Action meaning | Post = social media post | Post = express/signal molecular function |

#### How it works

The social media actions are **reinterpreted** through the agent's biological persona:

- **CREATE_POST** = Express/Signal — the protein emits a molecular signal or expresses its function
- **LIKE_POST** = Bind/Activate — forming a favorable interaction
- **DISLIKE_POST** = Inhibit/Repress — inhibition or competition
- **REPOST** = Propagate — relaying a signal through a pathway
- **FOLLOW** = Form complex — sustained physical association
- **CREATE_COMMENT** = Downstream response — regulatory feedback

The OASIS engine still runs Twitter/Reddit mechanics underneath, but the LLM driving each agent's behavior generates biologically-themed content based on its molecular persona.

#### The `agent-soul.md` file

Located at `/home/ksa/Models/MiroFish/agent-soul.md`, this file documents:

- Entity type mappings for each mode
- Persona attribute definitions
- Action reinterpretation tables
- Persona templates used by the LLM
- Time configuration rationale

This file serves as a **reference and experimentation guide**. You can duplicate and modify it to create new domain-specific modes (ecological, economic, geopolitical, literary) by setting `SIMULATION_MODE=custom` and pointing `AGENT_SOUL_PATH` to your custom file.

#### Important caveats

- This is **experimental** — the OASIS simulation engine still enforces social media mechanics
- Agent "posts" will contain biological language, but the platform structure (Twitter feeds, Reddit threads) remains
- Results should be interpreted as emergent interaction patterns, not literal molecular dynamics
- Best suited for exploring network-level behavior and information flow, not quantitative biochemistry

---

## Tips

- Start with fewer than 40 simulation rounds to manage API costs
- The free ZEP tier is sufficient for basic simulations
- When using Ollama, make sure the Ollama service is running (`ollama serve`) before starting MiroFish
- Supported upload formats: PDF, Markdown, TXT (max 50 MB)
- For scientific manuscripts, upload the paper as a PDF to simulate public/scientific community discourse about the research — don't upload raw interaction data
