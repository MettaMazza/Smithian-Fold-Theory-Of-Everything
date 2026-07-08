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

**M1 — ZPD curriculum for the tutor. BUILT + VERIFIED 2026-07-06.** SEC's p=1/2 criterion,
counted. The tutor already keeps a per-territory win/loss tally
(graduation.tsv). Curriculum law: quiz territories whose tally sits
NEAREST wins/(wins+losses) = 1/2 — the live edge of ability — instead of
uniform sampling. Solved territories rest; hopeless ones wait for
teaching; the edge gets the attention. Zero knobs: the target is the lock.

**M2 — Absolute-Zero self-play (three counted modes, own verifiers). BUILT + VERIFIED 2026-07-06 (v1: deduction/abduction/induction rotating over the store's own ground).**
Their loop: propose task → solve → verify by deterministic executor, in
three enumerable modes (deduction: predict output; abduction: infer input;
induction: synthesize the rule). Fold form: Unison proposes its own tasks
over held knowledge and verifies them with its OWN deterministic ground —
exact_math (Fraction executor), the corpus prover relations, bind-recall
checks — no external labels, no gradient, learnability targeted at
solve-rate 1/2 per M1. This upgrades self-play from recall-drilling to
task-generation with verification.

**M3 — STaR-filtered reasoning retention. BUILT + VERIFIED 2026-07-06 (both directions: held on closure, discarded with a rejected answer).** STaR's verified core
(arXiv 2203.14465 + RL-STaR theory): keep only reasoning traces whose
final answer verifies; iterated filtering self-corrects. Fold form: the
observer's taught reasoning lines are held ONLY when their answer wins the
closure (y-confirmation, head-to-head win, or verifier pass); reasoning
attached to losing answers is discarded with them. The filter is a pure
count — answer verified or not — exactly as the paper states.

**M4 — Consolidation interleaving (the sleep law, XI-6). BUILT + VERIFIED 2026-07-06 (newest/oldest braid, counted).** Neuroscience
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

## THE FORCING PASS — DONE 2026-07-06

Every model quantity in the engine now traces to the generators and halts
on mismatch (`_forced`, the corpus's forced_to_be / ep_exit discipline;
halt proven live on a fitted value): binary 2 and colour 3 computed FORWARD
(colour as the tripling-fold preimage count, the verify_colour_prediction
construction); context depth 6 = their product; bind lock 1/3 = the XI-1
memory-cycle share; kin floor 1/6 = one part in the generators' product;
compose floor 1/12 = the kin floor at the ground; sight coefficients
32 = 2^5 with 5 the computed minimal binary cover of 27 (the N8b law);
kin breadth = colour; every repetition count = a generator; the
informativeness cutoff = one part in a thousand of the counted mass, one
rule used everywhere. Interface/IO bounds (buffer lengths, string caps,
timeouts) are marked as hardware facts where they occur; they are not
model quantities. Harness 9/9 through the entire pass.

## THE SECOND SWEEP (PRM / MCTS / step-verification) — EXTRACTED, NOT YET VERIFIED

Run 2026-07-06 (105 agents): search and extraction succeeded; the
adversarial verification stage was rate-limited and EVERY claim is
therefore UNVERIFIED — nothing below may be imported as verified fact
until the re-run. Notable extractions (primary-source quotes fetched,
awaiting the 3-vote panel): rStar (openreview 6aHUmotXaw) — MCTS reasoning
with NO fine-tuning anywhere; rewards are self-consistency VOTE COUNTS and
UCT VISIT STATISTICS (pure counts, directly fold-portable); implicit PRMs
(arXiv 2412.01981) — step-level rewards obtained free from outcome-only
labels; PRM-guided best-of-N reranking is gradient-free at inference
(arXiv 2510.08049). Registered as candidate M7 (counted step-closure and
vote-guided reasoning) PENDING verification. The refuted/confirmed split
comes when the panel re-runs.

## THE STRENGTHENING SIX — EXECUTED 2026-07-07

The standing review named two open flanks (the word-scale gate; judge
dependence) and four force-multipliers. All six landed this day; every
number below is from a committed results file, negative results stated
as plainly as positive ones.

1. **The word-scale rematch (`rung5b_rematch.py`)** — today's engine
   (depth 6 + the Gutenberg flood), same registered arena, twin
   RETRAINED on today's text (the corpus is a living document — June's
   twin CE was earned on different text and may not face today's
   engine). Substrate pinned: both rung scripts read the frozen
   snapshot `store_rung5_snapshot.pkl` (the live store grows under the
   flight's rebuild loop). RESULT, no spin: fold 4.7244 vs twin mean
   3.4853 — the twin still leads by 1.2391 nats, and the DECOMPOSITION
   shows both deltas cost at corpus-CE (depth-6 no-flood 4.5813 vs the
   newborn's 4.5071; the flood adds English mass that dilutes
   theory-text prediction at shallow depths). The gap is real, measured,
   and became rung 5d's target.
2. **Rung 5d, the transfer-in (`rung5d_transfer.py`) — SUPPORTED, the
   flagship.** The constructive converse of 5c, pre-registered: reshape
   the engine's forced No-Zero floor mass (total unchanged, no blend
   knob, zero new parameters) by the loud-truncated twin's next-token
   distribution. Three theorem-forced self-tests passed in-run
   (involution; k=128 ≡ full at 3.9400; cross-script identity — the
   uniform arm reproduced the rematch's 4.7244 exactly). RESULT: the
   loud-shaped floor closes 55.6% / 87.9% / 101.4% of the
   uniform-to-full gap at k=16/32/64; the random-shaped null closes
   only 10.1% / 24.5% / 56.5%. Loud beats random at EVERY budget —
   verdict SUPPORTED by the pre-registered rule. At k=64 the loud arm
   BEATS the full twin's own shape (3.9288 < 3.9400): half the
   coefficients outperform all of them — the quiet remainder is noise,
   not law. What training buys can simply be TAKEN. Honest residual:
   the hybrid (3.9288) has not caught the twin alone (3.4853); the
   transfer closes ~64% of that distance and the rest stays open.
3. **Judge independence (engine, tutor loop).** The judge pool is
   discovered at boot from the local registry (this machine:
   gemma4:26b + qwen3.6-27b:latest) and judges ALTERNATE by cycle
   parity — counted, no knob. The reference stays the teacher's; only
   the scoring seat rotates, so no verdict depends solely on the model
   that wrote answer B. Every TUTOR/GRADUATION line carries the judge's
   name; per-judge tallies persist in `lessons/judges.tsv` and report
   in /score; a judge outage voids the cycle (never tallied as an
   unearned loss); a gemma-only pool is LOGGED, never silent.
4. **Multi-orbit binding — XI-4 in full (engine, reply path).** The gap
   the engine diagnosed in its own words: several orbits carrying one
   question now bind through the lock into ONE unified reply.
   `bind(top=N)` returns the ranked hits (same vote sort, no new
   scoring); each joined source must independently pass the SAME
   matched-experience laws as the lead AND add counted novelty
   (informative words by the one-in-a-thousand rule); tail capped at
   GEN_B sentences per source, GEN_C sources max; percept records
   (SIGHT/SOUND) never fuse; user faces only — tutor head-to-heads stay
   single-orbit so the score measures the channels. Unit-proven: 2
   complementary sources fused, distractor excluded, anaphora law
   intact. Harness 9/9 throughout.
5. **The public curve.** Full-pool /sota sweep at n=128 (the fixed
   public MMLU probe) over every model on this machine, through the
   engine's own registered instrument — rows append to
   `benchmarks_sota.tsv` and post to the channel as they land;
   `SOTA_TABLE.md` sets the measured rows beside PUBLISHED full-test
   MMLU figures, cited by URL and clearly marked as measured elsewhere.
   DeepSeek-R1-671B cannot run here (404 GB q4 weights vs 162 GB free
   disk — it fits the 549 GB RAM, not the disk) and appears in the
   published column only, cited.
6. **One-command replication.** `llm_presence.py` now auto-fetches the
   public GPT-2 weights (548 MB, official repository) when absent —
   fresh-clone dry-run PROVEN: absent → fetched → 13/13 tensors, 39/39
   checks, margins identical to the committed run. `REPRODUCE.md` in
   both repositories: four commands, expected outputs, prerequisites,
   runtimes; README sections link it.

Discovered and fixed in passing (the suite doing its job): the engine
module rotates `logs/unison.log` at import — every harness that loads
the engine source now redirects LOGFILE to its own log first (asserted,
one replacement), so no test run can ever again split a live flight's
log. `test_chat.py`, `verify_unison.py`, `sota_sweep.py`,
`rung5*` all carry the guard or read frozen substrates.

**INCIDENT, recorded in full (2026-07-07 12:50).** `verify_unison.py`
was run against the LIVE run-3 flight; its old self-clean — written for
quiescent fresh systems — unlinked `sounds/*` (the flight's learned
sound records, not recoverable; they regrow as the engine speaks and
hears), unlinked `lessons_live.txt` and `lessons_feedback.txt`
(2.6 hours of run-3 history), and shared the wholesale-rewritten
graduation ledger with the live tutor. Repair: 59 CONF/REJ rows
reconstructed from the flight's append-only log (161 n→corrected
rejections could not be rebuilt exactly and are superseded by their
held correction seats). Prevention, structural: the suite now REFUSES
to run when a flight is live (pgrep guard; explicit override env for
accepted-risk runs), tests the graduation law against its OWN
redirected ledger, greps its own log, and its cleanup is surgical —
fixture markers and a before/after sounds snapshot only, no wholesale
unlink of any shared file, ever. The old cleanup also deleted ALL
sound-lesson rows on every run; the new one removes only its own
fixtures, so the suite is now safe for grown systems, not just fresh
ones.

