# Example Prompts for MIROFISH-BIO

These are tested prompts for the biological simulation mode (`SIMULATION_MODE=biological`). Each prompt is designed to be pasted into the simulation requirement field in the MIROFISH-BIO UI alongside the corresponding PDF upload.

---

## 1. NiTRO — Coronavirus Metabolic Warfare (Detailed Prompt)

**Paper:** NiTRO computational tool for coronavirus-host metabolic hijacking analysis

**Prompt:**
```
// Simulate the dynamics of coronavirus-host metabolic warfare. This study investigates how three
// pathogenic coronaviruses (SARS-CoV, SARS-CoV-2, and MERS-CoV) hijack host cell metabolism,
// and how a computational tool called NiTRO identifies gene-pair knockouts that can rescue
// infected metabolic states. Each entity below is a character in this world. Focus entirely on
// the biological entities and their metabolic interactions — do NOT create entity types for
// researchers, software tools, journals, or experimental methods.
//
// Key characters and their roles:
//
// The Viruses (the antagonists):
// - SARS-CoV: The original SARS virus, decreases host biomass, perturbs oxidative
//   phosphorylation and vitamin E metabolism
// - SARS-CoV-2: The COVID-19 virus, increases host biomass production, uniquely affects
//   vitamin D and vitamin C metabolism, generates the most virus-specific rescue targets
//   (4,592 unique KO pairs at 48h)
// - MERS-CoV: Middle East respiratory syndrome virus, minimal biomass change, uniquely
//   perturbs sphingolipid metabolism
//
// The Metabolic Hub Genes (the defenders/targets):
// - CPT2 (carnitine palmitoyltransferase 2): Major hub at 24h, controls fatty acid transport
//   into mitochondria, targeted by metformin
// - SDHA (succinate dehydrogenase): TCA cycle enzyme, hub at 48h, links mitochondrial
//   metabolism to viral defense, targeted by metformin
// - FH (fumarase): TCA cycle enzyme, hub at 24h for SARS-CoV and SARS-CoV-2
// - CAT (catalase): Redox balance guardian, targeted by N-acetylcysteine (NAC)
// - IDH1/IDH2 (isocitrate dehydrogenases): Druggable hubs connecting multiple rescue pathways
// - GLB1 (beta-galactosidase): Emerges as key hub at 48h
// - DTYM (deoxythymidylate kinase): Nucleotide metabolism hub at 48h
// - SLC5A3 (inositol transporter): Druggable hub for SARS-CoV and SARS-CoV-2
//
// The Mitochondrial Transporters (the supply chain):
// - SLC25A13 (aspartate-glutamate carrier): Pan-coronavirus target, upregulated by all three
//   viruses
// - SLC25A15 (ornithine carrier): Upregulated during prolonged infection
// - SLC25A10 (dicarboxylate carrier/DIC): Affected in SARS-CoV and SARS-CoV-2 but not MERS-CoV
// - Carnitine-acylcarnitine carrier (CAC): Shared pan-CoV transport perturbation
//
// The Drugs (the interventions):
// - Metformin: Predicted to rescue CPT2/SDHA perturbations; inhibits SARS-CoV-2 by 99% in
//   vitro; reduced Long-COVID by 41% in phase 3 trial
// - Statins (targeting HMGCR): Disrupt lipid-raft viral entry; 35% lower mortality in
//   hospitalized cohorts
// - Dipyridamole (targeting ADA): Improves platelet counts and lymphocytes; phase III trials
//   underway
// - N-acetylcysteine/NAC (bolstering CAT): Mixed clinical results — reduced respiratory failure
//   progression but failed in larger RCTs
// - Ribavirin (targeting ADK/NT5C2): Refuted clinically — no improvement in viral clearance or
//   mortality
//
// Prediction tasks — simulate how this metabolic community would discuss and debate these
// questions:
// 1. Based on everything in this study, what is the single most important discovery? Let the
//    characters debate and arrive at their own conclusion.
// 2. What is the second major finding? (Hint: consider the dramatic temporal shift — at 24 hours
//    the three viruses share 707 common rescue gene pairs, but by 48 hours this shared signal
//    almost completely collapses to near-zero overlap. What does this reveal about the nature of
//    viral metabolic hijacking over time?)
// 3. What is the third major finding? (Hint: consider the clinical validation — NiTRO's top
//    computational predictions for metabolic drug targets align with independently obtained
//    experimental and clinical trial evidence. What does this say about the power of genome-scale
//    metabolic modeling for drug repurposing?)
//
// Have the characters discuss, debate, and react to these findings from their own perspective —
// how does each finding affect them personally given their role in the metabolic network?
```

