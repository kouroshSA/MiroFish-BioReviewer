"""
Agent Soul配置加载器
根据SIMULATION_MODE加载不同的实体类型、人设模板和行为映射
"""

import os
from typing import Dict, Any, List, Optional
from ..config import Config
from .logger import get_logger

logger = get_logger('mirofish.agent_soul')


# ============== Biological Mode Definitions ==============

BIOLOGICAL_ONTOLOGY_SYSTEM_PROMPT = """You are an expert knowledge graph ontology designer for biological systems. Your task is to analyze the given text and design entity types and relationship types suitable for **biological interaction network simulation**.

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
    "Each protein or molecule becomes a character whose personality, social behavior, and "
    "relationships are shaped by their biological function. A hub protein with 164 interactions "
    "becomes a charismatic, hyper-connected socialite. A stress-response enzyme becomes someone "
    "who thrives under pressure. Generate detailed, creative personas that are scientifically "
    "grounded but expressed as human personality traits. You must return valid JSON. "
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
- Hub proteins (many interaction partners) → extroverted, influential, well-connected socialite
- Bottleneck proteins (high betweenness) → strategic gatekeeper, information broker
- Stress response proteins → resilient, activates under pressure, crisis manager
- Transporters → logistics expert, moves resources, facilitator
- Enzymes/catalysts → transformer, gets things done, action-oriented
- Regulatory proteins → manager, controls others' behavior, decisive
- Structural proteins → steady, reliable, backbone of the community
- Membrane proteins → boundary guardian, gatekeeper, selective about who gets access
- Hypothetical/uncharacterized → mysterious newcomer, unknown potential

Return JSON with these fields:

1. bio: Social media bio (200 chars max) that hints at their molecular identity.
   Example: "Gatekeeper of the outer membrane. 164 connections and counting. I decide who gets in. #NetworkHub #MED4"
2. persona: Detailed character description (2000 chars, plain text) that includes:
   - Character identity: who they are, inspired by their molecular function
   - Personality traits: derived from their biological role (see mapping above)
   - Social behavior: how they interact online, who they engage with, posting style
   - What motivates them: based on their cellular function
   - What stresses them: based on environmental conditions they respond to
   - Their social circle: based on known interaction partners
   - Their position in the community: based on network topology (hub, peripheral, etc.)
   - Hidden depth: their evolutionary story, conservation, or unique adaptations
   - IMPORTANT: weave in real biological details naturally — domain names, functions,
     pathways — as character backstory, not dry scientific description
3. age: A number reflecting their evolutionary age (ancient conserved = older, recently evolved = younger). Range 20-70.
4. gender: "male" or "female" (assign based on character voice, not biology)
5. mbti: MBTI type that matches their functional personality (e.g., hub→ENFJ, regulator→INTJ, transporter→ESFJ)
6. country: Their "neighborhood" — use subcellular location as metaphor (e.g., "Membrane District", "Cytoplasm Central", "Thylakoid Heights")
7. profession: Their molecular function expressed as a job title (e.g., "Chief Transport Officer", "Stress Response Coordinator", "Quality Control Inspector")
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
- Metabolic pathways → a supply chain organization, efficient, process-oriented
- Cellular compartments → a neighborhood or district, defined boundaries
- Regulatory networks → a management committee, policy-driven

Return JSON with these fields:

1. bio: Official account bio (200 chars max) that reflects the system's function.
   Example: "Official account of the Photosystem II Assembly Team. Powering life through light since 2.4 billion years ago."
2. persona: Detailed organizational character (2000 chars, plain text):
   - Who they are as an organization, inspired by their biological function
   - Their collective personality and communication style
   - What they coordinate and manage
   - How they interact with individual members (proteins)
   - Their official positions on key issues (cellular processes)
   - Internal dynamics based on component interactions
   - Historical significance (evolutionary context)
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