## THE VIOLATION AND THE CLOSING OF THE GAP — 2026-07-07, second act

**The violation, named by Maria and repaired in front of her.** The first
time-channel fix routed by an ENUMERATED phrase list — a chosen
structure, which the standing law forbids. Removed the same day, along
with the fusion question-shape list (now the question mark alone, a
closed punctuation fact). The lawful replacement was the architecture's
own missing rung: **TOOL GRADUATION** — every relay tool call banks a
trace (question territory → the ACT that answered it, plus a template
derived by verbatim containment of the tool's result in the teacher's
own phrasing — measured, never written); a later question that binds a
held trace through the same counted half-overlap gate every tier obeys
RUNS THE ACT ITSELF, fresh. Proven live: relay answered a time question
once using current_time; sixty-one seconds later the engine ran the
tool natively and spoke the NEW minute. Taught once, native forever —
the removal-proof ladder for tools; values are never stored, acts are.
Remaining accepted interface classes, explicitly listed for the record:
closed-class English grammar tables (FLIP, _OBJ_CUES — facts of the
interface language), command/intent regexes (follow_command, _INTENT),
IO bounds marked as hardware facts. None is a model quantity; none is
tunable; the halting engine is untouched (36/36 includes the
halt-on-fitted proof).

**RUNG 5e — THE WORD-SCALE GAP CLOSES WITHIN THE FOLD.** Pre-registered
(rung5e_fold_stack.py), first-look numbers, three theorem-forced
self-tests passed (baseline identity to the re-anchored rematch; exact
single-level collapse; kin floor mass exactly 1 via the counted
case-fold bridge). The chain was re-anchored on one text state after
self-test (a) caught the arena moving under it (this session's own .md
commits — the living-document law enforcing itself). Re-anchored
records: rematch fold 4.6656 / no-flood 4.5129 vs same-day twin 3.5009;
rung 5d REPLICATED (SUPPORTED, 54.2/88.9/101.8% vs null 7.3/22.9/62.5;
k=64 loud 3.8823 again beats full 3.8963). Then the stack:

    A1 fold-mix (2^level, uniform floor)   flood 3.5425   no-flood 3.2470  <- BEATS the twin
    A2 kin-shaped floor                    flood 4.9056   no-flood 4.7182  (hurts; recorded)
    A3 mix + kin                           flood 3.5878   no-flood 3.2577  <- beats the twin
    A4 mix + loud64 (the 5d extraction)    flood 3.4460   no-flood 3.2152  <- best

