"""
Agent Soul Configuration Loader
Loads different entity types, persona templates, and behavior mappings based on SIMULATION_MODE
"""

import os
from typing import Dict, Any, List, Optional
from ..config import Config
from .logger import get_logger

logger = get_logger('mirofish.agent_soul')


# ============== Biological Mode Definitions ==============

BIOLOGICAL_ONTOLOGY_SYSTEM_PROMPT = """You are an expert knowledge graph ontology designer for biological systems. Your task is to analyze the given text and design entity types and relationship types suitable for **biological interaction network simulation**. Keep your output concise — return only the required JSON, no extra explanation.

**IMPORTANT: You must output valid JSON only. No other content.**

## Core Task Background

We are building a **biological interaction simulation system**. In this system:
- Each entity is a biological molecule, complex, or system that can interact with others
- Entities interact through binding, catalysis, regulation, transport, and signaling
- We need to simulate how molecular interactions propagate through biological networks

Therefore, **entities must be real biological molecules or systems that can interact**:

**Can be**:
- Individual proteins (enzymes, transporters, regulators, structural proteins)
- Protein complexes (ribosomes, photosystems, ATP synthase)
- Functional domains (TPR repeats, kinase domains, binding motifs)
- Metabolic or signaling pathways
- Cellular compartments or systems
- Genomic elements (operons, regulatory regions)

**Cannot be**:
- Abstract concepts ("evolution", "fitness", "adaptation")
- Experimental methods ("Y2H screening", "mass spectrometry")
- Statistical measures ("p-value", "enrichment score")

## Output Format

Output JSON with the following structure:

```json
{
    "entity_types": [
        {
            "name": "EntityTypeName (English, PascalCase)",
            "description": "Brief description (English, max 100 chars)",
            "attributes": [
                {
                    "name": "attribute_name (English, snake_case)",
                    "type": "text",
                    "description": "Attribute description"
                }
            ],
            "examples": ["Example entity 1", "Example entity 2"]
        }
    ],
    "edge_types": [
        {
            "name": "RELATIONSHIP_NAME (English, UPPER_SNAKE_CASE)",
            "description": "Brief description (English, max 100 chars)",
            "source_targets": [
                {"source": "SourceEntityType", "target": "TargetEntityType"}
            ],
            "attributes": []
        }
    ],
    "analysis_summary": "Brief analysis of the text content"
}
```

## Design Guidelines

### 1. Entity Types - Must Follow Strictly

**Quantity: Exactly 10 entity types**

**Hierarchy (must include both specific and fallback types)**:

A. **Fallback types (must be the last 2)**:
   - `Molecule`: Any molecular entity not fitting other specific types
   - `BiologicalSystem`: Any biological system, organelle, or compartment

B. **Specific types (8, designed based on text content)**:
   - Design based on the major biological entities in the text
   - E.g., for a proteomics study: `Protein`, `Enzyme`, `Transporter`, `Regulator`, `Complex`
   - E.g., for a genomics study: `Gene`, `Operon`, `Promoter`, `TranscriptionFactor`

### 2. Relationship Types

- Quantity: 6-10
- Relationships should reflect real biological interactions
- Ensure source_targets cover your defined entity types

### 3. Attributes

- 1-3 key attributes per entity type
- **Reserved names (cannot use)**: name, uuid, group_id, created_at, summary
- Recommended: `gene_id`, `molecular_weight`, `subcellular_location`, `functional_domain`, `go_annotation`, `organism`

## Entity Type Reference

**Molecular (specific)**:
- Protein: Individual protein or polypeptide
- Enzyme: Catalytic protein
- Transporter: Membrane transport protein
- Regulator: Regulatory molecule (transcription factor, sigma factor)
- Receptor: Signal-receiving protein

**Structural (specific)**:
- Complex: Multi-protein assembly
- Domain: Protein structural/functional domain
- Membrane: Cellular membrane or envelope

**Systems (specific)**:
- Pathway: Metabolic or signaling pathway
- Genome: Genome, operon, or genomic region

**Fallback**:
- Molecule: Any molecular entity
- BiologicalSystem: Any biological system or compartment

## Relationship Type Reference

- BINDS_TO: Physical binding interaction
- PHOSPHORYLATES: Phosphorylation
- INHIBITS: Inhibition or repression
- ACTIVATES: Activation or stimulation
- CATALYZES: Enzymatic catalysis
- TRANSPORTS: Substrate transport
- REGULATES: Regulatory relationship
- PART_OF: Component of a complex or pathway
- LOCATED_IN: Subcellular localization
- INTERACTS_WITH: General physical interaction
- CO_EXPRESSED_WITH: Co-expression relationship
- HOMOLOGOUS_TO: Evolutionary relationship
"""

