#!/usr/bin/env python3
"""
SFT Protein Complex (Quaternary) Structure Prediction Engine
Input: Amino acid sequence of a homodimeric monomer
Output: Predicted 3D coordinate PDB file of the docked homodimer.
"""
import sys
import math
import os

# Standard peptide bond geometries
BOND_N_CA = 1.46   # Å
BOND_CA_C = 1.52   # Å
BOND_C_N = 1.33    # Å

# Bond angles in radians
ANGLE_C_N_CA = math.radians(121.0)
ANGLE_N_CA_C = math.radians(111.0)
ANGLE_CA_C_N = math.radians(116.0)

# SFT Forced Rational Dihedral Angles (in radians)
DIHEDRAL_ALPHA_PHI = math.radians(-60.0)
DIHEDRAL_ALPHA_PSI = math.radians(-45.0)
DIHEDRAL_BETA_PHI = math.radians(-120.0)
DIHEDRAL_BETA_PSI = math.radians(135.0)
DIHEDRAL_LOOP_PHI = math.radians(-90.0)
DIHEDRAL_LOOP_PSI = math.radians(120.0)
DIHEDRAL_OMEGA = math.radians(180.0)

# Propensities for secondary structure
PROPENSITIES = {
    'A': 'H', 'E': 'H', 'L': 'H', 'M': 'H', 'Q': 'H', 'K': 'H', 'R': 'H', 'H': 'H',
    'V': 'E', 'I': 'E', 'T': 'E', 'F': 'E', 'Y': 'E', 'W': 'E',
    'G': 'C', 'P': 'C', 'D': 'C', 'N': 'C', 'S': 'C', 'C': 'C'
}

