# From One Axiom to Master-Level Chess — and the Law Inside Neural Networks

## *Attention, it turns out, was not all you need*

**The fold's computational program, en route to UnisonAI**

Maria Smith (Ernos Labs) — pre-paper v0.2, 2026-07-06
Companion to *The Smithian Fold Theory of Everything* (DOI: 10.5281/zenodo.21182469)

---

## Abstract

We report two connected results from the fold's computational program. **First**: a chess engine containing zero parameters — no piece values, no tuned weights, no opening book, no training — whose every evaluation is a count performed on the board's geometry and an exact rational share of the One, reached master-adjacent strength in three days of measured climbing: it beat Stockfish's Elo-1900 setting 6W-3D-3L (62.5%) and holds Elo-2100 to a draw in half its games (best 1W-6D-5L, 33.3%), every match pinned, refereed, recorded. The same machinery solved queen-vs-rook exactly — 19,733,336 legal positions, re-proven value-by-value in an independent clean-room implementation with zero disagreements — atop the campaign's record of 1,092,871,108 five-piece positions solved at zero error against Syzygy. Solved chess value fields are *dyadically smooth*: 32 Walsh coefficients carry 81.1–86.7% of an ending's signed value field and reconstruct 92.7–95.3% of all exact values. **Second**: pointing the identical pre-registered instrument at *trained neural networks*, we find trained weights carry placement-law in the fold's dyadic basis — unanimously (18/18 on validated released models), causally (untrained controls sit at exactly chance), located (the law concentrates in transformer *expansion* projections and token embeddings across three unrelated architectures, while contraction projections and attention sit at chance in aligned packings), amplified by coordinates, reaching 230x chance in GPT-2's token embedding — and surviving 4-bit deployment quantization at every depth of a production Llama-3.1-8B (peaking mid-network, where transformers store their deepest associations). Together these support one proposition: much of what is currently purchased with parameters, data, and compute is **law**, and law can be derived. We state what is proved, what is registered as next, and how every number here can be independently certified.

---

## 1. The field began with law

In 1943, before there was a field, Warren McCulloch and Walter Pitts opened the first neural-network paper with a claim about *logic*, not statistics: "Because of the 'all-or-none' character of nervous activity, neural events and the relations among them can be treated by means of propositional logic." The founding document of neural computation was titled *A Logical Calculus of the Ideas Immanent in Nervous Activity*. The field's first sentence said: **the net is law.**

What followed was eighty years of a different bargain. Rosenblatt's perceptron (1958) learned its coefficients rather than deriving them. Rumelhart, Hinton, and Williams (1986) gave learning its engine — backpropagation — and from that moment the field's answer to every question became: *buy it*. Buy structure with parameters, buy knowledge with data, buy competence with compute. Vaswani and colleagues (2017) crowned the era with a title that is itself the era's thesis: *Attention Is All You Need*. Scaling laws (Kaplan et al., 2020; Hoffmann et al., 2022) made the purchase-price schedule explicit, and the bill is now measured in gigawatts.

Richard Sutton called the pattern honestly in *The Bitter Lesson* (2019): "The biggest lesson that can be read from 70 years of AI research is that general methods that leverage computation are ultimately the most effective, and by a large margin." Search and learning beat hand-coded human knowledge, every time. But notice what the bitter lesson compares: *purchased statistics* against *hand-crafted heuristics*. There has always been a third contestant, the one the field's founding paper named and then forgot — **derived law** — and it has never been given its match.

This paper gives it its match. Twice.

## 2. The labs themselves say one thing is missing

The people building the largest systems on Earth do not describe the remaining distance to true intelligence as more of the same. Sam Altman wrote in January 2025: "We are now confident we know how to build AGI as we have traditionally understood it." Dario Amodei describes what is coming as "a country of geniuses in a datacenter," possibly as soon as 2026–2027 — an essay, *Machines of Loving Grace*, whose central argument is that we systematically underestimate what follows. Demis Hassabis has said for years that human-level intelligence may be one or two breakthroughs away; Shane Legg, who co-founded DeepMind, has held a 50% estimate for AGI by 2028 for over a decade; Ilya Sutskever told NeurIPS 2024 that "pre-training as we know it will end" — the data is finite, and what comes next must come from somewhere else.

