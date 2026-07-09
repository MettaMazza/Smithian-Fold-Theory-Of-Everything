#!/usr/bin/env python3
"""
SFT Complex Comparison Engine
Computes global and interface dRMSD between predicted and experimental homodimer complexes.
"""
import sys
import math
import os

def parse_chains_ca(pdb_path):
    """
    Parses CA coordinates from a PDB file, splitting them by chain.
    Returns a dict mapping chain identifiers to lists of coordinates.
    """
    chains = {}
    if not os.path.exists(pdb_path):
        return None
        
    current_chain = None
    with open(pdb_path) as f:
        for line in f:
            # Only read the first model if it is an NMR structure
            if line.startswith("ENDMDL"):
                break
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                chain_id = line[21].strip()
                if not chain_id:
                    chain_id = "A"  # Default
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                
                if chain_id not in chains:
                    chains[chain_id] = []
                chains[chain_id].append((x, y, z))
    return chains

def compute_distance_matrix(coords):
    n = len(coords)
    dist_matrix = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dz = coords[i][2] - coords[j][2]
            d = math.sqrt(dx*dx + dy*dy + dz*dz)
            dist_matrix[i][j] = d
            dist_matrix[j][i] = d
    return dist_matrix

def compute_drmsd(matrix_a, matrix_b):
    n = len(matrix_a)
    total_sq_diff = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            diff = matrix_a[i][j] - matrix_b[i][j]
            total_sq_diff += diff * diff
            count += 1
    if count == 0:
        return 0.0
    return math.sqrt(total_sq_diff / count)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tools/compare_complex.py <predicted_complex.pdb> <experimental_complex.pdb>")
        sys.exit(1)
        
    pred_path = sys.argv[1]
    exp_path = sys.argv[2]
    
    print("=== SFT Complex Structure Comparison ===")
    pred_chains = parse_chains_ca(pred_path)
    exp_chains = parse_chains_ca(exp_path)
    
    if not pred_chains or not exp_chains:
        print("Error: Could not parse coordinates from one or both files.")
        sys.exit(1)
        
    pred_keys = sorted(list(pred_chains.keys()))
    exp_keys = sorted(list(exp_chains.keys()))
    
    print(f"Predicted complex chains: {pred_keys}")
    print(f"Experimental complex chains: {exp_keys}")
    
    if len(pred_keys) < 2 or len(exp_keys) < 2:
        print("Error: Complex comparison requires at least 2 chains in both files.")
        sys.exit(1)
        
    # Align predicted chain 1 and 2 to experimental chain 1 and 2
    pred_ca_A = pred_chains[pred_keys[0]]
    pred_ca_B = pred_chains[pred_keys[1]]
    
    exp_ca_A = exp_chains[exp_keys[0]]
    exp_ca_B = exp_chains[exp_keys[1]]
    
    # Trim to match sequence lengths
    len_monomer = min(len(pred_ca_A), len(pred_ca_B), len(exp_ca_A), len(exp_ca_B))
    pred_ca_A = pred_ca_A[:len_monomer]
    pred_ca_B = pred_ca_B[:len_monomer]
    exp_ca_A = exp_ca_A[:len_monomer]
    exp_ca_B = exp_ca_B[:len_monomer]
    
    # Concatenate chains for global comparison
    pred_global = pred_ca_A + pred_ca_B
    exp_global = exp_ca_A + exp_ca_B
    
    # Compute matrices
    mat_pred = compute_distance_matrix(pred_global)
    mat_exp = compute_distance_matrix(exp_global)
    
    # Global dRMSD
    global_drmsd = compute_drmsd(mat_pred, mat_exp)
    
    # Monomer A dRMSD
    mat_pred_mono = [row[:len_monomer] for row in mat_pred[:len_monomer]]
    mat_exp_mono = [row[:len_monomer] for row in mat_exp[:len_monomer]]
    mono_drmsd = compute_drmsd(mat_pred_mono, mat_exp_mono)
    
    # Interface dRMSD (only distances crossing the chain interface)
    total_sq_diff_int = 0.0
    count_int = 0
    for i in range(len_monomer):
        for j in range(len_monomer):
            # Distance from residue i in chain A to residue j in chain B
            dist_pred = mat_pred[i][len_monomer + j]
            dist_exp = mat_exp[i][len_monomer + j]
            diff = dist_pred - dist_exp
            total_sq_diff_int += diff * diff
            count_int += 1
            
    int_drmsd = math.sqrt(total_sq_diff_int / count_int) if count_int > 0 else 0.0
    
    print(f"\nMonomer folding dRMSD: {mono_drmsd:.3f} Å")
    print(f"Quaternary interface dRMSD: {int_drmsd:.3f} Å")
    print(f"Global complex dRMSD: {global_drmsd:.3f} Å")
    print("\nComparison complete. Zero parameter space command docking.")

if __name__ == "__main__":
    main()
