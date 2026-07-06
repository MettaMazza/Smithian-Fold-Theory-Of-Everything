# FOLD-AI — Rung 1: are trained neural weights sparse in the fold's spectrum?

Opened 2026-07-06 at Maria's direction. The thesis under test, stated before
any measurement: a trained network's weights encode a function whose LAWFUL
part is a compact object in the fold's own (dyadic/Walsh) coordinates -- the
same basis in which the chess value field concentrated (top-32 = 81-87%
energy, Rung 2.5 of the chess campaign). If trained weights concentrate
beyond nulls, training is (in part) a statistical purchase of structure that
fold mathematics can derive or compress -- the entry point to the fold AI
stack: derive the lawful core, train only the residual.

## Pre-registered design (fixed before any spectrum is computed)

- OBJECTS:
  1. W_enc and W_dec of Maria's trained SAE (gemma4_sae_1m.safetensors),
     row-major flattened, truncated to the largest 2^n <= size.
  2. The largest attention/MLP matrices of Kokoro-82M (local HF cache),
     same packing.
- TRANSFORM: Walsh-Hadamard, natural order, float64 (weights are floats;
  the chess transform was exact-integer -- noted, not hidden).
- STATISTIC: energy concentration C(k) = top-k squared coefficients / total
  energy, at the chess campaign's operating FRACTIONS of the space:
  6.1e-5, 4.9e-4, 3.9e-3 (the 32/256/2048-of-2^19 points).
- NULLS (both must be beaten at a given k for a verdict of structure):
  1. SHUFFLE null: 5 seeded permutations of the same tensor (identical
     value histogram, scrambled placement), same C(k). Seed 20260706.
  2. GAUSSIAN yardstick: iid normal matched to the tensor's mean/variance.
- SELF-TEST (theorem-forced): bit-reversal repacking of the index space is
  F2-linear and must preserve C(k) EXACTLY; a run whose self-test fails is
  void.
- VERDICT per tensor per k: real C(k) vs max(null C(k)); margins reported.
  No threshold tuning after seeing data. Negative results are recorded in
  full -- the chess campaign's own standard.

## What each outcome means (fixed in advance)

- CONCENTRATION BEYOND NULLS: trained weights carry dyadic law; proceed to
  Rung 2 (which components; reconstruction-vs-truncation quality; the
  derive-vs-train split).
- FLAT AT NULL LEVEL: the law (if any) is not in this basis/packing --
  proceed to the packing sweep (the chess campaign's Rung 2.5b lesson:
  relational coordinates nearly halved the error; packings matter).
  A flat verdict here is a verdict on ONE basis, never on the thesis.

## OBJECTS AMENDMENT (2026-07-06, logged post-registration -- Maria's catch)

