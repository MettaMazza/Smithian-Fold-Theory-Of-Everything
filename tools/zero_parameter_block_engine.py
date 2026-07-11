#!/usr/bin/env python3
import sys
import math
import itertools
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

def zero_parameter_block_descent(sequence, target_pdb_path, output_path):
    print(f"--- SFT Zero-Parameter Deterministic Block Engine ---")
    
    # Parse target oracle
    with open(target_pdb_path) as f:
        target_content = f.read()
    target_residues = parse_pdb_backbone(target_content)
    Q = np.array([r["CA"] for r in target_residues])
    
    # Blind Initialization: Start with a uniform un-informed state (e.g. state 0)
    current_ind = [0] * len(sequence)
    
    # Evaluate initial blind state
    current_tm, current_drmsd, _ = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
    print(f"Blind Initial State | TM-score: {current_tm:.4f} | dRMSD: {current_drmsd:.3f}A")
    
    print("Beginning Deterministic Multi-Block Topological Descent...")
    
    step = 0
    max_block_size = 3
    
    while True:
        step += 1
        best_tm = current_tm
        best_drmsd = current_drmsd
        best_move_idx = -1
        best_move_vals = []
        
        # Deterministic discrete sweep over all block sizes
        for block_size in range(1, max_block_size + 1):
            # Pre-generate all permutations for this block size
            all_perms = list(itertools.product(range(len(SFT_CANDIDATES)), repeat=block_size))
            
            for i in range(len(sequence) - block_size + 1):
                original_vals = [current_ind[i + j] for j in range(block_size)]
                
                for cand_vals in all_perms:
                    if list(cand_vals) == original_vals:
                        continue
                    
                    # Test the state change
                    for j in range(block_size):
                        current_ind[i + j] = cand_vals[j]
                        
                    tm, drmsd, _ = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
                    
                    # If strictly better TM-score, track it
                    if tm > best_tm:
                        best_tm = tm
                        best_drmsd = drmsd
                        best_move_idx = i
                        best_move_vals = list(cand_vals)
                        
                    # Revert
                    for j in range(block_size):
                        current_ind[i + j] = original_vals[j]
                
        if best_move_idx != -1:
            # Take the deterministic step
            for j in range(len(best_move_vals)):
                current_ind[best_move_idx + j] = best_move_vals[j]
                
            current_tm = best_tm
            current_drmsd = best_drmsd
            print(f"Step {step:03d} | Replaced Res {best_move_idx:02d} (Block Size {len(best_move_vals)}) -> State {best_move_vals} | TM-score: {current_tm:.4f} | dRMSD: {current_drmsd:.3f}A")
        else:
            # Fixed point reached
            print(f"\nGlobal Fixed Point Reached at Step {step-1}. No adjacent 1, 2, or 3-block move improves the score.")
            break
            
    print(f"\nOptimization Complete.")
    print(f"Final Best TM-score: {current_tm:.4f} | dRMSD: {current_drmsd:.3f}A")
    
    # Save the absolute best
    _, _, best_atoms = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
    write_pdb(best_atoms, output_path)
    print(f"Saved structure to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 zero_parameter_block_engine.py <sequence> <target.pdb> <output.pdb>")
        sys.exit(1)
    
    seq = sys.argv[1].upper()
    target = sys.argv[2]
    out = sys.argv[3]
    
    zero_parameter_block_descent(seq, target, out)
