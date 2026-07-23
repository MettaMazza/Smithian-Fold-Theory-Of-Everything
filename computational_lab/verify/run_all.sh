#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_dir"
mkdir -p build

python3 -m unittest discover -s tests -v
python3 run_lab.py
cc -std=c11 -Wall -Wextra -pedantic verify/fold_lab_certificate.c -o build/fold_lab_certificate
./build/fold_lab_certificate

python3 - <<'PY'
import json
from pathlib import Path
from sft_lab.receipt import verify_run_hash

receipt = json.loads(Path("receipts/latest.json").read_text())
if not verify_run_hash(receipt):
    raise SystemExit("receipt hash verification failed")
print("FOLD_LAB_RECEIPT verified=1 authority_identical=1")
PY
