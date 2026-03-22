# How to Run MiroFish

# If everything is set

npm run dev


● Background command "Pull qwen2.5:7b model via Ollama" completed (exit code 0)
                                                                                                                                                                            
● The qwen2.5:7b model pull completed successfully — everything is set up and ready to use.
                                                                                                                                                                            
❯ How can I run the tool?                                                                                                                                                   
                                                                                                                                                                            
● # 1. Activate the conda environment                                                                                                                                       
  conda activate mirofish                                         
                                                                                                                                                                            
  # 2. Go to the project directory                                                                                                                                          
  cd /home/ksa/Models/MiroFish                                                                                                                                              
                                                                                                                                                                            
  # 3. Start both frontend and backend                                                                                                                                      
  npm run dev                                                                                                                                                               
                                                                                                                                                                            
  This will launch:                                               
  - Frontend: http://localhost:3000
  - Backend API: http://localhost:5001                                                                                                                                      
                                      
  Before running, you need a ZEP API key — sign up for free at https://app.getzep.com/, then update your .env:                                                              
                                                                                                                                                                            
  nano /home/ksa/Models/MiroFish/.env
  # Replace your_zep_api_key_here with your actual key                                                                                                                      
                                                                                                                                                                            
  If you want to start only one service:                                                                                                                                    
  - npm run backend — backend only                                                                                                                                          
  - npm run frontend — frontend only                                                                                                                                        
                                
                                
API key (both free)

z_1dWlkIjoiZjk4ZjkwNzAtZGMxNi00NjQ1LTk4MmUtMjQ0YTRkNTc4ZDk4In0.FxGyQJJ2zAaiXFtdqo3x0_EtQBVBpWItY0Uv7O2Wq8xoCl0e_ceu55NOqr1QdHqn8mV4vg7ZAbSOCgzih_cZCQ
z_1dWlkIjoiZjk4ZjkwNzAtZGMxNi00NjQ1LTk4MmUtMjQ0YTRkNTc4ZDk4In0.FxGyQJJ2zAaiXFtdqo3x0_EtQBVBpWItY0Uv7O2Wq8xoCl0e_ceu55NOqr1QdHqn8mV4vg7ZAbSOCgzih_cZCQ

z_1dWlkIjoiYzg2NTE2YjUtNDJmZS00NTg3LThjMmMtY2UwNDZkMDllMDFlIn0.pA5h1OuWr5VRFQ8cARO_6K-hF1GnQ1Wy8wsLbY-AOiTzuWTarpe7eN4u2JmAznJphDHko5B110SQFfsHDPmoSg
z_1dWlkIjoiYzg2NTE2YjUtNDJmZS00NTg3LThjMmMtY2UwNDZkMDllMDFlIn0.pA5h1OuWr5VRFQ8cARO_6K-hF1GnQ1Wy8wsLbY-AOiTzuWTarpe7eN4u2JmAznJphDHko5B110SQFfsHDPmoSg

Prompt: // use natural language to predict if the price of XRP will increase or decrease from its current price of $1.49


