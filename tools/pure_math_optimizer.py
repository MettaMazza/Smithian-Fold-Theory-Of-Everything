#!/usr/bin/env python3
import sys
import math
import random
import numpy as np

# Import SFT core functions
from predict_structure import (
    build_backbone_coordinates, write_pdb
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

def evaluate_pure_mathematical_objective(sequence, indices):
    """
    Zero-parameter mathematical objective function.
    Minimizes the Radius of Gyration of the topological nodes.
    Penalizes mathematical node intersection.
    """
    phi_angles = [SFT_CANDIDATES[idx][0] for idx in indices]
    psi_angles = [SFT_CANDIDATES[idx][1] for idx in indices]
    
    # We use a dummy secondary structure list 'C' for coil because we are overriding 
    # all angles with the exact SFT candidates anyway.
    ss = ['C'] * len(sequence)
    atoms = build_backbone_coordinates(sequence, ss, phi_angles, psi_angles)
    
    ca_coords = [np.array(a["coord"]) for a in atoms if a["name"] == "CA"]
    
    # Mathematical self-avoidance (vertices cannot occupy the same discrete mathematical cell)
    # Using 1.0 unit cell distance as the theoretical floor instead of empirical van der Waals
    for i in range(len(ca_coords)):
        for j in range(i + 3, len(ca_coords)):
            dist_sq = np.sum((ca_coords[i] - ca_coords[j])**2)
            if dist_sq < 1.0: # Mathematical topological overlap limit
                return float('inf'), atoms
                
    # Pure Mathematical Objective: Radius of Gyration (Compactness of the topological graph)
    center_of_mass = np.mean(ca_coords, axis=0)
    rog_sq = 0.0
    for coord in ca_coords:
        rog_sq += np.sum((coord - center_of_mass)**2)
    rog = math.sqrt(rog_sq / len(ca_coords))
    
    return rog, atoms

def crankshaft_sa_local_search(sequence, start_ind, iters=300):
    """A highly focused local SA descent (Memetic local optimization)"""
    current_ind = start_ind.copy()
    current_score, _ = evaluate_pure_mathematical_objective(sequence, current_ind)
    
    best_ind = current_ind.copy()
    best_score = current_score
    
    T = 10.0
    T_min = 0.001
    alpha = 0.90
    
    while T > T_min:
        for _ in range(iters):
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
                
            new_score, _ = evaluate_pure_mathematical_objective(sequence, current_ind)
            
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
    print(f"--- SFT Pure Mathematical Optimizer ---")
    
    # Genetic Algorithm settings
    POP_SIZE = 100
    GENERATIONS = 150
    ELITISM = 5
    
    print("Generating zero-parameter random initial population...")
    population = []
    while len(population) < POP_SIZE:
        ind = [random.randint(0, len(SFT_CANDIDATES) - 1) for _ in range(len(sequence))]
        score, _ = evaluate_pure_mathematical_objective(sequence, ind)
        if score != float('inf'):
            population.append(ind)
            
    best_overall_ind = population[0].copy()
    best_overall_score, _ = evaluate_pure_mathematical_objective(sequence, best_overall_ind)
    
    print("Beginning Blind Mathematical Topological Descent...")
    
    for gen in range(GENERATIONS):
        fitness = []
        for ind in population:
            score, _ = evaluate_pure_mathematical_objective(sequence, ind)
            fitness.append(score)
            
        sorted_indices = np.argsort(fitness)
        population = [population[i] for i in sorted_indices]
        fitness = [fitness[i] for i in sorted_indices]
        
        gen_best_score = fitness[0]
        if gen_best_score < best_overall_score:
            best_overall_score = gen_best_score
            best_overall_ind = population[0].copy()
            
        valid_fitness = [f for f in fitness if f != float('inf')]
        median_fit = np.median(valid_fitness) if valid_fitness else float('inf')
        
        print(f"Gen {gen:03d} | Best RoG: {best_overall_score:.2f} | Pop Best: {gen_best_score:.2f} | Pop Median: {median_fit:.2f}")
        
        new_population = population[:ELITISM]
        
        if gen % 5 == 0:
            for i in range(min(3, len(new_population))):
                optimized_ind, opt_score = crankshaft_sa_local_search(sequence, new_population[i])
                new_population[i] = optimized_ind
                if opt_score < best_overall_score:
                    best_overall_score = opt_score
                    best_overall_ind = optimized_ind.copy()
        
        while len(new_population) < POP_SIZE:
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
                
            c1_score, _ = evaluate_pure_mathematical_objective(sequence, child1)
            if c1_score != float('inf'):
                new_population.append(child1)
                
            if len(new_population) < POP_SIZE:
                c2_score, _ = evaluate_pure_mathematical_objective(sequence, child2)
                if c2_score != float('inf'):
                    new_population.append(child2)
                
        population = new_population

    print(f"Optimization Complete.")
    print(f"Final Best Radius of Gyration: {best_overall_score:.2f}")
    
    _, best_atoms = evaluate_pure_mathematical_objective(sequence, best_overall_ind)
    write_pdb(best_atoms, output_path)
    print(f"Saved pure mathematical structure to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 pure_math_optimizer.py <sequence> <output.pdb>")
        sys.exit(1)
    
    seq = sys.argv[1].upper()
    out = sys.argv[2]
    
    run_ab_initio_algorithm(seq, out)
