"""FOLD-AI DASHBOARD: the campaign's longitudinal ledger -- every rung's
verdicts and margins in one table (the analog of the chess summit
dashboard). Reads the rung result files. Usage: python3 dashboard.py"""
import os, re

FILES = [("Rung1 validated", "rung1_validated_results.txt"),
         ("Rung1 exploratory(SAE)", "rung1_results.txt"),
         ("Rung2 A component map", "rung2_map_results.txt"),
         ("Rung2 B+C pack/control", "rung2_bc_results.txt"),
         ("Rung2 D+E LLM/quant", "rung2_de_results.txt")]
print("%-24s %-10s %s" % ("rung", "verdicts", "headline margins"))
for name, f in FILES:
    if not os.path.exists(f):
        print("%-24s %-10s" % (name, "pending")); continue
    t = open(f).read()
    s = t.count("STRUCTURE"); n = t.count("null-level")
    margins = [float(m) for m in re.findall(r"(\d+\.\d+)x", t)]
    top = sorted(margins, reverse=True)[:3]
    print("%-24s %-10s top: %s" % (name, "%d/%d" % (s, s + n) if (s + n) else "-",
                                   " ".join("%.1fx" % m for m in top)))
