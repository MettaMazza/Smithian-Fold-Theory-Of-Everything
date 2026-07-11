#!/usr/bin/env python3
import sys
import math
import numpy as np
from scipy.optimize import minimize
from predict_structure import evaluate_conformation, write_pdb, predict_secondary_structure

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

def autonomous_beam_search(sequence, output_path, beam_width=500):
    # Beam contains tuples of (score, state_sequence)
    beam = [(0.0, [])]
    
    # Calculate deterministic secondary structure propensities
    full_secondary_structures = predict_secondary_structure(sequence)
    
    for i in range(len(sequence)):
        next_beam = []
        partial_seq = sequence[:i+1]
        partial_ss = full_secondary_structures[:i+1]
        
        for current_score, state_seq in beam:
            for cand_idx in range(len(SFT_CANDIDATES)):
                new_seq = state_seq + [cand_idx]
                
                phi_angles = [SFT_CANDIDATES[idx][0] for idx in new_seq]
                psi_angles = [SFT_CANDIDATES[idx][1] for idx in new_seq]
                
                score, has_clash, _ = evaluate_conformation(partial_seq, partial_ss, phi_angles, psi_angles)
                
                if has_clash:
                    score += 999999.0  # Massive penalty for steric clash
                
                # Secondary structure mathematical penalty
                ss_target = full_secondary_structures[i]
                if ss_target == 'H' and cand_idx not in (0, 2):
                    score += 500.0
                elif ss_target == 'E' and cand_idx != 1:
                    score += 500.0
                
                next_beam.append((score, new_seq))
                
        # Sort by score ascending (we want to minimize hydrophobic distance and avoid clashes)
        # We also want to prioritize compactness.
        next_beam.sort(key=lambda x: x[0])
        beam = next_beam[:beam_width]
        
        clash_free_count = sum(1 for s, seq in beam if s < 999000.0)
        print(f"Step {i+1:02d}/{len(sequence)} | Beam Best Score: {beam[0][0]:.3f} | Viable Paths: {clash_free_count}/{len(beam)}")
        
    best_seq = beam[0][1]
    best_score = beam[0][0]
    print(f"\nAutonomous Search Complete. Best sequence: {best_seq}")
    print(f"Discrete Biophysical Score: {best_score:.3f}")
    
    print("\nInitiating V6 Continuous Microscopic Relaxation (Scipy Powell)...")
    phi_angles_init = [SFT_CANDIDATES[idx][0] for idx in best_seq]
    psi_angles_init = [SFT_CANDIDATES[idx][1] for idx in best_seq]
    
    # Flatten angles: all phis, then all psis
    initial_angles = phi_angles_init + psi_angles_init
    
    def objective(flat_angles):
        n = len(sequence)
        phis = flat_angles[:n]
        psis = flat_angles[n:]
        score, has_clash, _ = evaluate_conformation(sequence, full_secondary_structures, phis, psis)
        if has_clash:
            return score + 999999.0
        return score
        
    res = minimize(objective, initial_angles, method='Powell', options={'maxiter': 5, 'disp': True})
    
    final_phis = res.x[:len(sequence)]
    final_psis = res.x[len(sequence):]
    
    final_score, _, final_atoms = evaluate_conformation(sequence, full_secondary_structures, final_phis, final_psis)
    print(f"Final Relaxed Biophysical Score: {final_score:.3f}")
    
    write_pdb(final_atoms, output_path)
    print(f"Saved relaxed autonomous prediction to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 tools/autonomous_engine.py <sequence> <output_pdb>")
        sys.exit(1)
    seq = sys.argv[1].upper()
    out = sys.argv[2]
    autonomous_beam_search(seq, out, beam_width=500)
