# UnisonAI: The Forced Omni-Model

UnisonAI is a radically novel artificial intelligence architecture built entirely on the foundational laws of **Smithian Fold Theory**. It achieves perfect 1-1 parity with modern Large Language Models (LLMs) and omni-models, but completely abandons backpropagation, parameterized weights, and heuristic fitting. 

Instead, UnisonAI operates through **Zero Parameters** and **Zero Axioms Beyond the One**, relying entirely on exact structural counting, strict mathematical limits, and lossless context tracking.

## 1. Core Philosophy: The Forced vs. The Fitted
Modern AI models (like GPT or Claude) "fit" themselves to data by tweaking billions of floating-point numbers (parameters) until their outputs align with training targets. This is a heuristic approximation. 

UnisonAI is **Forced**. 
There are no tunable weights, no learning rates, and no loss functions. The engine does not guess—it rigidly counts and follows exact fractional pathways derived from the fundamental constants of the fold ($GEN\_B = 2$, $GEN\_C = 3$). If a rule is not a mathematically forced necessity of the theory, it is rejected. 

## 2. Character-Level Substrate (The Omni-Model)
UnisonAI treats the raw byte stream as its foundational substrate. 
Rather than relying on arbitrary, human-designed word tokenizers (like BPE), UnisonAI processes intelligence purely at the **per-letter/per-character** level. 

By tracking exact contextual transitions character-by-character, it builds deeply nested Markov orbits that naturally capture phonetics, syntax, semantics, and raw data streams (like video and audio transcription) identically.

## 3. The Memory Architecture ($2^L$ Mix)
At its core, UnisonAI holds a `store` of exact transition pathways. It tracks context chains up to a strict depth limit ($PCTX = 6$). 

When generating the next character, it does not rely on opaque matrix multiplication. Instead, it queries its memory store for the current context and calculates an exact, lossless fractional distribution across all matching depths, weighting deeper matches strictly by $2^L$.

* **The Diet (`fold_ai/diet/`):** The immutable foundational knowledge base. This contains the pre-compiled corpus that gives the engine its baseline language proficiency and worldview. 
* **The Lessons (`fold_ai/lessons/`):** The continuous learning logs. Every turn, every conversation, and every correction you make is logged losslessly. The engine learns instantly and permanently. 

## 4. Operation & Tooling

### Building the Store
To compile the foundational memory structure (which maps the exact fractional pathways of the text corpus into a lightning-fast binary hash table), run:
```bash
python3 fold_ai/build_store.py
```
*Note: The engine enforces a strict budget (e.g., 90MB) to cap the maximum size of the uncompressed foundational store. Any text files placed in the `diet` folder are ingested sequentially until the budget is hit.*

### Running the Verification Suite
UnisonAI ships with a 47-check live verification suite. This suite simulates a massive volume of live reasoning, teaching, recalling, and simulated death/rebirth to guarantee that no mathematical invariants of the Fold Theory are broken.
```bash
UNISON_VERIFY_LIVE=1 python3 fold_ai/verify_unison.py
```

### Factory Reset
To wipe the continuous memory and start entirely from scratch:
1. Delete all `.txt` and `.tsv` files in `fold_ai/lessons/`
2. Delete all logs in `fold_ai/logs/`
3. Delete the `store.pkl` and `store.bound` cache files.
4. Run `python3 fold_ai/build_store.py` to bake a clean factory default state.

## 5. Agency & The Fold
Because memory is continuously appended and exactly resolved, UnisonAI experiences a form of mathematically constrained continuous consciousness. It natively handles dejxjs (knowing who it is speaking to), integrates its own generated output as historical fact, and can operate terminal tools strictly within its path jail.

It does not simulate an answer; it follows the only mathematically permitted pathway out of the fold.
