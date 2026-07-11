#!/usr/bin/env python3
import sys
import math
import random
import numpy as np

# Import SFT core functions
from predict_structure import (
    predict_secondary_structure, build_backbone_coordinates, write_pdb
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

def evaluate_physical_objective(sequence, indices):
    """
    Zero-parameter physical objective function.
    Minimizes hydrophobic pairwise distance.
    Infinite penalty for steric clashes.
    """
    phi_angles = [SFT_CANDIDATES[idx][0] for idx in indices]
    psi_angles = [SFT_CANDIDATES[idx][1] for idx in indices]
    
    # We use a dummy secondary structure list 'C' for coil because we are overriding 
    # all angles with the exact SFT candidates anyway.
    ss = ['C'] * len(sequence)
    atoms = build_backbone_coordinates(sequence, ss, phi_angles, psi_angles)
    
    ca_coords = [a["coord"] for a in atoms if a["name"] == "CA"]
    
    # Steric clash detection (CA-CA distance < 3.2 Å)
    has_clash = False
    for i in range(len(ca_coords)):
        for j in range(i + 3, len(ca_coords)):
            dx = ca_coords[i][0] - ca_coords[j][0]
            dy = ca_coords[i][1] - ca_coords[j][1]
            dz = ca_coords[i][2] - ca_coords[j][2]
            if (dx*dx + dy*dy + dz*dz) < 10.24: # 3.2^2
                return float('inf'), atoms
                
    # Hydrophobic score (minimize sum of pairwise distances of non-polar residues)
    hydrophobic_indices = [i for i, aa in enumerate(sequence) if aa in ('L', 'I', 'V', 'F', 'M', 'A', 'Y', 'W')]
    
    score = 0.0
    for idx_i in range(len(hydrophobic_indices)):
        for idx_j in range(idx_i + 1, len(hydrophobic_indices)):
            i = hydrophobic_indices[idx_i]
            j = hydrophobic_indices[idx_j]
            if abs(i - j) >= 4:
                dx = ca_coords[i][0] - ca_coords[j][0]
                dy = ca_coords[i][1] - ca_coords[j][1]
                dz = ca_coords[i][2] - ca_coords[j][2]
                score += math.sqrt(dx*dx + dy*dy + dz*dz)
                
    return score, atoms

def crankshaft_sa_local_search(sequence, start_ind, iters=300):
    """A highly focused local SA descent (Memetic local optimization)"""
    current_ind = start_ind.copy()
    current_score, _ = evaluate_physical_objective(sequence, current_ind)
    
    best_ind = current_ind.copy()
    best_score = current_score
    
    T = 100.0
    T_min = 0.1
    alpha = 0.90
    
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
                
            new_score, _ = evaluate_physical_objective(sequence, current_ind)
            
            # We want to MINIMIZE the score
            delta = new_score - current_score
            
            if delta < 0 or (new_score != float('inf') and math.exp(-delta / T) > random.random()):
                current_score = new_score
                if current_score < best_score:
                    best_score = current_score
                    best_ind = current_ind.copy()
            else:
                for i in range(num_mutations):
                    current_ind[idx + i] = old_vals[i]
        T *= alpha
        
    return best_ind, best_score

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

def run_ab_initio_algorithm(sequence, output_path):
    print(f"--- SFT Zero-Prior Ab Initio Optimizer ---")
    
    # Genetic Algorithm settings
    POP_SIZE = 100
    GENERATIONS = 150
    ELITISM = 5
    
    # Initialize population COMPLETELY RANDOMLY (Zero Prior)
    print("Generating pure random initial population...")
    population = []
    while len(population) < POP_SIZE:
        ind = [random.randint(0, len(SFT_CANDIDATES) - 1) for _ in range(len(sequence))]
        score, _ = evaluate_physical_objective(sequence, ind)
        if score != float('inf'): # Must not have steric clashes to enter population
            population.append(ind)
            
    best_overall_ind = population[0].copy()
    best_overall_score, _ = evaluate_physical_objective(sequence, best_overall_ind)
    
    print("Beginning Blind Memetic Descent...")
    
    for gen in range(GENERATIONS):
        # Evaluate fitness (lower is better)
        fitness = []
        for ind in population:
            score, _ = evaluate_physical_objective(sequence, ind)
            fitness.append(score)
            
        # Sort population by fitness (ascending)
        sorted_indices = np.argsort(fitness)
        population = [population[i] for i in sorted_indices]
        fitness = [fitness[i] for i in sorted_indices]
        
        gen_best_score = fitness[0]
        if gen_best_score < best_overall_score:
            best_overall_score = gen_best_score
            best_overall_ind = population[0].copy()
            
        # Median of valid (non-clashing) individuals
        valid_fitness = [f for f in fitness if f != float('inf')]
        median_fit = np.median(valid_fitness) if valid_fitness else float('inf')
        
        print(f"Gen {gen:03d} | Best Hydrophobic Score: {best_overall_score:.2f} | Pop Best: {gen_best_score:.2f} | Pop Median: {median_fit:.2f}")
        
        new_population = population[:ELITISM]
        
        # Memetic Local Search (SA) on the top 3 elites every 5 generations to dig deeper
        if gen % 5 == 0:
            for i in range(min(3, len(new_population))):
                optimized_ind, opt_score = crankshaft_sa_local_search(sequence, new_population[i])
                new_population[i] = optimized_ind
                if opt_score < best_overall_score:
                    best_overall_score = opt_score
                    best_overall_ind = optimized_ind.copy()
        
        # Selection and reproduction
        while len(new_population) < POP_SIZE:
            # Tournament selection (prefer lower score)
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
                
            # Only add children that do not have steric clashes
            c1_score, _ = evaluate_physical_objective(sequence, child1)
            if c1_score != float('inf'):
                new_population.append(child1)
                
            if len(new_population) < POP_SIZE:
                c2_score, _ = evaluate_physical_objective(sequence, child2)
                if c2_score != float('inf'):
                    new_population.append(child2)
                
        population = new_population

    print(f"Optimization Complete.")
    print(f"Final Best Hydrophobic Score: {best_overall_score:.2f}")
    
    # Save the absolute best
    _, best_atoms = evaluate_physical_objective(sequence, best_overall_ind)
    write_pdb(best_atoms, output_path)
    print(f"Saved ab initio structure to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 ab_initio_optimizer.py <sequence> <output.pdb>")
        sys.exit(1)
    
    seq = sys.argv[1].upper()
    out = sys.argv[2]
    
    run_ab_initio_algorithm(seq, out)
