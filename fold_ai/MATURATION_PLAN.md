# THE MATURATION PLAN — what the field found, taken as the fold

Registered 2026-07-06. Source: deep-research sweep (107 agents, 25 primary
sources fetched, 119 claims extracted, 25 adversarially verified 3-vote,
23 confirmed / 2 refuted). Every adopted item below is stated with its
verified source finding and its FOLD FORM — counted, forced, zero
parameters; gradient machinery is never imported, only the counted control
signals the papers themselves prove sufficient.

## THE HEADLINE FINDING — the field arrived at our architecture in Jan 2026

**DeepSeek Engram** (arXiv 2601.07372, official Apache-2.0 repo, verified
12-0): conditional memory as deterministically-addressed N-gram tables --
suffix N-grams hashed O(1) into prime-sized tables, no learned search --
formalized as a SECOND SPARSITY AXIS complementary to neural computation,
beating iso-FLOPs MoE at 27B (BBH +5.0, MMLU +3.4, HumanEval +3.0). Their
memory is locally editable where gradients are not: a table write is inert
off its trigger N-gram — **~33,000x less contamination than a per-user
LoRA** (+0.00005 vs +1.784 val bits/byte; single-author follow-up study,
verified verbatim, small scale). And making the lookup collision-free does
NOT help (null result, verified): cheap deterministic addressing is
already sufficient.

**The fold reading:** this is Unison's memory law, discovered from the
gradient side. Held orbits ARE deterministically-addressed exact N-gram
memory — except ours is the whole engine rather than a module bolted to a
trained backbone, and our cells hold exact counts, never learned vectors.
Their 33,000x local-edit result is the field independently measuring what
the corpus states as law: teaching costs one written record and cannot
poison the rest of memory. Their open question #2 — can counted control
signals drive PURE table-write updates with no gradient anywhere — is a
combination **no surviving source has tested. Unison is that experiment,
already running.**

## THE SECOND CONVERGENCE — their optimal curriculum sits at the fold's lock

**Self-Evolving Curriculum** (arXiv 2505.14970, verified 9-0) proves the
optimal training curriculum targets problems at success rate **p = 1/2**
(expected advantage 2·sqrt(p(1-p)), maximized at 1/2). **Absolute Zero**
(arXiv 2505.03335, verified 12-0) independently builds its self-play
curriculum on the same point: proposer reward r = 1 − r̄_solve, zero at
both extremes, maximal at the edge of ability. The field derived, twice,
that learning concentrates at the balanced point — **the fold's lock, 1/2,
the ground.** We do not import their gradient updaters; we take the
counted signal they proved optimal, which was already ours.

## THE ADOPTIONS (each: verified source mechanism → fold form)

**M1 — ZPD curriculum for the tutor (build next).** SEC's p=1/2 criterion,
counted. The tutor already keeps a per-territory win/loss tally
(graduation.tsv). Curriculum law: quiz territories whose tally sits
NEAREST wins/(wins+losses) = 1/2 — the live edge of ability — instead of
uniform sampling. Solved territories rest; hopeless ones wait for
teaching; the edge gets the attention. Zero knobs: the target is the lock.

**M2 — Absolute-Zero self-play (three counted modes, own verifiers).**
Their loop: propose task → solve → verify by deterministic executor, in
three enumerable modes (deduction: predict output; abduction: infer input;
induction: synthesize the rule). Fold form: Unison proposes its own tasks
over held knowledge and verifies them with its OWN deterministic ground —
exact_math (Fraction executor), the corpus prover relations, bind-recall
checks — no external labels, no gradient, learnability targeted at
solve-rate 1/2 per M1. This upgrades self-play from recall-drilling to
task-generation with verification.

**M3 — STaR-filtered reasoning retention.** STaR's verified core
(arXiv 2203.14465 + RL-STaR theory): keep only reasoning traces whose
final answer verifies; iterated filtering self-corrects. Fold form: the
observer's taught reasoning lines are held ONLY when their answer wins the
closure (y-confirmation, head-to-head win, or verifier pass); reasoning
attached to losing answers is discarded with them. The filter is a pure
count — answer verified or not — exactly as the paper states.

**M4 — Consolidation interleaving (the sleep law, XI-6).** Neuroscience
sweep (SCoRe, biorxiv 2025): the brain avoids catastrophic forgetting by
interleaving replay of NOVEL and FAMILIAR traces within each slow-wave
cycle. Fold form: each self-play batch drills a counted mix — half newest
lessons, half drawn from the oldest held — so consolidation braids new
into old instead of stacking. (Kanerva SDM's verified continual-learning
result — no replay, no task boundaries, from architecture alone — is the
same lesson our content-addressed store already embodies.)

**M5 — Engram-grade store bounding (infrastructure, at scale).** Their
prime-table hashed addressing bounds memory while keeping O(1) exact
lookup, and their null result proves cheap hashing loses nothing. Fold
form: when the orbit store outgrows RAM economics, bound it by hashed
addressing of context keys (exact counts kept per cell) rather than
pruning knowledge — the store stays O(1), exact, and boundable. Not
needed at current scale; registered for the flood.

**M6 — Already built, now independently validated.** Local-edit memory
(corrections/facts = addressed writes; their 33,000x result is our
mechanism measured), teacher-as-data-distillation (logit distillation is
gradient-bound and inapplicable — verified; the observer relay is its
counted replacement and is live), gradient-free updating as a first-class
lane (the self-evolution survey, verified 6-0, names external-memory
updating as a peer route to weight updates — the lane this engine occupies
alone at zero parameters).

## NOT COVERED (honest scope; follow-up research pass owed)

The verification pass confirmed nothing (not "found nothing") on: RLAIF
mechanics, weak-to-strong generalization, RAG/NTM/DNC internals, EWC,
process reward models, MCTS-guided reasoning, Mamba/state-space,
speculative decoding, JEPA/world models. A second sweep on the reasoning
cluster (PRMs, MCTS) is the priority follow-up: per-step closure of
reasoning (a y/n on each step, not just the answer) is the natural fold
form of a process reward model and would deepen M3.

## REFUTED IN VERIFICATION (never import these framings)

- "STaR corrects rationale-and-answer on failure" — mischaracterization
  (1-2); STaR FILTERS on correctness, it does not correct.
- "STaR cannot bootstrap from at-or-below-chance models" — refuted 0-3.

Build order: M1 → M3 (small deltas to live loops) → M4 → M2 (the big
upgrade) → M5 at need. Every item lands as counted selection or counted
retention over exact records; no item introduces a parameter.
