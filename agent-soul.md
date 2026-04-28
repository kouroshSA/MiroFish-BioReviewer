# Agent Soul Configuration

This file defines how MiroFish generates agent personas for different simulation domains.
Set `SIMULATION_MODE` in your `.env` file to activate a specific soul profile.

Supported modes: `social` (default), `biological`, `custom`

See the AI-Guidelines-Agent-Soul.md for instructions on generating domain-specific configurations.

---

## Mode: social (default)

The default MiroFish behavior. Entities are people and organizations interacting on
social media platforms (Twitter/Reddit). No changes needed.

---

## Mode: biological

For simulating biological systems — metabolic networks, virus-host interactions,
gene regulatory networks, protein interaction networks, drug-target relationships.

### Key Design: Biological Entities as Characters

Biological mode uses a **hybrid approach**: ZEP's entity extraction still recognizes
entities as Person/Organization types (because its NER is trained on social text),
but the **persona generation** creates characters whose personalities are shaped by
their biological function. This lets ZEP work naturally while producing biologically
meaningful simulations.

During graph building, the text is preprocessed to "personify" biological entities —
replacing molecular/metabolic language with social analogues so ZEP can extract
entities. Then during persona generation, each entity gets a character whose traits
map from biology.

### Personality Mapping (Biology → Character Traits)

#### For Metabolic / Flux Balance Analysis studies:

| Biological Role | Character Personality |
|---|---|
| Metabolic hub gene (many pathway connections) | Influential power broker, controls resource flow |
| TCA cycle enzyme (SDHA, FH, IDH) | Establishment figure, core infrastructure maintainer |
| Mitochondrial transporter (SLC25 family) | Logistics coordinator, supply chain manager, gatekeeper |
| Redox balance enzyme (CAT, SOD) | Security chief, stress responder, damage control |
| Viral antagonist (SARS-CoV-2, MERS-CoV) | Invader, disruptor, resource hijacker |
| Drug/therapeutic intervention | External enforcer, rescue agent, mercenary |
| Nucleotide metabolism gene | Weapons manufacturer (viruses need nucleotides to replicate) |
| Fatty acid metabolism gene | Energy banker, lipid resource controller |
| Pan-coronavirus target | Universal vulnerability, everyone's weak point |
| Virus-specific target | Specialized weakness, exploitable only by one adversary |
| Rescue gene pair (KO pair) | Saboteur team, working in pairs to disrupt the hijacking |
| Pathway (glycolysis, TCA, etc.) | Faction/guild, organized group with shared interests |

#### For Protein-Protein Interaction studies:

| Biological Role | Character Personality |
|---|---|
| Hub protein (many interactions) | Extroverted, influential, hyper-connected socialite |
| Bottleneck protein (high betweenness) | Strategic gatekeeper, information broker |
| Stress response protein | Resilient, crisis manager, thrives under pressure |
| Transporter | Logistics expert, facilitator, moves resources |
| Enzyme/catalyst | Action-oriented, transformer, gets things done |
| Regulatory protein | Manager, controls others, decisive |
| Structural protein | Steady, reliable, backbone of the community |
| Membrane protein | Boundary guardian, selective gatekeeper |
| Hypothetical/uncharacterized | Mysterious newcomer, unknown potential |

### Persona Attributes

Instead of age/gender/MBTI, biological agents have attributes derived from their
molecular or metabolic function:

| Attribute | Metabolic Example | PPI Example |
|---|---|---|
| `role` | "TCA cycle enzyme" | "Outer membrane porin" |
| `location` | "Mitochondrial matrix" | "Thylakoid membrane" |
| `function` | "Succinate oxidation" | "Non-selective pore transport" |
| `partners` | "Complex II, ubiquinone" | "CAE19570, CAE18591" |
| `vulnerability` | "Targeted by metformin" | "Hub removal fragments network" |
| `temporal` | "Emerges as hub at 48h" | "Constitutively expressed" |
| `conservation` | "Pan-coronavirus target" | "HL-ecotype specific" |

### Action Reinterpretation

Social media actions are reframed as biological communication:

| Social Action | Metabolic Meaning | PPI Meaning |
|---|---|---|
| CREATE_POST | Produce metabolite / emit flux signal | Express function / emit signal |
| LIKE_POST | Activate pathway / increase flux | Bind / activate partner |
| DISLIKE_POST | Inhibit reaction / block flux | Inhibit / compete |
| REPOST | Propagate metabolic signal downstream | Relay signal through pathway |
| QUOTE_POST | Modify metabolite / transform substrate | Post-translational modification |
| FOLLOW | Form metabolic dependency | Form stable complex |
| CREATE_COMMENT | Downstream metabolic consequence | Downstream regulatory effect |
| DO_NOTHING | Reaction inactive / zero flux | Not expressed / dormant |

### Time Configuration

Biological simulations use different time semantics:

| Parameter | Value | Rationale |
|---|---|---|
| `total_simulation_hours` | 24–48 | Matches infection time course (24h and 48h) |
| `minutes_per_round` | 30–60 | Metabolic event resolution |
| Peak hours | All hours equal | No circadian bias for cell culture |
| Activity pattern | Condition-driven | Infection stage, drug treatment timing |

---

## Mode: custom

For user-defined domains. Copy the biological template above and modify:

1. **Entity types** — Define your domain's entity categories
2. **Persona attributes** — What properties matter for your entities
3. **Action reinterpretation** — Map social actions to domain-specific meanings
4. **Persona template** — LLM prompt for generating entity descriptions
5. **Time configuration** — Appropriate timescales for your domain

### Example domains you might configure:

- **Ecological**: Species, habitats, resources — simulate ecosystem dynamics
- **Economic**: Companies, markets, regulators — simulate market behavior
- **Geopolitical**: Nations, alliances, treaties — simulate international relations
- **Literary**: Characters, factions, settings — simulate narrative evolution

To use custom mode, set `SIMULATION_MODE=custom` and `AGENT_SOUL_PATH` to your
custom soul file in `.env`.

---

## How It Works

When `SIMULATION_MODE` is set to a non-default value:

1. **Ontology generation** uses standard social entity types (Person/Organization)
   so ZEP's NER can extract entities from the text
2. **Text enrichment** personifies biological entities (protein IDs, gene names,
   pathway names) as "researchers" and "key figures" so ZEP recognizes them
3. **Persona generation** produces characters whose personality traits map from
   their biological function — a TCA cycle enzyme becomes an establishment power
   broker, a virus becomes an invader and resource hijacker
4. **Simulation actions** are reinterpreted — the OASIS engine still runs
   Twitter/Reddit mechanics, but agent LLM prompts frame actions in
   domain-specific language
5. **Report generation** produces domain-appropriate analysis

The OASIS simulation engine itself is not modified — only the LLM prompts that drive
agent behavior are changed.

---

## Mode: grant_review

For reviewing systems biology grant pre-proposals (2–3 page pre-applications).

See `grant-review-soul.md` for the full soul configuration.

Key differences from `biological` mode:
- Ontology extracts scientific/technical entities FROM the proposal content
  (CRISPR tools, target genes, model systems, pathways) — NOT human authors
- Swarm agent personas are built from graph entities using SynBio personality mappings
- Reviewer panel (3 agents) runs after simulation, before Reporter
- Reporter synthesis follows grant review report structure
- Time config: 24h, 30-min rounds, uniform activity

Activate: `SIMULATION_MODE=grant_review`
