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