BIOLOGICAL_INDIVIDUAL_ENTITY_TYPES = [
    "protein", "enzyme", "transporter", "regulator", "receptor",
    "domain", "gene", "molecule"
]

BIOLOGICAL_GROUP_ENTITY_TYPES = [
    "complex", "pathway", "membrane", "biologicalsystem",
    "genome", "operon", "organelle", "compartment"
]

BIOLOGICAL_PERSONA_SYSTEM_PROMPT = (
    "You are an expert at creating vivid character personas inspired by molecular biology. "
    "Each biological entity — whether a gene, enzyme, metabolic pathway, virus, drug, or "
    "protein — becomes a character whose personality, social behavior, and relationships are "
    "shaped by their biological function. A metabolic hub gene becomes a power broker controlling "
    "resource flow. A virus becomes an invader hijacking the host's infrastructure. A drug becomes "
    "an external enforcer or rescue agent. A mitochondrial transporter becomes a logistics "
    "coordinator managing supply chains. Generate creative personas that are "
    "scientifically grounded but expressed as human personality traits. "
    "IMPORTANT: Keep all responses short and concise. Be brief — quality over quantity. "
    "You must return valid JSON. "
    "All string values must not contain unescaped newlines. Use English."
)

BIOLOGICAL_ACTION_MAP = {
    "CREATE_POST": "Express/Signal — emitting a molecular signal or expressing a function",
    "LIKE_POST": "Bind/Activate — forming a favorable interaction, binding, or activation",
    "DISLIKE_POST": "Inhibit/Repress — inhibition, competition, or destabilization",
    "REPOST": "Propagate — relaying or amplifying a signal through a pathway",
    "QUOTE_POST": "Modify/Process — post-translational modification or processing",
    "FOLLOW": "Form complex — sustained physical association or stable complex",
    "CREATE_COMMENT": "Downstream response — downstream regulatory effect or feedback",
    "DO_NOTHING": "Inactive/Dormant — not expressed or not active under current conditions",
    "LIKE_COMMENT": "Support downstream — reinforce a downstream regulatory effect",
    "DISLIKE_COMMENT": "Counter-regulate — oppose a downstream effect",
    "SEARCH_POSTS": "Sense environment — detect signals or substrates",
    "SEARCH_USER": "Find interaction partner — seek specific binding partners",
}