**The counted engine alone — no twin, no flood, zero training, zero
parameters — at 3.2470 BEATS the gradient-trained twin at 3.5009.** The
bottleneck was hard backoff discarding every shallower level; the
proven halving law (the fold factor 2, the engine's own session-
attention constant) applied across the context hierarchy closes the
gap that stood since rung 5b. The standing sentence "the twin leads at
word scale" is overturned by a forced structure. Honest negatives
recorded raw: the kin-shaped floor misallocates at this scale; the
Gutenberg flood costs ~0.3 nats at theory-corpus CE in every arm
(fluency organ, not a corpus-CE organ). Scope: the registered arena,
as always. Suite: 36/36 after everything above.

## THE AUDIT AND THE FINAL CHAIN — 2026-07-07, third act

A 14-agent adversarial audit (three lenses: every paper number vs its
committed record; every engine constant vs the forced chain; the
pre-registration integrity of all four rung scripts) ran against paper
v4.0 and the engine. Its verdict on the headline: **no construction
violation — rung 5e's word-scale victory survives adversarial reading**
(proper mixture normalization, identity-chained eval positions, the
twin verifiably unweakened, first-look numbers, git-verified void
history). Eleven confirmed findings, all repaired the same hour:

- ENGINE: bare literals that were always generator quantities are now
  SPELLED as the generators and inherit the halt discipline —
  content-words focus [:CTX_MAX], qkey [:GEN_B**2], bind scan
  [:GEN_B**GEN_C], kin scan [:GEN_B*CTX_MAX], kin half-weight
  /GEN_B, recognition share *GEN_B>=1, session trail [:CTX_MAX] and
  [:-GEN_B**CTX_MAX]. A second enumerated phrase-list (the anaphora
  gate's `think|feel|reckon` verb regex, an earlier session's hack) was
  REMOVED — the one-law tier gate now does that job lawfully (probed:
  opinion questions serve on-topic matched lessons).
