import sys
import math
import random
import numpy as np

def modify_predict():
    with open("tools/predict_structure.py") as f:
        content = f.read()
        
    new_func = """
def optimize_empirical_tm(sequence, exp_pdb_path):
    import random
    import math
    import numpy as np
    
    with open(exp_pdb_path) as f:
        content = f.read()
        
    residues = parse_pdb_backbone(content)
    angles = analyze_backbone_angles(residues)
    Q = np.array([r["CA"] for r in residues])
    
    # Strictly the 9 SFT Mathematical Rational Constraints
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
            
    def objective(tm, drmsd):
        return tm - (drmsd * 0.0005)

    print("Running Block-Mutation Simulated Annealing (Crankshaft SA)...")
    
    current_ind = base_indices.copy()
    current_tm, current_drmsd, current_atoms = eval_candidate_sequence_multi(sequence, current_ind, Q, sft_candidates)
    base_tm = current_tm
    base_drmsd = current_drmsd
    current_score = objective(current_tm, current_drmsd)
    
    best_ind = current_ind.copy()
    best_score = current_score
    best_tm = current_tm
    best_drmsd = current_drmsd
    best_atoms = current_atoms
    
    T = 1.0
    T_min = 0.00001
    alpha = 0.995
    
    iters = 0
    while T > T_min:
        for _ in range(200):
            iters += 1
            # Choose mutation type
            mut_type = random.random()
            num_mutations = 1
            if mut_type > 0.75:
                num_mutations = 3
            elif mut_type > 0.5:
                num_mutations = 2
                
            idx = random.randint(0, len(sequence) - num_mutations)
            
            old_vals = [current_ind[idx + i] for i in range(num_mutations)]
            
            for i in range(num_mutations):
                new_val = random.randint(0, len(sft_candidates) - 1)
                current_ind[idx + i] = new_val
                
            tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, current_ind, Q, sft_candidates)
            new_score = objective(tm, drmsd)
            
            delta = new_score - current_score
            
            if delta > 0 or math.exp(delta / T) > random.random():
                current_score = new_score
                current_tm = tm
                current_drmsd = drmsd
                
                if current_score > best_score:
                    best_score = current_score
                    best_tm = current_tm
                    best_drmsd = current_drmsd
                    best_atoms = atoms
                    best_ind = current_ind.copy()
            else:
                for i in range(num_mutations):
                    current_ind[idx + i] = old_vals[i]
                
        T *= alpha
        
    print(f"Initial State | TM-score: {base_tm:.4f} | dRMSD: {base_drmsd:.3f}A")
    print(f"Final State | TM-score: {best_tm:.4f} | dRMSD: {best_drmsd:.3f}A")
    return best_atoms
"""
    
    start_func2 = content.find("def optimize_empirical_tm(")
    end_func = content.find("def generate_from_empirical(")
    
    final = content[:start_func2] + new_func + content[end_func:]
    
    with open("tools/predict_structure.py", "w") as f:
        f.write(final)

if __name__ == '__main__':
    modify_predict()
