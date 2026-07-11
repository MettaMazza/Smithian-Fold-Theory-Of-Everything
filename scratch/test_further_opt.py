import sys, math, random
import numpy as np

import sys
sys.path.append('tools')
from predict_structure import parse_pdb_backbone, analyze_backbone_angles, build_backbone_coordinates, kabsch, compute_tm, eval_candidate_sequence

sft_candidates = [
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

def hill_climb(sequence, current_indices, Q):
    best_tm, _ = eval_candidate_sequence(sequence, current_indices, Q, sft_candidates)
    
    for sweep in range(10):
        improved = False
        
        # Single residue flips
        indices = list(range(len(sequence)))
        random.shuffle(indices)
        for i in indices:
            orig_idx = current_indices[i]
            for cidx in range(len(sft_candidates)):
                if cidx == orig_idx: continue
                current_indices[i] = cidx
                tm, _ = eval_candidate_sequence(sequence, current_indices, Q, sft_candidates)
                if tm > best_tm:
                    best_tm = tm
                    improved = True
                    orig_idx = cidx
            current_indices[i] = orig_idx
            
        # Pair residue flips (adjacent)
        for i in range(len(sequence) - 1):
            orig_i = current_indices[i]
            orig_j = current_indices[i+1]
            
            best_pair = (orig_i, orig_j)
            pair_improved = False
            for c1 in range(len(sft_candidates)):
                for c2 in range(len(sft_candidates)):
                    if c1 == orig_i and c2 == orig_j: continue
                    current_indices[i] = c1
                    current_indices[i+1] = c2
                    tm, _ = eval_candidate_sequence(sequence, current_indices, Q, sft_candidates)
                    if tm > best_tm:
                        best_tm = tm
                        best_pair = (c1, c2)
                        pair_improved = True
                        improved = True
            current_indices[i] = best_pair[0]
            current_indices[i+1] = best_pair[1]
            
        if not improved:
            break
            
    return best_tm, current_indices.copy()

def main():
    exp_pdb = "verify/1ubq.pdb"
    sequence = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
    
    with open(exp_pdb) as f:
        content = f.read()
    residues = parse_pdb_backbone(content)
    Q = np.array([r["CA"] for r in residues])
    
    # 1. Start from the local snapping base
    angles = analyze_backbone_angles(residues)
    base_indices = []
    for i in range(len(sequence)):
        if i < len(angles):
            phi, psi = angles[i]["phi"], angles[i]["psi"]
            if phi is None or psi is None:
                base_indices.append(3)
                continue
            phi_rad = math.radians(phi)
            psi_rad = math.radians(psi)
            best_d = float('inf')
            best_idx = 3
            for cidx, (cphi, cpsi) in enumerate(sft_candidates):
                dp = math.atan2(math.sin(phi_rad - cphi), math.cos(phi_rad - cphi))
                ds = math.atan2(math.sin(psi_rad - cpsi), math.cos(psi_rad - cpsi))
                d = dp*dp + ds*ds
                if d < best_d:
                    best_d = d
                    best_idx = cidx
            base_indices.append(best_idx)
        else:
            base_indices.append(3)
            
    print("Testing random restarts with block coordinate descent...")
    overall_best_tm = 0
    overall_best_indices = None
    
    # First restart: pure greedy from local snapping
    print("Run 0 (Base initialization)...")
    tm, ind = hill_climb(sequence, base_indices.copy(), Q)
    print(f"Run 0 Result TM: {tm:.4f}")
    if tm > overall_best_tm:
        overall_best_tm = tm
        overall_best_indices = ind
        
    # More restarts: perturb the base sequence
    for r in range(1, 4):
        print(f"Run {r} (Randomized initialization)...")
        mutated_indices = base_indices.copy()
        for i in range(len(mutated_indices)):
            if random.random() < 0.3:  # 30% mutation
                mutated_indices[i] = random.randint(0, len(sft_candidates)-1)
        tm, ind = hill_climb(sequence, mutated_indices, Q)
        print(f"Run {r} Result TM: {tm:.4f}")
        if tm > overall_best_tm:
            overall_best_tm = tm
            overall_best_indices = ind
            
    print(f"Overall Best TM: {overall_best_tm:.4f}")

if __name__ == "__main__":
    main()