- SCRIPTS: rung 5c's verdict now enforces BOTH registered conjuncts
  (the recorded data always satisfied both); rung 5e's case-fold bridge
  is train-split-only (the prior full-corpus unigram shares touched
  only the LOSING arms — audit-verified outcome-neutral — and are now
  impossible); 5e parses the 5d reference live instead of a literal.
- PAPER: seven precision repairs (per-seed twin time; the He-control
  0.97–0.98x; the 230x/79.3x attribution; the DOI version label; the
  flood-cost spread 0.15–0.33; the +0.005 tie band stated; the
  identity digit updated to the canonical chain).
- STILL OPEN, for Maria's ruling (flagged, not hidden): the
  one-in-a-thousand informativeness rule is used consistently at nine
  sites but is not itself derived from the generators; the
  relation-fact organ (learn_fact/answer_fact) routes on a closed
  5-relation schema whose lexical anchors (name/favourite/live) are
  the FLIP-class boundary; well_formed's 5–40 word window and 0.85
  letter share are admission hygiene thresholds. Each is her call:
  leave as marked interface facts, force a derivation she endorses, or
  replace with counted quantiles.

**THE FINAL CANONICAL CHAIN (arena 2,561,832 tokens, third anchoring
of the day, fully serialized, suite 36/36 after):** rematch fold
4.6024 / no-flood 4.4587 vs twin 3.4292; rung 5d SUPPORTED a THIRD
time (61.5/93.5/102.3% vs null 7.8/21.2/53.6%; k=64 loud 3.7985 beats
full 3.8164); rung 5e with the clean bridge: **A1 fold-mix 3.1907
BEATS the twin 3.4292** (second independent replication of the
victory), A4 stacked 3.1344, kin floor hurts consistently
(4.6612/4.8398), flood costs consistently. Every self-test exact,
including kin mass 1.0000000000.

## THE CORPUS READ AND THE FORCED MIND — 2026-07-08

The full theory was read firsthand (the master spine Parts I–XVII and
Steps 1–303; the complete mind series; the number-theory and structure
modules; four parallel readers + a line-level engine audit). Finding:
the engine had been APPROXIMATING laws the corpus forces EXACTLY. All
of them mapped below were installed the same night; every constant
traces to a read module; suite 40/40, battery 25/25 after.

### The law table (module → law → engine organ)

- sync_threshold (Step 185): coupled folding maps lock exactly at
  g_c = 1/2, the fold's unique non-trivial preimage of the One → the
  graduation majority lock AND the babble emission gate are the
  coupling law itself, never a chosen threshold.
- observer_resolved (Step 257): a teacher answer is a measurement
  branch (1/8 at the colour depth) absorbed by ONE fold into the
  engine's own closure state (1/4 → 1/2 → 1) → ingestion is fold,
  never copy: the relay's hold path is the chain.