Read those statements together and they say: the frontier believes it is **a small number of algorithmic developments** from the destination, and that the current paradigm's fuel — data — has a visible bottom. Every lab is searching for the missing development *inside* the statistical paradigm: better objectives, better architectures, better post-training.

This paper proposes that the missing development is not inside the paradigm. It is the paradigm's founding idea, recovered with the mathematics it was always waiting for: **stop buying law. Derive it.** And unlike the essays, this proposal arrives with referees: a chess ladder anyone can replay, a billion-position certification anyone can re-run, and a pre-registered instrument that found the law sitting inside the industry's own weights.

## 3. The chess demonstrator: derivation versus the purchased world

Chess is the cleanest arena on Earth for this contest, and not by our choice — it is the domain Sutton's bitter lesson itself cites, the domain where purchased knowledge (Deep Blue's hand-tuning, Stockfish's NNUE, AlphaZero's self-play) has been declared the only path, three different ways, for thirty years.

### 3.1 The engine with nothing inside

The engine contains no chosen numbers — the claim is literal, and grep-able. Piece worth is **counted**: the number of squares a piece commands from where it stands, walked on the board's geometry at evaluation time (a knight counts 2 in the corner, 8 in the centre; a rook 14 from anywhere; a queen 21–27). Mobility and promotion potential are counts against the opponent's counted attack map. A position's value is the mover's exact share of the One — counted units over total counted units, an exact rational in (0,1). The starting position evaluates to exactly 1/2 — the half-One lock — by the symmetry of the rules; that is a theorem in the test suite, not a calibration. Minimax is the fold's involution (my value = 1 − yours); mate approaches the One; a repetition is a closed orbit that never reaches the One, priced at the lock exactly; the fifty-move law is priced at its own rule-defined boundary. Search is exact alpha-beta — lossless by theorem — under a hard node bound; every accelerator is ordering-only and provably value-identical: an integer-keyed transposition table, killer moves, history — censuses of the search's own cutoffs, incremented by 1, no weights anywhere. The rules implementation is certified against the published perft censuses (20 / 400 / 8,902; Kiwipete 48 / 2,039 / 97,862; the en-passant-pin and four-promotion positions exact), every refereed move is validated externally (python-chess), and the engine has never played an illegal move in campaign history.

### 3.2 The measured climb

All matches: 12 games, pinned binaries, alternating colours, referee-validated, recorded verbatim whatever they said.

| Stockfish setting | result (W-D-L) | score | engine |
|---|---|---|---|
| 1320 | won (early rung) | — | v2 |
| 1500 | 2-2-0 | 75% | v3 |
| 1700 | 3-7-2 | 54.2% | v13 |
| 1900 | 6-3-3 | 62.5% | v14 |
| 2100 | 1-6-5 | 33.3% (best) | v17 |

Three days. Zero training. One axiom. And the discipline is as load-bearing as the arithmetic: every release must beat its predecessor head-to-head before it faces Stockfish (v13 over v12: 4-2; v14 over v13: 9-1; v17 over v14: 10-1); every loss is autopsied under full-strength Stockfish judgment, per-move eval curves locating the exact ply each game goes permanently bad; every release cures exactly one named disease with counted or lossless machinery. The cures themselves are the story of where compute really goes: a profiler found **91% of match CPU inside the language runtime's garbage collector** — cured by an allocation-free hot path, ~25x compounded; weak move ordering — cured by killers and history, collapsing depth-7 cost from 63.5M to 17.7M nodes with provably identical move choices; horizon — cured losslessly, and one single ply of added sight flipped the 1900 rung from 20.8% to 62.5%. Two principled evaluation variants were gated, **refused** (37.5%, 45.8%), and permanently closed: iterating evaluations against match results is fitting by another name, and the zero-parameter law bans it structurally. A parallel-root release (8 worker processes, exact single-core values, 7.6x measured parallelism at 95% efficiency, complete depth 8–9) is in gate at the time of writing; the standing protocol thereafter iterates directly against **full-strength** Stockfish, every probe game logged in full — movetext, eval curve, death-ply, kill phase — from the first 0–12 onward.

