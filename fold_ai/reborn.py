#!/usr/bin/env python3
"""THE REBORN (run 5) -- the controlled fresh slate, run by hand, once.

Maria's mandate (2026-07-08): the prior runs' data was gained under
uncontrolled conditions (pre-schema code, harness pollution, and a
scoreboard that survived the last reset and mixed runs) -- not a
scientific baseline. Run 5 is born INTO the subject-and-graph schema:
every datum from minute zero carries a speaker and a graph node.

What it does, in order:
  1. REFUSES to run while the flight is alive (the pgrep law).
  2. Backs up everything it will touch to backups/pre_reborn_<stamp>.tar.gz.
  3. Clears ALL learned data -- INCLUDING graduation.tsv, judges.tsv and
     traces.tsv, the survivors of the last reset (commit a84d4f5) that
     left run 4's scoreboard mixed with run 3's.
  4. KEEPS: store.pkl / store.bound (the LIBRARY -- read books carry no
     user provenance; pass --library to clear them too), diet/, backups/,
     benchmarks*.tsv (instrument rows, timestamped), the code.
  5. NO migration -- tainted provenance is left in the backup, period.

First wake after this performs graph genesis (roots + primordial mesh +
library nodes) and registers the operator's seat.
"""
import glob, os, subprocess, sys, tarfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# 1. the pgrep law: never touch a living flight
if subprocess.run(["pgrep", "-f", "unison_chat.py"], capture_output=True).stdout.strip():
    sys.exit("REFUSED: the flight is alive (unison_chat.py running). Land it first.")

CLEAR = sorted(
    glob.glob("lessons/*.tsv") + glob.glob("lessons/*.txt")
    + glob.glob("sounds/*.npz") + glob.glob("sounds/index.tsv")
)
if "--library" in sys.argv:
    CLEAR += [f for f in ("store.pkl", "store.bound") if os.path.exists(f)]

# 2. the backup: everything touched, plus the log archives, in one tar
stamp = time.strftime("%Y%m%d-%H%M%S")
os.makedirs("backups", exist_ok=True)
tar_path = "backups/pre_reborn_" + stamp + ".tar.gz"
with tarfile.open(tar_path, "w:gz") as tar:
    for f in CLEAR + sorted(glob.glob("logs/archive/*.log")) + sorted(glob.glob("benchmarks*.tsv")):
        if os.path.exists(f):
            tar.add(f)
print("backup:", tar_path, f"({os.path.getsize(tar_path)//1024} KB, {len(CLEAR)} files to clear)")

# 3. the clear -- learned data only; the code and the library stand
for f in CLEAR:
    os.unlink(f)
    print("cleared:", f)

print("\nREBORN complete. Next wake is run 5: graph genesis + the operator's"
      "\nseat; every datum from minute zero carries a subject and a node.")