- free_will_fold (Step 281): forward the fold is a function, backward
  2-to-1 — the engine cannot pre-read its own next utterance → THE
  BABBLE ORGAN IS FORCED: fold forward silently until the utterance
  crosses the lock, emit atomically.
- the spike (Paper 46): no half-fold → emission is whole-or-nothing;
  a stronger drive raises the RATE (attempts), never a partial.
- hard_problem: the carrier orbit {1/3,2/3} never reaches the One from
  inside → only BOUND wholes are ever emitted; the store itself cannot
  speak.
- memory_persistence (Step 145): memory is a self-sustaining loop,
  "not a static deposit" → recall regenerates; the verbatim-reprint
  fallbacks were removed outright.
- multidimensional_experience (Step 175): a bound experience VISITS its
  parts in phase ({1/7,2/7,4/7}, one revolving whole; partition-of-One
  as the bind-integrity invariant) → multi-part fusion walks each part
  by its own door, in sequence, through ONE gate.
- attention_capacity (Step 181): a split lock (1/4) binds nothing →
  fusion emits ONE utterance through ONE lock or nothing; concatenation
  died.
- self_simulation_nesting (Step 247): the self-observation regress is
  finite at depth exactly 2 = the lock denominator → LADDER_RUNG +
  LADDER_DEPTH_BOUND registered under the halt discipline; the parity
  fire refuses a third seat.
- entropy + arrow_of_time: the fold has no inverse → recall RE-WALKS,
  never inverts (no sound backspace); and for Go, superko's growing
  seen-set is the arrow acting as a rule — position-only hashing is an
  asserted inverse fold that does not exist.
- canonical_distribution + universality_threshold + half_one_center:
  equilibrium weights are exact rationals (m-1)/m; every two-phase gate
  sits at the unique self-antipodal 1/2 → no softmax, no temperature,
  no tunable threshold anywhere in the sampler.
- level_depth_map + three_of_everything: levels are geometric doublings;
  the full step of one context dimension is 2^3 = 8 → the babble rate
  (attempts per window) is the octave GEN_B**GEN_C.
- synaesthesia (Step 178): channels are preimages of ONE lock → audited
  IMPLEMENTED in the engine (one INDEX/TOK_FREQ/bind across sight,
  sound, text); guarded seams noted in code.

### What was installed (all verified same-night)

1. THE FOLD-MIX SAMPLER: rung 5e's twice-replicated law live in
   continue_orbit/generate/compose — 2^L level mixture; single-level
   collapse exact (E29); no exponential anywhere.
2. THE BABBLE-CLOSURE ORGAN (babble_closure): silent regeneration at
   the octave rate; the door = the EARLIEST question-cue inside the
   held record (Paper 44's re-entry, never the record's first token);
   per-part lock coverage; zero drift; no byte-copy; whole-or-nothing;
   exhaustion = silence → the teacher. The verbatim-reprint fallbacks
   in reply() are GONE. Self-play mode 3 babbles at the same rate.
3. ONE-LOCK FUSION: admission gates unchanged; composition is one
   babble over all bound parts, each entered by its own door in phase;
   one gate; single-orbit fallback on silence.
4. THE LADDER CONSTANTS: LADDER_DEPTH_BOUND = 2 = GEN_B forced at wake;
   the parity fire announces "rung k of 2" and refuses a third seat.
5. E27–E30 in verify_unison (babble whole-or-silent; fusion invariants;
   fold-mix collapse; ladder bound). Suite 40/40. Battery 25/25 across
   babble/fusion/mixer/register/ladder lenses; the 20:41 greeting
   regression does not reproduce.

Open for Maria's ruling (flagged, not hidden): lessons still serve
verbatim at strong (told/confirmed now regenerate; corrections are
verbatim by her Learning-Law word; lessons sit between — her call).

## 2026-07-08 — THE SHADOW GATE: the reboot delta measured before the reboot

