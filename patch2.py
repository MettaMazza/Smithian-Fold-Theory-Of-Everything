import sys, math

def modify_predict():
    with open("tools/predict_structure.py") as f:
        content = f.read()
    
    # We will redefine generate_from_empirical to use the tertiary packing optimizer 
    # instead of just building the backbone without optimization.
    new_func = """
def generate_from_empirical(sequence, exp_pdb_path):
    with open(exp_pdb_path) as f:
        content = f.read()
        
    residues = parse_pdb_backbone(content)
    angles = analyze_backbone_angles(residues)
    
    ss_states = []
    
    for i in range(len(sequence)):
        if i < len(angles):
            phi, psi = angles[i]["phi"], angles[i]["psi"]
            if phi is None or psi is None:
                ss_states.append('C')
                continue
                
            # Classify as H, E, or C based on proximity to SFT candidates
            diff_alpha_phi = abs((phi + 180) % 360 - 180 - (-60.0))
            diff_alpha_psi = abs((psi + 180) % 360 - 180 - (-45.0))
            
            diff_beta_phi = abs((phi + 180) % 360 - 180 - (-120.0))
            diff_beta_psi = abs((psi + 180) % 360 - 180 - (135.0))
            
            if diff_alpha_phi < 25.0 and diff_alpha_psi < 25.0:
                ss_states.append('H')
            elif diff_beta_phi < 35.0 and diff_beta_psi < 35.0:
                ss_states.append('E')
            else:
                ss_states.append('C')
        else:
            ss_states.append('C')
            
    print(f"Empirical SS: {''.join(ss_states)}")
    atoms = optimize_tertiary_packing(sequence, ss_states)
    return atoms
"""
    # Replace the generate_from_empirical function
    start = content.find("def generate_from_empirical")
    end = content.find("def main():")
    final = content[:start] + new_func + content[end:]
    
    with open("tools/predict_structure.py", "w") as f:
        f.write(final)

modify_predict()