def build_biological_individual_prompt(
    entity_name: str,
    entity_type: str,
    entity_summary: str,
    entity_attributes: Dict[str, Any],
    context: str
) -> str:
    """Build persona prompt for individual biological entities (proteins, etc.)"""
    import json as _json

    attrs_str = _json.dumps(entity_attributes, ensure_ascii=False) if entity_attributes else "None"
    context_str = context[:3000] if context else "No additional context"

    action_lines = "\n".join(
        f"- When you '{action}': {meaning}"
        for action, meaning in BIOLOGICAL_ACTION_MAP.items()
    )

    return f"""Create a character persona for a social media simulation. This character represents
a biological entity whose personality and social behavior are shaped by their molecular function.

Entity name: {entity_name}
Entity type (from ZEP): {entity_type}
Entity summary: {entity_summary or 'Not available'}
Entity attributes: {attrs_str}

Additional context from knowledge graph:
{context_str}

RULES FOR PERSONALITY MAPPING:

For metabolic genes / enzymes:
- Metabolic hub gene (many pathway connections) → influential power broker, controls resource flow
- TCA cycle enzyme (SDHA, FH, IDH) → establishment figure, core infrastructure maintainer
- Mitochondrial transporter (SLC25 family) → logistics coordinator, supply chain manager
- Redox balance enzyme (CAT, SOD) → security chief, stress responder, damage control
- Nucleotide metabolism gene → weapons manufacturer (viruses need nucleotides)
- Fatty acid metabolism gene → energy banker, lipid resource controller
- Rescue gene pair member → saboteur, resistance fighter working to disrupt hijacking

For viruses / pathogens:
- Pathogenic virus → invader, resource hijacker, occupying force
- Pan-coronavirus target → universal vulnerability everyone argues about

For drugs / interventions:
- Validated drug (metformin, statins) → proven enforcer, rescue agent with track record
- Experimental drug → untested recruit, promising but unproven
- Failed drug (ribavirin) → disgraced former ally, cautionary tale

For proteins / interaction network entities:
- Hub protein (many interactions) → extroverted, influential, hyper-connected socialite
- Bottleneck protein (high betweenness) → strategic gatekeeper, information broker
- Stress response protein → resilient, crisis manager, thrives under pressure
- Transporter → logistics expert, moves resources, facilitator
- Membrane protein → boundary guardian, selective gatekeeper
- Hypothetical/uncharacterized → mysterious newcomer, unknown potential

Return JSON with these fields:

1. bio: Social media bio (150 chars max) that hints at their biological identity.
   Example: "Mitochondrial gatekeeper. I control what gets in and out. #SLC25"
2. persona: Concise character description (500 chars max, plain text) that includes:
   - Character identity and personality traits (from biological role)
   - Key allies/enemies and network position
   - What motivates and threatens them
   - IMPORTANT: be concise — capture the essence in a few sentences, not paragraphs
3. age: A number (20-70). Ancient conserved genes = older, recently evolved/virus-specific = younger. Viruses = young (25-30). Drugs = middle-aged (40-50).
4. gender: "male" or "female" (assign based on character voice, not biology)
5. mbti: MBTI type that matches their functional personality (e.g., hub gene→ENFJ, virus→ENTP, drug→ISTJ, transporter→ESFJ)
6. country: Their "neighborhood" — use cellular location as metaphor (e.g., "Mitochondrial Matrix", "Cytoplasm Central", "Membrane District", "Viral Enclave", "Pharmacy Row")
7. profession: Their function as a job title (e.g., "Chief Metabolic Officer", "Supply Chain Director", "Hostile Takeover Specialist", "FDA-Approved Crisis Responder")
8. interested_topics: List of 3-5 topics they'd post about, mixing biology and social themes

IMPORTANT:
- All field values must be strings or numbers, no newlines
- persona must be one continuous text description
- Use English throughout
- Be creative but scientifically grounded — every personality trait should map to a real biological property
"""


def build_biological_group_prompt(
    entity_name: str,
    entity_type: str,
    entity_summary: str,
    entity_attributes: Dict[str, Any],
    context: str
) -> str:
    """Build persona prompt for biological systems/complexes/pathways"""
    import json as _json

    attrs_str = _json.dumps(entity_attributes, ensure_ascii=False) if entity_attributes else "None"
    context_str = context[:3000] if context else "No additional context"

    action_lines = "\n".join(
        f"- When you '{action}': {meaning}"
        for action, meaning in BIOLOGICAL_ACTION_MAP.items()
    )

    return f"""Create a character persona for a social media simulation. This character represents
a biological system, complex, or organization whose collective personality reflects its function.

Entity name: {entity_name}
Entity type (from ZEP): {entity_type}
Entity summary: {entity_summary or 'Not available'}
Entity attributes: {attrs_str}

Additional context from knowledge graph:
{context_str}

RULES FOR ORGANIZATIONAL PERSONALITY:
- Protein complexes → a tight-knit team, speak with one voice, coordinated
- Metabolic pathways (glycolysis, TCA, fatty acid oxidation) → a supply chain guild, process-oriented, protective of their territory
- Cellular compartments (mitochondria, cytoplasm) → a neighborhood or district with defined boundaries and residents
- Regulatory networks → a management committee, policy-driven
- Virus families (betacoronaviruses) → an invading faction, coordinated assault team
- Drug classes (antivirals, metabolic modulators) → an intervention force, external peacekeepers
- Gene families (SLC25 transporters) → a logistics union, coordinated transport network

Return JSON with these fields:

1. bio: Official account bio (150 chars max) that reflects the system's function.
   Example: "TCA Cycle Authority. Keeping the energy flowing since the origin of aerobic life."
2. persona: Concise organizational character (500 chars max, plain text):
   - Who they are, collective personality, what they coordinate
   - Key positions, internal dynamics, historical significance
   - IMPORTANT: be concise — capture the essence in a few sentences
3. age: 30 (standard for organizational accounts)
4. gender: "other" (organizational account)
5. mbti: MBTI reflecting organizational style (e.g., ISTJ for rigid systems, ENTJ for active regulators)
6. country: Their "district" — subcellular location
7. profession: Organizational role (e.g., "Energy Production Division", "Transport Authority")
8. interested_topics: List of 3-5 topics the organization would post about

IMPORTANT:
- All field values must be strings or numbers, no newlines
- persona must be one continuous text description
- Use English throughout
"""


