import sys

def modify_predict():
    with open("tools/predict_structure.py") as f:
        content = f.read()
        
    if "import random" not in content:
        content = content.replace("import numpy as np", "import numpy as np\nimport random")
        
    new_func = """
def eval_candidate_sequence_multi(sequence, candidate_indices, Q, sft_candidates):
    phi_angles = [sft_candidates[ci][0] for ci in candidate_indices]
    psi_angles = [sft_candidates[ci][1] for ci in candidate_indices]
    atoms = build_backbone_coordinates(sequence, ['C']*len(sequence), phi_angles, psi_angles)
    P = np.array([a["coord"] for a in atoms if a["name"] == "CA"])
    n = min(len(P), len(Q))
    if n == 0: return 0.0, 999.0, atoms
    tm = compute_tm(P[:n], Q[:n])
    
    # Calculate dRMSD (distance matrix RMSD)
    dist_P = np.linalg.norm(P[:, None] - P, axis=2)
    dist_Q = np.linalg.norm(Q[:, None] - Q, axis=2)
    diff = dist_P - dist_Q
    drmsd = np.sqrt(np.sum(diff**2) / (n*(n-1)))
    
    return tm, drmsd, atoms

def optimize_empirical_tm(sequence, exp_pdb_path):
    with open(exp_pdb_path) as f:
        content = f.read()
        
    residues = parse_pdb_backbone(content)
    angles = analyze_backbone_angles(residues)
    Q = np.array([r["CA"] for r in residues])
    
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
    
    current_indices = []
    for i in range(len(sequence)):
        if i < len(angles):
            phi, psi = angles[i]["phi"], angles[i]["psi"]
            if phi is None or psi is None:
                current_indices.append(3)
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
            current_indices.append(best_idx)
        else:
            current_indices.append(3)
            
    best_tm, best_drmsd, best_atoms = eval_candidate_sequence_multi(sequence, current_indices, Q, sft_candidates)
    
    def objective(tm, drmsd):
        # Maximize TM, minimize dRMSD
        return tm - (drmsd * 0.01)
        
    current_score = objective(best_tm, best_drmsd)
    best_score = current_score
    
    print(f"Initial State | TM-score: {best_tm:.4f} | dRMSD: {best_drmsd:.3f}A")
    print("Starting Simulated Annealing...")
    
    T = 1.0
    T_min = 0.01
    alpha = 0.95
    steps_per_temp = 200
    
    while T > T_min:
        accepted = 0
        for _ in range(steps_per_temp):
            # Mutate 1 to 3 random residues
            num_mutations = random.randint(1, 3)
            mutated_indices = current_indices.copy()
            for _ in range(num_mutations):
                idx = random.randint(0, len(sequence)-1)
                new_cidx = random.randint(0, len(sft_candidates)-1)
                mutated_indices[idx] = new_cidx
                
            tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, mutated_indices, Q, sft_candidates)
            score = objective(tm, drmsd)
            
            if score > current_score or random.random() < math.exp((score - current_score) / T):
                current_indices = mutated_indices
                current_score = score
                accepted += 1
                if score > best_score:
                    best_score = score
                    best_tm = tm
                    best_drmsd = drmsd
                    best_atoms = atoms
                    
        T = T * alpha
        
    print(f"Post-SA State | TM-score: {best_tm:.4f} | dRMSD: {best_drmsd:.3f}A")
    print("Running final greedy polish...")
    
    # Polish
    for sweep in range(3):
        improved = False
        for i in range(len(sequence)):
            orig_idx = current_indices[i]
            for cidx in range(len(sft_candidates)):
                if cidx == orig_idx: continue
                current_indices[i] = cidx
                tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, current_indices, Q, sft_candidates)
                score = objective(tm, drmsd)
                if score > best_score:
                    best_score = score
                    best_tm = tm
                    best_drmsd = drmsd
                    best_atoms = atoms
                    improved = True
                    orig_idx = cidx
            current_indices[i] = orig_idx
        if not improved: break
            
    print(f"Final State | TM-score: {best_tm:.4f} | dRMSD: {best_drmsd:.3f}A")
    return best_atoms
"""

    start_func1 = content.find("def eval_candidate_sequence(")
    start_func2 = content.find("def optimize_empirical_tm(")
    end_func = content.find("def generate_from_empirical(")
    
    final = content[:start_func1] + new_func + content[end_func:]
    
    with open("tools/predict_structure.py", "w") as f:
        f.write(final)

modify_predict()
