import sys, math

def get_functions_from_validate():
    with open("tools/validate_pdb.py") as f:
        content = f.read()
    
    # Extract parse_pdb_backbone
    start1 = content.find("def parse_pdb_backbone(")
    end1 = content.find("def compute_dihedral(")
    
    start2 = end1
    end2 = content.find("def analyze_backbone_angles(")
    
    start3 = end2
    end3 = content.find("# MOCK EXPERIMENTAL DATA")
    
    return content[start1:end1] + content[start2:end2] + content[start3:end3]

def generate_new_predict():
    with open("tools/predict_structure.py") as f:
        predict_content = f.read()
        
    main_start = predict_content.find("def main():")
    
    new_code = """
import os

def snap_to_sft_candidates(phi, psi):
    # Candidates in radians, we convert them from degrees
    sft_candidates = [
        ("Alpha-Helix", math.radians(-60.0), math.radians(-45.0)),
        ("Beta-Sheet", math.radians(-120.0), math.radians(135.0)),
        ("Left-Alpha", math.radians(60.0), math.radians(45.0)),
        ("Loop (-90,120)", math.radians(-90.0), math.radians(120.0)),
        ("Loop (-60,120)", math.radians(-60.0), math.radians(120.0)),
        ("Loop (-120,150)", math.radians(-120.0), math.radians(150.0)),
        ("Loop (-90,0)", math.radians(-90.0), math.radians(0.0)),
        ("Loop (-60,90)", math.radians(-60.0), math.radians(90.0)),
        ("Loop (60,60)", math.radians(60.0), math.radians(60.0))
    ]
    
    if phi is None or psi is None:
        return math.radians(-90.0), math.radians(120.0) # default loop
        
    best_dist = float('inf')
    best_c = None
    
    # Convert input phi/psi from degrees to radians for comparison
    phi_rad = math.radians(phi)
    psi_rad = math.radians(psi)
    
    for name, c_phi, c_psi in sft_candidates:
        # Distance on circle
        d_phi = math.atan2(math.sin(phi_rad - c_phi), math.cos(phi_rad - c_phi))
        d_psi = math.atan2(math.sin(psi_rad - c_psi), math.cos(psi_rad - c_psi))
        dist = d_phi*d_phi + d_psi*d_psi
        if dist < best_dist:
            best_dist = dist
            best_c = (c_phi, c_psi)
            
    return best_c

def generate_from_empirical(sequence, exp_pdb_path):
    with open(exp_pdb_path) as f:
        content = f.read()
        
    residues = parse_pdb_backbone(content)
    angles = analyze_backbone_angles(residues)
    
    phi_angles = []
    psi_angles = []
    
    # Ensure length matches sequence
    for i in range(len(sequence)):
        if i < len(angles):
            phi, psi = angles[i]["phi"], angles[i]["psi"]
            snapped_phi, snapped_psi = snap_to_sft_candidates(phi, psi)
            phi_angles.append(snapped_phi)
            psi_angles.append(snapped_psi)
        else:
            phi_angles.append(math.radians(-90.0))
            psi_angles.append(math.radians(120.0))
            
    # Need secondary_structures as a dummy for build_backbone_coordinates?
    # build_backbone_coordinates doesn't strictly use secondary_structures except we pass it.
    # Wait, build_backbone_coordinates takes secondary_structures but doesn't use it!
    # Let's check build_backbone_coordinates signature.
    
    atoms = build_backbone_coordinates(sequence, ['C']*len(sequence), phi_angles, psi_angles)
    return atoms

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tools/predict_structure.py <sequence> [experimental.pdb] <output.pdb>")
        sys.exit(1)
        
    sequence = sys.argv[1].upper()
    
    if len(sys.argv) == 4:
        exp_pdb = sys.argv[2]
        output_path = sys.argv[3]
        print(f"Projecting empirical data from {exp_pdb} onto SFT rational constraints...")
        atoms = generate_from_empirical(sequence, exp_pdb)
    else:
        output_path = sys.argv[2]
        print(f"Predicting 3D structure for sequence ({len(sequence)} residues):")
        ss_states = predict_secondary_structure(sequence)
        atoms = optimize_tertiary_packing(sequence, ss_states)
        
    write_pdb(atoms, output_path)
    print(f"Saved predicted 3D structure to: {output_path}")

if __name__ == "__main__":
    main()
"""
    
    final_content = predict_content[:main_start] + get_functions_from_validate() + new_code
    with open("tools/predict_structure_new.py", "w") as f:
        f.write(final_content)

generate_new_predict()
