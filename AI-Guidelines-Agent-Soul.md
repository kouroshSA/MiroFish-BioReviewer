# AI Guidelines: Generating Agent Souls from Scientific Manuscripts

This document provides structured instructions for an AI model to critically read a scientific manuscript and generate appropriate agent-soul configurations for MiroFish-BIO simulations.

---

## Overview

MiroFish-BIO simulates biological systems by turning molecular entities (proteins, genes, pathways, drugs, viruses) into characters with personalities derived from their biological function. The quality of a simulation depends on how well the agent-soul configuration captures the dynamics described in the source manuscript.

An AI model should follow the steps below to produce a domain-appropriate `agent-soul` configuration.

---

## Step 1: Critical Reading of the Manuscript

Read the manuscript end-to-end and extract:

1. **Study type** — What kind of study is this?
   - Proteomics / protein-protein interaction network
   - Metabolomics / flux balance analysis
   - Transcriptomics / gene regulatory network
   - Host-pathogen interaction
   - Drug-target analysis
   - Multi-omics integration
   - Other

2. **Key biological entities** — Identify the major players:
   - Which specific proteins, genes, enzymes, or metabolites are central?
   - Are there pathogens, drugs, or external perturbations?
   - What are the hubs, bottlenecks, or most-discussed entities?

3. **Interaction types** — What kinds of relationships dominate?
   - Physical binding, phosphorylation, inhibition, activation
   - Metabolic flux, substrate-product, enzyme-reaction
   - Regulatory (transcription factor-target), signaling cascades
   - Host-pathogen hijacking, drug-target intervention

4. **Temporal dynamics** — Does the system change over time?
   - Time-course data (e.g., 0h, 24h, 48h post-infection)
   - Condition-dependent changes (treated vs. untreated, wild-type vs. mutant)
   - Developmental stages, disease progression

5. **Key findings and narrative** — What is the story?
   - What is the central conflict (e.g., virus vs. host metabolism)?
   - What are the surprises or unexpected connections?
   - Which entities are validated (clinically, experimentally) vs. predicted?

---

## Step 2: Determine Entity Categories

Based on the manuscript, define 8 specific entity types plus 2 fallback types (total: 10).

**Selection criteria:**
- Entity types should reflect the actual biological categories in the paper
- Each type should have at least 2-3 real examples from the manuscript
- Types should be distinguishable — avoid overlapping categories
- Consider both individual molecules and systems/complexes

**Examples by study type:**

| Study Type | Typical Entity Types |
|---|---|
| PPI network | Protein, Enzyme, Transporter, Regulator, Receptor, Complex, Pathway, Domain |
| Metabolic/FBA | Enzyme, Transporter, Metabolite, Pathway, Cofactor, Regulator, Complex, Gene |
| Host-pathogen | HostProtein, ViralProtein, Enzyme, Transporter, DrugCompound, Pathway, Complex, Receptor |
| Drug-target | DrugCompound, TargetProtein, Enzyme, Transporter, Pathway, Receptor, Biomarker, Complex |

Always end with the two fallback types: `Molecule` and `BiologicalSystem`.

---

## Step 3: Design Personality Mappings

Map each entity type to character traits. The mapping should reflect the entity's biological function in the context of the specific manuscript.

**Guiding principles:**
- A protein's personality should mirror what it does in the cell
- Network position matters: hubs are influential, peripherals are specialists
- Temporal changes create character arcs (e.g., a gene that becomes a hub at 48h is a "rising star")
- Antagonistic relationships (virus vs. host, drug vs. target) create natural dramatic tension

**Template for each entity type:**

```
[Entity type]: [Biological role in this paper] -> [Character personality]
  - Network position: [hub/peripheral/bottleneck/bridge] -> [social influence level]
  - Temporal behavior: [constitutive/induced/repressed] -> [character stability]
  - Interactions: [activator/inhibitor/transporter/structural] -> [social style]
  - Vulnerability: [drug target/knockout effect/mutation] -> [character weakness]
```

---

## Step 4: Define Relationship Types

Select 6-10 relationship types that reflect the actual interactions in the manuscript.

**Selection criteria:**
- Prioritize relationships that are experimentally validated in the paper
- Include both direct (physical binding) and indirect (regulatory) relationships
- Cover positive (activation, cooperation) and negative (inhibition, competition) interactions

