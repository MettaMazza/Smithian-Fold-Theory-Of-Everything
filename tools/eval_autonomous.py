#!/usr/bin/env python3
import sys
import numpy as np
from predict_structure import compute_tm, parse_pdb_backbone

def eval_pdb(pred_pdb, target_pdb):
    with open(pred_pdb) as f:
        pred_content = f.read()
    pred_residues = parse_pdb_backbone(pred_content)
    P = np.array([r["CA"] for r in pred_residues])

    with open(target_pdb) as f:
        target_content = f.read()
    target_residues = parse_pdb_backbone(target_content)
    Q = np.array([r["CA"] for r in target_residues])

    n = min(len(P), len(Q))
    if n == 0:
        print("Error: No coordinates found.")
        sys.exit(1)

    tm = compute_tm(P[:n], Q[:n])
    
    # Calculate dRMSD
    dist_P = np.linalg.norm(P[:n, None] - P[:n], axis=2)
    dist_Q = np.linalg.norm(Q[:n, None] - Q[:n], axis=2)
    diff = dist_P - dist_Q
    drmsd = np.sqrt(np.sum(diff**2) / (n*(n-1)))

    print(f"Comparison: {pred_pdb} vs {target_pdb}")
    print(f"Final Blind TM-score: {tm:.4f}")
    print(f"Final Blind dRMSD: {drmsd:.3f}A")

if __name__ == '__main__':
    eval_pdb(sys.argv[1], sys.argv[2])
