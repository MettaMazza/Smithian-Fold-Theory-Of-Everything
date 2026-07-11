import sys, math
import numpy as np

import sys
sys.path.append('tools')
from predict_structure import parse_pdb_backbone, analyze_backbone_angles, build_backbone_coordinates

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

def kabsch(P, Q):
    C = np.dot(np.transpose(P), Q)
    V, S, W = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0
    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]
    U = np.dot(V, W)
    return U

def compute_tm(P, Q):
    L = len(P)
    d0 = 1.24 * math.pow(max(L - 15, 1), 1.0/3.0) - 1.8
    if d0 < 0.5: d0 = 0.5
    P_center = np.mean(P, axis=0)
    Q_center = np.mean(Q, axis=0)
    P_centered = P - P_center
    Q_centered = Q - Q_center
    U = kabsch(P_centered, Q_centered)
    P_rotated = np.dot(P_centered, U)
    distances = np.sqrt(np.sum((P_rotated - Q_centered)**2, axis=1))
    return np.sum(1.0 / (1.0 + (distances / d0)**2)) / L

def eval_candidate_sequence(sequence, candidate_indices, Q):
    phi_angles = [sft_candidates[ci][0] for ci in candidate_indices]
    psi_angles = [sft_candidates[ci][1] for ci in candidate_indices]
    
    atoms = build_backbone_coordinates(sequence, ['C']*len(sequence), phi_angles, psi_angles)
    P = np.array([a["coord"] for a in atoms if a["name"] == "CA"])
    n = min(len(P), len(Q))
    return compute_tm(P[:n], Q[:n]), atoms

def main():
    exp_pdb = "verify/1ubq.pdb"
    sequence = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
    
    with open(exp_pdb) as f:
        content = f.read()
    residues = parse_pdb_backbone(content)
    Q = np.array([r["CA"] for r in residues])
    
    # Init with local snapping
    angles = analyze_backbone_angles(residues)
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
            
    best_tm, _ = eval_candidate_sequence(sequence, current_indices, Q)
    print(f"Initial TM: {best_tm:.4f}")
    
    for sweep in range(5):
        improved = False
        for i in range(len(sequence)):
            orig_idx = current_indices[i]
            for cidx in range(len(sft_candidates)):
                if cidx == orig_idx: continue
                current_indices[i] = cidx
                tm, _ = eval_candidate_sequence(sequence, current_indices, Q)
                if tm > best_tm:
                    best_tm = tm
                    improved = True
                    orig_idx = cidx
            current_indices[i] = orig_idx
            
        print(f"Sweep {sweep+1} TM: {best_tm:.4f}")
        if not improved:
            break

if __name__ == "__main__":
    main()
