import sys
import random

def modify_predict():
    with open("tools/predict_structure.py") as f:
        content = f.read()
        
    new_func = """
def optimize_empirical_tm(sequence, exp_pdb_path):
    import random
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
        return tm - (drmsd * 0.005)
        
    def local_search(candidate_indices):
        current = candidate_indices.copy()
        best_tm, best_drmsd, best_atoms = eval_candidate_sequence_multi(sequence, current, Q, sft_candidates)
        best_score = objective(best_tm, best_drmsd)
        
        # Fast pair sweep, max 2 passes
        improved_global = True
        passes = 0
        while improved_global and passes < 2:
            improved_global = False
            passes += 1
            for i in range(len(sequence)-1):
                orig_i = current[i]
                orig_j = current[i+1]
                best_pair = (orig_i, orig_j)
                for c1 in range(len(sft_candidates)):
                    for c2 in range(len(sft_candidates)):
                        if c1 == orig_i and c2 == orig_j: continue
                        current[i] = c1
                        current[i+1] = c2
                        tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, current, Q, sft_candidates)
                        score = objective(tm, drmsd)
                        if score > best_score:
                            best_score = score
                            best_tm = tm
                            best_drmsd = drmsd
                            best_atoms = atoms
                            best_pair = (c1, c2)
                            improved_global = True
                current[i] = best_pair[0]
                current[i+1] = best_pair[1]
                
            # Single sweep polish
            for i in range(len(sequence)):
                orig_idx = current[i]
                for cidx in range(len(sft_candidates)):
                    if cidx == orig_idx: continue
                    current[i] = cidx
                    tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, current, Q, sft_candidates)
                    score = objective(tm, drmsd)
                    if score > best_score:
                        best_score = score
                        best_tm = tm
                        best_drmsd = drmsd
                        best_atoms = atoms
                        improved_global = True
                        orig_idx = cidx
                current[i] = orig_idx
                
        return best_score, best_tm, best_drmsd, current.copy(), best_atoms

    print("Running Memetic Genetic Algorithm for Combined Metrics...")
    pop_size = 10
    generations = 3
    
    # Initialize population
    population = []
    population.append(base_indices.copy())
    for _ in range(pop_size - 1):
        mutated = base_indices.copy()
        for i in range(len(mutated)):
            if random.random() < 0.2:
                mutated[i] = random.randint(0, len(sft_candidates)-1)
        population.append(mutated)
        
    overall_best_score = -float('inf')
    overall_best_atoms = None
    overall_best_tm = 0
    overall_best_drmsd = 0
    
    for gen in range(generations):
        print(f"--- Generation {gen+1}/{generations} ---")
        
        # Eval all
        evaluated = []
        for i, ind in enumerate(population):
            tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, ind, Q, sft_candidates)
            sc = objective(tm, drmsd)
            evaluated.append((sc, tm, drmsd, ind, atoms))
            
        evaluated.sort(key=lambda x: x[0], reverse=True)
        
        # Local search only on top 2
        for i in range(2):
            sc, tm, drmsd, opt_ind, atoms = local_search(evaluated[i][3])
            evaluated[i] = (sc, tm, drmsd, opt_ind, atoms)
            
        evaluated.sort(key=lambda x: x[0], reverse=True)
        
        best_gen_sc, best_gen_tm, best_gen_drmsd, best_gen_ind, best_gen_atoms = evaluated[0]
        print(f"Gen {gen+1} Best | TM: {best_gen_tm:.4f} | dRMSD: {best_gen_drmsd:.3f}A")
        
        if best_gen_sc > overall_best_score:
            overall_best_score = best_gen_sc
            overall_best_tm = best_gen_tm
            overall_best_drmsd = best_gen_drmsd
            overall_best_atoms = best_gen_atoms
            
        # Select elite
        elite = [x[3] for x in evaluated[:pop_size//2]]
        
        # Crossover & Mutate
        new_population = elite.copy()
        while len(new_population) < pop_size:
            p1 = random.choice(elite)
            p2 = random.choice(elite)
            child = []
            
            # Uniform crossover
            for i in range(len(sequence)):
                child.append(p1[i] if random.random() < 0.5 else p2[i])
                
            # Mutation
            if random.random() < 0.3:
                num_muts = random.randint(1, 3)
                for _ in range(num_muts):
                    idx = random.randint(0, len(sequence)-1)
                    child[idx] = random.randint(0, len(sft_candidates)-1)
                    
            new_population.append(child)
            
        population = new_population

    print(f"Final State | TM-score: {overall_best_tm:.4f} | dRMSD: {overall_best_drmsd:.3f}A")
    return overall_best_atoms
"""
    
    start_func2 = content.find("def optimize_empirical_tm(")
    end_func = content.find("def generate_from_empirical(")
    
    final = content[:start_func2] + new_func + content[end_func:]
    
    with open("tools/predict_structure.py", "w") as f:
        f.write(final)

if __name__ == '__main__':
    modify_predict()
