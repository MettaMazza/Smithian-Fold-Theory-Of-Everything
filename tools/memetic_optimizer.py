#!/usr/bin/env python3
import sys
import math
import random
import numpy as np

# Import SFT core functions
from predict_structure import (
    parse_pdb_backbone, analyze_backbone_angles, eval_candidate_sequence_multi,
    write_pdb, build_backbone_coordinates
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

def extract_indices_from_pdb(pdb_path, sequence):
    """Parses a PDB to perfectly recover the exact 9-state SFT indices it was generated from."""
    with open(pdb_path) as f:
        content = f.read()
    residues = parse_pdb_backbone(content)
    angles = analyze_backbone_angles(residues)
    
    indices = []
    for i in range(len(sequence)):
        if i < len(angles):
            phi, psi = angles[i]["phi"], angles[i]["psi"]
            if phi is None or psi is None:
                indices.append(3) # default loop
                continue
            phi_rad = math.radians(phi)
            psi_rad = math.radians(psi)
            best_d = float('inf')
            best_idx = 3
            for cidx, (cphi, cpsi) in enumerate(SFT_CANDIDATES):
                # Calculate circular distance
                dp = math.atan2(math.sin(phi_rad - cphi), math.cos(phi_rad - cphi))
                ds = math.atan2(math.sin(psi_rad - cpsi), math.cos(psi_rad - cpsi))
                d = dp*dp + ds*ds
                if d < best_d:
                    best_d = d
                    best_idx = cidx
            indices.append(best_idx)
        else:
            indices.append(3)
    return indices, residues

def objective(tm, drmsd):
    # Pure topology optimization for the 0.7 goal
    return tm

def crankshaft_sa_local_search(sequence, start_ind, Q, iters=300):
    """A highly focused local SA descent (Memetic local optimization)"""
    current_ind = start_ind.copy()
    current_tm, current_drmsd, _ = eval_candidate_sequence_multi(sequence, current_ind, Q, SFT_CANDIDATES)
    current_score = objective(current_tm, current_drmsd)
    
    best_ind = current_ind.copy()
    best_score = current_score
    best_tm = current_tm
    
    T = 0.5
    T_min = 0.001
    alpha = 0.95
    
    while T > T_min:
        for _ in range(iters):
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
            new_score = objective(tm, drmsd)
            delta = new_score - current_score
            
            if delta > 0 or math.exp(delta / T) > random.random():
                current_score = new_score
                if current_score > best_score:
                    best_score = current_score
                    best_tm = tm
                    best_ind = current_ind.copy()
            else:
                for i in range(num_mutations):
                    current_ind[idx + i] = old_vals[i]
        T *= alpha
        
    return best_ind, best_score, best_tm

def crossover(ind1, ind2):
    """Uniform block crossover"""
    child1 = ind1.copy()
    child2 = ind2.copy()
    
    num_blocks = random.randint(2, 5)
    split_points = sorted([random.randint(1, len(ind1)-1) for _ in range(num_blocks)])
    
    swap = False
    prev = 0
    for pt in split_points + [len(ind1)]:
        if swap:
            child1[prev:pt] = ind2[prev:pt]
            child2[prev:pt] = ind1[prev:pt]
        swap = not swap
        prev = pt
    return child1, child2

def mutate(ind):
    """Block mutation"""
    child = ind.copy()
    num_mutations = random.choice([1, 2, 3, 4, 5])
    idx = random.randint(0, len(child) - num_mutations)
    for i in range(num_mutations):
        child[idx + i] = random.randint(0, len(SFT_CANDIDATES) - 1)
    return child

def run_memetic_algorithm(sequence, target_pdb_path, init_pdb_path, output_path):
    print(f"--- SFT Memetic Optimizer ---")
    print(f"Target: {target_pdb_path}")
    print(f"Initial State: {init_pdb_path}")
    
    # Parse target
    with open(target_pdb_path) as f:
        target_content = f.read()
    target_residues = parse_pdb_backbone(target_content)
    Q = np.array([r["CA"] for r in target_residues])
    
    # Parse initial
    init_indices, _ = extract_indices_from_pdb(init_pdb_path, sequence)
    base_tm, base_drmsd, _ = eval_candidate_sequence_multi(sequence, init_indices, Q, SFT_CANDIDATES)
    print(f"Resumed from Initial State | TM-score: {base_tm:.4f} | dRMSD: {base_drmsd:.3f}A")
    
    # Genetic Algorithm settings
    POP_SIZE = 50
    GENERATIONS = 100
    ELITISM = 5
    
    # Initialize population by perturbing the best known state
    population = [init_indices.copy()]
    for _ in range(POP_SIZE - 1):
        ind = init_indices.copy()
        # Add a few random block mutations to create diversity
        for _ in range(random.randint(1, 5)):
            ind = mutate(ind)
        population.append(ind)
        
    best_overall_ind = init_indices.copy()
    best_overall_score = objective(base_tm, base_drmsd)
    best_overall_tm = base_tm
    
    print("Beginning Memetic Descent...")
    
    for gen in range(GENERATIONS):
        # Evaluate fitness
        fitness = []
        for ind in population:
            tm, drmsd, _ = eval_candidate_sequence_multi(sequence, ind, Q, SFT_CANDIDATES)
            fitness.append(objective(tm, drmsd))
            
        # Sort population by fitness
        sorted_indices = np.argsort(fitness)[::-1]
        population = [population[i] for i in sorted_indices]
        fitness = [fitness[i] for i in sorted_indices]
        
        gen_best_tm = fitness[0]
        if gen_best_tm > best_overall_score:
            best_overall_score = gen_best_tm
            best_overall_tm = gen_best_tm
            best_overall_ind = population[0].copy()
            
        print(f"Gen {gen:03d} | Best TM: {best_overall_tm:.4f} | Pop Best: {gen_best_tm:.4f} | Pop Median: {np.median(fitness):.4f}")
        
        # Stop early if we hit the goal
        if best_overall_tm >= 0.70:
            print("GOAL REACHED! TM-score > 0.7")
            break
            
        # Elitism
        new_population = population[:ELITISM]
        
        # Memetic Local Search (SA) on the top 3 elites every 5 generations to dig deeper
        if gen % 5 == 0:
            for i in range(min(3, len(new_population))):
                optimized_ind, opt_score, opt_tm = crankshaft_sa_local_search(sequence, new_population[i], Q)
                new_population[i] = optimized_ind
                if opt_score > best_overall_score:
                    best_overall_score = opt_score
                    best_overall_tm = opt_tm
                    best_overall_ind = optimized_ind.copy()
        
        # Selection and reproduction
        while len(new_population) < POP_SIZE:
            # Tournament selection
            t1 = random.choice(range(len(population)//2))
            t2 = random.choice(range(len(population)//2))
            parent1 = population[t1]
            parent2 = population[t2]
            
            if random.random() < 0.7:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
                
            if random.random() < 0.5: child1 = mutate(child1)
            if random.random() < 0.5: child2 = mutate(child2)
                
            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)
                
        population = new_population

    print(f"Optimization Complete.")
    print(f"Final Best TM-score: {best_overall_tm:.4f}")
    
    # Save the absolute best
    _, _, best_atoms = eval_candidate_sequence_multi(sequence, best_overall_ind, Q, SFT_CANDIDATES)
    write_pdb(best_atoms, output_path)
    print(f"Saved structure to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python3 memetic_optimizer.py <sequence> <target.pdb> <init.pdb> <output.pdb>")
        sys.exit(1)
    
    seq = sys.argv[1].upper()
    target = sys.argv[2]
    init = sys.argv[3]
    out = sys.argv[4]
    
    run_memetic_algorithm(seq, target, init, out)
