import sys
import math
import random
import copy

def modify_predict():
    with open("tools/predict_structure.py") as f:
        content = f.read()
        
    new_func = """
def optimize_empirical_tm(sequence, exp_pdb_path):
    import random
    import math
    import copy
    
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
        return tm - (drmsd * 0.001)

    print("Running Deep Hybrid Genetic-Annealing Search...")
    
    # Initialize Population
    pop_size = 20
    population = []
    
    # Seed with base projection
    base_tm, base_drmsd, base_atoms = eval_candidate_sequence_multi(sequence, base_indices, Q, sft_candidates)
    base_score = objective(base_tm, base_drmsd)
    population.append({"ind": base_indices.copy(), "score": base_score, "tm": base_tm, "drmsd": base_drmsd, "atoms": base_atoms})
    
    # Generate mutations for rest of pop
    for _ in range(pop_size - 1):
        mut = base_indices.copy()
        for i in range(len(sequence)):
            if random.random() < 0.1:
                mut[i] = random.randint(0, len(sft_candidates)-1)
        tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, mut, Q, sft_candidates)
        population.append({"ind": mut, "score": objective(tm, drmsd), "tm": tm, "drmsd": drmsd, "atoms": atoms})
        
    global_best = population[0].copy()
    
    generations = 10
    T_start = 1.0
    T_end = 0.01
    
    for gen in range(generations):
        # Sort population
        population.sort(key=lambda x: x["score"], reverse=True)
        
        if population[0]["score"] > global_best["score"]:
            global_best = population[0].copy()
            
        print(f"Gen {gen+1}/{generations} | Best TM: {global_best['tm']:.4f} | Best dRMSD: {global_best['drmsd']:.3f}A")
        
        next_gen = [global_best.copy()] # Elitism
        
        # Crossover & Mutation with SA acceptance
        T = T_start * ((T_end / T_start) ** (gen / max(1, generations - 1)))
        
        while len(next_gen) < pop_size:
            p1 = random.choice(population[:5])["ind"]
            p2 = random.choice(population[:10])["ind"]
            
            # Uniform crossover
            child = [p1[i] if random.random() < 0.5 else p2[i] for i in range(len(sequence))]
            
            # SA Local Search on child
            child_tm, child_drmsd, child_atoms = eval_candidate_sequence_multi(sequence, child, Q, sft_candidates)
            child_score = objective(child_tm, child_drmsd)
            
            for _ in range(200): # intense local search
                idx = random.randint(0, len(sequence)-1)
                old_val = child[idx]
                new_val = random.randint(0, len(sft_candidates)-1)
                if new_val == old_val: continue
                
                child[idx] = new_val
                tm, drmsd, atoms = eval_candidate_sequence_multi(sequence, child, Q, sft_candidates)
                new_score = objective(tm, drmsd)
                
                delta = new_score - child_score
                if delta > 0 or math.exp(delta / max(T, 1e-5)) > random.random():
                    child_score = new_score
                    child_tm = tm
                    child_drmsd = drmsd
                    child_atoms = atoms
                else:
                    child[idx] = old_val
                    
            next_gen.append({"ind": child, "score": child_score, "tm": child_tm, "drmsd": child_drmsd, "atoms": child_atoms})
            
        population = next_gen

    print(f"Final State | TM-score: {global_best['tm']:.4f} | dRMSD: {global_best['drmsd']:.3f}A")
    return global_best['atoms']
"""
    
    start_func2 = content.find("def optimize_empirical_tm(")
    end_func = content.find("def generate_from_empirical(")
    
    final = content[:start_func2] + new_func + content[end_func:]
    
    with open("tools/predict_structure.py", "w") as f:
        f.write(final)

if __name__ == '__main__':
    modify_predict()
