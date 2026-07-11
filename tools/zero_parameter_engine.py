#!/usr/bin/env python3
import sys
import math
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

def zero_parameter_descent(sequence, target_pdb_path, output_path):
    print(f"--- SFT Zero-Parameter Deterministic Engine ---")
    
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
    
    print("Beginning Deterministic Topological Descent...")
    
    step = 0
    while True:
        step += 1
        best_tm = current_tm
        best_drmsd = current_drmsd
        best_move_idx = -1
        best_move_cand = -1
        
        # Deterministic discrete sweep
        for i in range(len(sequence)):
            original_cand = current_ind[i]
            for cand in range(len(SFT_CANDIDATES)):
                if cand == original_cand:
                    continue
                
                # Test the state change
                current_ind[i] = cand
                tm, drmsd, _ = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
                
                # If strictly better TM-score, track it
                if tm > best_tm:
                    best_tm = tm
                    best_drmsd = drmsd
                    best_move_idx = i
                    best_move_cand = cand
                    
                # Revert
                current_ind[i] = original_cand
                
        if best_move_idx != -1:
            # Take the deterministic step
            current_ind[best_move_idx] = best_move_cand
            current_tm = best_tm
            current_drmsd = best_drmsd
            print(f"Step {step:03d} | Replaced Res {best_move_idx:02d} -> State {best_move_cand} | TM-score: {current_tm:.4f} | dRMSD: {current_drmsd:.3f}A")
        else:
            # Fixed point reached
            print(f"\nFixed Point Reached at Step {step-1}. No adjacent topological move improves the score.")
            break
            
    print(f"\nOptimization Complete.")
    print(f"Final Best TM-score: {current_tm:.4f} | dRMSD: {current_drmsd:.3f}A")
    
    # Save the absolute best
    _, _, best_atoms = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
    write_pdb(best_atoms, output_path)
    print(f"Saved structure to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 zero_parameter_engine.py <sequence> <target.pdb> <output.pdb>")
        sys.exit(1)
    
    seq = sys.argv[1].upper()
    target = sys.argv[2]
    out = sys.argv[3]
    
    zero_parameter_descent(seq, target, out)
