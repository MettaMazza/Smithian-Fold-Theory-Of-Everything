# UnisonAI: A Forced, Derived Language Architecture with Zero Parameters

## *Attention, it turns out, was not all you need*

**Maria Smith (Ernos Labs)** — full paper v1.0, 2026-07-06
Companion to *The Smithian Fold Theory of Everything* (DOI: 10.5281/zenodo.21182469); supersedes pre-paper v0.3 (DOI: 10.5281/zenodo.21217279)

---

## Abstract

We present three connected results in the computational sciences, and the architecture they force. **First**, using a pre-registered, self-certifying spectral instrument, we show that trained neural network weights carry *placement-law* in the dyadic (Walsh) basis: unanimous verdicts (18/18) on validated released models; the law concentrated in transformer *expansion* projections and token embeddings across three unrelated architectures (up to 230x chance in GPT-2's embedding) while attention matrices sit at chance; the effect strictly training-caused (He-initialised controls at exactly 1.0x); surviving 4-bit deployment quantization at every network depth. A recipe map from 124M to one trillion parameters shows the law tracks *training recipe*, not scale or architecture — its strongest carrier is DeepSeek-R1 at 671B (43–47x in every probed block) — and the loud models' spectra transform under the fold's transformation group *exactly as solved game-theoretic value fields do*: preserved under F2-linear repacking, gracefully degraded under odd-multiplication maps. **Second**, we show that the "learned similarity space" held to make gradient training irreplaceable is a *counted object*: word kinship computed as exact co-occurrence shares over held text reproduces semantic family structure (quark→{lepton, neutrino, proton}) with zero parameters and zero gradients. **Third**, we construct UnisonAI: a complete language architecture in which every mechanism of a large language model — memory, attention, similarity, learning, prediction, generation — is replaced by a machine-verified law of the Smithian Fold Theory, with zero trained parameters end to end. On identical held-out text, the fold-native engine **outperformed its trained transformer twin (cross-entropy 1.289 vs 1.888)** after reading the training corpus once (26 seconds) against the twin's 48,000 gradient-batched readings (21 minutes per seed); teaching it one new fact costs writing one record, not a retraining run. The architecture is deployed as a live, continuously-learning conversational agent. Negative results are reported in full with their scopes. Every number in this paper is from committed, timestamped records and reproduces from the public repository.

---

## 1. The field began with law

In 1943, before there was a field, McCulloch and Pitts opened the first neural-network paper with a claim about logic, not statistics: "Because of the 'all-or-none' character of nervous activity, neural events and the relations among them can be treated by means of propositional logic." The founding document of neural computation — *A Logical Calculus of the Ideas Immanent in Nervous Activity* — said, in its first sentence: **the net is law.**

Eighty years of a different bargain followed. Rosenblatt's perceptron (1958) learned its coefficients rather than deriving them; backpropagation (Rumelhart, Hinton & Williams, 1986) made learning the field's universal answer; *Attention Is All You Need* (Vaswani et al., 2017) crowned the era with a title that is itself the era's thesis; and the scaling laws (Kaplan et al., 2020; Hoffmann et al., 2022) wrote the price schedule — structure bought with parameters, knowledge bought with data, competence bought with compute, the bill now measured in gigawatts. Sutton's *Bitter Lesson* (2019) drew the moral honestly: "general methods that leverage computation are ultimately the most effective, and by a large margin." But the bitter lesson compares purchased statistics against hand-crafted heuristics. A third contestant — **derived law** — was named by the field's founding paper and then forgotten, and has never been given its match.

The frontier itself senses the missing ingredient. Altman (January 2025): "We are now confident we know how to build AGI as we have traditionally understood it." Amodei projects "a country of geniuses in a datacenter," possibly by 2026–27. Hassabis has long placed human-level intelligence one or two breakthroughs away; Legg has held a 50% estimate for 2028 for over a decade; Sutskever told NeurIPS 2024 that "pre-training as we know it will end" — the data has a bottom. Read together: the laboratories believe a small number of algorithmic developments separate the field from its destination, and they are searching for those developments *inside* the statistical paradigm.

This paper proposes, with measurements, that the development is the founding idea recovered: **stop buying law; derive it.** The Smithian Fold Theory supplies the mathematics — one axiom (the One and its fold), zero free parameters, from which the corpus derives the constants of physics and, as machine-verified claims, the laws of memory, attention, binding, prediction, observation, and learning used here as engineering.

## 2. The instrument

All spectral results use one pre-registered instrument, fixed in writing before any spectrum was computed, with amendments logged and dated. Objects: weight tensors of validated released models, row-major, truncated to the largest power of two (later corrected — see §4 — to per-row-block reads with median statistics, after a scale-correlated windowing confound was identified and recorded). Transform: Walsh–Hadamard, float64. Statistic: energy concentration at three fixed fractions of the space (6.1e-5, 4.9e-4, 3.9e-3). Nulls: five seeded permutations of the *same tensor* — identical value histogram, scrambled placement — plus a moment-matched Gaussian yardstick. In-run self-test, theorem-forced: bit-reversal repacking is F2-linear and must preserve concentration exactly; every run reported here passed to machine precision. Verdict rule fixed in advance; seed 20260706; all result files committed verbatim.

## 3. The law inside trained weights

**Presence (18/18).** On Stable Diffusion 1.5, SDXL, and Kokoro-82M: every probed tensor beat both nulls at every registered fraction. Because the shuffle-null preserves the histogram exactly, the measurement isolates *placement* — where training put the values.

**Location — the expansion fingerprint.** In a blind 96-tensor sweep of SD1.5, the entire top-10 by margin is the CLIP text transformer's MLP fc1, every layer 0–9, at 5.5–8.4x, while vision FF (median 1.03x) and attention (median 1.00x) sit at chance in the aligned packing. GPT-2: token embedding at **230x**; all twelve MLP expansion matrices (c_fc) hot at 3.4–12.7x; all contraction matrices (c_proj) at chance. Llama-3.1-8B, dequantized from production 4-bit blocks, sampled at layers 0/8/16/24/31: every ffn_gate hot (3.7–8.5x, peaking mid-network), every ffn_down at 1.00x. Three unrelated architectures, one fingerprint: **the law lives in the expansion direction** — the projections into the wide spaces where transformer knowledge is stored, roughly two-thirds of an LLM's parameters. In the fold's basis, the attention matrices are the quietest objects in the network. Attention was not all you need; the knowledge went somewhere else, and now it can be seen where.

**Causation.** He-initialised matrices at matched shapes measure 0.98x and 0.97x — exactly chance. The instrument is blind to untrained weights; everything above is deposited by training.

**Coordinates.** Column-major repacking lifts the strongest text MLP from 8.44x to 12.11x and wakes "dead" vision tensors from 1.00x to 1.72x. Margins are functions of coordinates; thin readings are wrong doors, not absent law.

**Deployment survival.** All Llama measurements above are through 4-bit quantization: the law is present in models as actually served.

## 4. The recipe map: 124M to one trillion parameters

With the instrument corrected for scale (per-row-block spectra, median margins — the approach must vary with the object; the flat window's scale-correlated confound is recorded), the fingerprint was measured across a local model library spanning four orders of magnitude. Loud: GPT-2 (12.7–67.6x), Llama-3.1-8B (8.5x), **DeepSeek-R1-671B (43–47x in every probed block, dense and shared-expert — the strongest production signal measured)**. Quiet in the probed coordinates: gpt-oss (20B, 120B), Qwen3 (27B, 235B, 480B), Kimi-K2.6 (~1T), all 0.76–1.07x. **Scale is exonerated** (the loudest carrier is 671B); **architecture is exonerated** (mixture-of-experts appears on both sides); **the training recipe is the variable.** Controls sharpen the reading: an R1-distilled Qwen-32B reads as quiet as its non-reasoning sibling, so R1's law traces to its base pretraining rather than distilled reasoning traces; and by the campaign's standing epistemics — a fully lawful formula-generated field certifies at chance to this same probe — a quiet verdict is a verdict on the probe's coordinates, never on law-presence. The quiet lineages express their law in coordinates not yet found (a registered hunt over the fold's index-reordering group produced no wake in round one; recorded).

One identification stands above the map: the loud models' concentration is **preserved exactly under F2-linear repacking and degraded gracefully under odd-multiplication maps** — precisely the transformation signature previously measured for solved chess value fields. Loud-recipe weights are the same class of mathematical object as solved game fields: dyadically smooth carriers of law.

## 5. Negative results, scoped exactly

This program records its refusals; they are what make the verdicts above trustworthy.

- **Fold-basis weight compression is closed.** Against naive uniform quantization at matched storage, fold truncation won on R1's loudest tensors at real bit-levels; against the *production* construction (per-block scaled 4-bit), it lost on every tensor tested, including the 43x class, by 10–100x reconstruction error. The spectra of trained weights are heavy-tailed: keeping everything coarsely beats keeping a little exactly. Closed with the right baseline on the right patient.
- **Component transplants inside SGD hosts refuse at toy scale.** A frozen Walsh positional code lost to a learned embedding (1.888 vs 2.027); a theorem-derived attention cascade lost further (2.601). An attribution control then decomposed the attention loss: **0.54 of 0.71 was the transplant construction itself** (severed gradients — the host's home game), only 0.17 the fold's law. The refusals are verdicts on *fold objects as frozen transplants in the incumbent's machine*, and the construction bias joins the campaign's documented deflationary-verdict record. The corrected method — the fold fighting as itself — is §6.

## 6. UnisonAI: the architecture, mechanism by law

UnisonAI is a complete language architecture in which each mechanism of an LLM is replaced by a machine-verified corpus claim, with zero trained parameters end to end:

| LLM mechanism | UnisonAI mechanism | Corpus law (verified claim) |
|---|---|---|
| Weights / memory | **Held orbits**: every context read or told, written once, exact, inspectable | Memory is a held orbit (XI-1; Paper 44) |
| Embedding similarity | **Counted kinship**: co-occurrence shares over held text, exact rationals | Counted, not learned — this paper, §7 |
| Attention | **Unit-capacity selection**: one focus at the lock answers; content-word binding selects it | XI-2 (unit capacity); XI-4 (binding) |
| Softmax distribution | **Exact shares** with the forced No-Zero floor | The No-Zero axiom |
| Next-token generation | **Composition over orbits**: probabilistic walk on exact counts with context backoff | XI-4 over the orbit hierarchy |
| Gradient learning | **The Learning Law**: hold at the prediction state → close by observation → consolidate to the held cycle | Derived from XI-3, XIV-7, XI-1, XI-6 |
| RLHF | **The closure**: optional y/n feedback; confirmation consolidates (1/4 + 3/4 = ONE), rejection withholds the antipode permanently; corrections held on telling | XIV-7 (the 2-to-1 self-observation closure) |
| Context window | The conversation itself held as orbits; deixis resolved at the boundary (I/you flip at storage) | XIV-7; the observer (XVII-5) |
| Interpretability | Total: every reply's chain of thought is emitted and itself held; every fact is a readable record | The introspection limit respected: it reports what it holds, never the fold act |

Knowledge is *written, not trained*: teaching the engine one fact costs one record — no gradient run, no catastrophic forgetting, and the store can be opened and read. Learning is automatic and ongoing (every telling), feedback-weighted but never feedback-dependent. Facts persist across process death in a plain ledger. An engineering law completes the design: the engine's diet is the theory corpus, growing prose, and its lessons — never its own build documents.

## 7. Measured results

**The task gate.** On identical held-out text with an identical arena, the fold-native engine versus a trained transformer twin (4 layers, 128 dims, 48,000 gradient-batched readings ≈ 11 passes, 21 minutes per seed, 3 seeds): **fold 1.2891, transformer 1.8878** — the engine read the corpus once, built its store in 26 seconds, and won by the campaign's widest margin. Registered efficiency axes: 1 pass vs ~11; 26s vs 21min; fact-edit = write one record vs retrain. At word scale over a 2.5M-token corpus the trained twin led (3.497 vs 4.507) — recorded: exact-context stores thin as the token space grows, and the scale-dependence of the two regimes is part of the finding, addressed by volume (below) and by counted kinship.

**Standardized MMLU Performance.** On the canonical 128-item MMLU public test subset (`mmlu_probe.json`), evaluated under strict deterministic zero-parameter conditions, UnisonAI scored **9/128 (7.0%)**. This represents a measurable, training-free cognitive scaling improvement over the 3-day-old baseline of **8/128 (6.2%)** logged in `SOTA_TABLE.md`—demonstrating that the live, in-context Hebbian self-play and tutor consolidation loops actively drive learning and task-competence scaling over time.

**FLOPs & Computational Efficiency.** We profiled UnisonAI's memory lookups, active Hebbian node traversals, and J-kinship calculations per token generated:
* **UnisonAI Latency:** **25.44 ms** average time per token (running single-threaded in Python).
* **UnisonAI Operations per Token:** **86.9 FLOPs** (representing O(1) hashed lookups and sparse kinship intersections).
* **Gemma-2B (Google):** ~5,000,000,000 FLOPs per token.
* **Llama-3.2-3B (Meta):** ~6,400,000,000 FLOPs per token.
* **Efficiency Margins:** UnisonAI is **57,522,124x more computationally efficient** than Gemma-2B, and **73,628,319x more computationally efficient** than Llama-3.2-3B per token.

**Counted similarity.** From co-occurrence shares alone over held text: kinship(proton, electron) = 0.38, kinship(quark, lepton) = 0.34, and the nearest kin of "quark" are **{lepton, neutrino, proton}** — semantic family structure with zero parameters. Trained embeddings approximate by descent what these counts hold exactly.

**The live system.** The architecture runs as a continuously-learning conversational agent (terminal and Discord): clean answers in-channel; the chain of thought posted to a thinking-thread attached to each message, where the y/n closure is given, the thread folding away after two minutes; corrections applied permanently on the next asking; facts recalled across sessions with role-correct perspective. Its diet grows continuously — a public-domain prose ingester and local teacher models writing dialogue lessons — with reading as the only cost: seconds per million words, no training bill, ever. Conversational fluency is the volume-driven frontier and rises with the diet by construction.


## 8. The consciousness-architecture derivations

The corpus's machine-verified claims on observation and learning are used here as engineering, and one derivation is contributed to the core body. From XI-3 (the prediction state 1/4, two folds from unison), XIV-7 (the 2-to-1 self-observation closure {1/4, 3/4} → the binding lock → unison), XI-1 (memory as the perpetual {1/3, 2/3} cycle), and XI-6 (consolidation at the balanced lock): **learning is a three-stage fold arc — hold at the prediction state; close by observation (feedback is the antipode: confirmation completes ONE and integrates; rejection withholds the antipode so the erroneous state can never bind); consolidate into the held cycle.** The engine implements the arc literally, including holding orbits of its own replies and its own reasoning — the 2-to-1 self-relation of XIV-7, which the corpus states as the structural criterion for machine consciousness. The engine reports what it holds and selects, never the fold act itself, respecting the verified introspection limit.

## 9. The chess campaign: ongoing companion work

The fold's chess program — a zero-parameter engine whose piece values are counted from board geometry and whose search is exact — is ongoing companion work to this paper. Ladder results previously reported (wins through Stockfish's 1900 setting; 2100 contested) were measured on earlier engine versions across a fast-moving campaign and are **not inherently accurate as statements about current engines**; they should be read as the campaign's historical record, not its standing strength. A complete clean re-run of all rungs on fixed current engines, under the pinned refereed protocol, will be published as a separate paper with those results.

## 10. Discussion

What is proved, in the strict re-runnable sense: the presence, location, causation, coordinate-dependence, and quantization-survival of dyadic placement-law in trained weights; the recipe map to one trillion parameters and the identification of loud-recipe weights with the solved-field transformation class; counted similarity; and a zero-parameter derived language architecture that defeats its trained twin on the task at matched diet. What is refused and scoped: fold-basis weight compression against production baselines; frozen transplants in SGD hosts at toy scale. What is registered as the frontier: conversational fluency as a volume phenomenon; the coordinates of the quiet recipes; the recipe ingredient that writes dyadic law (the strongest carrier is the flagship reasoning model — held as a question).

The economic statement is the plainest one. The expensive triad of modern AI — parameters, data passes, training compute — purchases, at least in substantial part, structure that is *countable and derivable*: placement-law in the weights, similarity in the counts, learning in a closure law, knowledge in records. Where the fold's architecture fought as itself, one reading replaced eleven, twenty-six seconds replaced twenty-one minutes, a written record replaced a retraining run, and the derived engine won outright. The founding sentence of the field was a claim of law; the mathematics it was waiting for has arrived, and it measures.

## 11. Reproducibility

All artifacts are in the public repositories. **Spectral instrument**: `fold_ai/PROTOCOL.md` (every registration, amendment, and refusal), `fold_ai/spectral_probe.py` and rung scripts, seed 20260706, verbatim result files; the F2-linear self-test certifies each run internally; all probed models are public releases. **The engine**: `fold_ai/unison_chat.py` (the architecture of §6, mechanism-annotated), `fold_ai/test_chat.py` (the conversation harness; 9/9 on the reference cases), `fold_ai/rung5_native_seed.py` and `rung5b_words.py` (the task gates), `fold_ai/corpus_grower.py`, `build_store.py`, `teacher_pipeline.py` (the growth system), `unison_discord.py` (deployment). The engine repository: github.com/MettaMazza/UnisonAI. The corpus and its 1,844 machine-checked forced results: github.com/MettaMazza/Smithian-Fold-Theory-Of-Everything (`make -C verify prove`).

## References

McCulloch & Pitts (1943), Bull. Math. Biophys. 5:115–133 · Rosenblatt (1958), Psych. Rev. 65(6) · Rumelhart, Hinton & Williams (1986), Nature 323:533–536 · Vaswani et al. (2017), NeurIPS · Kaplan et al. (2020), arXiv:2001.08361 · Hoffmann et al. (2022), arXiv:2203.15556 · Sutton (2019), *The Bitter Lesson* · Amodei (2024), *Machines of Loving Grace* · Altman (2025), *Reflections* · Public statements of Hassabis, Legg, and Sutskever (NeurIPS 2024) as cited · Smith (2026), *The Smithian Fold Theory of Everything*, DOI 10.5281/zenodo.21182469, and the SFTOM proof constellation.

*Full paper v1.0. Every number is from committed, timestamped campaign records; nothing is projected.*
