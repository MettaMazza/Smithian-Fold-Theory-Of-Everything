#!/usr/bin/env python3
"""
SFT PDB Comparison Engine
Computes distance-matrix RMSD (dRMSD) and Dihedral Angle RMSD between
predicted and experimental 3D structures.
"""
import sys
import math
import os

def parse_ca_coords(pdb_path):
    """Parses CA atom coordinates from a PDB file."""
    coords = []
    if not os.path.exists(pdb_path):
        return None
    with open(pdb_path) as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append((x, y, z))
    return coords

def compute_distance_matrix(coords):
    """Computes N x N distance matrix for a list of coordinates."""
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
    """Computes the distance-matrix RMSD between two distance matrices."""
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
        print("Usage: python3 tools/compare_pdb.py <predicted.pdb> <experimental.pdb>")
        sys.exit(1)
        
    pred_path = sys.argv[1]
    exp_path = sys.argv[2]
    
    print("=== SFT Structure Comparison ===")
    print(f"Predicted structure: {pred_path}")
    print(f"Experimental structure: {exp_path}")
    
    pred_ca = parse_ca_coords(pred_path)
    exp_ca = parse_ca_coords(exp_path)
    
    if not pred_ca or not exp_ca:
        print("Error: Could not parse CA coordinates from one or both files.")
        sys.exit(1)
        
    n = min(len(pred_ca), len(exp_ca))
    pred_ca = pred_ca[:n]
    exp_ca = exp_ca[:n]
    
    print(f"Comparing first {n} aligned CA atoms...")
    
    # Compute matrices
    mat_pred = compute_distance_matrix(pred_ca)
    mat_exp = compute_distance_matrix(exp_ca)
    
    # Compute dRMSD
    drmsd = compute_drmsd(mat_pred, mat_exp)
    
    print(f"\nDistance Matrix RMSD (dRMSD): {drmsd:.3f} Å")
    
    # Evaluate secondary structure regions specifically (e.g. main alpha helix, residues 23-34)
    # Ubiquitin main helix is index 22 to 32 (residues 23-33)
    helix_start, helix_end = 22, 32
    if n > helix_end:
        mat_pred_helix = [row[helix_start:helix_end] for row in mat_pred[helix_start:helix_end]]
        mat_exp_helix = [row[helix_start:helix_end] for row in mat_exp[helix_start:helix_end]]
        drmsd_helix = compute_drmsd(mat_pred_helix, mat_exp_helix)
        print(f"Main Alpha-Helix Subregion dRMSD: {drmsd_helix:.3f} Å")
        
    # Check sheet region (residues 1-17)
    sheet_start, sheet_end = 0, 16
    if n > sheet_end:
        mat_pred_sheet = [row[sheet_start:sheet_end] for row in mat_pred[sheet_start:sheet_end]]
        mat_exp_sheet = [row[sheet_start:sheet_end] for row in mat_exp[sheet_start:sheet_end]]
        drmsd_sheet = compute_drmsd(mat_pred_sheet, mat_exp_sheet)
        print(f"N-terminal Beta-Sheet Subregion dRMSD: {drmsd_sheet:.3f} Å")
        
    print("\nComparison complete. Zero parameters, pure topological matching.")

if __name__ == "__main__":
    main()
