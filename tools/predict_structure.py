#!/usr/bin/env python3
"""
SFT Protein Structure Prediction Engine
Input: Amino acid sequence
Output: Predicted 3D coordinate PDB file using zero-parameter topological coordinates.
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
# Helix: phi = -1/6 (-60°), psi = -1/8 (-45°)
DIHEDRAL_ALPHA_PHI = math.radians(-60.0)
DIHEDRAL_ALPHA_PSI = math.radians(-45.0)

# Sheet: phi = -1/3 (-120°), psi = 3/8 (+135°)
DIHEDRAL_BETA_PHI = math.radians(-120.0)
DIHEDRAL_BETA_PSI = math.radians(135.0)

# Loop: phi = -90°, psi = 120° (standard loop average)
DIHEDRAL_LOOP_PHI = math.radians(-90.0)
DIHEDRAL_LOOP_PSI = math.radians(120.0)

# Peptide bond dihedral is always trans
DIHEDRAL_OMEGA = math.radians(180.0)

# Amino acid propensities
PROPENSITIES = {
    # Helix-favoring
    'A': 'H', 'E': 'H', 'L': 'H', 'M': 'H', 'Q': 'H', 'K': 'H', 'R': 'H', 'H': 'H',
    # Sheet-favoring
    'V': 'E', 'I': 'E', 'T': 'E', 'F': 'E', 'Y': 'E', 'W': 'E',
    # Loop/Turn
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
    """
    Places the 4th atom relative to the previous 3 atoms using the NeRF method.
    """
    v1 = [p3[i] - p2[i] for i in range(3)]
    v2 = [p2[i] - p1[i] for i in range(3)]
    
    u1 = normalize(v1)
    u2 = normalize(v2)
    
    # Normal to plane (p1, p2, p3)
    un = normalize(cross_product(u2, u1))
    
    # Orthonormal coordinate system vectors at p3
    x_axis = u1
    y_axis = normalize(cross_product(un, u1))
    z_axis = un
    
    # Local coordinates of the next atom
    theta = bond_angle
    chi = dihedral
    
    # Direction vector in local frame
    # Since theta is the bond angle, the vector points back, so x is -cos(theta)
    dx = -math.cos(theta)
    dy = math.sin(theta) * math.cos(chi)
    dz = math.sin(theta) * math.sin(chi)
    
    # Transform to global frame
    gx = dx * x_axis[0] + dy * y_axis[0] + dz * z_axis[0]
    gy = dx * x_axis[1] + dy * y_axis[1] + dz * z_axis[1]
    gz = dx * x_axis[2] + dy * y_axis[2] + dz * z_axis[2]
    
    return [
        p3[0] + bond_length * gx,
        p3[1] + bond_length * gy,
        p3[2] + bond_length * gz
    ]

def predict_secondary_structure(sequence):
    """
    Determines Helix (H), Sheet (E), or Loop (C) for each residue in the sequence
    using a deterministic local smoothing window.
    """
    n = len(sequence)
    raw = [PROPENSITIES.get(aa, 'C') for aa in sequence]
    predicted = ['C'] * n
    
    # Smoothing window of size 5
    for i in range(n):
        start = max(0, i-2)
        end = min(n, i+3)
        window = raw[start:end]
        
        count_H = window.count('H')
        count_E = window.count('E')
        count_C = window.count('C')
        
        if count_H >= 3:
            predicted[i] = 'H'
        elif count_E >= 3:
            predicted[i] = 'E'
        else:
            predicted[i] = 'C'
            
    # Hard constraints: Helices need >= 4 residues, Sheets >= 3
    # Group contiguous blocks
    i = 0
    while i < n:
        state = predicted[i]
        j = i
        while j < n and predicted[j] == state:
            j += 1
        length = j - i
        if state == 'H' and length < 4:
            for k in range(i, j):
                predicted[k] = 'C'
        elif state == 'E' and length < 3:
            for k in range(i, j):
                predicted[k] = 'C'
        i = j
        
    return predicted

def build_backbone_coordinates(sequence, secondary_structures, phi_angles, psi_angles):
    """Generates 3D Cartesian coordinates for N, CA, C of each residue using custom dihedrals."""
    atoms = []
    
    # Place first residue in standard coordinates in plane
    # N1 at origin
    n_coord = [0.0, 0.0, 0.0]
    # CA1 along x axis
    ca_coord = [BOND_N_CA, 0.0, 0.0]
    # C1 in xy-plane
    # Angle N-CA-C = 111°
    c_x = ca_coord[0] + BOND_CA_C * math.cos(math.pi - ANGLE_N_CA_C)
    c_y = ca_coord[1] + BOND_CA_C * math.sin(math.pi - ANGLE_N_CA_C)
    c_coord = [c_x, c_y, 0.0]
    
    atoms.append({"name": "N", "resnum": 1, "resname": sequence[0], "coord": n_coord})
    atoms.append({"name": "CA", "resnum": 1, "resname": sequence[0], "coord": ca_coord})
    atoms.append({"name": "C", "resnum": 1, "resname": sequence[0], "coord": c_coord})
    
    for i in range(1, len(sequence)):
        resname = sequence[i]
        resnum = i + 1
        phi = phi_angles[i]
        
        # Get coordinates of last 3 placed atoms
        p1 = atoms[-3]["coord"]  # N(i-1)
        p2 = atoms[-2]["coord"]  # CA(i-1)
        p3 = atoms[-1]["coord"]  # C(i-1)
        
        # Place N(i)
        # Dihedral psi(i-1)
        prev_psi = psi_angles[i-1]
        n_coord = place_next_atom(p1, p2, p3, BOND_C_N, ANGLE_CA_C_N, prev_psi)
        atoms.append({"name": "N", "resnum": resnum, "resname": resname, "coord": n_coord})
        
        # Place CA(i)
        # Dihedral omega(i-1) is always trans (180°)
        ca_coord = place_next_atom(p2, p3, n_coord, BOND_N_CA, ANGLE_C_N_CA, DIHEDRAL_OMEGA)
        atoms.append({"name": "CA", "resnum": resnum, "resname": resname, "coord": ca_coord})
        
        # Place C(i)
        # Dihedral phi(i)
        c_coord = place_next_atom(p3, n_coord, ca_coord, BOND_CA_C, ANGLE_N_CA_C, phi)
        atoms.append({"name": "C", "resnum": resnum, "resname": resname, "coord": c_coord})
        
    return atoms

def evaluate_conformation(sequence, secondary_structures, phi_angles, psi_angles):
    """
    Builds the coordinates and computes the hydrophobic compact score
    and checks for steric clashes.
    Returns: (score, has_clash, atoms)
    """
    atoms = build_backbone_coordinates(sequence, secondary_structures, phi_angles, psi_angles)
    
    # Extract CA coordinates
    ca_coords = [a["coord"] for a in atoms if a["name"] == "CA"]
    
    # Hydrophobic score (minimize sum of pairwise distances of non-polar residues)
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
                
    # Steric clash detection (CA-CA distance < 3.2 Å)
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
    """
    Optimizes the dihedral angles of loop residues to minimize the hydrophobic compact score
    without steric clashes.
    """
    n = len(sequence)
    # Start with default dihedrals
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
            
    # Find all loop indices
    loop_indices = [i for i in range(n) if secondary_structures[i] == 'C']
    
    # SFT rational loop angles candidates
    candidates = [
        (math.radians(-90.0), math.radians(120.0)),
        (math.radians(-60.0), math.radians(120.0)),
        (math.radians(-120.0), math.radians(150.0)),
        (math.radians(-90.0), math.radians(0.0)),
        (math.radians(-60.0), math.radians(90.0)),
        (math.radians(60.0), math.radians(60.0)),
    ]
    
    best_score, best_clash, best_atoms = evaluate_conformation(sequence, secondary_structures, phi_angles, psi_angles)
    
    # Greedy sweep over loops (2 iterations)
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
            
    # Run a final check on best parameters
    return best_atoms

def write_pdb(atoms, file_path):
    """Writes the generated coordinates into standard PDB format."""
    with open(file_path, "w") as f:
        f.write("HEADER    SFT PREDICTED STRUCTURE\n")
        atom_num = 1
        for a in atoms:
            x, y, z = a["coord"]
            resname = a["resname"]
            map_3letter = {
                'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
                'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
                'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
                'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
            }
            res_3 = map_3letter.get(resname, 'ALA')
            f.write(f"ATOM  {atom_num:5d}  {a['name']:<4s}{res_3} A{a['resnum']:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {a['name'][0]}\n")
            atom_num += 1
        f.write("END\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tools/predict_structure.py <sequence> <output.pdb>")
        print("Example (Ubiquitin first 20 residues):")
        print("  python3 tools/predict_structure.py MQIFVKTLTGKTITLEVEPS output.pdb")
        sys.exit(1)
        
    sequence = sys.argv[1].upper()
    output_path = sys.argv[2]
    
    print(f"Predicting 3D structure for sequence ({len(sequence)} residues):")
    print(f"Sequence: {sequence}")
    
    # 1. Predict secondary structure regions
    ss_states = predict_secondary_structure(sequence)
    print(f"Predicted SS: {''.join(ss_states)}")
    
    # 2. Build 3D coordinates using tertiary packing optimizer
    atoms = optimize_tertiary_packing(sequence, ss_states)
    
    # 3. Write PDB file
    write_pdb(atoms, output_path)
    print(f"Saved predicted 3D structure to: {output_path}")


if __name__ == "__main__":
    main()
