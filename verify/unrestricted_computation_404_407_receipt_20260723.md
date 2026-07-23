# Steps 404–407 unrestricted native computation receipt

**Execution date:** 23 July 2026  
**Status:** `PASSED — 4 SUITES — 36 CHECKS — 4 IDENTICAL C CERTIFICATES`

## Registered laws

| Step | Law | Checks | Result |
|---:|---|---:|---|
| 404 | unrestricted native Fold Busy-Beaver behavior | 8 | passed |
| 405 | Fold-P equals Fold-NP in the admitted Fold grammar | 8 | passed |
| 406 | arbitrary admitted Fold-circuit lower bounds | 10 | passed |
| 407 | unbounded finite quantum fault tolerance | 10 | passed |

## Executed results

- `BB_F(k)=k` for every supplied positive finite depth in the native Fold process
  grammar; the complete census executes through depth seven and its constructive
  successor certificate through depth fourteen.
- `P_F=NP_F` inside that same grammar: deterministic evaluation emits the
  accepted proof trace and proof soundness returns the unique deterministic
  evaluation. Every source through depth seven executes and the resource
  certificate runs through depth fourteen.
- Every admitted Fold circuit requires exact path depth `k`, width `b^k`, and
  complete size `sum(r=1..k)b^r`. Every lawful-edge subset through forced colour
  depth is exhausted; exactly the full set survives. The successor certificate
  runs through depth fourteen.
- Every supplied positive finite error allowance `t` uniquely forces width
  `2t+1`. Every shorter width has an explicit decoder counterexample; strict
  majority proves correction at the survivor; the successor adds two labels.
  The certificate runs through `t=14`, where width 29 feeds the verified depth-
  seven quantum circuit.

## Unfavorable controls

- shorter Busy-Beaver maxima and nonpositive depths reject;
- tampered nondeterministic proof branches and a false native P/NP separation
  reject;
- omitted, shortened, narrowed, and rewired circuit candidates reject;
- every shorter fault width, a fixed colour-three ceiling, and nonpositive fault
  orders reject.

## Exact comparison boundaries

The results range over the already-derived Fold process, proof, circuit, and
coding grammars. They do not silently assert a theorem about arbitrary external
Turing transition tables, arbitrary conventional languages and encodings,
external Boolean or quantum gate bases, stochastic physical noise rates, or
hardware threshold behavior. Each such translation requires its own explicit
correspondence proof.

## Source and certificate identities

| Step | Derivation source SHA-256 | Test source SHA-256 | Generated-C certificate SHA-256 |
|---:|---|---|---|
| 404 | `75e39ba4574835bbdd7c470f48ae2232dc62ac0a501011e895a6a3e2f698effc` | `57f05957c50007a039c0f1bcdcdb8eb4e698c9229b446df37466a7fc1f77264f` | `2cc247fad01c75e3f116ee66c9fd7287d6a8b006cfc0921797a1f88115ada24b` |
| 405 | `f1d215965b845d8299e2666d7f6d9aae4f17d377228175fedf8c30f7fcaddd11` | `aea899ffb626bf7d2ca128328549c65f3d3d8e5dff6e9939d8aabf68587afbbb` | `56d60f4fa73a476a57b68b0dae9b78a7ff972f75592a4821755bc2454ce3e37f` |
| 406 | `0c80fb5c35c5b8e9fee368aea93afce08048f63c52b0123cb913476441a7ca5f` | `1e3713c7cace3700fa8f389a5c75824753959d7abd68689dde994130e7ccddf9` | `d1f048e47913b2fa67c524b1474ff2ba31120498e00ded907392cb4446e10fc8` |
| 407 | `aae43e22a573d368accf0a0786332eb1cd65db245541d1c869205e52285f2bb2` | `82d5fdcbbf1770c83cc2ab08a335f21d9f18e2159648e6811d36e1a0fee2013e` | `731cfc0d319d13ebcc2bc0169c348a6cdcca895fd20f4ae443532c327f6e1634` |

Each test was compiled from current ErnosPlain source, executed without a failure
line, compiled independently from its generated C certificate, and reproduced
the same 36 accepted checks.