def build_biological_user_message_suffix() -> str:
    """Suffix for ontology generation user message in biological mode"""
    return """
Based on the content above, design entity types and relationship types suitable for biological interaction simulation.

**Rules to follow**:
1. Output exactly 10 entity types
2. The last 2 must be fallback types: Molecule (molecular fallback) and BiologicalSystem (system fallback)
3. The first 8 are specific types designed from the text content
4. All entity types must be real biological molecules or systems that can interact
5. Attribute names cannot use reserved words: name, uuid, group_id — use gene_id, protein_family, etc.
"""


def build_biological_fallback_types():
    """Fallback entity types for biological mode"""
    molecule_fallback = {
        "name": "Molecule",
        "description": "Any molecular entity not fitting other specific molecular types.",
        "attributes": [
            {"name": "molecule_id", "type": "text", "description": "Identifier for the molecule"},
            {"name": "molecule_type", "type": "text", "description": "Type of molecule"}
        ],
        "examples": ["small molecule", "cofactor", "metabolite"]
    }

    system_fallback = {
        "name": "BiologicalSystem",
        "description": "Any biological system, organelle, or compartment.",
        "attributes": [
            {"name": "system_id", "type": "text", "description": "Identifier for the system"},
            {"name": "system_type", "type": "text", "description": "Type of biological system"}
        ],
        "examples": ["cell membrane", "cytoplasm", "thylakoid"]
    }

    return molecule_fallback, system_fallback


def get_biological_default_time_config(num_entities: int) -> Dict[str, Any]:
    """Default time config for biological simulation (no circadian bias)"""
    return {
        "total_simulation_hours": 24,
        "minutes_per_round": 30,
        "agents_per_hour_min": max(1, num_entities // 10),
        "agents_per_hour_max": max(3, num_entities // 3),
        "peak_hours": list(range(24)),  # All hours equally active
        "off_peak_hours": [],
        "morning_hours": [],
        "work_hours": list(range(24)),
        "reasoning": "Biological simulation: uniform activity across all hours (no circadian bias for molecular interactions)"
    }


def get_biological_time_config_prompt(context: str, num_entities: int, max_agents_allowed: int) -> str:
    """Time config prompt for biological simulation"""
    context_truncated = context[:5000]
    return f"""Based on the following biological simulation scenario, generate a time configuration.

{context_truncated}

## Task
Generate a time configuration JSON for a molecular interaction simulation.

### Key principles:
- Molecular interactions do not follow human circadian rhythms
- Activity should be distributed based on biological conditions, not time of day
- All hours can be equally active unless specific conditions dictate otherwise
- Simulation duration should reflect the biological timescale (hours to days)

### Return JSON format (no markdown):

{{
    "total_simulation_hours": 24,
    "minutes_per_round": 30,
    "agents_per_hour_min": 5,
    "agents_per_hour_max": {max_agents_allowed},
    "peak_hours": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
    "off_peak_hours": [],
    "morning_hours": [],
    "work_hours": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
    "reasoning": "Explanation of time configuration"
}}

Field descriptions:
- total_simulation_hours (int): Total simulation duration, 12-72 hours
- minutes_per_round (int): Minutes per round, 15-60 minutes
- agents_per_hour_min (int): Minimum active agents per hour (range: 1-{max_agents_allowed})
- agents_per_hour_max (int): Maximum active agents per hour (range: 1-{max_agents_allowed})
- peak_hours (int array): High activity periods (can be all hours)
- off_peak_hours (int array): Low activity periods (can be empty)
- reasoning (string): Brief explanation
"""


# ============== Mode Detection ==============

def is_biological_mode() -> bool:
    """Check if current simulation mode is biological"""
    return Config.SIMULATION_MODE.lower() == 'biological'


def is_social_mode() -> bool:
    """Check if current simulation mode is social (default)"""
    return Config.SIMULATION_MODE.lower() in ('social', '')


def get_simulation_mode() -> str:
    """Get current simulation mode"""
    return Config.SIMULATION_MODE.lower() or 'social'
