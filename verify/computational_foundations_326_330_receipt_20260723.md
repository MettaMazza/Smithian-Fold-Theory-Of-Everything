# Steps 326–330 Execution Receipt — Fold Computational Foundations

**Date:** 23 July 2026  
**Claims:** `SFT-COMP-OBS-326`, `SFT-COMP-RES-327`,
`SFT-COMP-ENC-328`, `SFT-COMP-INFO-329`, `SFT-COMP-MACHINE-330`  
**Status:** INTERNALLY CLOSED + EXECUTED + FINITE CENSUS

## Derivation boundary

No measured value, trained relation, application target, conventional machine,
external probability model, or imported mathematical answer is an input.  The
five derivations consume only the established Fold corpus and the Step 325 exact
state-transition law.  Conventional field names classify the resulting laws only
after derivation.

## Exact source and certificate identities

| Step | Derivation source SHA-256 | Test source SHA-256 | C certificate SHA-256 |
|---|---|---|---|
| 326 | `341dd5f094bb665e6a1d1f3d8cf6146ff81257fd694bdd2a36905ff7f4612c91` | `1745c8bf7ce0e1027f5927938cb488c79278a751d3db00b2c6cc531eb51ce6cb` | `55b3fde865f74cd7d4321b04c5218dc1185aa3e4d8cbcbad1f3e706964d46aa2` |
| 327 | `7ef5761a5ad3813f3c7f200c676c25ca491c88adf0126a3c7c9a0ac9da065a85` | `8054953b62d727c1a25aa346b285e0d03c54ddfef1b94c826219c7894a1c25c3` | `0c22d7c851c524a84e6eafa37d2fb95b87ca8a77b8ccdcf6e3ab8e623b012a9b` |
| 328 | `b79a96ecf532bb84cda409548dfe06aec42b213eb3b7195f01ed86485d338e89` | `741be21420746e243167112d2cef7436a94a10532287ae768a24b02bec5cea89` | `b3c88308395e70b9c4c86b20f37384d0172bec1c8f74deb4eba636827deb6bb1` |
| 329 | `cef818a681f3b24be576ae61d03fb958ef5a36d3abd70743411307b10f26110a` | `3259666c188e4684302a47a405389f1f69a24578673007ad03dc1bc9e9bbc6b7` | `38034883b635177e42ddb4b59cf0174d2b2144473b77391aecca676178d63b5e` |
| 330 | `0d33a914702396ad783be74f873fdf1918b7d178b8c80331708488e0902a5b4c` | `f02b3ef56451c336f85b0ada158f4d33eda76e28d775803493fe77ae67af597e` | `99f4cc4cb410f47816eaf6e730ae6ce778aa6158d779a1f07b50c74c22d3dc46` |

## Purpose-matched focused executions

Each test was compiled from current ErnosPlain source inside an isolated copy of
`foundation/`, `constants/`, and `data/`, then executed with `/usr/bin/time -l`.

| Step | Test | Checks | Failures | Real | User | System | Maximum RSS | Peak footprint |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 326 | `test_computational_observation` | 7 | 0 | 30.91 s | 30.39 s | 0.05 s | 10,207,232 B | 9,962,432 B |
| 327 | `test_computational_resources` | 9 | 0 | 0.94 s | 0.73 s | 0.00 s | 5,292,032 B | 5,030,848 B |
| 328 | `test_computational_encoding` | 9 | 0 | 0.48 s | 0.24 s | 0.00 s | 4,489,216 B | 4,145,920 B |
| 329 | `test_computational_information` | 13 | 0 | 1.17 s | 0.94 s | 0.00 s | 5,799,936 B | 5,555,328 B |
| 330 | `test_computational_process_machine` | 12 | 0 | 12.99 s | 12.73 s | 0.02 s | 9,027,584 B | 8,700,672 B |

Focused total: **50 checks, zero failures**.

## Executed coverage

- **Observation:** every source state and every image class at depths 1–7;
  exact binary fibre membership, retained classes, and complete partitions.
- **Resources:** every depth 1–7 and every intermediate observation count;
  state space, walked time, closing paths, retained distinctions, and closed
  histories.
- **Encoding:** every one of the 254 states across depths 1–7; lawful alphabet,
  exact encode/decode round trips, observed suffixes, and redundancy.
- **Information:** every depth and every intermediate observation count; exact
  quantity/multiplicity, branch partition, measurement-weight bridge,
  uncertainty bridge, dyadic loss, and periodic retention.
- **Process/machine:** every dyadic state and every process split through depth 7;
  transition totality, single-valued execution, unique terminal, termination,
  composition/decomposition, and the complete period-b recurrent machine.

## Unfavorable controls

The focused executions reject:

- singleton observation fibres and shifted observation targets;
- shortened closure time and nonbinary history growth;
- out-of-alphabet symbols and changed-symbol identity;
- perturbed information accounting and incomplete-cycle identity;
- false period-one recurrence and an extra terminal state.

All rejection controls passed.  No unfavorable row was omitted from the receipt.

## Independent C-certificate executions

Each generated certificate was compiled independently with `cc -O2` and executed:

```text
test_computational_observation      rc=0 checks=7  fail_lines=0
test_computational_resources        rc=0 checks=9  fail_lines=0
test_computational_encoding         rc=0 checks=9  fail_lines=0
test_computational_information      rc=0 checks=13 fail_lines=0
test_computational_process_machine  rc=0 checks=12 fail_lines=0
```

## Complete corpus gate

Command:

```text
./verify/prove_current_source_isolated.sh
```

Final output:

```text
CURRENT_SOURCE_COMPLETE suites=332 checks=2059 failures=0
CERTIFICATE_COMPARE identical=332 drifted=0 absent=0 total=332
ISOLATED_BUILD=/private/tmp/sft-current-source.Q0xniS
```
