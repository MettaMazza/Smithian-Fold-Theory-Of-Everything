# After Turing: The Fold Machine - v1.0 release notes

## Release status

`PREPARED - NOT PUSHED - NOT DEPOSITED - NOT PUBLISHED`

Recommended Git tag: `after-turing-fold-machine-v1.0`  
Scientific author and publication authority: Maria Smith, Ernos Labs

## Result

This release publishes the complete declared Smithian Fold derivation of the mathematical sciences of classical and quantum computation. It synchronizes:

- Steps 325–407 and the 164-row fundamental-computation census;
- the 409-suite, 2,693-check, zero-failure main-corpus seal;
- 409 byte-identical source/generated-C certificate pairs;
- the portable `computational_lab/` release;
- twelve closed-law demonstrations and eight exact finite investigations;
- 25 standalone tests and 20 unfavorable controls;
- an independent 34-check C reproduction;
- the PDF-first paper, Markdown source and Zenodo metadata.

## Main files

- `papers/After_Turing_The_Fold_Machine.md`
- `output/pdf/After_Turing_The_Fold_Machine_v1.pdf`
- `FUNDAMENTAL_COMPUTATION_CENSUS.md`
- `computational_lab/`
- `verify/foundation_induction_multifault_401_403_receipt_20260723.md`
- `verify/unrestricted_computation_404_407_receipt_20260723.md`
- `publication/zenodo_after_turing_fold_machine_v1_metadata.json`
- `publication/after_turing_fold_machine_v1_manifest.json`

## Reproduction

```bash
./verify/prove_current_source_isolated.sh
cd computational_lab
./verify/run_all.sh
cd ..
python3 publication/verify_after_turing_release.py
```

Expected corpus result:

```text
CURRENT_SOURCE_COMPLETE suites=409 checks=2693 failures=0
CERTIFICATE_COMPARE identical=409 drifted=0 absent=0 total=409
```

Expected laboratory result:

```text
Ran 25 tests
OK
FOLD_LAB_COMPLETE theorems=12 finite=8 frontier=0 closed_frontiers=4 negative_controls=20 promoted=0
FOLD_LAB_C_CERTIFICATE checks=34 failures=0
FOLD_LAB_RECEIPT verified=1 authority_identical=1
AFTER_TURING_RELEASE_VERIFIED checksums=15 archive_members=347 focused_suites=83 focused_checks=691 certificates=83 lab_tests=25 c_checks=34 failures=0
```

## Scientific boundary

The closed results cover every declared census row. Fold uniqueness remains correctly conditional on the mechanically generated 84-form composition grammar through size three. Fault tolerance is exhaustive for separately registered `t=1,2,3` masks and is generalized by a necessity/sufficiency induction to the unique minimum width `2t+1` for every positive finite `t`. The native laws `BB_F(k)=k`, `P_F=NP_F`, and exact lawful-Fold-circuit lower bounds are closed in Steps 404–406. No conventional Turing-table, external complexity-class, arbitrary external gate-basis, or stochastic hardware theorem is inferred without a separate correspondence derivation.

Unison AI, Fold Chess, Fold Go and Fold Protein were not run for this release. Their translations are future-paper work and do not select these laws.

## Release procedure after explicit authorization

1. rerun the two reproduction commands;
2. verify the publication manifest and PDF rendering receipt;
3. commit only the reviewed release paths, preserving unrelated worktree changes;
4. push the authorized Git branch and tag;
5. create a new Zenodo article draft from the prepared metadata;
6. reserve its DOI, insert it into the paper, CFF and metadata, then rerender and
   reverify the PDF and all hashes;
7. upload the manifest-listed files with the finished PDF first;
8. save and preview the complete draft record;
9. publish only after Maria Smith's final explicit approval;
10. record the concept/version DOI, publication date and Git commit in the
    repository.

If publication occurs after 23 July 2026, update the prepared publication date
everywhere before the DOI-bearing render.