Prompt used for MED4 (based on Claude's suggestion)
Analyze this scientific manuscript about the first protein-protein interaction (PPI) network for the marine cyanobacterium Prochlorococcus marinus MED4. The study 
mapped 1,084 experimentally validated interactions among 428 proteins using CrY2H-seq screening, then expanded the network to 1,741 interactions using AI models (ppiGPLM,ppiDCE, ppiBTEP) combined with AlphaFold3 structural predictions and quantum tunneling features. Simulate a scientific review panel discussing: (1) What are the most impactful findings and their implications for marine microbiology? (2) How might the "N-terminal paradox" — where sequence features driving AI predictions are
concentrated at protein N-termini but depleted at structural interfaces — reshape how we interpret deep learning models of protein interactions? (3) What experiments or follow-up studies should be prioritized? (4) What is the "big picture" and overarching finding of the study, (5) How could this interactome framework be applied to other ecologically important but understudied microorganisms? Generate predictions about the future impact of this work on systems biology, AI-driven proteomics, and ocean ecology.

  ---
  Big Picture Finding
                     
  The central discovery is a dual architecture in the MED4 interactome:
                                                                                                                                                                            
  - Core hubs (e.g., a porin, a TPR-repeat scaffold) are broadly connected with high betweenness centrality — they're the network's highways for information flow           
  - Adaptive hubs (an ABC transporter, a glutaredoxin, a glycosyltransferase) carry high-light-adaptation domains and are embedded in dense hub-hub subnetworks — they wire 
  MED4's survival machinery (transport, stress defense, glycosylation) directly into the core network rather than isolating it in peripheral modules                        
                                                                  
  The surprise is that high-light adaptive functions aren't statistically enriched as a class among hubs — instead, a few individually critical adaptive proteins occupy    
  bottleneck positions linking photosynthesis, stress response, and glycosylation. This suggests evolution integrated adaptation through strategic placement of a few key
  proteins, not wholesale rewiring.                                                                                                                                         
                                                                  
  The second major finding is the "N-terminal paradox": the AI model (ppiGPLM) relies heavily on N-terminal sequence features to predict interactions, yet those same       
  residues are depleted at predicted structural contact interfaces. This implies the model is learning allosteric or specificity-determining signals rather than direct
  binding contacts — a fundamental insight into what deep learning models actually capture about protein interactions.           
  
  
  
  
# New, BIOLOGICAL prompt
▎ Simulate the social dynamics of the Prochlorococcus marinus MED4 protein interaction network. Each protein is a character in this world, identified by ORF IDs (e.g.,
  CAE19578, CAE19570, CAE18880, CAE18591, CAP16453, CAE19428, CAE19713). Focus entirely on the proteins and their molecular interactions as social relationships — do NOT
  create entity types for researchers, software tools, journals, or experimental methods.

  ▎ Key characters and their roles:
  ▎ - CAE19578 (outer membrane porin): The most connected character with 164 interactions, an extreme hub and bottleneck
  ▎ - CAP16453 (hypothetical protein): Second most connected with 134 interactions, mysterious and uncharacterized
  ▎ - CAE18591 (TPR scaffold protein): Third-ranked hub with 70 interactions, bridges translation, photosynthesis, and protein folding
  ▎ - CAE19570 (glutaredoxin): Oxidative stress responder, hub-bottleneck with 21 interactions, connects to photosystem II
  ▎ - CAE18880 (BPD-type ABC transporter): Extreme hub with 40 interactions, coordinates transport and metabolite export
  ▎ - CAE19713 (glycosyltransferase): Links glycosylation to photosynthetic machinery, hub-bottleneck with 18 interactions
  ▎ - CAE19428 (OBG-family GTPase): Regulatory hub with 65 interactions, universally conserved

  ▎ Prediction tasks — simulate how this protein community would discuss and debate these questions:
  ▎ 1. What is the single biggest discovery from this interactome? (The network reveals a dual hub architecture: broadly connected "core hubs" vs. tightly clustered
  "adaptive hubs" that wire high-light survival functions directly into the network core — suggesting evolution integrated environmental adaptation through strategic
  placement of a few key proteins, not wholesale network rewiring)
  ▎ 2. What is the second major finding? (The "N-terminal paradox": an AI model trained to predict protein interactions relies most heavily on N-terminal sequence features,
   yet those exact residues are depleted at predicted structural contact interfaces — implying the model captures allosteric or specificity-determining signals beyond
  direct binding contacts)
  ▎ 3. What is the third major finding? (A tri-model AI consensus framework combining three independent sequence-based predictors with AlphaFold3 structural features and
  quantum tunneling descriptors rescued 657 additional interactions from single-detected experimental data, expanding the network to 1,741 interactions while preserving its
   scale-free architecture)

  ▎ Have the proteins discuss, debate, and react to these findings from their own perspective — how does each finding affect them personally given their role in the
  network?

  
# Bug fixes made

  Changes made                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                      
  1. Queue gate (concurrency limiter) — llm_client.py, simulation_config_generator.py, oasis_profile_generator.py                                                                                                                                     
  - Added a process-wide threading.Semaphore(2) that limits concurrent LLM requests to 2 at a time                                                                                                                                                    
  - All three files that call chat.completions.create() now go through this gate                                                                                                                                                                      
  - Configurable via MAX_CONCURRENT_LLM_REQUESTS=2 in .env                                                                                                                                                                                            
                                                                                                                                                                                                                                                      
  2. Concise response instructions — agent_soul.py                                                                                                                                                                                                    
  - Added "Keep all responses short and concise" to BIOLOGICAL_PERSONA_SYSTEM_PROMPT                                                                                                                                                                  
  - Added "Keep your output concise" to BIOLOGICAL_ONTOLOGY_SYSTEM_PROMPT                                                                                                                                                                             
  - Reduced persona field limit from 2000 chars to 500 chars (both individual and group)                                                                                                                                                              
  - Reduced bio limit from 200 to 150 chars                                                                                                                                                                                                           
  - Simplified the bullet-point instructions to be less verbose themselves                                                                                                                                                                            
                                                                                                                                                                                                                                                      
  3. Max rounds default wired up — config.py, simulation.py, .env                                                                                                                                                                                     
  - Changed default from 10 to 90 in config.py                                                                                                                                                                                                        
  - Set OASIS_DEFAULT_MAX_ROUNDS=90 in .env                                                                                                                                                                                                           
  - The API endpoint now actually uses this value as the default instead of None, so every simulation run is capped at 90 rounds unless overridden       

  