**Map each relationship to a social interaction style:**

| Biological Relationship | Social Analogue |
|---|---|
| Physical binding | Close alliance, partnership |
| Phosphorylation | Empowerment, promotion |
| Inhibition | Opposition, rivalry |
| Catalysis | Mentorship, enabling |
| Transport | Logistics, facilitation |
| Co-expression | Shared community, same social circle |
| Degradation | Hostile takeover, elimination |

---

## Step 5: Calibrate Action Interpretations

Review the default action map and adjust for the manuscript's domain:

```
CREATE_POST  -> [What does "expressing" mean in this system?]
LIKE_POST    -> [What does "activating/supporting" mean?]
DISLIKE_POST -> [What does "inhibiting/opposing" mean?]
REPOST       -> [What does "signal relay" mean?]
QUOTE_POST   -> [What does "modification/processing" mean?]
FOLLOW       -> [What does "forming a stable complex" mean?]
DO_NOTHING   -> [What does "inactive/dormant" mean?]
```

Ensure the actions make biological sense for the specific system. For example:
- In a metabolic network, REPOST = "propagate flux signal downstream"
- In a PPI network, REPOST = "relay phosphorylation cascade"
- In a host-pathogen study, LIKE_POST for a virus = "successfully hijack resource"

---

## Step 6: Set Time Configuration

Determine appropriate simulation timescales from the manuscript:

- **Duration**: Match the experimental timeframe (e.g., 48h infection time-course -> 48h simulation)
- **Resolution**: Set minutes_per_round based on the speed of the biological processes (metabolic: 15-30 min, transcriptional: 30-60 min, developmental: 60+ min)
- **Activity pattern**: Molecular simulations typically use uniform activity across all hours (no circadian bias) unless the paper specifically studies circadian rhythms

---

## Step 7: Generate the Configuration

Produce the final output as structured configuration that includes:

1. **Entity types** with attributes and examples drawn from the manuscript
2. **Personality mappings** specific to the entities in the paper
3. **Relationship types** reflecting the paper's interaction data
4. **Action interpretations** calibrated for the domain
5. **Time configuration** matching the experimental design
6. **System prompt fragments** for persona generation, incorporating paper-specific context

---

## Step 8: Validation Checklist

Before finalizing, verify:

- [ ] Every entity type has real examples from the manuscript
- [ ] Personality mappings are scientifically grounded (each trait maps to a real function)
- [ ] Relationship types cover the main interactions discussed in the paper
- [ ] No abstract concepts are listed as entities (no "evolution", "fitness", "p-value")
- [ ] Time configuration matches the experimental design in the paper
- [ ] Action interpretations make biological sense for this specific system
- [ ] The configuration would produce agents that could "argue" about the paper's key findings
- [ ] Hub entities have appropriately influential personalities
- [ ] Antagonistic entities (virus vs. host, drug vs. target) have opposing traits
- [ ] Responses are concise — persona descriptions should be 500 characters max

---

## Example: Host-Pathogen Metabolic Study

For a paper studying SARS-CoV-2 metabolic hijacking via flux balance analysis:

**Entity types**: HostEnzyme, ViralProtein, Transporter, MetabolicHub, DrugCompound, RescueGene, SignalingProtein, PathwayRegulator, Molecule, BiologicalSystem

**Key personality mappings**:
- SDHA (TCA cycle hub) -> "Old-guard establishment power broker, controls the energy supply everyone depends on"
- SARS-CoV-2 NSP12 -> "Ruthless invader, hijacks nucleotide production lines for its own replication"
- Metformin -> "Battle-tested enforcer with FDA credentials, intervenes to restore metabolic order"
- SLC25A1 (citrate transporter) -> "Logistics coordinator at the mitochondrial border, decides what crosses"

**Time config**: 48h duration, 30-min rounds, uniform activity (cell culture, no circadian bias)

---

## Notes

- These guidelines are meant to be followed by an AI model (e.g., Claude, GPT-4, Qwen) that has access to the manuscript text
- The AI should adapt these guidelines to the specific paper — not every section will apply to every study type
- When in doubt, prioritize biological accuracy over creative flair
- Keep all generated text concise to avoid bloating simulation prompts
