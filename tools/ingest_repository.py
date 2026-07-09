#!/usr/bin/env python3
"""
SFT Ingestion Engine
Extracts clean prose from all .ep and .md files in the repository and
saves them into the diet/ directory to bake the Smithian Fold Theory
directly into Unison's memory graph.
"""
import os
import re

BASE = "/Users/mettamazza/Desktop/Smithian Fold Theory"
DIET_FILE = BASE + "/fold_ai/diet/gb_sft_corpus.txt"

def clean_prose(text):
    # Remove markdown links, code blocks, backticks, bolding
    text = re.sub(r"\[([^\]]+)\]\(file://[^\)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"```[a-z]*\n(.*?)\n```", r"\1", text, flags=re.S)
    text = text.replace("`", "")
    text = text.replace("**", "")
    text = text.replace("###", "").replace("##", "").replace("#", "")
    return text

def parse_ep_file(file_path):
    prose_lines = []
    with open(file_path, errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                # Strip # and comments
                cleaned = line.lstrip("#").strip()
                if cleaned and not cleaned.startswith("===") and not cleaned.startswith("---"):
                    prose_lines.append(cleaned)
            elif line.startswith("define"):
                # Convert definition to prose
                words = line.split()
                name = words[1].replace("_", " ")
                prose_lines.append(f"Define {name} in the fold.")
    return " ".join(prose_lines)

def parse_md_file(file_path):
    with open(file_path, errors="ignore") as f:
        content = f.read()
    return clean_prose(content)

def main():
    print("=== Ingesting SFT Repository Corpus into Diet ===")
    
    all_prose = []
    exclude_dirs = {".git", "diet", "node_modules", "verify", ".gemini", "backups", "scratchpad"}
    
    for root, dirs, files in os.walk(BASE):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]
        
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".ep"):
                print(f"Parsing EP: {os.path.basename(file)}")
                prose = parse_ep_file(file_path)
                if prose:
                    all_prose.append(prose)
            elif file.endswith(".md") and not file.startswith("task.md") and not file.startswith("walkthrough.md"):
                print(f"Parsing MD: {os.path.basename(file)}")
                prose = parse_md_file(file_path)
                if prose:
                    all_prose.append(prose)
                    
    # Write to diet
    os.makedirs(os.path.dirname(DIET_FILE), exist_ok=True)
    full_text = "\n\n".join(all_prose)
    
    with open(DIET_FILE, "w") as f:
        f.write(full_text)
        
    print(f"\nSuccessfully wrote SFT corpus ({len(full_text)//1000} KB) to {DIET_FILE}")

if __name__ == "__main__":
    main()
