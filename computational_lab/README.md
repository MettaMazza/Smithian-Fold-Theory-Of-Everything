# Fold Computational Laboratory

A standalone, proof-carrying showcase of the Smithian Fold Theory computational and quantum derivations. It is a new project and has no dependency on the old Desktop `TuringBot`.

## What is implemented

- Native Fold tape with `One` blank, two fibre labels, exact observation, substitution, counted motion, held reverse records, and per-transition certificates.
- Restrained autonomous execution with immutable actions, declared resource limits, full alternatives, proof-verified choices, and fail-closed behavior.
- One exact reversible/quantum execution model with complete word support, phase, interference, joint composition, controlled gates, measurement records, and multi-error recovery.
- Twelve closed-law demonstrations: halting, Entscheidungs boundary, incompleteness, computational-model correspondence, information/channel laws, reversibility cost, measurement, interference/entanglement, quantum error correction, consensus, internal self-reproduction, and Maxwell-style information accounting.
- Eight exact finite investigations: small native Busy Beaver, satisfiability, process-description minima, reversible circuit minima, quantum circuit minima, finite proof search, self-copy minima, and fault recovery.
- A six-obligation admission gate plus an immutable synchronization ledger recording that Steps 404–407 closed the four formerly native-frontier questions in the main corpus. The laboratory never promotes them itself.
- Tamper-evident JSON receipts and an independently compiled C certificate.

See [CONSTITUTION.md](CONSTITUTION.md) for the scientific and safety boundary.

## Run

From this directory:

```sh
python3 run_lab.py
python3 -m unittest discover -s tests -v
cc -std=c11 -Wall -Wextra -pedantic verify/fold_lab_certificate.c -o build/fold_lab_certificate
./build/fold_lab_certificate
```

The first command refuses to run if any frozen main-corpus authority hash differs. Its default evidence artifact is `receipts/latest.json`.

## Current exact boundaries

- Tape alphabet: both forced fibre labels.
- Theorem demonstrations: 12 registered-law instances, each with one negative control.
- Native Busy Beaver: every exact length-four word over the declared four-action grammar on the declared two-label tape.
- Satisfiability: all eight depth-three assignments for one declared two-clause instance.
- Process minima: all action words of lengths one through three in the declared grammar.
- Circuit minima: every declared circuit through depths three (reversible) and two (quantum), compared branch by branch.
- Proof-search descriptions: all words at depths one through four.
- Self-copy: every description at depths one through three.
- Fault recovery: every nonempty mask of weight at most `t`, for both labels, at `t=1,2,3`; 162 cases.

No finite result is presented as an unrestricted solution. The general native laws are authority-locked imports from the main corpus: `BB_F(k)=k`, `P_F=NP_F`, exact lawful-Fold-circuit lower bounds, and minimum finite-order fault width `2t+1`. No application translation is performed by this project.