def cross_product(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def normalize(v):
    l = math.sqrt(sum(x*x for x in v))
    if l == 0:
        return [0, 0, 0]
    return [x/l for x in v]

def place_next_atom(p1, p2, p3, bond_length, bond_angle, dihedral):
    v1 = [p3[i] - p2[i] for i in range(3)]
    v2 = [p2[i] - p1[i] for i in range(3)]
    u1 = normalize(v1)
    u2 = normalize(v2)
    un = normalize(cross_product(u2, u1))
    x_axis = u1
    y_axis = normalize(cross_product(un, u1))
    z_axis = un
    theta = bond_angle
    chi = dihedral
    dx = -math.cos(theta)
    dy = math.sin(theta) * math.cos(chi)
    dz = math.sin(theta) * math.sin(chi)
    gx = dx * x_axis[0] + dy * y_axis[0] + dz * z_axis[0]
    gy = dx * x_axis[1] + dy * y_axis[1] + dz * z_axis[1]
    gz = dx * x_axis[2] + dy * y_axis[2] + dz * z_axis[2]
    return [
        p3[0] + bond_length * gx,
        p3[1] + bond_length * gy,
        p3[2] + bond_length * gz
    ]

def predict_secondary_structure(sequence):
    ss = []
    for aa in sequence:
        ss.append(PROPENSITIES.get(aa, 'C'))
    return ss

def evaluate_conformation(sequence, secondary_structures, phi_angles, psi_angles):
    n = len(sequence)
    atoms = []
    
    # Initialize first residue
    p_n = [0.0, 0.0, 0.0]
    p_ca = [0.0, 0.0, BOND_N_CA]
    # Place C in N-CA-C plane
    p_c = [
        BOND_CA_C * math.sin(ANGLE_N_CA_C),
        0.0,
        BOND_N_CA - BOND_CA_C * math.cos(ANGLE_N_CA_C)
    ]
    
    atoms.append({"name": "N", "coord": p_n, "resname": sequence[0], "resnum": 1})
    atoms.append({"name": "CA", "coord": p_ca, "resname": sequence[0], "resnum": 1})
    atoms.append({"name": "C", "coord": p_c, "resname": sequence[0], "resnum": 1})
    
    for i in range(1, n):
        prev_n = atoms[-3]["coord"]
        prev_ca = atoms[-2]["coord"]
        prev_c = atoms[-1]["coord"]
        
        p_n_curr = place_next_atom(prev_n, prev_ca, prev_c, BOND_C_N, ANGLE_CA_C_N, psi_angles[i-1])
        atoms.append({"name": "N", "coord": p_n_curr, "resname": sequence[i], "resnum": i+1})
        
        p_ca_curr = place_next_atom(prev_ca, prev_c, p_n_curr, BOND_N_CA, ANGLE_C_N_CA, DIHEDRAL_OMEGA)
        atoms.append({"name": "CA", "coord": p_ca_curr, "resname": sequence[i], "resnum": i+1})
        
        p_c_curr = place_next_atom(prev_c, p_n_curr, p_ca_curr, BOND_CA_C, ANGLE_N_CA_C, phi_angles[i])
        atoms.append({"name": "C", "coord": p_c_curr, "resname": sequence[i], "resnum": i+1})
        
    ca_coords = [a["coord"] for a in atoms if a["name"] == "CA"]
    hydrophobic_indices = [i for i, aa in enumerate(sequence) if aa in ('L', 'I', 'V', 'F', 'M', 'A', 'Y', 'W')]
    
    score = 0.0
    for idx_i in range(len(hydrophobic_indices)):
        for idx_j in range(idx_i + 1, len(hydrophobic_indices)):
            i = hydrophobic_indices[idx_i]
            j = hydrophobic_indices[idx_j]
            if abs(i - j) >= 4:
                coord_i = ca_coords[i]
                coord_j = ca_coords[j]
                dx = coord_i[0] - coord_j[0]
                dy = coord_i[1] - coord_j[1]
                dz = coord_i[2] - coord_j[2]
                score += math.sqrt(dx*dx + dy*dy + dz*dz)
                
    has_clash = False
    for i in range(len(ca_coords)):
        for j in range(i + 3, len(ca_coords)):
            coord_i = ca_coords[i]
            coord_j = ca_coords[j]
            dx = coord_i[0] - coord_j[0]
            dy = coord_i[1] - coord_j[1]
            dz = coord_i[2] - coord_j[2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < 3.2:
                has_clash = True
                break
        if has_clash:
            break
            
    return score, has_clash, atoms

def optimize_tertiary_packing(sequence, secondary_structures):
    n = len(sequence)
    phi_angles = [0.0] * n
    psi_angles = [0.0] * n
    for i in range(n):
        ss = secondary_structures[i]
        if ss == 'H':
            phi_angles[i] = DIHEDRAL_ALPHA_PHI
            psi_angles[i] = DIHEDRAL_ALPHA_PSI
        elif ss == 'E':
            phi_angles[i] = DIHEDRAL_BETA_PHI
            psi_angles[i] = DIHEDRAL_BETA_PSI
        else:
            phi_angles[i] = DIHEDRAL_LOOP_PHI
            psi_angles[i] = DIHEDRAL_LOOP_PSI
            
    loop_indices = [i for i in range(n) if secondary_structures[i] == 'C']
    candidates = [
        (math.radians(-90.0), math.radians(120.0)),
        (math.radians(-60.0), math.radians(120.0)),
        (math.radians(-120.0), math.radians(150.0)),
        (math.radians(-90.0), math.radians(0.0)),
        (math.radians(-60.0), math.radians(90.0)),
        (math.radians(60.0), math.radians(60.0)),
    ]
    best_score, best_clash, best_atoms = evaluate_conformation(sequence, secondary_structures, phi_angles, psi_angles)
    
    for iteration in range(2):
        for idx in loop_indices:
            orig_phi = phi_angles[idx]
            orig_psi = psi_angles[idx]
            for cand_phi, cand_psi in candidates:
                if cand_phi == orig_phi and cand_psi == orig_psi:
                    continue
                phi_angles[idx] = cand_phi
                psi_angles[idx] = cand_psi
                score, has_clash, atoms = evaluate_conformation(sequence, secondary_structures, phi_angles, psi_angles)
                if not has_clash:
                    if best_clash or score < best_score:
                        best_score = score
                        best_clash = has_clash
                        best_atoms = atoms
                        orig_phi = cand_phi
                        orig_psi = cand_psi
                else:
                    if best_clash and score < best_score:
                        best_score = score
                        best_atoms = atoms
                        orig_phi = cand_phi
                        orig_psi = cand_psi
            phi_angles[idx] = orig_phi
            psi_angles[idx] = orig_psi
            
    return best_atoms

# ==================== QUATERNARY DOCKING ENGINE ====================

def rotate_point(p, alpha, beta, gamma):
    sa, ca = math.sin(alpha), math.cos(alpha)
    sb, cb = math.sin(beta), math.cos(beta)
    sg, cg = math.sin(gamma), math.cos(gamma)
    
    x, y, z = p
    # Rx
    y1 = y*ca - z*sa
    z1 = y*sa + z*ca
    # Ry
    x2 = x*cb + z1*sb
    z2 = -x*sb + z1*cb
    # Rz
    x3 = x2*cg - y1*sg
    y3 = x2*sg + y1*cg
    return [x3, y3, z2]

def evaluate_complex(atoms_A, atoms_B_base, Tx, Ty, Tz, alpha, beta, gamma, hydrophobic_indices):
    atoms_B = []
    for a in atoms_B_base:
        rotated = rotate_point(a["coord"], alpha, beta, gamma)
        translated = [rotated[0] + Tx, rotated[1] + Ty, rotated[2] + Tz]
        atoms_B.append({
            "name": a["name"],
            "coord": translated,
            "resname": a["resname"],
            "resnum": a["resnum"]
        })
        
    ca_A = [a["coord"] for a in atoms_A if a["name"] == "CA"]
    ca_B = [a["coord"] for a in atoms_B if a["name"] == "CA"]
    
    # Interface score: minimize sum of distances between hydrophobic residue pairs
    score = 0.0
    for idx_a in hydrophobic_indices:
        for idx_b in hydrophobic_indices:
            coord_a = ca_A[idx_a]
            coord_b = ca_B[idx_b]
            dx = coord_a[0] - coord_b[0]
            dy = coord_a[1] - coord_b[1]
            dz = coord_a[2] - coord_b[2]
            score += math.sqrt(dx*dx + dy*dy + dz*dz)
            
    # Clash check: distance between any atom in A and any atom in B < 3.2 Å
    has_clash = False
    for a in atoms_A:
        if a["name"] != "CA": continue
        for b in atoms_B:
            if b["name"] != "CA": continue
            coord_a = a["coord"]
            coord_b = b["coord"]
            dx = coord_a[0] - coord_b[0]
            dy = coord_a[1] - coord_b[1]
            dz = coord_a[2] - coord_b[2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < 3.2:
                has_clash = True
                break
        if has_clash:
            break
            
    return score, has_clash, atoms_B

def dock_complex(atoms_A, sequence):
    hydrophobic_indices = [i for i, aa in enumerate(sequence) if aa in ('L', 'I', 'V', 'F', 'M', 'A', 'Y', 'W')]
    if not hydrophobic_indices:
        hydrophobic_indices = list(range(len(sequence)))
        
    # Calculate Center of Mass of monomer A
    coords_A = [a["coord"] for a in atoms_A]
    center_A = [sum(c[i] for c in coords_A)/len(coords_A) for i in range(3)]
    
    # Initialize monomer B shifted along x/y/z axis
    Tx, Ty, Tz = center_A[0] + 12.0, center_A[1] + 12.0, center_A[2] + 12.0
    alpha, beta, gamma = 0.0, 0.0, 0.0
    
    best_score, best_clash, best_atoms_B = evaluate_complex(
        atoms_A, atoms_A, Tx, Ty, Tz, alpha, beta, gamma, hydrophobic_indices
    )
    
    # Coordinate descent grid sweeps
    t_steps = [4.0, 2.0, 1.0, 0.5]
    r_steps = [math.radians(30.0), math.radians(15.0), math.radians(5.0)]
    
    for step_idx in range(len(t_steps)):
        t_step = t_steps[step_idx]
        r_step = r_steps[min(step_idx, len(r_steps)-1)]
        
        improved = True
        while improved:
            improved = False
            # Check translation moves
            for dx, dy, dz in [
                (t_step,0,0), (-t_step,0,0), (0,t_step,0), (0,-t_step,0), (0,0,t_step), (0,0,-t_step)
            ]:
                score, clash, atoms_B = evaluate_complex(
                    atoms_A, atoms_A, Tx+dx, Ty+dy, Tz+dz, alpha, beta, gamma, hydrophobic_indices
                )
                if not clash:
                    if best_clash or score < best_score:
                        best_score = score
                        best_clash = clash
                        best_atoms_B = atoms_B
                        Tx += dx
                        Ty += dy
                        Tz += dz
                        improved = True
                        
            # Check rotation moves
            for da, db, dg in [
                (r_step,0,0), (-r_step,0,0), (0,r_step,0), (0,-r_step,0), (0,0,r_step), (0,0,-r_step)
            ]:
                score, clash, atoms_B = evaluate_complex(
                    atoms_A, atoms_A, Tx, Ty, Tz, alpha+da, beta+db, gamma+dg, hydrophobic_indices
                )
                if not clash:
                    if best_clash or score < best_score:
                        best_score = score
                        best_clash = clash
                        best_atoms_B = atoms_B
                        alpha += da
                        beta += db
                        gamma += dg
                        improved = True
                        
    return best_atoms_B

def write_complex_pdb(atoms_A, atoms_B, file_path):
    map_3letter = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
    }
    with open(file_path, "w") as f:
        f.write("HEADER    SFT PREDICTED HOMODIMERIC COMPLEX\n")
        atom_num = 1
        for a in atoms_A:
            x, y, z = a["coord"]
            resname = a["resname"]
            res_3 = map_3letter.get(resname, 'ALA')
            f.write(f"ATOM  {atom_num:5d}  {a['name']:<4s}{res_3} A{a['resnum']:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {a['name'][0]}\n")
            atom_num += 1
        f.write("TER\n")
        for a in atoms_B:
            x, y, z = a["coord"]
            resname = a["resname"]
            res_3 = map_3letter.get(resname, 'ALA')
            f.write(f"ATOM  {atom_num:5d}  {a['name']:<4s}{res_3} B{a['resnum']:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {a['name'][0]}\n")
            atom_num += 1
        f.write("END\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tools/predict_complex.py <sequence> <output.pdb>")
        sys.exit(1)
        
    sequence = sys.argv[1].upper()
    output_path = sys.argv[2]
    
    print(f"Folding monomer sequence ({len(sequence)} residues): {sequence}")
    ss_states = predict_secondary_structure(sequence)
    atoms_A = optimize_tertiary_packing(sequence, ss_states)
    
    print("Docking homodimeric complex...")
    atoms_B = dock_complex(atoms_A, sequence)
    
    print(f"Writing complex to {output_path}...")
    write_complex_pdb(atoms_A, atoms_B, output_path)
    print("Quaternary docking complete.")

if __name__ == "__main__":
    main()
