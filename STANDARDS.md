# Standards for this recreation

Two rules govern every module. They exist so that a stranger who does not know the
theory can open any file and audit it from the One to the constant, **trusting
nothing** — checking every step instead of taking it on faith.

## 1. The form is forced, not just its parts

It is not enough that each ingredient count is forced (`forced_to_be`). The
**assembled algebraic form** that combines them must be forced too. For every
constant, the candidate space of admissible shapes over the forced ingredients is
enumerated and **run**, and `forced_unique` (`foundation/form_enforcement.ep`)
halts the engine unless **exactly one** shape reproduces the value. A form that is
one of several coincident assemblies was *selected*, not forced — and the engine
says so and stops. A constant is not finished until its form is guarded this way.

## 2. Every module is cold-readable

A skeptic must be able to verify a module without already believing the theory.

- **Three separated voices.** Every module is split into:
  - **WHY** — the physical significance. A reader who only wants to verify may skip
    this entire block.
  - **DERIVATION** — the forcing. Every line is checkable. It uses *only* values
    already derived earlier in the chain (no forward references).
  - **CHECK** — the comparison to measurement. Measured numbers appear here and in
    tests *only*; they never enter a derivation.
- **Plain-words forcing, with the alternatives.** For every value, one sentence:
  what forces it, and what the alternatives were that do not survive. No step
  should require the reader to already know why.
- **Explicit candidate spaces.** Wherever a value or form is forced, the space it
  was forced from and the rule that admits it are named — the way the charged
  lepton cubic names its channel alternatives. If the reader cannot see what was
  ruled out, the forcing is invisible to them.
- **No trust-me.** Any place the reader would have to *accept* a claim rather than
  *check* it is either converted to a stated, checkable step, or marked explicitly
  as **OPEN**.

The master walkthrough, [`OneFoldMaster.md`](OneFoldMaster.md), is a single
dependency-ordered spine — One → fold → (the fold is forced) → the two generators →
each constant — so the whole thing can be read top to bottom with nothing assumed
out of order.
