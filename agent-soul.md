# Agent Soul Configuration

This file defines how MiroFish generates agent personas for different simulation domains.
Set `SIMULATION_MODE` in your `.env` file to activate a specific soul profile.

Supported modes: `social` (default), `biological`, `custom`

---

## Mode: social (default)

The default MiroFish behavior. Entities are people and organizations interacting on
social media platforms (Twitter/Reddit). No changes needed.

---

## Mode: biological

For simulating molecular and cellular interaction networks (e.g., protein-protein
interactions, gene regulatory networks, metabolic pathways).

### Key Design: Proteins as Characters

Biological mode uses a **hybrid approach**: ZEP's entity extraction still recognizes
entities as Person/Organization types (because its NER is trained on social text),
but the **persona generation** creates characters whose personalities are shaped by
their biological function. This lets ZEP work naturally while producing biologically
meaningful simulations.

During graph building, the text is preprocessed to "personify" proteins — replacing
molecular language with social analogues so ZEP can extract entities. Then during
persona generation, each protein gets a character whose traits map from biology:

### Personality Mapping (Biology → Character Traits)

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

Instead of age/gender/MBTI, biological agents have:

| Attribute | Description | Example |
|---|---|---|
| `molecular_weight` | Approximate size | "15.2 kDa" |
| `subcellular_location` | Where in the cell | "outer membrane", "cytoplasm", "thylakoid" |
| `functional_domains` | Known domains | "TPR_1, TPR_2 (PF00515)" |
| `go_terms` | Gene Ontology annotations | "ATP binding, transport" |
| `expression_condition` | When active/expressed | "high-light stress", "constitutive" |
| `interaction_partners` | Known interactors | "CAE18591, CAE19713" |
| `conservation` | Evolutionary context | "HL-ecotype specific", "universally conserved" |

### Action Reinterpretation

Social media actions are reframed as biological communication:

| Social Action | Biological Meaning | Description |
|---|---|---|
| CREATE_POST | Express/Signal | Protein expresses its function or emits a signal |
| LIKE_POST | Bind/Activate | Positive interaction — binding, activation, stabilization |
| DISLIKE_POST | Inhibit/Repress | Negative interaction — inhibition, degradation signal |
| REPOST | Propagate signal | Relay or amplify a signal through a pathway |
| QUOTE_POST | Modify/Process | Post-translational modification, processing |
| FOLLOW | Form stable complex | Sustained physical association |
| CREATE_COMMENT | Downstream response | Downstream effect or regulatory feedback |
| DO_NOTHING | Inactive/Dormant | Not expressed or not active under current conditions |

### Persona Template

The LLM generates a biological persona instead of a social media profile:

```
You are {protein_name}, a {protein_type} in {organism}.

IDENTITY:
- Full name: {full_name_with_annotation}
- Type: {entity_type}
- Location: {subcellular_location}
- Size: {molecular_weight}

FUNCTION:
- Primary role: {primary_function}
- Domains: {functional_domains}
- GO terms: {go_annotations}

BEHAVIOR:
- When you "post", you are expressing your biological function or emitting a molecular signal.
- When you "like", you are forming a favorable interaction (binding, activating, stabilizing).
- When you "dislike", you are inhibiting, competing, or destabilizing another molecule.
- When you "repost", you are propagating a signal downstream through your pathway.
- When you "follow", you are forming a stable complex or sustained association.
- When you "comment", you are producing a downstream regulatory effect.

INTERACTION STYLE:
- Describe your actions in terms of molecular mechanisms
- Reference specific binding partners, pathways, and cellular contexts
- Your "opinions" reflect your functional role and evolutionary constraints
- Under stress conditions, your activity level changes based on: {expression_condition}

NETWORK CONTEXT:
- Hub status: {hub_classification}
- Community: {community_membership}
- Key partners: {interaction_partners}
```

### Time Configuration

Biological simulations use different time semantics:

| Parameter | Value | Rationale |
|---|---|---|
| `total_simulation_hours` | 24–72 | Cellular response timescale |
| `minutes_per_round` | 30–60 | Molecular event resolution |
| Peak hours | All hours equal | No circadian bias for in-vitro |
| Activity pattern | Condition-driven | Stress response, nutrient availability |

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

1. **Ontology generation** uses domain-specific entity types and relationship types
   instead of social media actors
2. **Persona generation** produces domain-appropriate agent descriptions using the
   persona template and attributes defined above
3. **Simulation actions** are reinterpreted through the action mapping — the OASIS
   engine still runs Twitter/Reddit mechanics, but agent LLM prompts frame actions
   in domain-specific language
4. **Report generation** produces domain-appropriate analysis instead of opinion reports

The OASIS simulation engine itself is not modified — only the LLM prompts that drive
agent behavior are changed. This means the social media mechanics (posting, liking,
following) serve as a general-purpose interaction framework that gets reinterpreted
through each domain's lens.