---

## 2. MED4 — Prochlorococcus Protein Interaction Network (Detailed Prompt)

**Paper:** First protein-protein interaction (PPI) network for Prochlorococcus marinus MED4

**Prompt:**
```
// Simulate the social dynamics of the Prochlorococcus marinus MED4 protein interaction network.
// Each protein is a character in this world, identified by ORF IDs (e.g., CAE19578, CAE19570,
// CAE18880, CAE18591, CAP16453, CAE19428, CAE19713). Focus entirely on the proteins and their
// molecular interactions as social relationships — do NOT create entity types for researchers,
// software tools, journals, or experimental methods.
//
// Key characters and their roles:
// - CAE19578 (outer membrane porin): The most connected character with 164 interactions, an
//   extreme hub and bottleneck
// - CAP16453 (hypothetical protein): Second most connected with 134 interactions, mysterious
//   and uncharacterized
// - CAE18591 (TPR scaffold protein): Third-ranked hub with 70 interactions, bridges translation,
//   photosynthesis, and protein folding
// - CAE19570 (glutaredoxin): Oxidative stress responder, hub-bottleneck with 21 interactions,
//   connects to photosystem II
// - CAE18880 (BPD-type ABC transporter): Extreme hub with 40 interactions, coordinates transport
//   and metabolite export
// - CAE19713 (glycosyltransferase): Links glycosylation to photosynthetic machinery,
//   hub-bottleneck with 18 interactions
// - CAE19428 (OBG-family GTPase): Regulatory hub with 65 interactions, universally conserved
//
// Prediction tasks — simulate how this protein community would discuss and debate these
// questions:
// 1. What is the single biggest discovery from this interactome? (The network reveals a dual hub
//    architecture: broadly connected "core hubs" vs. tightly clustered "adaptive hubs" that wire
//    high-light survival functions directly into the network core — suggesting evolution integrated
//    environmental adaptation through strategic placement of a few key proteins, not wholesale
//    network rewiring)
// 2. What is the second major finding? (The "N-terminal paradox": an AI model trained to predict
//    protein interactions relies most heavily on N-terminal sequence features, yet those exact
//    residues are depleted at predicted structural contact interfaces — implying the model captures
//    allosteric or specificity-determining signals beyond direct binding contacts)
// 3. What is the third major finding? (A tri-model AI consensus framework combining three
//    independent sequence-based predictors with AlphaFold3 structural features and quantum
//    tunneling descriptors rescued 657 additional interactions from single-detected experimental
//    data, expanding the network to 1,741 interactions while preserving its scale-free
//    architecture)
//
// Have the proteins discuss, debate, and react to these findings from their own perspective —
// how does each finding affect them personally given their role in the network?
```

---

## 3. MED4 — Concise Review Panel Prompt

**Paper:** Same MED4 protein interaction network paper (shorter, review-style prompt)

**Prompt:**
```
// Analyze this scientific manuscript about the first protein-protein interaction (PPI) network
// for the marine cyanobacterium Prochlorococcus marinus MED4. The study mapped 1,084
// experimentally validated interactions among 428 proteins using CrY2H-seq screening, then
// expanded the network to 1,741 interactions using AI models (ppiGPLM, ppiDCE, ppiBTEP)
// combined with AlphaFold3 structural predictions and quantum tunneling features. Simulate a
// scientific review panel discussing:
// (1) What are the most impactful findings and their implications for marine microbiology?
// (2) How might the "N-terminal paradox" — where sequence features driving AI predictions are
//     concentrated at protein N-termini but depleted at structural interfaces — reshape how we
//     interpret deep learning models of protein interactions?
// (3) What experiments or follow-up studies should be prioritized?
// (4) What is the "big picture" and overarching finding of the study?
// (5) How could this interactome framework be applied to other ecologically important but
//     understudied microorganisms?
// Generate predictions about the future impact of this work on systems biology, AI-driven
// proteomics, and ocean ecology.
```

---

## Tips for Writing Effective Prompts

1. **Start with `//`** — the prompt field accepts comment-style syntax for readability
2. **Name your key entities explicitly** — the ontology generator and entity reader will map these to simulation agents
3. **Add "do NOT create entity types for researchers, software tools, journals"** — this keeps the simulation focused on biological entities, not meta-entities
4. **Include prediction tasks with hints** — guiding the agents toward specific findings produces much richer debate
5. **Use the phrase "have the characters discuss, debate, and react"** — this activates the multi-agent discussion dynamics
6. **For biological mode**, describe entities in terms of roles, relationships, and functional context rather than just listing names
