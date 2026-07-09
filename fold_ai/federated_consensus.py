#!/usr/bin/env python3
"""
SFT Federated Hebbian Mesh Consensus
Decentralized consensus tool that merges the learned files, corrections, and facts
of multiple UnisonAI instances using deterministic rational matching.
"""
import sys
import os

def parse_tsv_mesh(file_path):
    mesh = {}
    if not os.path.exists(file_path):
        return mesh
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                key, val = parts[0], parts[1]
                mesh[key] = val
    return mesh

def write_tsv_mesh(mesh, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        for key in sorted(mesh.keys()):
            f.write(f"{key}\t{mesh[key]}\n")

def merge_meshes(mesh_a, mesh_b):
    merged = dict(mesh_a)
    for key, val in mesh_b.items():
        if key in merged:
            # Deterministic conflict resolution (zero parameters)
            # Choose the longer answer (more information content) or alphabetically first as tie-breaker
            val_a = merged[key]
            if len(val) > len(val_a):
                merged[key] = val
            elif len(val) == len(val_a):
                if val < val_a:
                    merged[key] = val
        else:
            merged[key] = val
    return merged

def merge_lessons(dir_a, dir_b, output_dir):
    files = ["facts.tsv", "corrections.tsv", "graduation.tsv"]
    for fn in files:
        path_a = os.path.join(dir_a, "lessons", fn)
        path_b = os.path.join(dir_b, "lessons", fn)
        path_out = os.path.join(output_dir, "lessons", fn)
        
        mesh_a = parse_tsv_mesh(path_a)
        mesh_b = parse_tsv_mesh(path_b)
        
        merged = merge_meshes(mesh_a, mesh_b)
        write_tsv_mesh(merged, path_out)
        print(f"Merged {fn}: {len(mesh_a)} keys + {len(mesh_b)} keys -> {len(merged)} keys")

def verify_consensus():
    print("=== SFT Federated Consensus Verification ===")
    test_dir = "/Users/mettamazza/Desktop/Smithian Fold Theory/verify/federated_test"
    dir_a = os.path.join(test_dir, "instance_a")
    dir_b = os.path.join(test_dir, "instance_b")
    dir_out = os.path.join(test_dir, "merged")
    
    # Write mock files for instance A
    os.makedirs(os.path.join(dir_a, "lessons"), exist_ok=True)
    with open(os.path.join(dir_a, "lessons", "facts.tsv"), "w") as f:
        f.write("Q: SFT\tA: Smithian Fold Theory is parameter-free.\n")
        f.write("Q: Capital\tA: The capital is the One.\n")
        
    # Write mock files for instance B (contains overlap and a conflict)
    os.makedirs(os.path.join(dir_b, "lessons"), exist_ok=True)
    with open(os.path.join(dir_b, "lessons", "facts.tsv"), "w") as f:
        f.write("Q: SFT\tA: Smithian Fold Theory is parameter-free and derived from first-principles.\n") # conflict (B is longer)
        f.write("Q: Observer\tA: The observer watches the fold.\n") # new key
        
    merge_lessons(dir_a, dir_b, dir_out)
    
    # Read back merged facts
    merged = parse_tsv_mesh(os.path.join(dir_out, "lessons", "facts.tsv"))
    print("Merged keys: ", list(merged.keys()))
    
    # Assertions
    check_keys = sorted(list(merged.keys())) == ["Q: Capital", "Q: Observer", "Q: SFT"]
    check_conflict = "derived from first-principles" in merged["Q: SFT"]
    
    if check_keys and check_conflict:
        print("Consensus Verification Status: PASS")
        # Cleanup
        for root, dirs, files in os.walk(test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(test_dir)
        sys.exit(0)
    else:
        print("Consensus Verification Status: FAIL")
        sys.exit(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_consensus()
    elif len(sys.argv) >= 4:
        merge_lessons(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python3 fold_ai/federated_consensus.py <dir_a> <dir_b> <output_dir>")
        print("  or:  python3 fold_ai/federated_consensus.py --verify")

if __name__ == "__main__":
    main()