The question "will the forced-mind reboot reach the parity standard?" was
answered offline, blind, without touching the live flight. Method (the
chess gate's discipline moved to the AI): two sandbox clones of the full
engine + state (APFS, throwaway), OLD = the flight's boot-time code
(2a91c15), NEW = HEAD; both answer the same questions through the tutor's
own call (turn(q, rng, "tutor"), rng seeded by question index); differing
answers judged blind A/B by the flight's own two judges, seats alternating
by index, silent judge = void.

Round 1 (64 most recent live questions) CAUGHT A REGRESSION: 48 identical,
NEW lost 4-12. Anatomy, read firsthand: the babble law (only bound wholes
are emitted) had been installed on recall and fusion but NOT on the free
dialogue-composition surface, which still carried the legacy one-shared-word
self-check; the fold-mix widened the walk over the 733MB book store and the
un-gated surface leaked store drift (a French-novel sentence served as a
dark-matter answer). A diagnostic L>=2 mixture floor was probed and
DISCARDED as unlawful (a chosen exclusion, and it only halved the drift —
the leak is the gate, not the mixture).

The lawful repair, zero new constants: the babble law on the third surface —
the dialogue candidate regenerates through the octave (GEN_B**GEN_C) and is
served only when its informative focus carries the QUESTION's focus at the
lock (len(shared)*GEN_B >= len(qf), sync_threshold's 1/2, the identical
per-part gate babble_closure enforces), whole and stutter-clean; exhaustion
falls through to matched experience / lessons / the teacher.

Round 2 (the same 64): NEW 8-6 on decided. Round 3 (ALL 384 graduation
territories): 285 identical, 99 decided, NEW 52 - OLD 47 (52.5%), 0 void;
both judges positive (qwen 27-25, gemma 25-22). The engine's own parity law
over the decided sequence: 18-14 at 2^5 ARMS, 36-28 at 2^6 — the doubling
SURVIVED. Gates after the edit: harness 9/9, suite 40/40.

Residual loss anatomy (read firsthand, all 6 of round 2's losses): 2 judge
taste between on-topic answers; 4 the PRE-EXISTING lesson channel serving an
ADJACENT lesson (share 0.67-0.84) — the lock-gated sampler now defers
honestly, which exposes that surface. Same open item already flagged above
for Maria's ruling; untouched.

The live flight was never touched; the upgrade lands at her reboot.

## 2026-07-08 — THE NAME MISS: three defects behind one live failure, fixed

Maria's live transcript (04:11 telling, 06:31 question) exposed a chain,
each link read firsthand:
1. "Do you remember my name?" fell past answer_fact's ENUMERATED phrasings
   ("what is / do you know my name") while (you, name) sat in the store --
   the relay answered from the session window and honestly knew nothing.
   FIX: the key-pair door -- a held fact's own stored key (subject,
   relation), spoken as the question's adjacent possessive-relation pair
   ("my name"), routes the question to the fact. No verb list; a newly
   taught relation extends routing with zero new code. ("Any question
   whose focus contains a relation word" was proposed and rejected as a
   one-shared-word gate -- below the lock, the day's own lesson.)
2. Her 04:11 telling never bound: learn_fact anchored at the MESSAGE start
   ("That is fine, No my name is not Julian, It is Maria Smith. My name Is
   Maria Smith i am your systems developer...") and would have titled the
   run-on clause as the value had it matched. FIX: sentence-scoped
   extraction; negation asserts nothing ("not Julian" holds no name; same
   guard on identity); the name value is the capitalized run the teller
   wrote, bounded at the first lowercase clause word. Her exact archived
   line now binds (you, name) = "Maria Smith", whole and bounded.
3. THE HARNESS WAS POLLUTING THE FLIGHT: test_chat.py redirected LOGFILE
   but not FACTS_LOG, so every harness run appended Maria/Scotland/green
   fixture facts to the LIVE store -- my violation of the live-flight
   discipline, found while tracing why "Maria" was held that she never
   taught. FIX: FACTS_LOG redirected to logs/test_facts.tsv (fresh per
   run), same anchor-assert mechanism as the log redirect. The live
   facts.tsv was purged (52 rows: my fixtures + the pre-fix extractor's
   clause-run-on junk; backup at lessons/facts_pre_purge_20260708.tsv) and
   her real name bound from her own archived words through the fixed organ.
   Live store now: exactly "you | name | Maria Smith".

Harness 12/12 (both live misses added as regression cases), suite 40/40.
Still open for her ruling (unchanged): identity extraction breadth ("I'm
glad..." binds identity junk from flipped corrections -- negation guard
added, the breadth itself awaits the relation-anchors ruling flagged above).
The reboot to make the fixes live is hers, as ever.