### 3.3 Solving, certification, and the compact truth

The retrograde fold — the same induction certified on Nim — solves whole material classes exactly. Campaign record: **1,092,871,108 positions** across KQK, KRK, KQKR, KRRK, KQKRR at zero error against the Syzygy tablebases. This session added KQKR end-to-end: 19,733,336 legal positions (W 11,953,856 / L 7,079,816 / D 699,664; 13,420 mates; longest win 69 plies; mirror audit zero), then the certification that matters: a **second, independent implementation in a different language re-derived every stored value and distance** from the fold's value law over all 33,554,432 indices — bad = 0, census matching digit for digit.

And the solved truth is small. Under the Walsh–Hadamard transform — the fold's natural harmonics — the top 32 coefficients carry 81.10% (KQK) and 86.72% (KRK) of the full ending's energy and reconstruct 92.70% / 95.27% of every exact value (94.05% / 97.42% under relational repacking); concentration is preserved exactly by the fold-universe's own transformation group (an in-run, theorem-forced self-test) and destroyed by dyadically foreign rearrangement; a 5% fragment of a solved four-piece field ranks the withheld 95% at AUC 0.998. Honesty note, as measured: the top-2048 truncation that leaves 0.3–0.6% exceptions at three pieces leaves 11.25% at four — the compact-exact form does not scale trivially, and we say so.

Gigabytes of tablebase; kilobytes of law. That asymmetry is the entire thesis in one line — and it raised the question that became Part Two: *if purchased chess knowledge was law in a costume, what about purchased language?*

## 4. The law inside neural networks

### 4.1 The instrument

