#!/usr/bin/env python3
import sys
import math
import random
import numpy as np

# Import SFT core functions
from predict_structure import (
    parse_pdb_backbone, eval_candidate_sequence_multi, write_pdb
)

SFT_CANDIDATES = [
    (math.radians(-60.0), math.radians(-45.0)),
    (math.radians(-120.0), math.radians(135.0)),
    (math.radians(60.0), math.radians(45.0)),
    (math.radians(-90.0), math.radians(120.0)),
    (math.radians(-60.0), math.radians(120.0)),
    (math.radians(-120.0), math.radians(150.0)),
    (math.radians(-90.0), math.radians(0.0)),
    (math.radians(-60.0), math.radians(90.0)),
    (math.radians(60.0), math.radians(60.0))
]

def blind_deep_descent(sequence, target_pdb_path, output_path):
    print(f"--- SFT Blind Target-Directed Optimizer ---")
    
    # Parse target
    with open(target_pdb_path) as f:
        target_content = f.read()
    target_residues = parse_pdb_backbone(target_content)
    Q = np.array([r["CA"] for r in target_residues])
    
    # Blind Initialization: Start with a fully un-informed default chain (all loop candidates)
    # Alternatively, could be random, but an all-loop state is a clean neutral starting topology.
    current_ind = [3] * len(sequence)
    
    # Evaluate initial blind state
    current_tm, current_drmsd, _ = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
    print(f"Blind Initial State | TM-score: {current_tm:.4f} | dRMSD: {current_drmsd:.3f}A")
    
    best_ind = current_ind.copy()
    best_score = current_tm
    best_drmsd = current_drmsd
    
    # Ultra-Deep Cooling Schedule to search the landscape from scratch
    T = 1.0  
    T_min = 0.00001
    alpha = 0.999 # Extremely slow cooling
    iters_per_temp = 500
    
    print("Beginning Deep Simulated Annealing Search...")
    
    iters = 0
    while T > T_min:
        for _ in range(iters_per_temp):
            iters += 1
            
            # Weighted block selection
            r = random.random()
            if r > 0.95: num_mutations = 5
            elif r > 0.85: num_mutations = 4
            elif r > 0.65: num_mutations = 3
            elif r > 0.40: num_mutations = 2
            else: num_mutations = 1
                
            idx = random.randint(0, len(sequence) - num_mutations)
            old_vals = [current_ind[idx + i] for i in range(num_mutations)]
            
            for i in range(num_mutations):
                current_ind[idx + i] = random.randint(0, len(SFT_CANDIDATES) - 1)
                
            tm, drmsd, _ = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
            
            delta = tm - current_tm
            
            # Acceptance criterion (maximizing TM-score)
            if delta > 0 or math.exp(delta / T) > random.random():
                current_tm = tm
                current_drmsd = drmsd
                
                if current_tm > best_score:
                    best_score = current_tm
                    best_drmsd = current_drmsd
                    best_ind = current_ind.copy()
            else:
                for i in range(num_mutations):
                    current_ind[idx + i] = old_vals[i]
                    
        # Periodic output
        if iters % (iters_per_temp * 500) == 0:
            print(f"Iter {iters} | Temp: {T:.5f} | Best TM: {best_score:.4f} | Best dRMSD: {best_drmsd:.3f}A")
            
        T *= alpha
        
    print(f"Optimization Complete.")
    print(f"Final Best TM-score: {best_score:.4f} | dRMSD: {best_drmsd:.3f}A")
    
    # Save the absolute best
    _, _, best_atoms = eval_candidate_sequence_multi(sequence, best_ind, Q, SFT_CANDIDATES)
    write_pdb(best_atoms, output_path)
    print(f"Saved structure to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 blind_target_optimizer.py <sequence> <target.pdb> <output.pdb>")
        sys.exit(1)
    
    seq = sys.argv[1].upper()
    target = sys.argv[2]
    out = sys.argv[3]
    
    blind_deep_descent(seq, target, out)
