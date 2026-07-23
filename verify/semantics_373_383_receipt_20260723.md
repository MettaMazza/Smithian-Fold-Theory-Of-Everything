# Steps 373–383 Execution Receipt — Fold Semantics and Program Theory

**Date:** 23 July 2026
**Status:** INTERNALLY CLOSED + EXECUTED + FINITE CENSUS

## Boundary

These laws consume only closed Fold syntax, transition, algorithms, computability,
and complexity. Conventional language semantics, variable environments, type
systems, compiler targets, and proof calculi do not enter as premises. Every
admitted word, prefix, residual type, specification, transformation, compiled
trace, and proof is exhausted through forced depth seven. No new assembled
constant is asserted.

## Identities

| Step | Source SHA-256 | Test SHA-256 | Certificate SHA-256 |
|---|---|---|---|
| 373 | `3ab43d5243d5d4d6ee0f626c7ad4fa9d745e0bd4902ef14624c62c071c07a40c` | `47a614142604ee4d197aaf73f53745e0266ec1e684e044cb7e2ff38b76a4bad1` | `d6f79ed2d45452b374a57ce86b4ebefd0a062bd625a1765f9caf82274fddc3ff` |
| 374 | `5f50dd712556e58414941863f280a5d71e2a5a1f8553130579d5aac53cf5ab74` | `5c271ca5e0cd61ba3490efc8e7e992099ea0d2add92d495b8c5547bd11eba699` | `080a927a7584cf0834c0929f9d17203013b89f2303734c026c080a0bbe870566` |
| 375 | `4969fece08242e7218035ce2615376fbbba5b391f502084c29487465858bf189` | `eb4eb687501cca984153701fc7d7bb06ef3970a11f8e4ad5392ccbe09c5a9c19` | `0141ca17038a352495b87071c4e7d0da3a87b11128dcf118d2b5e0c380207682` |
| 376 | `f588cfc806f3d41a4b7266d1f5b108899f01c2855e1bc8bb36c3f7005677756c` | `e88184ba9660d8347957478f585017ccec4b9c6b08cbff330de8e10503ee2334` | `699580d012dd593b193d4f39d39377cbecbee6d6fe6c178076d5ddbb383e6051` |
| 377 | `2805a4b75592fd67a454c050bfc205359291d30b1b1e6f2ccf734f316aed1599` | `76865c8a8a53e52071bf69fd173b2a130e01e315cfa8474fd4139306de477b65` | `36b02852dedd67aa2494c59e99a4b600597730241134eefced2e8271e78b8785` |
| 378 | `26f0ce17a4e84cf9fd24910631a2835ceee0f0f0e88285d3a697f85d63c8053c` | `3ee6f99bbcbb722838adf4ccccc6f8af87019536ba7d2242c9413eeb2862d3fc` | `e3220737e86f772fedd12efe379bd60a220f17b99202661b09ad5d720a85261e` |
| 379 | `6399fcb3a94c6a8d9678167882f15034df6a85c6b5f9a6fa0f073cf3dc29d1fa` | `a008b03ec37377c9b257e6e7b58454c74a293c1ee10560ad1c4b0550b42deb98` | `94e02538ac321a6a74129134d02d584650edb6fae2ff414da790c5df6206150e` |
| 380 | `8cb8336fae53cffc0f50d07d08f3e5a846f8c31949bc7507975aeb1bc7a25443` | `db19640e646abd56fc0e05b1e8e953603341089f8a7fae1a52f879d6d8411899` | `0762b84c24cb268ca2e47c5d18e932d3b81efcb6e644fda8bf28f0dd41590313` |
| 381 | `32eb7556f85a6a5576df2c08e42d9cf95786768bbfd1476f1be7992538d9a05d` | `1a44c562d0310c183317c14fcbd5e68e3a4010815d1c044a911c0a1beee6a3c9` | `c34dcf7306f7d43579315a4a29c5e35730d307a6ac14fb9c845c1270c787d384` |
| 382 | `f5f940199fc325c8d81b623e4ef9205f8eeed40996d9969515837038a05547da` | `7d0c800ebbf3328e43e6abcd0c61ea8083a16e891db051d06f2a74d4f90a3162` | `2db5016796c228fe98abd82061b12fc6113ac61c95e9bb69a65be8a0a04fd841` |
| 383 | `dd9504483b2475fc8ce47718b91c31cb0715ea970a4f62aa66453b4234ed7a7d` | `95dc6d832154589b24d119112c8d8d9224029ed48472868a0c980ff8640f30ad` | `cccfce42fde4e91d346bd29025a20e2ef17bd062daa757f6d166e5ca619057f0` |

## Focused execution

| Step | Checks | Failures | Real | Maximum RSS |
|---|---:|---:|---:|---:|
| 373 | 6 | 0 | 0.16 s | 1,720,320 B |
| 374 | 7 | 0 | 0.14 s | 1,769,472 B |
| 375 | 6 | 0 | 2.27 s | 4,308,992 B |
| 376 | 6 | 0 | 0.44 s | 2,473,984 B |
| 377 | 7 | 0 | 0.16 s | 1,736,704 B |
| 378 | 5 | 0 | 0.24 s | 1,835,008 B |
| 379 | 6 | 0 | 0.16 s | 1,753,088 B |
| 380 | 5 | 0 | 0.74 s | 2,703,360 B |
| 381 | 6 | 0 | 0.20 s | 2,228,224 B |
| 382 | 7 | 0 | 0.16 s | 1,720,320 B |
| 383 | 5 | 0 | 0.18 s | 1,703,936 B |

Focused total: **66 checks, zero failures**. All 11 generated certificates were
also compiled independently with `cc -O2`, executed, and returned their identical
check counts with zero failure lines.

Unfavorable controls reject outside/overlong syntax, changed bindings, overlong
evaluation, shifted denotations, wrong/untyped terms, changed program meanings,
premature termination, false postconditions, changed specification type/resource,
changed transformations, shortened/tampered compiled traces, false proof claims,
and tampered proof edges.

## Complete corpus gate

```text
CURRENT_SOURCE_COMPLETE suites=385 checks=2442 failures=0
CERTIFICATE_COMPARE identical=385 drifted=0 absent=0 total=385
ISOLATED_BUILD=/private/tmp/sft-current-source.hqtnxs
```