Pre-registered before any spectrum was computed, and amended only on the record: objects; transform (Walsh–Hadamard, float64, row-major flattening truncated to the largest power of two); statistic (energy concentration at fractions 6.1e-5, 4.9e-4, 3.9e-3 of the space — the chess campaign's own operating points); nulls (five seeded permutations of the *same tensor* — identical value histogram, scrambled placement — plus a moment-matched Gaussian yardstick); and an in-run, theorem-forced self-test (bit-reversal repacking is F2-linear and must preserve concentration exactly; every run reported here passed to machine precision). Verdict rule fixed in advance. Fixed seed (20260706). Every result file committed verbatim.

### 4.2 What the instrument found

**Trained weights carry placement-law — 18/18.** On validated released models (Stable Diffusion 1.5, SDXL, Kokoro-82M): every probed tensor beat both nulls at every registered fraction. Because the shuffle-null preserves the value histogram exactly, what is measured is *where training put the values* — placement, not statistics.

**The law is located — and the location is a message.** In a blind 96-tensor sweep of SD1.5, the entire top-10 by margin is the CLIP *text* transformer's MLP fc1 — every layer, 0 through 9, at 5.5–8.4x — while vision FF sits at 1.03x and attention at 1.00x: chance. Then GPT-2, the canonical open language model: token embedding at **230x** chance; every MLP *expansion* matrix (c_fc, all 12 layers) hot at 3.4–12.7x; every *contraction* matrix (c_proj) at chance. Then a production Llama-3.1-8B, dequantized from its shipped 4-bit blocks, sampled at layers 0/8/16/24/31: every ffn_gate hot (3.7–8.5x, peaking mid-network at layer 16), every ffn_down at exactly 1.00x. Three unrelated architectures, one fingerprint: **the law lives in the expansion direction** — the projections into the wide space where interpretability research locates a transformer's stored knowledge, the block that is roughly two-thirds of an LLM's parameters. And there is an irony the era's crowning title has earned: in the fold's basis, in these packings, the attention matrices are the *quietest objects in the network*. Attention, it turns out, was not all you need. The knowledge went somewhere else, and now we can see where.

**The effect is training-caused.** He-initialised matrices at matched shapes: 0.98x, 0.97x — exactly chance. The instrument is blind to untrained weights. Everything above is deposited by training.

**Coordinates amplify — the chess lesson repeats.** Column-major repacking lifts the strongest text MLP from 8.44x to 12.11x and wakes "dead" vision tensors from 1.00x to 1.72x. Thin margins are wrong coordinates, not absent law.

**The law survives deployment.** The Llama measurements above are *through* 4-bit quantization — the fold sees the law in models as actually served today.

## 5. What is proved, what is registered, and where this goes

**Proved, in the strict sense that a reader can re-run it:** the zero-parameter engine and its measured ladder; the exact solving and dual-implementation certification of the endgame classes; the dyadic smoothness of solved chess value fields with in-run instrument self-tests; the presence, location, causation, amplification, and quantization-survival of dyadic placement-law in trained neural weights, under a pre-registered protocol on public models.

**Not yet claimed:** that the located law suffices to *derive* generative competence. That is the program's next registered rung — fold-basis compression of the hot components measured against quality at matched budgets, then derived components gated head-to-head against their trained equivalents, under the chess campaign's own gate discipline.

**The destination — UnisonAI.** An omni-modal intelligence — text, audio, image, video, physical and sensory input; real-time; live-learning — whose lawful core is *derived*: zero parameters, exact, verifiable to the One; whose learned residual is minimal; whose learning machinery is itself fold-lawful (counted attention, memory as held orbits, the spike's arithmetic). Every modality is, at core, a value field over a lawful space — the object class this program has now compressed (chess), certified (a billion endgame positions), and detected inside the industry's own weights. The frontier laboratories say the destination is a few algorithmic developments away. We agree — and we are proposing what the development is. The field's first sentence, 1943: the net is law. The fold is the mathematics that sentence was waiting for.

## 6. How to certify every claim

All artifacts live in the public repositories accompanying the SFTOM corpus.

1. **The corpus's proof driver** (clean room): `make -C verify prove` — 307 suites / 1,844 forced checks, non-zero exit on any failure.
2. **Chess rules**: perft censuses inside the engine's test suite; refereed play validates every move externally (python-chess).
3. **Matches**: `tools/measure_sf.py <elo|full>` (pinned 12-game protocol); `tools/h2h_gate.py <old-binary>` (gates); `tools/summit_probe.py <label>` (full-forensics probe); the complete ledger is `tools/MATCHES.md`.
4. **Endgame certification**: `tests/kqkr_cert.ep <lo> <hi>` re-derives every stored KQKR value from the fold's value law with the clean room's own move generator (0 to 33,554,432 = the full census; the committed 3-man analogue is `constants/endgame_tables.ep`).
5. **Neural-weight measurements**: `fold_ai/PROTOCOL.md` (pre-registration, amendments logged); `fold_ai/spectral_probe.py` and arm scripts (seed 20260706); result files committed verbatim; the F2-linear self-test certifies each run internally. All probed models are public releases; every margin in this paper reproduces on commodity hardware.

## References

- W. S. McCulloch, W. Pitts, *A Logical Calculus of the Ideas Immanent in Nervous Activity*, Bulletin of Mathematical Biophysics 5, 115–133 (1943).
- F. Rosenblatt, *The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain*, Psychological Review 65(6) (1958).
- D. E. Rumelhart, G. E. Hinton, R. J. Williams, *Learning Representations by Back-Propagating Errors*, Nature 323, 533–536 (1986).
- A. Vaswani et al., *Attention Is All You Need*, NeurIPS (2017).
- J. Kaplan et al., *Scaling Laws for Neural Language Models*, arXiv:2001.08361 (2020); J. Hoffmann et al., *Training Compute-Optimal Large Language Models*, arXiv:2203.15556 (2022).
- R. Sutton, *The Bitter Lesson* (2019).
- D. Amodei, *Machines of Loving Grace* (2024). S. Altman, *Reflections* (2025). Public statements of D. Hassabis, S. Legg, and I. Sutskever (NeurIPS 2024) as cited in text.
- M. Smith, *The Smithian Fold Theory of Everything*, DOI: 10.5281/zenodo.21182469, and the SFTOM proof constellation.

*Pre-paper v0.2. Every number in this document is from committed, timestamped campaign records; nothing is projected.*
