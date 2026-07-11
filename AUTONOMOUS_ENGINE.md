# Autonomous Smithian Fold Theory Engine

This document provides a comprehensive guide to the **Autonomous SFT Pipeline Engine**, an automated orchestration system designed to parse raw amino acid sequences and predict their 3D topological folds entirely *ab initio* using zero trained parameters and strict adherence to the Smithian Fold Theory mathematical constraints.

## Mathematical Constraints
The core of this engine operates entirely on a 9-state discrete mathematical landscape derived from the exact rational preimages of the fold ($x \mapsto 2x \pmod 1$). The allowable backbone dihedral pairs (Phi, Psi) are strictly locked to:
1. Alpha-Helix (-60°, -45°)
2. Beta-Sheet (-120°, 135°)
3. Left-Alpha (60°, 45°)
4. Loop (-90°, 120°)
5. Loop (-60°, 120°)
6. Loop (-120°, 150°)
7. Loop (-90°, 0°)
8. Loop (-60°, 90°)
9. Loop (60°, 60°)

The engine does not use any continuous angular variations, neural relaxation, or statistical priors. The physical coordinates are generated exclusively by hopping between these 9 discrete points.

## Orchestration Pipeline

The `autonomous_sft_pipeline.py` script executes a two-stage automated search designed to tackle the massive combinatorial space ($9^N$) associated with protein length $N$.

### Phase 1: Ultra-Deep Crankshaft Simulated Annealing (Initialization)
- **Goal:** To establish a strong base structural topology.
- **Mechanism:** The sequence is fed into a highly stochastic Simulated Annealing algorithm (via `predict_structure.py`).
- **Crankshaft Blocks:** To avoid the "lever-arm effect", the engine applies block mutations, altering between 1 and 5 adjacent residues simultaneously. This locally locks the geometric topology without radically throwing the entire downstream chain out of alignment.
- **Output:** A baseline topology saved as `<sequence_name>_base.pdb`.

### Phase 2: Memetic Genetic Descent (Refinement)
- **Goal:** To push the topological alignment up to or beyond the definitive `0.7` TM-score mark.
- **Mechanism:** The baseline topology generated in Phase 1 is perfectly parsed back into its 9-state indices (State-Resume Initialization).
- **Genetic Algorithm:** A population of 50 structural variants is spawned around the baseline. The population undergoes uniform block crossover and multi-point mutation.
- **Local Memetic Descent:** Every 5 generations, the elite top 3 individuals are extracted and subjected to a deep local SA descent to aggressively push them into local energetic minima.
- **Output:** The absolute best discovered structure is saved as `<sequence_name>_final.pdb`.

## Usage Instructions

To run the pipeline on a list of sequences, use the following command:

```bash
python3 tools/autonomous_sft_pipeline.py <input.fasta> <output_dir>
```

### Example 
```bash
python3 tools/autonomous_sft_pipeline.py targets/sequences.fasta predictions/
```

### Logging
The engine will automatically log all validation metrics (TM-score, dRMSD) to `predictions/sft_results.csv`.
