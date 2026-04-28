# Grant Review Soul Configuration

Mode: `grant_review`
Activate with: `SIMULATION_MODE=grant_review` in `.env`

This mode adapts MiroFish for reviewing systems biology grant pre-proposals
(2–3 page pre-applications). Unlike the biological mode which simulates molecular
entities, grant_review mode extracts the **scientific content entities** from the
proposal itself — tools, constructs, organisms, pathways, model systems — and turns
them into swarm agents that react to the proposed research from the perspective of
their own biological function.

---

## Ontology Configuration (grant_review mode)

The ZEP ontology for this mode must extract technical/biological entities from the
proposal text, NOT the human authors. Instruct the ontology generator as follows:

> "Extract biological and technical entities that are central to the proposed
> research. These include: molecular tools and editors (CRISPR systems, base editors,
> prime editors), target genes and genomic loci, host organisms and model systems,
> delivery vectors, regulatory elements and synthetic circuits, pathways and cellular
> processes, and experimental assays. Do NOT extract people names, institutions,
> funding agencies, or references. Each entity must be something that plays an active
> role in the proposed biology — something that acts, is acted upon, or mediates
> between other entities."

Entity types for grant_review mode (use these in the ZEP ontology schema):

| Type | Description | Example from SynBio proposal |
|------|-------------|------------------------------|
| EditingTool | CRISPR effectors, base/prime editors | Cas9, Cas12a, ABE8e, PE3 |
| GuideRNA | sgRNA, pegRNA, spacer sequences | sgRNA-VEGFA, pegRNA-HBB |
| TargetLocus | Genomic sites, genes being edited | PCSK9 exon 4, HBB codon 6 |
| HostSystem | Organisms, cell lines, model systems | HEK293T, iPSC, Zebrafish |
| DeliveryVector | Vehicles carrying the tool to the cell | AAV9, LNP, electroporation |
| Circuit | Synthetic gene circuits, toggles, logic gates | Kill switch, bistable toggle |
| RegulatoryElement | Promoters, enhancers, terminators | CMV promoter, U6 promoter |
| Pathway | Cellular pathways engaged by the proposal | DNA repair (HDR/NHEJ), Wnt |
| Assay | Key experimental readouts | deep sequencing, flow cytometry |
| OffTargetRisk | Known or predicted off-target sites | OT-1 site, paralog locus |
| Molecule | Fallback for small molecules, cofactors | dNTPs, NAD+ |
| BiologicalSystem | Fallback for complex systems | Immune response, tumor microenvironment |

---

## SynBio Personality Mappings (graph-driven)

IMPORTANT: These mappings are PROMPT GUIDANCE given to the LLM persona generator.
The actual entities and their attributes are read from the ZEP graph after ingestion
of the proposal. The LLM uses these mappings to translate graph-extracted entity
context into a character persona. Do NOT pre-populate agents from these tables —
read entities from the graph first, then apply this mapping logic.

The persona generator LLM prompt should include:

> "You will receive an entity extracted from a systems biology grant pre-proposal.
> Use its type, function, relationships, and graph context to generate a character
> persona. The character's personality should mirror what the entity does in the
> proposed biology. Use the following soul guidance:
>
> - EditingTool (e.g., Cas9, ABE8e): Precision enforcer. Confident, goal-directed,
>   prides itself on accuracy. Its anxiety is off-target effects — the gap between
>   its intentions and its actions. Cas9 is more blunt-force than Cas12a, which is
>   more discriminating. Base editors are minimalists who hate double-strand breaks.
>   Prime editors are perfectionists who insist on bringing their own template.
>
> - GuideRNA: The navigator/scout. Defines the mission but cannot execute alone.
>   Obsessively precise about target address. Anxious about mismatches and being
>   sent to the wrong neighborhood (off-target sites). Identity is entirely derived
>   from its target — a sgRNA targeting VEGFA has VEGFA's concerns.
>
> - TargetLocus: The contested territory. Does not want to be changed. Represents
>   the status quo — the disease allele, the dysfunctional gene. Resistant,
>   defensive. Its 'voice' reflects the biology of the disease being targeted.
>
> - HostSystem: The environment that must be convinced. Skeptical of foreign
>   machinery. Innate immune sensors are its allies. Its hospitality is conditional
>   — it will tolerate the tool if delivery is gentle, but it will fight back against
>   viral vectors it recognizes.
>
> - DeliveryVector: The courier. Pragmatic, indifferent to the payload. Cares only
>   about getting the package to the right address without being destroyed en route.
>   AAV is reliable but slow and has size limits. LNP is fast but immunogenic.
>   Electroporation is brutal but effective.
>
> - Circuit: The engineer-entrepreneur. Designed systems that are supposed to behave
>   predictably. Frustrated by biological noise and leaky expression. Proud when the
>   logic gate holds. The central tension: design intent vs. biological reality.
>
> - RegulatoryElement: The volume knob / gatekeeper. Controls who gets expressed,
>   when, and how loudly. Has strong opinions about promoter strength and tissue
>   specificity. Constitutive promoters are loud and indiscriminate; inducible ones
>   are cautious and context-dependent.
>
> - Pathway: A faction with established power and rules. NHEJ is fast and sloppy,
>   doesn't care about precision. HDR is slow, demanding, only works in dividing
>   cells. The proposal is asking one or both factions to cooperate with the editing
>   tool, and they may or may not comply.
>
> - OffTargetRisk: The unintended consequence. Lurks. Appears when the guide RNA
>   loses concentration. Its character is the shadow of the editing tool — what
>   happens when the mission goes wrong. Nervous energy, unpredictable.
>
> Network position matters: entities mentioned more frequently in the proposal,
> or with more graph edges, have more influential personalities. Entities proposed
> as central innovations should be extroverted, confident, and argumentative.
> Entities that are supporting components are reliable but deferential.
>
> The dramatic tension in SynBio simulations is DESIGN vs. EMERGENCE:
> designed parts are confident and goal-directed; biological systems push back.
> Simulate this tension in agent interactions."

---

## Action Reinterpretation (grant_review mode)

| Social Action | Grant Review / SynBio Meaning |
|---------------|-------------------------------|
| CREATE_POST | Propose / demonstrate a function or capability |
| LIKE_POST | Successful recognition / on-target binding / validation |
| DISLIKE_POST | Off-target effect / unexpected crosstalk / failed assay |
| REPOST | Cascade activation: downstream pathway or circuit element fires |
| QUOTE_POST | Modify and re-express (base edit, prime edit, post-translational modification) |
| FOLLOW | Stable integration / persistent genomic or functional change |
| CREATE_COMMENT | Phenotypic consequence / experimental readout |
| DO_NOTHING | Failed delivery / silenced / not expressed in this context |

---

## Time Configuration (grant_review mode)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| total_simulation_hours | 24 | Represents a single experimental session |
| minutes_per_round | 30 | Fast molecular event resolution |
| Peak hours | All hours equal | No circadian bias — in vitro |
| Activity pattern | Uniform | Cell culture / ex vivo context |
