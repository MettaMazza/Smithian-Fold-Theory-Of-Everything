# Fold Computational Laboratory validation receipt

**Execution date:** 23 July 2026  
**Status:** PASSED — STANDALONE — AUTHORITY-LOCKED — MAIN-CORPUS CLOSURES SYNCHRONIZED

## Main-corpus authority seal

```text
CURRENT_SOURCE_COMPLETE suites=409 checks=2693 failures=0
CERTIFICATE_COMPARE identical=409 drifted=0 absent=0 total=409
ISOLATED_BUILD=/private/tmp/sft-current-source.lsQrgl
```

The standalone manifest verified fifteen frozen main-corpus sources, including Steps 404–407 and their receipt. All fifteen were present and byte-identical.

## Standalone execution

```text
FOLD_LAB_COMPLETE theorems=12 finite=8 frontier=0 closed_frontiers=4 negative_controls=20 promoted=0 run_hash=fa2cebf51ee6d7651b4f8f46e1533b1ffb91ef32862c845375fb6280f660c7fa
FOLD_LAB_C_CERTIFICATE checks=34 failures=0
FOLD_LAB_RECEIPT verified=1 authority_identical=1
```

The Python verification route executed 25 tests with zero failures. The separately compiled C certificate reproduced the closed numerical consequences and bounded-census results with 34 checks and zero failures.

## Evidence identities

| Artifact | SHA-256 |
|---|---|
| Authority manifest | `39ddcb85b0c57eff6ac621d67eac3712171e8c61913226442e73d6979a2b0abe` |
| Complete JSON evidence receipt | `38a0262a5a9194eb10c4d58c4679a1862caf5f8045d05b2069ed4df4f5ca6a7e` |
| Independent C source | `e3264c94ebb9c69a4bfa8910c0874983bf3536332bb0bf02da90099f325e12fa` |
| Compiled C certificate | `a4f6bef3bd66c74bb9fe5114fc6b2db861db9186cedf79f2d67b72406c204add` |
| Constitution | `52826d0204aa4d9e7a46b602d104c1eaecf6c7628ea770c3c661239d8c80f86c` |

## Scientific boundary

- The twelve theorem-class entries demonstrate consequences of already registered SFT laws; the program is not used to select those laws.
- The eight finite results are exact only within their declared generated spaces.
- Steps 404–407 close the native laws `BB_F(k)=k`, `P_F=NP_F`, exact lawful-Fold-circuit lower bounds, and minimum width `2t+1`; the laboratory records them as `CLOSED_BY_MAIN_CORPUS` and does not promote them from its finite investigations.
- Conventional Turing-table Busy Beaver, external-language P versus NP, arbitrary external gate bases, and stochastic physical-hardware thresholds remain outside the native comparison boundary.
- No code or data from the old Desktop `TuringBot`, Unison AI, Fold Chess, Fold Go, or Fold Protein was imported; none of those projects was modified or executed by this project.
- No external replication, self-modifying process, network operation, or pretrained model was used by the proof laboratory.
