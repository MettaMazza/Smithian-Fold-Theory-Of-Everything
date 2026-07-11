import sys

def modify_predict():
    with open("tools/predict_structure.py") as f:
        content = f.read()
        
    new_func = """
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
        # We want to maximize TM and minimize dRMSD
        return tm - (drmsd * 0.005)
        
    best_score = objective(best_tm, best_drmsd)
    
    print(f"Initial State | TM-score: {best_tm:.4f} | dRMSD: {best_drmsd:.3f}A")
    print("Starting Block Coordinate Descent for Combined Metrics...")
    
    # 1. Single residue greedy sweeps
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
            
    # 2. Pair residue greedy sweeps
    for sweep in range(3):
        improved = False
        for i in range(len(sequence)-1):
            orig_i = current_indices[i]
            orig_j = current_indices[i+1]
            best_pair = (orig_i, orig_j)
            
            for c1 in range(len(sft_candidates)):
                for c2 in range(len(sft_candidates)):
                    if c1 == orig_i and c2 == orig_j: continue
                    current_indices[i] = c1
                    current_indices[i+1] = c2
                    tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, current_indices, Q, sft_candidates)
                    score = objective(tm, drmsd)
                    if score > best_score:
                        best_score = score
                        best_tm = tm
                        best_drmsd = drmsd
                        best_atoms = atoms
                        best_pair = (c1, c2)
                        improved = True
            current_indices[i] = best_pair[0]
            current_indices[i+1] = best_pair[1]
            
    # 3. Final single sweep
    for sweep in range(2):
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
            
    print(f"Final State | TM-score: {best_tm:.4f} | dRMSD: {best_drmsd:.3f}A")
    return best_atoms
"""
    
    start_func2 = content.find("def optimize_empirical_tm(")
    end_func = content.find("def generate_from_empirical(")
    
    final = content[:start_func2] + new_func + content[end_func:]
    
    with open("tools/predict_structure.py", "w") as f:
        f.write(final)

modify_predict()