The SAE named above is an UNTESTED experimental training run (Maria's own
flag): a flat verdict on it would measure that run's convergence, not the
thesis. Its results are DEMOTED to exploratory. Rung 1's validated objects
are released, working, full-precision models from Maria's library, read
directly (no quantized GGUFs in Rung 1 -- 4-bit quantization confounds the
spectrum with the quantizer's own structure):
  1. Stable Diffusion v1.5 (v1-5-pruned-emaonly.safetensors) -- largest 2D
     matrices.
  2. SDXL base 1.0 -- largest 2D matrices.
  3. Kokoro-82M (local) -- largest 2D matrices.
Design otherwise unchanged: same transform, statistic, fractions, nulls,
self-test, verdict rule.

## RUNG 2 REGISTRATION (2026-07-06, before any Rung-2 spectrum)

- ARM A, COMPONENT MAP: every 2D tensor of SD1.5 with >= 2^20 elements,
  same battery (3 shuffle nulls for speed at map scale -- amendment noted;
  verdict rule unchanged). Output: concentration-vs-null margin per
  component class (embedding / attention / FF / conv-as-2D).
- ARM B, PACKING: for the two strongest and two thinnest Arm-A tensors,
  column-major and transpose packings vs the row-major baseline -- the
  chess Rung-2.5b question (do coordinates amplify thin margins?).
- ARM C, TRAINED-VS-UNTRAINED: seeded He-init matrices of matched shapes
  run through the identical battery -- training should ADD structure;
  untrained must sit at null (this is also the instrument's negative
  control).

## RUNG 2 ARMS D+E REGISTRATION (2026-07-06, before any spectrum)

- ARM D, THE FULL LLM: GPT-2 (openai-community, full-precision
  safetensors, the canonical open language model). Objects: token
  embedding (wte) + ALL transformer MLP matrices (c_fc, c_proj, 12
  layers). Same battery, 3 shuffle nulls, row-major AND column-major
  (Arm B's amplification lesson applied from the start).
- ARM E, QUANTIZATION SURVIVAL: Maria's production Llama-3.1-8B GGUF,
  DEQUANTIZED ffn_gate/ffn_up (Q4_K) and ffn_down (Q6_K) at layers
  0/8/16/24/31. Question: does training's dyadic law survive 4-bit
  deployment quantization? Survival -> the compression rung applies
  directly to the models Maria actually serves.

## RUNG 3 REGISTRATION (2026-07-06, before any measurement)

QUESTION: does the located law cash as deployable compression?
- OBJECTS: GPT-2's law-bearing matrices (all 12 c_fc + wte, the Rung-2
  hot class), fold-basis truncated: keep the top-k Walsh coefficients,
  zero the rest, inverse-transform back to weights.
- BUDGETS: k swept at 50% / 25% / 12.5% / 6.25% of coefficients per
  matrix. BASELINE at matched storage: round-to-nearest uniform
  quantization of the same matrices at the bit-width giving the same
  compressed size.
- QUALITY METRIC (fixed in advance, self-contained): on a fixed
  16-prompt set (written into the harness before any run), full-model
  forward pass; report (a) mean KL divergence of next-token
  distributions vs the unmodified model, (b) top-1 next-token agreement
  rate. Lower KL / higher agreement wins at matched budget.
- CONTROL: the same truncation applied to the LAW-QUIET class (c_proj)
  must hurt MORE at the same k if the concentration is real capacity --
  the law-location result made falsifiable at the quality level.
- VERDICT RULE: fold-truncation beats matched-budget quantization on
  both metrics at >= 2 of 4 budgets = the compression rung is TAKEN.

## RUNG 3b REGISTRATION (2026-07-06, before any measurement; after 3's refusal)

Rung 3 refused naive aligned-basis truncation (0/4; recorded). The chess
campaign's own theorems name the two constructions to test before the
compression door closes -- both were proven there:
- ARM A, PACKING SWEEP FOR QUALITY: fold-truncation quality (same metrics,
  same prompts, keep=0.25 and 0.125) under three packings of each c_fc:
  row-major (the refused baseline), column-major, and MORTON (bit-interleaved
  row/column -- the dyadically natural 2D order, the fold's own coordinate
  for a matrix). Verdict: any packing beating row-major KL by >2x reopens
  the compression route through coordinates.
- ARM B, SPECTRUM + EXCEPTIONS (the chess compact-exact construction):
  reconstruction = inverse(top-k spectrum) + the top-m largest residuals
  stored exactly; budgets matched to quantization at the same total bits
  (k coefficient-entries + m exception-entries, 32 bits each vs uniform
  quantization at equal storage). Sweep (k,m) splits 75/25, 50/50, 25/75
  of the same budget at 4 and 3 bits-per-weight equivalents. Verdict rule:
  spectrum+exceptions beats pure quantization on KL at either bit level =
  the construction transfers; both refuse = compression through this basis
  is CLOSED for trained weights and the campaign routes to Rung 4 on
  detection evidence alone (recorded either way).

## RUNG 3b OUTCOME (recorded): REFUSED -- compression through the raw Walsh
basis is CLOSED for trained weights (col-major improved 1.7x, under the 2x
bar; spec+exceptions lost at 4b and tied-in-rubble at 3b -- the 0.3% KL
letter-of-rule edge at 0% agreement is NOT claimed; margin clause missing
from the registration, noted as a registration flaw). Detection results
(Rungs 1-2) stand. Route: Rung 4.

## RUNG 4 REGISTRATION (2026-07-06, before any run)

THE FIRST DERIVATION GATE: derived component vs learned component under
IDENTICAL training -- the chess gate discipline applied to model parts.
- COMPONENT: positional encoding. Baseline: learned positional embeddings
  (the GPT-2 way). Challenger: a DERIVED positional code with zero
  parameters -- the Walsh functions of the position index (the fold's own
  harmonics; the rows of the dyadic character table), fixed, never trained.
- ARENA: two identical small character-level transformers (same dims,
  heads, layers, data, steps, seed), trained on the SFTOM corpus's own
  text. The ONLY difference: learned wpe vs derived Walsh code.
- METRIC: held-out cross-entropy after a fixed step budget; three seeds
  each; the mean decides. Lower loss wins.
- MEANING: a win means a trained component of every GPT since 2018 can be
  REPLACED by a zero-parameter derived object at equal-or-better quality
  -- the first brick of the UnisonAI core. A loss is recorded like all
  the others.

## RUNG 2f REGISTRATION (2026-07-06, before any spectrum): THE SCALING SURVEY

The law-fingerprint across the frontier scale axis, from Maria's library:
Kokoro 82M -> Llama-3.1-8B -> gpt-oss-120B -> Qwen3-Coder-480B (MoE) ->
DeepSeek-R1 671B (MoE) -> Kimi-K2.6 ~1T (MoE). Objects: dequantized FFN
gate/up (expansion) tensors sampled at early/mid/late depth per model; for
MoE giants, individual EXPERT tensors (new question: do experts carry the
fingerprint individually?). Same locked battery (3 shuffle nulls, both
packings, fractions as registered, seed 20260706). Output: margin-vs-scale
curve. Registered predictions (fixed now): the expansion fingerprint
appears at every scale; per the thesis, margin does NOT vanish with scale.
No further prediction on slope -- the curve is the discovery.

## RUNG 4 OUTCOME (recorded): REFUSED. Learned wpe 1.8878 vs derived Walsh
code 2.0269 (3 seeds each, tiny scale: 4L/128d/char-level). The raw Walsh
code as a frozen additive positional organ loses at this scale. Noted for
any future re-match: fixed positional codes are known to close the gap at
scale (Vaswani et al. report sinusoidal ~= learned at full scale), so a
registered larger-scale re-match is legitimate; no variant-grinding at
this scale. NEXT CANDIDATE: the attention gate, from the corpus's own
unit-capacity theorem (verify_attention_capacity, Claim XI-2) -- design to
be registered before any run.

## RUNG 2f AMENDMENT (2026-07-06, on Maria's observation, before the curve
is read as physics): the flat 2^26 probe window truncates large tensors --
a scale-correlated instrument confound (fragments of rows dilute
row-structured concentration). CORRECTED INSTRUMENT registered: per-ROW-
BLOCK spectra -- probe each large tensor as consecutive full-row blocks of
~2^22, take the MEDIAN block margin (median, not max, fixed now). The
scale curve is only read from the corrected instrument; the flat-window
numbers stand as the record of why the correction was needed. Maria's
standing principle, from chess and stated by her here: THE APPROACH MUST
VARY WITH SCALE -- coordinates and windows are per-object, never
one-size-fits-all.

## RUNG 2f OUTCOME (recorded, corrected instrument, complete to 1T):
THE RECIPE MAP. Loud: GPT-2 (12.7-67.6x), Llama-3.1-8B (8.5x),
DeepSeek-R1-671B (43-47x, every row-block, dense + shared-expert -- the
strongest production signal measured). Silent: gpt-oss 20B/120B (~1x),
Qwen3 27B/235B/480B (0.76-1.04x), Kimi-K2.6 ~1T (0.96-1.06x).
CONCLUSIONS FORCED BY THE DATA: scale exonerated (loudest carrier is
671B); architecture exonerated (MoE on both sides); the variable is the
TRAINING RECIPE. Open question, held as a question: the loudest carrier
is the flagship reasoning-RL model. Registered predictions: "fingerprint
at every scale" REFUTED as stated -- the fingerprint is per-recipe, not
universal; "margin does not vanish with scale" CONFIRMED within loud
recipes (R1). Maria's principle codified: the approach varies with the
object; the object is the recipe.
