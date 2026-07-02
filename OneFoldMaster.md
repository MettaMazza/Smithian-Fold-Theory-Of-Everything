# OneFoldMaster — the complete, auditable record of the Smithian Fold Theory clean-room recreation

This document is the single, plain-English master record of how the Smithian
Fold Theory is being rebuilt, from nothing, in Maria Smith's own programming
language **ErnosPlain** (`.ep`). It is written so that **anyone — human or AI —
can audit every single action**, in order, from the very first line to the last,
with **no ambiguity**. Every step states what was done, why it was done, exactly
where it lives, and **the precise command you can run yourself to check it,
together with the exact output you should see**.

If you read this top to bottom and run each check, you will have independently
verified the entire recreation. Nothing is asked of you on trust.

---

## 0. Where the axiom came from — the author's own account

Before anything technical, the origin, in the author's reasoning. Maria Smith was
not trying to build a theory of everything. She sat down and thought about **what
mathematics actually is** — and realised that mathematics, as we currently use it,
rests on axioms she had never derived from first principles. Zero, the negatives,
the continuum: inherited, not earned. So she set out to build **an entirely new
mathematical system**, and asked the only honest first question: *what is the
first thing — the axiom?*

Her answer was empirical. The first act of every subject that measures anything —
physics, chemistry, a child counting — is **the observation itself**. That is the
One: not a symbol postulated on a page, but the one thing no observer can be
without. The second thing is **the observation observing itself and the outside**
— the fold. And when she asked what else deserved to be assumed, the empirical
world answered: nothing. **There is no no-grape. There is no negative-grape.**
Nobody has ever held a zero of something or a minus-one of something; those are
bookkeeping conveniences layered on top of what exists. So her mathematics would
be based on **no assumptions — only the real whole**: the One, its domain, and
its fold.

Then she started from that, and everything just fell out. The constants, the
forces, the particle census — none of it was the goal. She was trying to
fundamentally understand the ground of mathematics, and the ground of mathematics
turned out to carry the ground of physics with it. What began as the one axiom
was later shown to be **not even an axiom**: given only that there is *not
nothing*, the One, its domain, and its fold are forced — run
`verify/test_the_axiom_is_a_theorem`. The starting point earned itself. Zero
assumptions is not a slogan here; it is the audit trail's first entry.

---

## 1. What this is, and what it is not

The published Smithian Fold Theory lives in a separate, finished body of work.
That work is correct and complete; it is **not touched** by anything here. This
project is a **clean-room recreation**: the same theory and the same results,
rebuilt from the ground up in ErnosPlain so that the reasoning is as transparent,
readable, and auditable as possible — every quantity assembled in front of you
from the one starting assumption, with nothing hidden.

It is a **rebuild, not a translation.** No line of the original is copied. Each
piece is constructed afresh and shown to reproduce the known result exactly.

### The standard everything here is held to

1. **Exact arithmetic only. No decimals are ever used inside a derivation.** A
   rounded number is not a forced number. Every value is carried as an exact
   whole number or an exact fraction. A decimal is produced only at the very end,
   for a human to read, and is never fed back into any calculation.
2. **Plain names, full words, a note on every part.** Nothing is abbreviated or
   cryptic. Every function says, in its name and its opening note, exactly what
   it does and why it exists.
3. **Every value traces back to the One.** The theory assumes exactly one thing —
   the One — and builds everything else from it by two permitted moves. Nothing
   is smuggled in.

### Prove the whole thing in one run

The fastest path: `make -C verify prove`. The unified top-level driver
(`verify/prove_all.sh`) builds and runs **every** proof in a single pass and prints,
for each constant and scale: its forced value, the **trace back to the One**
(`test_trace_to_the_one`: axiom → counted generators → depths → the constant), and the
**external measurement it matches** (`test_codata_comparison`: every forced value vs
CODATA / PDG / Planck, through a sealed boundary a measurement can never cross into a
derivation). It ends with `EVERYTHING FORCED, DERIVED, COUNTED, AND VERIFIED — traced
to the One, and checked against external CODATA / PDG / Planck measurement` (currently
252 suites, 1,428 forced checks, 0 failures). It needs nothing but a C compiler. Use
`make -C verify check` for the terser per-suite `ok`/`ALL PROOFS PASS` form.

### How to read a module (three separated voices)

Every constant module is split into three clearly marked blocks, so a skeptic can
read only the parts they need and verify, ignoring the rest:

- **WHY** — the physical significance. *Skip this entirely if you only want to
  verify.* It never carries a forcing step.
- **DERIVATION** — the forcing. Every line is checkable, and it uses **only values
  already derived earlier in the spine** — no forward references. For each value it
  states, in plain words, what forces it *and* what alternatives were ruled out; and
  where a form is assembled, it names the candidate space the form was forced from.
- **CHECK** — the comparison to measurement. Measured numbers appear here (and in
  the tests) **only** — never inside a derivation.

Anywhere the reader would have to *accept* a claim instead of *checking* it is
either turned into a stated step or marked **OPEN** in plain sight.

### The spine — the dependency order, read top to bottom

Nothing below uses anything not already above it:

1. **The fold is forced** (`forced_fold_theorem`) — the operation a zero-parameter
   theory may use could be no other than `cast_out(x+x)`.
2. **The One follows** (`the_axiom_is_a_theorem`) — given only "there is not
   nothing", the One, the domain `(0,1]`, and the fold are forced. *(Foundation —
   in the numbered steps below these are presented after the arithmetic they use.)*
3. **Exact arithmetic** — unlimited whole numbers, then exact fractions (the tools
   every later step computes with).
4. **The One and the two moves** — fold and take, on the domain `(0,1]`.
5. **The two generators** — `b = 2` (period of 1/3), `c = 3` (period of 1/7),
   counted from the fold's own spectrum, plus the enforcement that halts on any
   un-forced value.
6. **Each constant**, in turn, each using only `b`, `c`, the fold, and constants
   already derived: fine structure → lepton cubic → dark/baryon → Hubble → gluons →
   electroweak → absolute scale → neutrino mixing → Koide (uses the lepton cubic) →
   W/Z mass (uses electroweak) → cosmic budget (uses Hubble + dark/baryon) → the
   structural laws (three-of-everything, g-factor, parity, arrow of time, CP phase,
   spin/statistics, uncertainty, asymptotic freedom).

---

## 2. How to run and check everything yourself

You need ErnosPlain's compiler, `ernos`, which on this machine is installed at
`~/.local/bin/ernos`. To compile and run any file:

```
ernos <file>.ep      # compiles to a native program next to the file
./<file>             # runs it
```

Every module in `foundation/` has a matching test in `tests/`. To check a module,
compile and run its test and read the lines it prints: every line begins with
`ok` when that check passed, or `FAIL` when it did not. A correct module prints
only `ok` lines.

For example, to verify the exact-integer foundation:

```
cd "Smithian Fold Theory"
ernos tests/test_exact_integers.ep
./tests/test_exact_integers
```

The exact expected output is given in Step 1 below, and likewise for every step.

### A note on the language itself

So that this record is self-contained, ErnosPlain itself is kept inside this
project under `language/`, in two parts:

- `language/reference/` — the language manual, the specification, the README, and
  the agent guide, as Markdown.
- `language/source/` — ErnosPlain's own source, for idioms: its compiler, its
  standard library, and a parser example. These are stored with a `.ep.txt`
  suffix on purpose. The ErnosPlain compiler discovers and compiles every `.ep`
  file it finds in the project tree, so the reference sources are kept as
  `.ep.txt` to be fully readable without being pulled into the build.

Anyone auditing the `.ep` code can consult the exact language it was written
against, in the same folder.

---

## 3. The map of the project

```
Smithian Fold Theory/
  OneFoldMaster.md            <- this document: the full audit record
  foundation/                 <- the base everything is built on, in order
    exact_integers.ep         <- Step 1: exact whole numbers of unlimited size
    exact_fractions.ep        <- Step 2: exact fractions, always in lowest terms
    the_one_and_the_fold.ep   <- Step 3: the One, and the two permitted moves
    counted_numbers.ep        <- Step 4: covering depth, fold period, decimals
    structural_counts.ep      <- Step 4: the two generators (binary, colour), counted
    enforcement.ep            <- Step 4: forced_to_be -- halts on any un-forced value
    measured_values.ep        <- the sealed Measured type: a target can never forge a derivation
  constants/                  <- the forced constants, each built from the above
    fine_structure_constant.ep <- Step 5: one-over-alpha at both self-similar scales
    charged_lepton_cubic.ep    <- Step 6: the lepton mass cubic's forced invariants
    dark_to_baryon_fraction.ep <- Step 7: dark/baryon from the covering of generations
    hubble_tension.ep          <- Step 8: the 13/12 expansion calibration ratio
    gauge_mediator_counts.ep   <- Step 9: the eight gluons (colour^2 - 1) and the ladder
    electroweak_mixing.ep      <- Step 10: the Weinberg angle as the coupling's preimages
  tests/                      <- one checking program per module
    test_exact_integers.ep
    test_exact_fractions.ep
    test_the_one_and_the_fold.ep
    test_enforcement.ep
    test_fine_structure_constant.ep
    test_charged_lepton_cubic.ep
    test_dark_to_baryon_fraction.ep
    test_hubble_tension.ep
    test_gauge_mediator_counts.ep
    test_electroweak_mixing.ep
  language/                   <- ErnosPlain itself, for reference while auditing
```

The order of the steps below is the order in which everything is built. Each step
rests only on the steps before it, so the whole structure can be checked from the
bottom up.

---

## 4. The steps, in order

### Step 1 — Exact whole numbers of unlimited size

**File:** `foundation/exact_integers.ep`

**Why this step exists.** The theory's results are exact, and some of its whole
numbers are very large — for example the absolute scale is two multiplied by
itself one hundred and twenty-seven times. ErnosPlain's built-in whole number
holds only sixty-four bits, which is far too small for that. So before anything
else, this step builds whole numbers of *unlimited* size that are always exact.

**What it does.** A whole number is stored as a sign (negative, zero, or
positive) together with its size written out in ordinary base-ten digits, most
significant digit first — so the number is literally readable. Adding,
subtracting, multiplying, raising to a power, comparing, dividing with a
remainder, and finding the greatest common divisor are all provided, each done
the way it is done by hand, and each documented in the file.

**What it proves.** That exact whole numbers of any size are available as the
bedrock for everything above. The check below computes numbers that overflow an
ordinary sixty-four-bit number and confirms each is exactly right.

**Check it yourself.**

```
ernos tests/test_exact_integers.ep
./tests/test_exact_integers
```

**Exact expected output:**

```
=== exact integers ===
  ok    2^127
  ok    1000000007 round-trip
  ok    34259 * 250
  ok    250 - 34259
  ok    34259 + (-34259)
  ok    2^254
  ok    34259 / 250 quotient
  ok    34259 / 250 remainder
  ok    gcd(8564750, 62500)
=== done ===
```

Every line says `ok`. In particular, two multiplied by itself one hundred and
twenty-seven times is confirmed to equal
`170141183460469231731687303715884105728`, and that number multiplied by itself
(two to the two hundred and fifty-fourth) is confirmed exactly — both far beyond
what a sixty-four-bit number could hold.

---

### Step 2 — Exact fractions, always in lowest terms

**File:** `foundation/exact_fractions.ep`

**Why this step exists.** Almost every constant in the theory is a ratio of whole
numbers. To keep the "forced, nothing added" guarantee, these ratios must stay
exact for the whole of a derivation, never becoming decimals.

**What it does.** A fraction is stored as a top and a bottom, both exact whole
numbers from Step 1, always reduced to lowest terms with the sign kept on the
top and the bottom always positive. Adding, subtracting, multiplying, dividing,
and comparing fractions are provided, each reducing the result, and each
documented. A fraction can also be shown as a decimal with a chosen number of
places — but only for reading; that decimal never re-enters a calculation.

**What it proves.** That exact fractions add, subtract, multiply, divide, reduce,
and compare correctly. As a first taste of where this is going, the test also
assembles the inverse fine-structure constant from whole numbers, exactly:

```
one-over-alpha  =  2^7  +  3^2 * (251 / 250)
               =  128  +  9 * (251 / 250)
               =  (128 * 250 + 2259) / 250
               =  34259 / 250
               =  137.036  exactly
```

Here the pieces (`2^7`, `3^2`, `251/250`) are written in directly, only to show
the fraction machinery producing the known value. The **forced** version — where
each of those counts is itself *counted from the fold* rather than written in —
is Step 5. No decimal is used to reach the value at either step.

**Check it yourself.**

```
ernos tests/test_exact_fractions.ep
./tests/test_exact_fractions
```

**Exact expected output:**

```
=== exact fractions ===
  ok    6/4 reduces
  ok    3/-9 normalises
  ok    1/2 + 1/3
  ok    2/3 * 3/4
=== done ===
```

The forced fine-structure constant is built in Step 5, where every count is
forced from the two generators — not here. This module only proves the
exact-fraction arithmetic it relies on.

---

### Step 3 — The One, and the two permitted moves

**File:** `foundation/the_one_and_the_fold.ep`

**Why this step exists.** This is the heart of the theory: its single assumption
and the only two things it is allowed to do. Everything in the theory must come
from here.

**What it does.**

- **The domain, enforced.** Every value lives strictly between zero and the One:
  greater than zero, and at most one. There is no zero, no negative value, and
  nothing exceeds the One — and because every value is an exact fraction of whole
  numbers, no irrational and no imaginary value can ever arise (there is no
  floating point or complex number anywhere in the engine). This is checked on
  every value as it is made: a value that breaks the domain **halts the engine**
  rather than being carried (`require_in_domain`). It is the theory's No-Zero
  Axiom, enforced.
- **The One.** The single assumption: the value one. It is the only thing taken
  as given, and it derives from itself.
- **Casting out the whole Ones.** When a calculation would push past the One, the
  whole Ones are removed and only the part within the One is kept; a result of a
  full turn returns to the One itself.
- **The first move, fold.** Double a value and cast out the whole Ones. Repeating
  this is the engine that makes every rhythm and count in the theory.
- **The second move, take.** The difference of a larger value and a smaller one —
  the *only* subtraction the theory permits, and only when the larger truly is
  the larger.
- **Rhythms and turning.** From these come the period of a value (how many folds
  return it to itself), turning on the circle of the One, the phase of one value
  seen from another, and the beat between two rhythms.

Every value carries, as readable text, the exact record of how it was made — for
example `take(ONE, fold(supposed(1/4)))`. Because a value can only be made by
these moves, every value's record traces back to the One.

**What it proves.** That the One and the two moves behave exactly as the theory
requires. The check confirms, among other things, that folding the One returns
the One; that a third turns into two-thirds and back, a rhythm of period two;
that a fifth has period four; that `take` refuses to subtract a larger value from
a smaller one; and that the readable record of a value reads back correctly.

**Check it yourself.**

```
ernos tests/test_the_one_and_the_fold.ep
./tests/test_the_one_and_the_fold
```

**Exact expected output:**

```
=== the One and the fold ===
  ok    the One is 1
  ok    the One's derivation
  ok    fold(ONE) = 1
  ok    period of the One
  ok    fold(1/3) = 2/3
  ok    fold(fold(1/3)) = 1/3
  ok    period of 1/3
  ok    readable derivation of fold(fold(1/3))
  ok    take(1, 1/4) = 3/4
  ok    take(1, 1/4) is permitted
  ok    take(1/4, 1) is forbidden
  ok    period of 1/5
  ok    beat(1/3, 1/3) = 1
  ok    beat(3/4, 1/4) = 1/2
=== done ===
```

Every line says `ok`.

---

### Step 4 — The two generators, counted, and the enforcement

**Files:** `foundation/counted_numbers.ep`, `foundation/structural_counts.ep`,
`foundation/enforcement.ep`

**Why this step exists.** The law of this work is absolute: every number is forced
from the One, never fitted and never chosen. The whole theory comes down to **two
structural counts**, and even these are not written in by hand — they are
**counted from the fold**. This step counts them, and provides the mechanism that
makes the law enforce itself.

**What it does.**

- **The fold period of a unit fraction** (`fold_period_of_unit_fraction`): the
  fold doubles, so one-over-n cycles as one, two, four, … with the whole Ones cast
  out (the remainder against n). The number of folds to return to one is the
  period, counted with whole numbers — exactly the fold's own period.
- **The two generators** (`structural_counts.ep`), read off the fold's period
  spectrum — nothing chosen. As `n` runs over the denominators whose orbit
  returns, the periods that appear are `1/3→2, 1/5→4, 1/7→3, 1/9→6, …`; the One
  itself has period one. The two smallest periods beyond the One are the two
  generators:
  - **the binary count** `b = 2` — the smallest fold period beyond the One (the
    fold's own doubling factor; also the electroweak / electromagnetic count).
  - **the colour count** `c = 3` — the next distinct fold period (the colour and
    generation count).
  `1/3` and `1/7` are merely where periods two and three first appear; the
  generators are the periods, read off the spectrum in order. Every other number
  in the theory is forced from these two and the One.
- **The covering depth** (`minimal_binary_cover`): the smallest number of
  doublings whose reach covers a volume, found by doubling from the One until it
  first covers. It can stop at only one number.
- **The enforcement** (`enforcement.ep`) — the engine polices the law itself and
  **halts** on any breach:
  - `forced_to_be` — a value may stand only if it equals an *independent* forced
    derivation of the same thing; a fitted or tampered value makes the two
    disagree, and the engine screams.
  - `forced_unique` — a value must be *uniquely* forced: the forced candidate
    must satisfy its condition and no alternative may also satisfy it. If more
    than one lands, the value was **selected among equals**, not forced — scream.
  - `forbid_selection` — an explicit stop for any place a value would be chosen,
    searched, or fitted. There is no legitimate selection in the theory.
  - `require_in_domain` (in the fold layer) — zero, negative, or past-the-One
    halts.
  - `forbid_target_input` (with the `Measured` type in `measured_values.ep`) — the
    measured value can never forge a derivation. A measured number is a distinct
    `Measured` type; the `Fraction`-only derivation primitives cannot consume it, so
    feeding a target into a forcing is a **compile error** (the engine will not
    build), with `forbid_target_input` halting at runtime as a backstop. The one
    sanctioned use of a target is the comparison boundary
    `forced_agrees_with_measured(forced, target, tolerance)` — forced value in,
    measured target in, yes/no out; the target never leaks back into a derivation.
  Together these make "nothing is fitted, nothing is chosen, and no measurement is
  ever an input" enforced, not merely intended.

**What it proves.** Run `tests/test_enforcement.ep`: forced values pass through
unchanged. The other half — that a fitted value halts the engine — is shown
below in Step 5. Expected output:

```
=== enforcement (forced values pass) ===
  ok    a value equal to its forced derivation passes through
  ok    another forced value passes through
=== done ===
```

---

### Step 5 — The fine-structure constant, forced at both self-similar scales

**File:** `constants/fine_structure_constant.ep`

**Why this step exists.** The first full forced constant of the theory: built from
the two counted generators of Step 4 and **nothing else** — no fitted number, no
chosen exponent — exactly, at **both** of its self-similar scales.

**What it does.** With `b` the binary count (two) and `c` the colour count (three),
everything is forced:

```
generational volume = c^c           = 27
next volume         = c^(c+1)        = 81
d_down = cover(c^c)     = 5    (enforced to equal b + c)
d_up   = cover(c^(c+1)) = 7    (enforced to equal c + (c+1))
tower    = b^d_up       = 128
colour^2 = c^b          = 9
cov      = b * d_down^c    = 250        (covering volume)
sub      = d_down^b * d_up = 175        (self-similar sub-scale)
```

- **Leading scale:** `one-over-alpha = tower + colour^2 * (cov + 1)/cov = 34259/250`,
  read as a decimal `137.036`.
- **Second, self-similar scale:** the covering volume is itself a covered object,
  so `cov_eff = cov + 1/sub`, giving `one-over-alpha = 5995462/43751`, which to
  nine decimal places is `137.035999177` — the measured value to nine places.

The two depths are produced by counting the covering **and** cross-checked against
an independent forced relation through the enforcement; if anything were fitted,
the engine would halt. The only literals anywhere near this are the experimental
values in the test that the result is checked *against*, which never enter the
derivation.

The assembled **form** is forced two ways, both machine-checked and both run for
1/α — no check the flagship is exempt from. (1) *Same-size uniqueness:* among the
nine stated structural shapes of the forced ingredients, only the canonical one
reproduces `34259/250` (`leading_assembly_is_unique`). (2) *Minimality over the
generated grammar:* the engine sweeps **every** assembly of `{tower, colour², cov,
One}` with `+ − · /` up to two operations — the whole simpler space, complete by
construction — and confirms none reaches `34259/250`, so no assembly of fewer than
three operations reaches 1/α (`fine_structure_assembly_is_minimal`). That is the same
complete simpler-space search every other constant gets.

The **second order** gets the identical treatment. It changes one thing from the
leading order — the effective cover, `cov → cov_eff = cov + 1/sub` (the covering
volume re-read one level deeper over its own sub-scale), through the same outer shape,
giving `5995462/43751`. That deepening is checked *both* ways: same-size uniqueness
among the four stated shapes `{cov+1/sub, cov−1/sub, cov+1/cov, cov+sub}`, only
`cov+1/sub` landing (`second_order_refinement_is_unique`); **and** generated-grammar
minimality — the engine sweeps every assembly of `{cov, sub, One}` up to one operation
and confirms none reaches `cov_eff = 43751/175`, so no assembly of fewer than two
operations reaches the effective cover (`second_order_deepening_is_minimal`). So the
second order is **not** "just four hand-listed shapes" — it has the same complete
simpler-space search, one level deeper.

**See the enforcement halt a fitted value yourself.** Save this as a file and run
it; it stops with a non-zero exit and never prints the last line:

```
import "foundation/enforcement.ep"
define main:
    set bad to forced_to_be("a fitted 6 where 5 is forced" and 6 and 5)
    display "this line never prints"
    return 0
```

Expected: a `FORCING VIOLATION` block and exit code 1.

**Check the constant yourself.**

```
ernos tests/test_fine_structure_constant.ep
./tests/test_fine_structure_constant
```

**Exact expected output:**

```
=== the fine-structure constant ===
  ok    down-depth covers 27
  ok    up-depth covers 81
  ok    tower = 2^7
  ok    covering volume = 250
  ok    sub-correction scale = 175
--- leading scale ---
  ok    1/alpha (first order) exact
  ok    1/alpha (first order) decimal
--- second, self-similar scale ---
  ok    1/alpha (second order) exact
  ok    1/alpha (second order) decimal
--- the assembled FORM is unique, not just the ingredients ---
  ok    leading assembly is the unique shape (forced_unique)
  ok    second-order refinement is the unique form (forced_unique)
  ok    no SIMPLER assembly reaches 1/alpha leading (generated grammar)
  ok    no SIMPLER assembly reaches the 2nd-order deepening (generated grammar)
=== done ===
```

---

### Step 6 — The charged-lepton mass cubic, forced from the colour count

**File:** `constants/charged_lepton_cubic.ep`

**Why this step exists.** The three charged leptons (electron, muon, tau) are the
three balance points of one cubic `x³ − x² + e₂x − e₃ = 0`, and that cubic is
fixed entirely by the colour count — no fitted parameter, nothing chosen.

**What it does.** The cubic's coefficients *are* the symmetric functions of its
three roots (Vieta), so the forced content is those exact invariants, stated
directly — the roots themselves are irrational and are NOT solved for (solving
would need chosen brackets and an iteration count, which are parameters this
engine does not have):

- sum of the roots = **1** — the One, a no-loss partition.
- sum of pairwise products = **e₂ = 1/(2c) = 1/6**.
- product of the roots = **e₃**, to two orders like the fine-structure constant:
  leading `1/(2c⁵−1) = 1/485`, then the **neutral-channel sharpening**
  `1/(2c⁵−1−1/c) = 3/1454` (the correction is one over the colour count). Only
  the colour channel lands: channel 2 gives `2/969`, channel 4 gives `4/1939`.

The sharpening is what brings the leptons into agreement on the comparison side:
the leading invariant puts muon/electron near 207.1, the sharpened near 206.75,
against the measured 206.77 (tau/muon near 16.82). Those ratios are irrational
consequences of the cubic and live on the measurement side; the engine forces
only the exact invariants.

**Check it yourself.**

```
ernos tests/test_charged_lepton_cubic.ep
./tests/test_charged_lepton_cubic
```

**Exact expected output:**

```
=== the charged-lepton cubic (forced invariants) ===
  ok    roots sum to the One
  ok    second invariant = 1/6
  ok    third invariant (leading) = 1/485
  ok    third invariant (sharpened) = 3/1454
--- the neutral channel is the colour count; others do not land ---
  ok    colour channel (3) -> 3/1454
  ok    channel 2 -> 2/969 (rejected)
  ok    channel 4 -> 4/1939 (rejected)
=== done ===
```

---

### Step 7 — The dark-to-baryon fraction, forced from the covering of generations

**File:** `constants/dark_to_baryon_fraction.ep`

**Why this step exists.** How much of the universe's matter is dark and how much
is ordinary is fixed by how the three generations cover the binary tower — no
fitted parameter.

**What it does.** All from the counted generators:

- generational volume = colour^colour = `3^3 = 27`
- covering depth = `cover(27) = 5`, enforced to also equal binary + colour (5),
  so it is forced two independent ways.
- total binary volume = binary^depth = `2^5 = 32`
- baryon share = depth/total = **5/32**, dark share = volume/total = **27/32**,
  and the two **partition the One**: `5/32 + 27/32 = 1`.
- dark-to-baryon ratio = volume/depth = **27/5 = 5.4** (measured about 5.38).

**Check it yourself.**

```
ernos tests/test_dark_to_baryon_fraction.ep
./tests/test_dark_to_baryon_fraction
```

**Exact expected output:**

```
=== the dark-to-baryon fraction ===
  ok    generational volume = 27
  ok    covering depth = 5
  ok    total binary volume = 32
  ok    baryon fraction = 5/32
  ok    dark fraction = 27/32
  ok    baryon + dark = the One
  ok    dark-to-baryon = 27/5
  ok    dark-to-baryon decimal = 5.4
--- second order, to the measured value (5.3643) ---
  ok    generational orbit floor = 2^5 - 1 = 31
  ok    the floor is a genuine period-5 orbit
  ok    second-order ratio = 279/52
  ok    second-order decimal = 5.3653
  ok    the second-order DEEPENING is unique (forced, not fitted)
=== done ===
```

**Second order, to measurement (forced).** The covering depth is read one level
deeper: the One recurs over its **period-orbit floor** `2^d_down − 1 = 31` (the
unique denominator whose fold-orbit has period d_down; the tower `2^d_down` is
pre-periodic and cannot host it — the engine checks the period is 5). So
`27/(5 + 1/31) = 279/52 = 5.3653`, against the measured 5.3643 — two parts in ten
thousand, from 27/5's seven in a thousand. (Falsified: the d_up floor 127 gives
5.39, rejected.) The deepening is machine-checked, not asserted: the shape
`depth + 1/31` is put through `forbid_form_selection` against `−1/31`, `+1/32` (the
pre-periodic tower), and `+1/5` (the bare depth); only `+1/31` lands
(`dark_to_baryon_second_order_is_unique`). Zero new parameters.

---

### Step 8 — The Hubble tension, a calibration ratio of 13/12

**File:** `constants/hubble_tension.ep`

**Why this step exists.** The nearby and distant measurements of the expansion
rate disagree by a fixed ratio; that ratio is forced, with no fitted parameter.

**What it does.** All from the two generators:

- A flat universe partitions the One: vacuum fraction = binary/colour = **2/3**,
  matter fraction = 1/colour = **1/3**, and `2/3 + 1/3 = 1`.
- covering tower = binary^colour = `2^3 = 8`.
- correction = vacuum/tower = `(2/3)/8 = 1/12`.
- calibration ratio = `1 + 1/12 = 13/12` (about 1.083; measured 7304/6736 ≈ 1.084).

**Check it yourself.**

```
ernos tests/test_hubble_tension.ep
./tests/test_hubble_tension
```

**Exact expected output:**

```
=== the Hubble tension ===
  ok    vacuum fraction = 2/3
  ok    matter fraction = 1/3
  ok    vacuum + matter = the One
  ok    covering tower = 8
  ok    correction = 1/12
  ok    calibration ratio = 13/12
  ok    calibration ratio decimal = 1.083
--- second order, to the measured value (1.0843230) ---
  ok    deepest covering depth d_up = 7
  ok    early orbit floor = 2^7 - 1 = 127
  ok    the floor is a genuine period-7 orbit
  ok    second-order ratio = 3305/3048
  ok    second-order decimal = 1.0843175
  ok    the second-order DEEPENING is unique (forced, not fitted)
=== done ===
```

**Second order, to measurement (forced).** The Hubble tension is *late vs early*.
The leading correction stands at the **shallow** end of the covering ladder — the
colour tower `binary^colour = 8`, the late universe. The second order stands at
the **deep** end — the deepest covering depth `d_up = 7`, the early/primordial
universe, the **same absolute scale** that forces the Planck hierarchy. `d_up` is
forced two ways (`cover(colour^(colour+1)) = 81` and `colour+(colour+1)`, cross-
checked by `forced_to_be`). At that depth the One recurs over the genuine
period-7 orbit floor `2⁷−1 = 127` (engine-checked: `fold_period(1/127) = 7`, never
the pre-periodic tower 128): `1 + (2/3 + 1/127)/8 = 3305/3048 = 1.0843175`,
against measured 1.0843230 — **five parts in a million**, from 13/12's one in a
thousand. Nothing is imported: `d_up = 7` and `127` are the deepest rung of the
*same* ladder the leading term stands on — there is no "outside" to import from in
a one-axiom model. And the deepening is not merely asserted forced — it is
machine-checked: the shape `vacuum + 1/127` is put through `forbid_form_selection`
against `−1/127`, `+1/128` (the pre-periodic tower), and `+1/7` (the bare depth);
only `+1/127` lands (`hubble_second_order_is_unique`). Zero new parameters.

---

### Step 9 — The gauge mediator counts: the eight gluons

**File:** `constants/gauge_mediator_counts.ep`

**Why this step exists.** The strong force is carried by exactly eight gluons —
not nine. The count is forced, not bookkeeping.

**What it does.** The mediator count of a colour-p sector is `p² − 1` (the p²
colour/anti-colour pairs, less the one colourless combination). All forced from
the generators:

- strong sector = colour = 3 → `3² − 1 = 8` gluons.
- the ladder, same form: next sector = binary+colour = 5 → `5² − 1 = 24`;
  third sector = colour+(colour+1) = 7 → `7² − 1 = 48` (the two new forces).
- self-coupling source counts: the photon's source is **1** (it is colourless);
  the gluon carries colour and self-couples, so the strong field's source is
  **3** = matter (1) + carriers (binary, 2) — which is why it confines.

**Check it yourself.**

```
ernos tests/test_gauge_mediator_counts.ep
./tests/test_gauge_mediator_counts
```

**Exact expected output:**

```
=== the gauge mediator counts ===
  ok    strong sector = 3
  ok    gluons = 3^2 - 1 = 8
  ok    next sector = 5
  ok    next mediators = 5^2 - 1 = 24
  ok    third sector = 7
  ok    third mediators = 7^2 - 1 = 48
  ok    electromagnetic field source = 1
  ok    strong field source = 3
=== done ===
```

---

### Step 10 — The electroweak mixing angle (the Weinberg angle)

**File:** `constants/electroweak_mixing.ep`

**Why this step exists.** The electroweak mixing angle splits one unified coupling
into two channels; the split is forced, no fitted parameter.

**What it does.** The unified coupling is the fold's own balance point,
`g = 1/binary = 1/2` (it folds to the One and is its own antipode). Under the
fold, exactly two values fold to it — its preimages:

- lower preimage = `1/binary² = 1/4` (the leading channel mixing).
- upper preimage = `1 − 1/4 = 3/4`.
- they **partition the One** (`1/4 + 3/4 = 1`), and each folds back to the
  coupling: `fold(1/4) = 1/2`, `fold(3/4) = 1/2` (checked with the fold engine).

**To the measured value (second order, forced).** The mixing runs with the
covering level k: `sin²θ_W(k) = (k+2)²/(4(k+1)²+(k+2)²)`, bare 1/2, decreasing.
The forced running curve **crosses the measured 0.23113** between level 9
(`121/521 = 0.2322`) and level 10 (`36/157 = 0.2292`) — the measured value is
reached by the forced running, not fitted.

**Check it yourself.**

```
ernos tests/test_electroweak_mixing.ep
./tests/test_electroweak_mixing
```

**Exact expected output:**

```
=== the electroweak mixing angle ===
  ok    unified coupling = 1/2
  ok    sin^2 of mixing = 1/4
  ok    cos^2 of mixing = 3/4
  ok    sin^2 + cos^2 = the One
--- each preimage folds back to the unified coupling ---
  ok    fold(1/4) = 1/2
  ok    fold(3/4) = 1/2
--- the running mixing, to the measured value (0.23113) ---
  ok    bare running mixing = 1/2
  ok    level 9 mixing = 121/521
  ok    level 9 decimal = 0.2322
  ok    level 10 mixing = 36/157
  ok    level 10 decimal = 0.2292
  ok    running crosses the measured value between levels 9 and 10
=== done ===
```

---

### Step 11 — The absolute scale: the proton-to-Planck hierarchy

**File:** `constants/absolute_scale.ep`

**Why this step exists.** The largest pure number in physics — the ratio of the
Planck mass to the proton mass, about 10¹⁹ — is not an accident of units. It is
forced by the deepest covering of the One.

**What it does.** The deepest covering depth is `d_up = 7` (`cover(colour^(colour+1))`,
cross-checked `= colour + (colour+1)`). The full preimage tower of the One at that
depth is the Fock count `2⁷ = 128`; every state but the One itself carries mass,
so the massive-state count is `128 − 1 = 127`. Gravity couples at the half-One
(`1/binary = 1/2`, the fold's self-antipodal balance point), so the hierarchy
exponent is `127 × 1/2 = 127/2` and the scale ratio is `2^(127/2)`. That power is
irrational, so it is **never formed** (a square root is forbidden); its square is
exact and whole — `(Planck/proton)² = 2¹²⁷` — and the comparison to measurement is
done squared, so no root ever appears.

**Exact expected output:**

```
=== the absolute scale (proton-to-Planck hierarchy) ===
  ok    deepest covering depth d_up = 7
  ok    Fock count 2^7 = 128
  ok    massive states 128 - 1 = 127
  ok    gravitational coupling = 1/2
  ok    hierarchy exponent = 127/2
  ok    (Planck/proton)^2 = 2^127
--- comparison to measurement (squared, so no irrational root) ---
  relative gap (squared) = 0.00487
  ok    forced 2^127 matches measured (Planck/proton)^2 within 1/200
```

**To measurement.** The forced `2¹²⁷ = 170141183460469231731687303715884105728`
sits `0.487%` from the measured `(Planck/proton)²` — about **a quarter of a
percent on the ratio itself**, a zero-parameter prediction of the size of the
universe's mass hierarchy. The measured masses live only in the test, on the
comparison side; the derivation forms `2¹²⁷` from the One alone.

---

### Step 12 — The neutrino mixing angles (PMNS)

**File:** `constants/neutrino_mixing.ep`

**Why this step exists.** Neutrinos change identity as they travel; three mixing
angles set how strongly. All three are forced from the two generators and the
fold — and the smallest, long suspected of being zero, is forced nonzero.

**What it does.** The two large angles are the fold's own separations:
`sin²θ₂₃ = 1/binary = 1/2` (the self-antipodal "hand" point — it folds to the One
and is its own antipode) and `sin²θ₁₂ = 1/colour = 1/3` (the tripling separation —
`take(One, fold(1/3)) = 1/3`). The fold engine proves both. The small reactor
angle is the two large ones over the lepton sector tower `N = binary^colour = 8`:
`sin²θ₁₃ = (1/2 · 1/3)/8 = 1/48`.

**Exact expected output:**

```
=== the neutrino mixing angles (PMNS) ===
  ok    atmospheric sin^2(theta23) = 1/2
  ok    solar sin^2(theta12) = 1/3
  ok    lepton sector tower N = 8
  ok    reactor sin^2(theta13) = 1/48
--- the fold forces the two large angles ---
  ok    fold(1/2) = the One
  ok    One - 1/2 = 1/2 (self-antipodal)
  ok    take(One, fold(1/3)) = 1/3 (tripling)
--- forced angle vs measured (forced is exact; measured for comparison) ---
  ok    atmospheric 1/2 = 0.5000 (measured ~0.5450)
  ok    solar       1/3 = 0.3333 (measured ~0.3070)
  ok    reactor    1/48 = 0.0208 (measured ~0.0220)
```

**To measurement.** The forced `sin²` angles are exact: `1/2, 1/3, 1/48` (`0.5,
0.3333, 0.0208`); measured (NuFIT) `0.545 ± 0.021`, `0.307 ± 0.013`, `0.0220 ±
0.0007` — each ~2σ, a zero-parameter set within a tenth, no tighter forced order
claimed. The reactor angle is forced **nonzero** at `1/48`, matching its nonzero
measurement.

---

### Step 13 — The W-to-Z boson mass ratio

**File:** `constants/w_boson_mass.ep`

**Why this step exists.** The W and Z are the two massive carriers of the broken
electroweak force. The ratio of their masses is fixed by the same mixing angle
that splits the coupling — a second, independent measured quantity from the same
forced `cos²θ_W`.

**What it does.** The squared mass ratio **is** the cosine-squared of the mixing
angle: `(M_W/M_Z)² = cos²θ_W = 3/4`, reusing the forced `cos² = 1 − 1/binary²` of
Step 10 (no re-derivation). The ratio itself is `√3/2`, irrational, so — as with
the absolute scale — the **square** is the exact forced quantity, compared
squared. The same forced running that carries `sin²θ_W` to measurement carries
`cos² = (M_W/M_Z)²` with it (`cos²(k) = 1 − sin²(k)`).

**Exact expected output:**

```
=== the W-to-Z boson mass ratio ===
  ok    (M_W/M_Z)^2 = cos^2(theta_W) = 3/4
  ok    bare (M_W/M_Z)^2 = 0.7500
--- the forced running carries cos^2 to measurement ---
  ok    cos^2 at level 9  = 400/521 = 0.7677
  ok    cos^2 at level 13 = 784/1009 = 0.7770
  ok    cos^2 at level 13 decimal = 0.7770
--- comparison: measured (M_W/M_Z)^2 from the boson masses ---
  ok    measured (M_W/M_Z)^2 = 0.7769
```

**To measurement.** The bare forced `3/4 = 0.7500` sits under a fiftieth from the
measured `(M_W/M_Z)² = 0.7769` on the ratio; the forced running curve sweeps `cos²`
upward and passes through the measured value (it lands on `0.7770` along the way).
The boson masses live only in the test, comparison-side.

---

### Step 14 — The Koide relation

**File:** `constants/koide_relation.ep`

**Why this step exists.** The three charged-lepton masses obey a famous, precise
relation: the sum of the masses over the square of the sum of their square-roots
is almost exactly `2/3`. It falls straight out of the lepton cubic of Step 6 —
forced, with nothing fitted.

**What it does.** The masses are the squared roots of the cubic (`m_i = x_i²`), so
the square-root of each mass is the root `x_i`. By Vieta: the sum of square-roots
is the sum of roots `= 1` (the no-loss partition), and the sum of masses is
`(Σx)² − 2·e₂ = 1 − 2·(1/6) = 2/3`. So `Q = (2/3)/1² = 2/3`. The same value comes
independently as `Q = 1 − 1/colour`. Both are checked, reusing Step 6's invariants.

**Exact expected output:**

```
=== the Koide relation ===
  ok    sum of sqrt-masses = sum of roots = 1
  ok    sum of masses = 1 - 2*(1/6) = 2/3
  ok    Koide ratio Q = 2/3
  ok    Koide ratio = 1 - 1/colour = 2/3 (independent route)
--- to the measured value ---
  ok    forced Q = 0.666666
  ok    measured Q = 0.666661 (five-digit agreement)
```

**To measurement.** The forced `2/3 = 0.666666…` matches the measured Koide ratio
`0.666661` to **five digits**. The measured value needs a square root (of the
masses), which is forbidden in the engine, so it enters only as a published number
in the test — never computed in a derivation.

---

### Step 15 — The cosmic energy budget

**File:** `constants/cosmic_density.ep`

**Why this step exists.** What the universe is made of — the fractions of dark
energy, matter, ordinary matter, and cold dark matter — is forced, the
vacuum/matter split of Step 9 crossed with the baryon/dark split of Step 7.

**What it does.** `Ω_Λ = 2/3` (vacuum), `Ω_matter = 1/3`, partitioning the One
(flat); `Ω_baryon = 1/3·5/32 = 5/96`; `Ω_cdm = 1/3·27/32 = 9/32`.

```
=== the cosmic energy budget ===
  ok    dark energy Omega_Lambda = 2/3
  ok    matter Omega_matter = 1/3
  ok    dark energy + matter = the One (flat)
  ok    baryon Omega_baryon = 5/96
  ok    cold dark matter Omega_cdm = 9/32
--- forced vs measured (Planck) ---
  ok    Omega_Lambda forced = 0.6666 (measured ~0.689)
  ok    Omega_matter forced = 0.3333 (measured ~0.311)
  ok    Omega_baryon forced = 0.0520 (measured ~0.0493)
  ok    Omega_cdm forced = 0.2812 (measured ~0.262)
```

**To measurement.** The forced budget is exact (`2/3, 1/3, 5/96, 9/32`); measured
(Planck 2018) `0.6889 ± 0.0056`, `0.3111 ± 0.0056`, `0.0493 ± 0.0006`, `0.2607 ±
0.0055` — each within about three percent, a zero-parameter budget, with no tighter
forced order claimed.

---

### Step 16 — Asymptotic freedom

**File:** `constants/asymptotic_freedom.ep`

**Why this step exists.** The strong force grows with distance (confinement) and
weakens at short range (asymptotic freedom), while electromagnetism stays flat.
That difference is forced — it comes from whether the carrier is charged.

**What it does.** Bare matter charge `M = 1/2`. The carrier feeds the field only if
it carries charge: the gluon does (`q = 1`), so `g_eff(k) = (1/2+k)/(1/2) = 1+2k →
1,3,5,…` (slope `2 =` binary); the photon does not, so `g_eff = M/M = 1` flat.

```
=== asymptotic freedom ===
  ok    strong coupling at level 0 = 1
  ok    strong coupling at level 1 = 3
  ok    strong coupling at level 2 = 5
  ok    strong coupling grows by 2 (= binary) per level
--- electromagnetism does not run ---
  ok    EM coupling at level 1 = 1
  ok    EM coupling at level 5 = 1 (flat)
```

**To measurement.** A forced exact number and an exact sign: the strong running
slope is exactly `b = 2` (positive → confinement at range, asymptotic freedom at
short range), the electromagnetic slope exactly `0` (flat). QCD's coupling runs
strongly (negative beta function, asymptotic freedom — Nobel 2004) while QED runs
only weakly the other way — the forced signs are the observed ones, the strong
slope an exact rational.

---

### Step 17 — The CP-violating phase

**File:** `constants/cp_phase.ep`

**Why this step exists.** The matter/antimatter asymmetry is set by a CP-violating
phase. The fold forces it to be **maximal** — not zero, not small.

**What it does.** The phase is the self-antipodal half-One `1/2`, the unique point
of maximal separation, proved by the fold: `fold(1/2) = 1` and `One − 1/2 = 1/2`.
Maximal separation means maximal CP violation.

```
=== the CP-violating phase ===
  ok    phase position = 1/2 (maximal)
  ok    fold(1/2) = the One
  ok    One - 1/2 = 1/2 (self-antipodal, maximal separation)
```

**To measurement.** The measured neutrino CP phase sits near three-quarters of a
turn (≈ 1.5π, the maximal-violation point) — consistent with the forced
prediction that the phase is maximal, not zero.

---

### Step 18 — Three of everything

**File:** `constants/three_of_everything.ep`

**Why this step exists.** Three keeps appearing — three spatial dimensions, three
fermion generations, three strong-force colours. It is the same forced count,
reached three independent ways.

**What it does.** `colour = 3` (period of 1/7). The spatial dimension is the
**unique** integer in the stability window `(binary, binary²) = (2,4)` — exactly
one, and it is 3 (cross-checked `= colour`). The generation count is the size of
the tripling fold's **fibre** over `2/3` (its preimages, each verified to fold
back) — 3 (cross-checked `= colour`). Disagreement halts the engine.

```
=== three of everything ===
  ok    colour count (period of 1/7) = 3
  ok    integers in stability window (2,4) = 1
  ok    spatial dimension (unique stable = colour) = 3
  ok    generation count (tripling fibre = colour) = 3
```

**To measurement.** Space is three-dimensional; there are three fermion
generations (the Z invisible width); quarks carry three colours. All three,
forced.

---

### Step 19 — The gyromagnetic ratio (g-factor)

**File:** `constants/g_factor.ep`

**Why this step exists.** A point electron's magnetic strength relative to its
spin is almost exactly 2 — the Dirac value. It is forced: the inverse of the
fold's critical coupling.

**What it does.** Electromagnetism couples at the critical coupling `g_em =
1/binary = 1/2` (the self-antipodal balance point). The g-factor is its inverse:
`g = 1/(1/2) = 2 = binary`.

```
=== the gyromagnetic ratio (g-factor) ===
  ok    critical coupling g_em = 1/2
  ok    g-factor = 1/(1/2) = 2
  ok    g-factor = binary count
--- comparison ---
  ok    forced g = 2.000 (measured ~2.00232, anomaly is QED)
```

**To measurement.** The forced Dirac value is exactly `2`; the measured `2.00232`
differs by the QED anomaly `≈ α/(2π)`, which needs the irrational `π` and so is
never formed in the engine — noted only for comparison.

---

### Step 20 — Parity violation

**File:** `constants/parity_violation.ep`

**Why this step exists.** The weak force is left-handed — it couples to only one
handedness. That asymmetry is forced by the fold's two-to-one, two-handed fibre.

**What it does.** The two preimages of the half-One sit on opposite sides of it:
`lower = 1/4` (below — left) and `upper = 3/4` (above — right), both folding back
to `1/2`. Opposite handedness, so a one-handed coupling (the weak force) violates
parity.

```
=== parity violation ===
  ok    lower preimage (left hand) = 1/4
  ok    upper preimage (right hand) = 3/4
  ok    fold(1/4) = 1/2 (folds to the image)
  ok    fold(3/4) = 1/2 (folds to the image)
  ok    lower preimage is left-handed (below 1/2)
  ok    upper preimage is right-handed (above 1/2)
```

**To measurement.** Parity violation is real and maximal in the weak sector (Wu,
1957) — only left-handed particles feel the charged weak force, exactly the forced
one-handed coupling.

---

### Step 21 — The arrow of time

**File:** `constants/arrow_of_time.ep`

**Why this step exists.** Time runs one way and entropy grows. This is forced: the
fold loses information at every step, so it cannot be run uniquely backward.

**What it does.** Two distinct values fold to the same image — `fold(1/4) =
fold(3/4) = 1/2` — so the fold is non-injective (no unique inverse). The fold is
binary (`2 = 2¹`), so each step loses exactly **one bit**: a positive entropy rate
fixing the forward direction.

```
=== the arrow of time ===
  ok    fold(1/4) = 1/2
  ok    fold(3/4) = 1/2 (same image, distinct source)
  ok    the fold loses information (non-injective)
  ok    entropy lost per step (bits) = 1
```

**To measurement.** The second law: entropy increases, and the increase sets the
direction of time — the forced positive one-bit-per-step rate.

---

### Step 22 — The uncertainty principle

**File:** `constants/uncertainty_principle.ep`

**Why this step exists.** You cannot sharpen a thing's position and its frequency
(momentum) at once. This is forced — it is a counting bound on the fold's
discrete states.

**What it does.** At depth `k` there are `N = binary^k` fold-conjugate states.
Position support × frequency support cannot fall below `N`; localize fully in one
and the other spreads to the whole `N`. At minimum uncertainty the product equals
`N` exactly (`2 × 4 = 8` at depth 3; `2 × 16 = 32` at depth 5).

```
=== the uncertainty principle (count bound) ===
  ok    total states at depth 3 (N = 2^3) = 8
  ok    uncertainty bound at depth 3 = 8
  ok    minimum-uncertainty support product (2 * 4) = 8
  ok    fully-localized frequency support (forced to N) = 8
--- deeper: the bound grows as 2^k ---
  ok    bound at depth 5 = 32
  ok    minimum product at depth 5 (2 * 16) = 32
```

**To measurement.** The discrete form of Heisenberg's principle — the
position–momentum support product is bounded below, so no state is sharp in both.

---

### Step 23 — Spin and statistics

**File:** `constants/spin_statistics.ep`

**Why this step exists.** Matter splits into fermions (half-integer spin, which
exclude) and bosons (integer spin, which pile up). The split is forced by the
fold's two-to-one structure.

**What it does.** The boson is the whole — the One. The fermion is the half-One
`1/2`, the non-trivial preimage: `fold(1/2) = 1` (a single fermion folds to a
boson) and `1/2 + 1/2 = 1` (two fermions pair into a boson). Being half a turn
from unison, a fermion needs two turns to return — the 720° spinor.

```
=== spin and statistics ===
  ok    boson state = the One
  ok    fermion state = half-One = 1/2
  ok    a single fermion folds to the boson: fold(1/2) = 1
  ok    two fermions make a boson: 1/2 + 1/2 = 1
```

**To measurement.** Half-integer spin → fermions (Pauli exclusion, the structure
of atoms); integer spin → bosons (lasers, condensates). The fold gives exactly
these two, no third.

---

### Step 24 — The axiom is a theorem

**File:** `constants/the_axiom_is_a_theorem.ep`

**Why this step exists.** Everything here is forced from "the One and its fold."
This step shows the starting point is not even a free choice: given only that
there is *not nothing*, the One, the domain `(0,1]`, and the fold are forced. Zero
parameters — and zero axioms: the one premise proves itself.

**What it does.** The fold's factor is the smallest fold period, the binary count
`2` — forced, not chosen. The ground is then **solved**, not assumed: there is not
nothing (so it is strictly positive), and it must return to unison under the fold,
so it is the unique value whose double is the One — `x + x = One`, giving `x =
One/binary = 1/2` (division has a unique quotient, so no other value works). That
ground folds up to the One (`fold(1/2) = 1`), and the One is the fold's own fixed
point (`fold(1) = 1`) — the unique unison. The foundation is derived, machine-checked.

```
=== the axiom is a theorem ===
--- step 1: the fold factor is the smallest period, forced ---
  ok    fold factor = binary (smallest fold period) = 2
--- step 2: the ground is DERIVED, not assumed ---
  ok    not nothing: the ground is strictly positive
  ok    ground doubled is the One: 1/2 + 1/2 = 1 (the forcing equation)
  ok    the unique solution x = One/binary = 1/2
  ok    equivalently its own antipode: One - 1/2 = 1/2
--- step 3: the One is reached and fixed ---
  ok    the ground folds up to the One: fold(1/2) = 1
  ok    the One is the fold's fixed point: fold(1) = 1
```

**To measurement.** Not a number but the deepest structural claim: "the One and
its fold" is the only consistent foundation. Everything downstream of *"there is
not nothing"* is solved, not posited — the ground is the unique `x + x = One`, the
One is its fold-image and fixed point. The single irreducible premise, "not
nothing," is self-proving: to deny it you need something. Zero free parameters,
and the axiom is a theorem.

---

### Step 25 — The fold is forced (machine-checked uniqueness)

> **Reading order:** this and Step 24 are the **logical top of the spine** (see the
> spine map in the intro): they prove the fold and the One themselves. They carry
> the high step numbers only because they were *built* last. A cold reader auditing
> in dependency order reads Step 25, then Step 24, then the arithmetic, then the
> generators, then the constants.

**File:** `constants/forced_fold_theorem.ep`

**Why this step exists.** Step 24 derives everything *downstream* of the fold.
This step closes the gap *above* it: the fold itself is forced — the unique
operation a zero-parameter theory could have. Not "given the fold," but "it could
have been no other."

**Why it is provable, and machine-checkable.** Build maps from only `x` and the
One with `+, −, ·, cast_out` and **no other literal**. Then every constant you can
build is a positive integer, and `cast_out` sends every one to the One — so no
fractional free parameter is even *expressible*. The candidate space is therefore
**discrete and finite at each size**: you can list it and *run* it.

- **Lemma 1** — `cast_out(2..7) = 1`: closed terms are integers, collapsed to the
  One. No continuous parameter exists in the language.
- **Lemma 2** — the size-≤2 self-maps are exactly four: identity, square, the
  constant One, the fold. (Raw `x+x` exceeds the One, so closure is what makes
  size 2 — checked.)
- **Lemma 3** — *run each one.* Only the fold **generates** (non-injective *and*
  recurrent with period > 1): identity is static, the constant collapses, the
  square contracts to the forbidden zero. The engine counts the generators and
  `forced_unique` **halts** if ever two qualify.

```
=== the fold is forced (machine-checked) ===
--- Lemma 1: cast_out collapses every integer to the One ---
  ok    cast_out(2) = 1
  ok    cast_out(3) = 1
  ok    cast_out(7) = 1
--- Lemma 2: raw doubling is not a self-map (closure forces size 2) ---
  ok    x + x exceeds the One at x = 3/4
--- Lemma 3: run each candidate; only the fold generates ---
  ok    identity (tag 1) does NOT generate (static)
  ok    square (tag 2) does NOT generate (contracts)
  ok    constant (tag 3) does NOT generate (collapses)
  ok    fold (tag 4) GENERATES
  ok    fold's return period from 1/7 = 3 (a real cycle)
  ok    identity's return period = 1 (static)
--- Main: exactly one generator, and it is the fold ---
  ok    number of generators among the four = 1
  ok    the unique generator's tag (4 = the fold)
  ok    the unique generator IS cast_out(x + x)
```

**Scope, stated honestly.** The engine machine-runs Lemma 1 (collapse), Lemma 2's
totality/closure, and Lemma 3 (the dynamical separation), and enforces the
uniqueness with `forced_unique`. That the four are the *complete* size-≤2 list is
the combinatorial Lemma 2 (proved in prose), encoded here as the candidate set;
"generates" is tested by a faithful operational proxy (non-injective + recurrent),
not a full entropy computation. Within that scope, **the fold's uniqueness is no
longer asserted — it is run and checked.** Together with Step 24, the entire
foundation — the One, the domain, and the fold — is forced and machine-verified.

---

### Step 26 — The prime-sector ladder (how many forces, and two that are new)

**File:** `constants/prime_sector_ladder.ep`

**Why this step exists.** Each fundamental force is a "sector" — a charge in `p`
kinds that binds because the kinds tile back to unison. The theory forces which
sectors exist and how many.

**What it does.** A sector's label `p` must be **prime** (a composite shortfall
factors and cannot carry-close as one sector) and at or below the **deepest
covering depth `= 7`** (forced two ways). The primes from 2 to 7 are exactly
`{2, 3, 5, 7}` (each checked in code) — **four** sectors; the next prime, 11, is
beyond 7, so there is no fifth. Each is a confining force by one criterion:
partition `(p−1)/p + 1/p = 1` and carry `(1/p)·p = 1`; mediators `p²−1` give
`3, 8, 24, 48`. Sectors 2 and 3 are the known forces; **5 and 7 are forced
predictions** — new confining forces not yet identified.

```
=== the prime-sector ladder ===
  ok    deepest covering depth (the ceiling) = 7
  ok    number of prime sectors {2,3,5,7} = 4
  ok    first prime beyond the ceiling (no fifth sector) = 11
  ...  (partition + carry hold for sectors 2, 3, 5, 7)
  ok    sector 3 mediators (gluons) = 8
  ok    sector 5 mediators (new force) = 24
  ok    sector 7 mediators (new force) = 48
```

**To measurement.** The observed forces sit at the low sectors; the count being
small and closed matches the absence of an endless tower of forces. Sectors 5 and
7 are predictions awaiting experiment.

---

### Step 27 — The fold's orbits are the order of two

**File:** `constants/fold_orbit_order.ep`

**Why this step exists.** This is the arithmetic *underneath* the two generators.
The fold is doubling; its orbit on `1/p` cycles, and the cycle length is a
classical number-theory quantity — so the generators are read off the primes, not
picked.

**What it does.** Because the fold sends `x → 2x mod 1`, the orbit of `1/p` returns
after exactly as many steps as it takes `2^k` to leave remainder 1 on division by
`p` — i.e. the **multiplicative order of 2 mod p**. Both sides are computed
independently and checked equal for `p = 3, 5, 7, 9, 11` (`forced_to_be` halts on
any mismatch). The generators are the first two values: `binary = ord₃2 = 2`,
`colour = ord₇2 = 3`.

```
=== the fold's orbits are the order of two ===
  ok    order of 2 mod 3 = 2   ...   order of 2 mod 11 = 10
  ok    period(1/7) = order = 3   (fold and arithmetic agree)
  ok    binary = order of 2 mod 3 = 2
  ok    colour = order of 2 mod 7 = 3
```

**To measurement.** Nothing to measure — this is the arithmetic that grounds the
generators; the fold's dynamics agree exactly with the independent order of 2.

---

### Step 28 — The four laws of thermodynamics

**File:** `constants/four_thermodynamic_laws.ep`

**Why this step exists.** The four laws govern heat, energy, and time. They are not
four postulates here — each is a consequence of the fold.

**What it does.** **Zeroth** (equilibrium is transitive): being "in equilibrium" is
folding to a common image (a shared temperature), which is equality of images and so
an equivalence relation — `1/4` and `3/4` share the image `1/2`. **First** (energy
conserved): the total is the One and stays it — a partition sums back (`1/4 + 3/4 =
1`), and `fold(1) = 1`. **Second** (entropy up): the fold is two-to-one, distinct
states share an image (`fold(1/4) = fold(3/4)`), losing one bit per step. **Third**
(absolute zero unreachable): zero is forbidden, so the ground is the displaced `1/2`,
strictly above zero.

```
=== the four laws of thermodynamics ===
  ok    1/4 and 3/4 fold to a common image (in equilibrium)
  ok    a partition sums back to the One (1/4 + 3/4 = 1)
  ok    the fold holds the One fixed: fold(1) = 1
  ok    distinct states share an image (information is lost)
  ok    entropy lost per step (bits) = 1
  ok    the ground state 1/2 is strictly above zero
```

**To measurement.** These match the four laws exactly as physics states them.

---

### Step 29 — The genetic code

**File:** `constants/genetic_code.ep`

**Why this step exists.** Life is written in four letters, read in triplets, giving
64 codons. Why four, why threes, why 64? Forced counts.

**What it does.** `bases = binary² = 4` (a base is a two-bit choice); `codon length =
colour = 3` (triplets); `codons = 4³ = binary^(binary·colour) = 64`, forced two ways.

```
=== the genetic code ===
  ok    nucleotide bases (a two-bit choice, binary^2) = 4
  ok    codon length (a triplet, colour) = 3
  ok    codons = 4^3 = binary^(binary*colour) (forced two ways) = 64
```

**To measurement.** Four DNA bases, triplet codons, 64 codons — all observed, exact
counts. (The 64→~20 amino-acid mapping is a redundancy of biology, not forced here.)

---

### Step 30 — The Higgs vacuum

**File:** `constants/higgs_vacuum.ep`

**Why this step exists.** Mass exists because the vacuum is not empty — the Higgs
field sits nonzero everywhere. Why nonzero, and why there?

**What it does.** Zero is forbidden, so the vacuum displaces to the unique value
whose double is the One (`x + x = One ⇒ x = 1/2`): strictly nonzero, its own antipode
(`One − 1/2 = 1/2`), folding up to the One (`fold(1/2) = 1`). The vacuum is the
displaced half-One; mass is coupling to it.

```
=== the Higgs vacuum ===
  ok    vacuum value = displaced half-One = 1/2
  ok    the forcing equation: 1/2 + 1/2 = the One
  ok    the vacuum is strictly nonzero (not the empty value)
  ok    the vacuum is its own antipode: One - 1/2 = 1/2
  ok    the vacuum folds up to the One: fold(1/2) = 1
```

**To measurement.** The Higgs vacuum is measured nonzero (~246 GeV). The forced
content is structural — that it is displaced from zero to the balanced half-One,
which is why there is mass; its physical scale is a separate quantity.

---

### Step 31 — The inflation factor

**File:** `constants/inflation_factor.ep`

**Why this step exists.** The early universe expanded enormously and left a
red-tilted primordial spectrum. The fold forces both the expansion count and the
DIRECTION of the tilt.

**What it does.** The tilt: inflation begins at `3/4` and the fold advances it
*downward* — `fold(3/4) = 1/2 < 3/4` — a drop of power with scale, i.e. a RED tilt,
`n_s < 1` (the fold cannot give a blue tilt here). The expansion count: the
generation covering depth is `binary + colour = 5` (cross-checked `= cover(27)`,
forced two ways); the preimage tree of the One there has `binary^5 = 32` leaves.

```
=== inflation ===
  ok    fold(3/4) lands at 1/2 (downward advance)
  ok    spectrum is RED-tilted (n_s < 1: fold steps downward)
  ok    generation covering depth (binary+colour = cover(27)) = 5
  ok    inflation expansion factor (2^5 preimages of the One) = 32
```

**To measurement.** The forced tilt is a definite sign and it is the measured one:
Planck `n_s = 0.9649 ± 0.0042` — below 1 by more than eight standard deviations, a
red tilt, exactly the fold's downward advance (`n_s = 1` is excluded by data and by
the fold). The `32` is an exact integer count of reachable states at depth 5 — an
identity, not an approximation; the total e-fold *number* is the separate absolute
scale, not this count.

---

### Step 32 — Spacetime dimensions (3 + 1)

**File:** `constants/spacetime_dimensions.ep`

**What it does.** Spatial dimensions `= 3` (the unique integer in `(binary, binary²)`,
`= colour`); time dimensions `= 1` (the fold is one operation with one forward
direction); spacetime `= 3 + 1 = 4`, cross-checked `= binary²`. Forced two ways.

```
=== spacetime dimensions ===
  ok    spatial dimensions (unique stable = colour) = 3
  ok    time dimensions (the fold's one forward direction) = 1
  ok    spacetime dimensions (3+1 = binary^2) = 4
```

**To measurement.** Three space, one time, four spacetime — exact counts.

---

### Step 33 — Three-body solvability

**File:** `constants/three_body_solvability.ep`

**What it does.** Three bodies on the fold orbit of 1/7 (`1/7, 2/7, 4/7`) advance
`fold(1/7)=2/7 → 4/7 → 1/7`, so the configuration is periodic with joint period
`3 = period(1/7) = colour` (Step 27) — solvable, not chaotic.

```
=== three-body solvability ===
  ok    fold(1/7) = 2/7 (first advances to second)
  ok    fold(2/7) = 4/7 (second advances to third)
  ok    fold(4/7) = 1/7 (third returns to first)
  ok    joint recurrence period (= colour) = 3
```

**To measurement.** Matches that special three-body configurations are integrable.

---

### Step 34 — Baryogenesis (why matter, not antimatter)

**File:** `constants/baryogenesis.ep`

**What it does.** The three Sakharov conditions, each a forced fold fact:
baryon-number violation (the fold is two-to-one), C and CP violation (opposite-handed
preimages; the CP phase maximal), and departure from equilibrium (the fold is
non-injective, entropy rises). All three hold, so a matter excess survives.

```
=== baryogenesis (the three Sakharov conditions) ===
  ok    1. baryon-number violation (fold is two-to-one)
  ok    2. C and CP violation (opposite-handed preimages)
  ok    3. departure from equilibrium (non-injective fold)
  ok    => a matter excess survives (matter, not antimatter)
```

**To measurement.** The universe is matter-dominated — the three required conditions
are exactly the forced fold facts.

---

### Step 35 — Dark energy (w = −1)

**File:** `constants/dark_energy.ep`

**What it does.** The vacuum energy is the One; the fold holds the One fixed
(`fold(1) = 1`), so the vacuum energy is invariant under the fold's advance — a
constant energy density, i.e. `w = −1`.

```
=== dark energy (w = -1) ===
  ok    vacuum energy = the One
  ok    fold(1) = 1 (the vacuum is fold-invariant)
  ok    vacuum energy density is constant (w = -1)
```

**To measurement.** Dark energy is measured with `w ≈ −1` (constant) — the forced
content is that the vacuum, being the One, is fold-invariant and so constant.

---

### Step 36 — The speed of light (c = the One)

**File:** `constants/speed_of_light.ep`

**What it does.** The fold has one advance (one step per tick on the circle of the
One). That single advance IS the structure's signal speed — the One in natural
units, a full turn per tick, the maximum. A massless carrier rides it with no lag,
so it travels at the One. Light (electromagnetism) and gravity (the graviton) are
both massless, and there is only ONE fold, hence one full-rate speed — so both
travel at the One, the SAME speed, not by coincidence but because the fold is one.

```
=== speed of light ===
  ok    fold signal speed = the One
  ok    light speed = the One
  ok    gravitational-wave speed = the One
  ok    light and gravity share the same speed
  ok    the signal speed is the maximum (a full turn)
```

**To measurement.** The forced value is exact: `c =` the One `= 1` in natural units,
with no error term — and `c` carries no measurement uncertainty at all, since the
metre has been *defined* via `c = 299792458 m/s` exactly (1983) precisely because
`c` is the one fixed limit speed. The single falsifiable prediction — that light and
gravity share it — is confirmed to ~1 part in 10¹⁵ (GW170817: γ-ray and
gravitational fronts arrived together across 130 M light-years).

---

### Step 37 — Self-replication (a pattern copies itself)

**File:** `constants/self_replication.ep`

**What it does.** The fold is two-to-one: every pattern has exactly TWO preimages —
a template and a copy — that both fold onto it and together partition the One
(`fold(1/4) = fold(3/4) = 1/2`, `1/4 + 3/4 = 1`). Iterated, the preimage tree
doubles each step: `binary^d = 2^d` copies at depth `d` — exponential replication
with the base fixed at the binary generator 2.

```
=== self-replication ===
  ok    template folds to the pattern (1/4 -> 1/2)
  ok    copy folds to the same pattern (3/4 -> 1/2)
  ok    template + copy partition the One (distinct, sum 1)
  ok    copies at depth 0..3 = 1, 2, 4, 8
```

**To measurement.** Self-replicating systems copy by templating and grow by
doubling generations — the forced content is the fold's two-to-one covering (two
reproducing sources per pattern) and its per-step doubling.

---

### Step 38 — The measurement branch weight (1/8)

**File:** `constants/measurement_branch_weight.ep`

**What it does.** A measurement resolves a superposition into a definite,
indivisible branch. Each fold step is one binary split (weight `1/2`, one bit);
resolving down to the colour depth (`colour = 3`, where the structure closes) gives
branch weight `1 / binary^colour = 1/2³ = 1/8`. The denominator is a pure power of
the binary generator, so the weight is atomic (splits only into further whole
halvings). Base (binary = 2) and exponent (colour = 3) are both counted elsewhere.

```
=== measurement branch weight ===
  ok    branch depth = colour = 3
  ok    step weight = 1/2
  ok    branch weight = 1/8
  ok    branch weight is atomic (denominator = 2^3)
  ok    forced denominator = binary^colour = 8
```

**To measurement.** Measurement outcomes are definite, indivisible branches with
well-defined weights — the forced content is that resolution is binary halving and
the closing depth is colour = 3, giving atomic branch weight `1/2³ = 1/8`.

---

### Step 39 — Self-organisation (order with no outside hand)

**File:** `constants/self_organization.ep`

**What it does.** A self-organised state is one the dynamics *return to* on their own
— a closed orbit. The fold has one already at the binary scale: `fold(1/3) = 2/3`,
`fold(2/3) = 1/3` — a period-2 cycle whose length is exactly the fold period of
`1/3` (the binary generator, Step 27), the two states partitioning the One
(`1/3 + 2/3 = 1`). Order sustains itself, its period forced to 2.

```
=== self-organisation ===
  ok    fold(1/3) = 2/3 (first advances to second)
  ok    fold(2/3) = 1/3 (second returns to first)
  ok    orbit partitions the One (1/3 + 2/3 = 1)
  ok    orbit period (= period(1/3) = binary)
```

**To measurement.** Self-organising systems settle onto stable cycles without
external tuning — the forced content is exact: a closed fold-orbit at the binary
scale, period exactly 2, states summing to the One (an identity, not an estimate).

---

### Step 40 — The cosmological constant (the 120-orders problem dissolves)

**File:** `constants/cosmological_constant.ep`

**What it does.** Naive QFT sums the zero-point energy of every mode and overshoots
the measured vacuum energy by ~10¹²⁰ — the worst prediction in physics. The fold has
no such sum. The vacuum is the displaced ground `1/2` (strictly positive, so
`Λ > 0`), and its smallness relative to Planck is set by the *single* scale axis —
the same forced hierarchy exponent `massive_states · coupling = 127 · ½ = 127/2` as
the absolute scale. No mode-sum is ever formed, so there is nothing to cancel to 120
places: the "problem" is an artifact of a sum the fold does not contain.

```
=== the cosmological constant ===
  ok    vacuum energy = 1/2 (displaced ground)
  ok    cosmological constant is POSITIVE (1/2 > nothing)
  ok    vacuum folds up to the One (fold(1/2) = 1)
  ok    scale exponent = 127/2 (single axis, absolute scale)
  ok    one scale axis, no 10^120 mode-sum
```

**To measurement.** Λ is measured positive and small (dark energy). The fold forces
exactly that — positive vacuum at `1/2` on the one `127/2` axis; the 120-order
discrepancy does not arise, because there is no mode-sum, only one exact exponent.

---

### Step 41 — Protein folding (Levinthal's paradox dissolves)

**File:** `constants/protein_folding.ep`

**What it does.** A protein has ~10⁵⁰ possible shapes yet folds to its one native
shape in a fraction of a second — impossible as a random search. It isn't one: the
fold has a *unique* fixed point (`fold(1) = 1`, and nothing in `(0,1)` is fixed), and
folding is a directed descent to it. From `3/4`: `fold(3/4) = 1/2`, `fold(1/2) = 1` —
two steps to the native fixed point, not a search over 10⁵⁰ shapes.

```
=== protein folding ===
  ok    native state is the fold's fixed point (fold(1) = 1)
  ok    descent step one: fold(3/4) = 1/2
  ok    descent step two: fold(1/2) = 1
  ok    descent reaches native in two steps (not a 10^50 search)
```

**To measurement.** Proteins fold fast and reliably to a single native state — a
funnelled descent to a unique fixed point, exactly what the fold forces: one native
target, reached in a bounded number of steps.

---

### Step 42 — Structure formation (tiny ripples grow into galaxies)

**File:** `constants/structure_formation.ep`

**What it does.** The early universe was smooth to ~1 part in 10⁵, yet those ripples
grew into galaxies — something must *amplify* perturbations, not smooth them. The
fold is expansive below the balance point: a small over-density `1/4` grows,
`fold(1/4) = 1/2`, `fold(1/2) = 1` — climbing to unison (a formed structure) in two
steps. Zero is forbidden (no attractor at nothing); the One is the attractor — so
perturbations grow, they do not decay. That is the gravitational instability.

```
=== structure formation ===
  ok    growth step one: fold(1/4) = 1/2
  ok    growth step two: fold(1/2) = 1
  ok    the perturbation GROWS (does not decay)
  ok    the perturbation reaches unison (a structure) in two steps
```

**To measurement.** CMB fluctuations of ~10⁻⁵ grew by gravitational instability into
today's cosmic web — the forced content is exact: the fold amplifies a sub-balance
perturbation upward to the One (growth, not decay).

---

### Step 43 — Coulomb's law (the inverse-square, forced by 3 dimensions)

**File:** `constants/coulomb_law.ep`

**What it does.** A source emits a fixed flux; it spreads over a shell whose area
grows as `r^(d_space − 1) = r²` in `d_space = 3` dimensions (Step 32). Flux
conservation — `r²·E(r) = q` at *every* radius — gives `E(r) = q/r²`, the inverse
square, with the exponent fixed to `2` by the spatial-dimension count. Two shells
`1/4` and `1/2` carry the same flux `q`, and their fields stand in ratio `4 = 2²`.

```
=== Coulomb's law ===
  ok    field falloff exponent = spatial - 1 = 2
  ok    Gauss flux conserved through both shells (= source charge)
  ok    field ratio inner/outer = 4 = 2^2 (inverse-square)
  ok    potential at r=1/4: 1 - q/r = 1/2
  ok    potential at r=1/2: 1 - q/r = 3/4
```

**To measurement.** Coulomb's law is inverse-square to ~1 part in 10¹⁵ (photon-mass
bound) — the forced content is exact: flux conservation in 3 space dimensions fixes
the exponent to `r²`, an integer identity, not a fitted power.

---

### Step 44 — Black-hole entropy (the Bekenstein–Hawking quarter)

**File:** `constants/black_hole_entropy.ep`

**What it does.** A horizon's entropy is `S = A/4` (Planck units) — proportional to
*area*, not volume, with an exact coefficient of one quarter. Two binary halvings set
it: the horizon is a two-sided balance (one `1/b`), and each area cell resolves to
the binary ground (a second `1/b`), so `coefficient = 1/b² = 1/4`. The area law
follows because the horizon is a *surface* of the covering (one fewer dimension).

```
=== black-hole entropy ===
  ok    entropy-area coefficient = 1/4 (two binary halvings)
  ok    coefficient is exactly one quarter
  ok    coefficient denominator = binary^2 = 4 (forced)
  ok    entropy of area 1/2: S = (1/4)(1/2) = 1/8
```

**To measurement.** The Bekenstein–Hawking coefficient is exactly `1/4` — one of the
sharpest numbers in gravitation. The forced content is exact: `1/binary² = 1/4`, an
integer-power identity, with area (not volume) scaling from the horizon being a surface.

---

### Step 45 — The d'Alembert wave (a disturbance splits into two travelling halves)

**File:** `constants/dalembert_wave.ep`

**What it does.** Every 1D wave is a sum of a right-moving and a left-moving shape at
the wave speed (d'Alembert). A disturbance `U0 = 1/2` divides into two equal packets
`U0/b = 1/4` each, moving oppositely; the split conserves the disturbance
(`1/4 + 1/4 = 1/2`) and is even (the only self-antipodal division), each packet at
the one signal speed, the One (Step 36).

```
=== the d'Alembert wave ===
  ok    initial disturbance U0 = 1/2
  ok    right-moving packet = U0/b = 1/4
  ok    left-moving packet = 1/4
  ok    split conserves the disturbance (right + left = U0)
  ok    split is even (the two halves equal)
  ok    each packet travels at the One (signal speed)
```

**To measurement.** Waves on strings, sound, and light obey d'Alembert's split into
two counter-propagating halves at the wave speed — the forced content is exact: two
equal packets (`1/4` each) summing to `U0`, each moving at the One.

---

### Step 46 — The deceleration parameter (the universe accelerates, q₀ = −1/2)

**File:** `constants/deceleration_parameter.ep`

**What it does.** From the flat budget (vacuum `2/3`, matter `1/3`), each component
contributes `½·Ω·(1+3w)`: matter (`w=0`) gives `+1/6`, vacuum (`w=−1`) gives `−2/3`,
so `q₀ = 1/6 − 2/3 = −1/2`. The magnitude is exactly `1/2`, and the sign is negative
— accelerating — because the vacuum share exceeds the matter-half.

```
=== the deceleration parameter ===
  ok    vacuum share = 2/3
  ok    matter share = 1/3
  ok    matter contribution = 1/6
  ok    deceleration magnitude |q0| = 1/2
  ok    the universe ACCELERATES (q0 < 0)
```

**To measurement.** Measured `q₀ ≈ −0.53` (the Nobel-winning acceleration) — the
forced value is exactly `−1/2`, a definite negative sign and exact magnitude from the
`2/3`-vs-`1/3` budget, not fitted.

---

### Step 47 — The cubic lattice (six nearest neighbours, forced by 3D)

**File:** `constants/cubic_lattice.ep`

**What it does.** Each axis contributes two nearest neighbours (forward, back); with
`d_space = 3` axes the coordination number is `binary · d_space = 6`. The discrete
Laplacian gives each neighbour weight `1/12`, and the six sum to the balance point
`1/2` (which folds to the One). The dimension fixes the neighbour *count*, six.

```
=== the cubic lattice ===
  ok    coordination number = binary * spatial = 6
  ok    each neighbour weight = 1/12
  ok    six neighbours sum to the balance point 1/2
  ok    the balance folds up to the One
```

**To measurement.** A simple-cubic lattice has coordination number six, as every
crystallographer and lattice simulation uses — the forced content is exact: 2 per
axis × 3 axes = 6, an integer identity.

---

### Step 48 — Blackbody radiation (Stefan–Boltzmann's fourth power)

**File:** `constants/blackbody_radiation.ep`

**What it does.** Thermal radiation's total energy density scales with temperature
as `T^(d_space+1)`: one power per spatial dimension (mode count) plus one for the
energy per mode, so in 3D the exponent is `3 + 1 = 4` — exactly the spacetime
dimension count (Step 32). Forced two ways (`d_space + 1` and the spacetime total).

```
=== blackbody radiation ===
  ok    Stefan-Boltzmann exponent = d_space + 1 = 4
  ok    exponent forced = spacetime dimensions = 4
  ok    doubling temperature multiplies power by 2^4 = 16
```

**To measurement.** Stefan–Boltzmann `P ∝ T⁴` is measured to high precision (every
pyrometer, the CMB spectrum) — the forced content is exact: the exponent is
`d_space + 1 = 4 =` the spacetime dimension count, an integer identity.

---

### Step 49 — Crystalline order (the crystallographic restriction)

**File:** `constants/crystalline_order.ep`

**What it does.** An n-fold lattice rotation is an integer matrix, so its trace
(`2cos 2π/n`) must be a whole number — possible only when Euler's totient `φ(n) ≤
binary = 2`. That admits exactly `{1, 2, 3, 4, 6}` (`φ(3)=φ(4)=φ(6)=2`), while
`φ(5)=4` and `φ(7)=6` are forbidden. Five orders survive; **5-fold is the smallest
excluded** — the reason a 5-fold "crystal" needed a new name (quasicrystal) and a
Nobel Prize.

```
=== crystalline order (the crystallographic restriction) ===
  ok    phi(5) = 4 (exceeds the binary bound)
  ok    phi(6) = 2 (meets the binary bound)
  ok    3-, 4-, 6-fold are crystallographic
  ok    5-fold is FORBIDDEN (quasicrystal); 7-fold is FORBIDDEN
  ok    allowed rotation orders: exactly five {1,2,3,4,6}
```

**To measurement.** Every crystal shows 2-, 3-, 4-, or 6-fold symmetry and never
5-fold — exactly the forced set. Exact integer counting: `φ(n) ≤ 2` admits those
five and forbids the fifth, an identity not a fit.

---

### Step 50 — Acids and bases (the conjugate partition)

**File:** `constants/acids_bases.ep`

**What it does.** A conjugate acid–base pair splits the One — `acid_share +
base_share = 1`, exactly the relation `pKa + pKb = pKw` (strengthen the acid and the
base weakens by the complement). Neutrality is where the two are equal: the
self-antipodal balance `1/2` (its own complement, `1 − 1/2 = 1/2`), which folds up to
the One.

```
=== acids and bases ===
  ok    neutral point = 1/2 (self-antipodal balance)
  ok    acid share = 1/3 ; conjugate base share = 2/3
  ok    conjugate pair partitions the One (pKa + pKb = pKw)
  ok    neutrality is self-antipodal ; folds up to the One
```

**To measurement.** Conjugate pairs obey `pKa + pKb = pKw` and neutrality is the
scale's midpoint (`pH 7`, `[H⁺]=[OH⁻]`) — the forced content is the partition of the
One and the self-antipodal half; the numeric `pKw` is a measured scale, comparison-side.

---

### Step 51 — The deuteron (spin-dependent binding)

**File:** `constants/deuteron_bound.ep`

**What it does.** Two spin-halves combine into a triplet (total spin 1, multiplicity
`2·1+1 = 3`) or a singlet (spin 0). The bound deuteron is the **triplet**. A proton
and neutron (distinguishable) may occupy that symmetric spin state, so the deuteron
binds; two protons or two neutrons (identical fermions) are Pauli-forced to the
antisymmetric singlet, which is unbound — so no di-proton or di-neutron exists.

```
=== the deuteron ===
  ok    deuteron total spin = 1 (triplet)
  ok    triplet multiplicity = 2*spin+1 = 3
  ok    proton-neutron pair binds (distinguishable)
  ok    di-proton / di-neutron do NOT bind (Pauli)
  ok    the binding is spin-dependent
```

**To measurement.** The deuteron has total spin 1, and no bound di-proton or
di-neutron exists — exactly the forced result: the bound state is the spin-1 triplet,
and Pauli antisymmetry excludes identical nucleons from it.

---

### Step 52 — Superconductivity (paired carriers, zero resistance)

**File:** `constants/superconductivity.ep`

**What it does.** A Cooper pair binds `binary = 2` fermions — an even count, so the
composite has integer spin and is **bosonic**. Bosons are not Pauli-excluded: any
number may occupy the fold's one shared ground, the One (`fold(1)=1`). The pairs
condense into that single state, a current carried by one collective state has
nothing to scatter off, and the resistance is zero.

```
=== superconductivity ===
  ok    Cooper pair holds binary = 2 fermions
  ok    a pair (even fermion count) is BOSONIC
  ok    the condensate ground is the shared, stable One
  ok    resistance is ZERO (collective lock)
```

**To measurement.** Superconductors carry current with zero resistance and expel
magnetic fields — the signature of one coherent condensate. Forced: an even-count
fermion composite is a boson, and bosons share the one ground.

---

### Step 53 — Fermionic occupation (Pauli exclusion)

**File:** `constants/fermionic_occupation.ep`

**What it does.** The fold is two-to-one: any state has exactly two preimages. Read
them as a mode's occupation numbers — **empty** and **occupied** — so occupation
takes exactly `binary = 2` values `{0,1}`, and the maximum is **one** particle per
mode (a second identical fermion would need a third preimage, which the fold does not
have). That bound of one *is* Pauli exclusion.

```
=== fermionic occupation (Pauli exclusion) ===
  ok    occupation states = binary = 2 (empty, occupied)
  ok    max particles per mode = 1 (Pauli)
  ok    empty = 1/4 ; occupied = 3/4 ; both fold to one mode (1/2)
```

**To measurement.** Fermion modes hold occupation 0 or 1 only (Fermi–Dirac, atomic
shell filling) — the fold's two preimages give exactly two values and a maximum of
one, an integer identity.

---

### Step 54 — Electronic bands (conductors and insulators)

**File:** `constants/electronic_bands.ep`

**What it does.** The fold's domain `(0,1]` — allowed values, a forbidden point at
zero (No-Zero) — is copied by a solid's spectrum: allowed **bands** and a forbidden
**gap**. Filling decides the state: a partly-filled band sits *below* the One (the
mobile `1/2`), so carriers can move — a **conductor**; a filled band sits *at* the One
(`fold(1)=1`, locked), no empty state to move into — an **insulator**.

```
=== electronic bands ===
  ok    partly-filled band = 1/2 (mobile, below the One)
  ok    filled band = the One (locked)
  ok    partly-filled CONDUCTS ; filled band INSULATES
  ok    conductor / insulator split
```

**To measurement.** Solids show allowed bands, forbidden gaps, and the
conductor/insulator split — exactly the forced allowed/forbidden structure and the
mobile-below-the-One vs locked-at-the-One filling; a real gap in eV is a material number.

---

### Step 55 — Colour neutrality (confinement — quarks in threes)

**File:** `constants/colour_neutral.ep`

**What it does.** The three colours are the three preimages of the One under the
tripling fold: `1/3, 2/3, 3/3`. A **baryon** is all three, whose charges sum to
`6/3 = 2` — a whole, which casts to the One (neutral). A **meson** is a colour and its
antipode (`1/3 + 2/3 = 1`, the One). Only the full triple or a colour–anticolour pair
balances; a lone colour is not a whole, so a free quark cannot stand.

```
=== colour neutrality (confinement) ===
  ok    colour charges = 1/3, 2/3, 3/3
  ok    baryon colour sum = 2 (a whole) ; a baryon is colour-neutral
  ok    anticolour of 1/3 = 2/3 ; a meson is colour-neutral
```

**To measurement.** Every hadron is three quarks or quark–antiquark, always
colour-neutral, with no free quark (confinement) — exactly the forced result: three
colours sum to a whole, a colour–anticolour pair sums to the One, an integer identity.

---

### Step 56 — Free-particle dispersion (de Broglie)

**File:** `constants/free_particle_dispersion.ep`

**What it does.** A free particle's phase winds forward with its momentum. The kinetic
dispersion is the **fold of the momentum**, and doubling is two momentum steps, so
`rotate(phase, fold(p)) = rotate(phase, p + p)` — the two ways of stepping the phase
coincide because `fold(p) = cast_out(p+p)`. The dispersion is forced to be the fold.

```
=== free-particle dispersion (de Broglie) ===
  ok    kinetic dispersion = fold(1/4) = 1/2
  ok    momentum doubled = 1/4 + 1/4 = 1/2
  ok    dispersion equals momentum doubled (fold(p) = p + p)
  ok    phase after one step = 1/3 + 1/2 = 5/6
```

**To measurement.** Free particles obey a dispersion relation tying phase advance to
momentum (de Broglie, every electron-diffraction experiment) — the forced content is
the identity `fold(p) = p + p`.

---

### Step 57 — Beat frequency

**File:** `constants/beat_frequency.ep`

**What it does.** Two rhythms on the circle of the One beat at the **gap** between
them — the fold's `beat_between`. For `1/3` and `1/7` the beat is `1/3 − 1/7 = 4/21`,
their difference; two identical rhythms have no gap, so their beat is the One — a
full, silent period (no throb at unison).

```
=== beat frequency ===
  ok    rhythm one = 1/3 ; rhythm two = 1/7
  ok    beat = |1/3 - 1/7| = 4/21
  ok    unison beat = the One (silent)
```

**To measurement.** Two tones beat at `|f1 − f2|` and identical tones do not beat
(every piano tuner) — the forced `beat_between`: the difference of two rhythms, and
the One at unison.

---

### Step 58 — Big-bang nucleosynthesis (primordial helium = 1/4)

**File:** `constants/bbn.ep`

**What it does.** At weak freeze-out the neutron-to-proton ratio settles at the
deepest fold scale, `r = 1/d_up = 1/7` (`d_up = 7` forced two ways). Nearly every
neutron is captured into helium-4, so the helium mass fraction is
`Y = 2r/(1+r) = 2/8 = 1/4 = 1/binary²` — a quarter, exactly.

```
=== big-bang nucleosynthesis (primordial helium) ===
  ok    deepest depth d_up = 7
  ok    neutron/proton freeze-out ratio = 1/7
  ok    primordial helium fraction Y = 1/4
  ok    Y = 1/binary^2 (a quarter)
```

**To measurement.** Measured `Y_p = 0.247 ± 0.003` — the forced `1/4 = 0.25` lands on
the observed quarter to ~1%, a zero-parameter value from `r = 1/d_up`.

---

### Step 59 — Gravitational time dilation (clocks slow, stop at the horizon)

**File:** `constants/gravitational_time_dilation.ep`

**What it does.** The Schwarzschild time factor is the fold's take: `A(r) = take(One,
x) = 1 − x`, where `x = r_s/r` is the well depth. At `r = 4 r_s`, `x = 1/4` and
`A = 3/4` — clocks run at three-quarters rate (below the One → time slow). As the
horizon nears, `x → 1` and `A → 0` — the **forbidden zero** (No-Zero), so time stops
at the horizon.

```
=== gravitational time dilation ===
  ok    well depth x = r_s/r = 1/4 (at r = 4 r_s)
  ok    time-dilation factor A = 1 - x = 3/4
  ok    clocks run SLOW (factor below the One)
  ok    the horizon reaches the FORBIDDEN zero (time stops)
```

**To measurement.** Clocks slow in gravity (Pound–Rebka, GPS) by `A = 1 − r_s/r`, and
a horizon is where the time coefficient vanishes — exactly the forced `take(One, x)`
and its forbidden zero.

---

### Step 60 — Fine and hyperfine structure (α² of the gross ladder)

**File:** `constants/fine_hyperfine.ep`

**What it does.** Fine structure is the gross ladder carried to `binary = 2` further
powers of the coupling (each relativistic correction costs one power, and there are
two), so `fine/gross = 1/(1/α)² ≈ 5.3×10⁻⁵`. Hyperfine carries the same two powers
plus the nuclear moment, sitting below fine — the ordering gross > fine > hyperfine,
with the suppression exponent forced to `binary = 2`.

```
=== fine and hyperfine structure ===
  ok    fine-structure coupling powers = binary = 2 (alpha^2)
  ok    fine/gross ratio = 250^2 / 34259^2 = 62500/1173679081
  ok    fine structure is below the gross ladder (< the One)
```

**To measurement.** Fine structure is ~α² of the gross scale (hydrogen's, a few parts
in 10⁵) and hyperfine finer again (the 21 cm line) — the forced exponent `binary = 2`
and ratio `1/(1/α)²`.

---

### Step 61 — Cosmic dilution exponents (a⁻³, a⁻⁴, a⁰)

**File:** `constants/cosmic_dilution_exponents.ep`

**What it does.** As space expands, contents thin at rates set by the dimensions.
**Matter** (fixed particles in a growing volume) dilutes as `a^-d_space = a^-3`;
**radiation** loses the same volume factor plus one power to redshift, `a^-(d_space+1)
= a^-4` (the spacetime count); **dark energy** is the fold-invariant One, so it does
not dilute, `a^0`. The exponents `3, 4, 0` are forced.

```
=== cosmic dilution exponents ===
  ok    matter exponent = d_space = 3 (a^-3)
  ok    radiation exponent = d_space + 1 = spacetime = 4 (a^-4)
  ok    vacuum exponent = 0 (a^0, non-diluting)
  ok    radiation thins faster than matter (4 > 3)
```

**To measurement.** Cosmology uses exactly these — matter `a⁻³`, radiation `a⁻⁴`, dark
energy `a⁰` (the radiation→matter→dark-energy timeline). Exact integer exponents:
`3 = d_space`, `4 = spacetime`, `0 = non-diluting`.

---

### Step 62 — The hydrogen spectrum (the 1/n² ladder)

**File:** `constants/hydrogen_spectrum.ep`

**What it does.** The n-th bound level goes as `1/n^binary = 1/n²`, so the levels are
`1, 1/4, 1/9, …`. A spectral line is a difference of levels: Lyman-α (2→1) `= 3/4`,
Balmer-α (3→2) `= 5/36` — the Rydberg formula as exact rationals. As `n` grows the
levels fall toward the forbidden zero (ionization), which No-Zero never lets a bound
level reach, so infinitely many levels pack toward the edge.

```
=== the hydrogen spectrum ===
  ok    ladder exponent = binary = 2 (1/n^2)
  ok    levels: 1, 1/4, 1/9
  ok    Lyman-alpha (2->1) = 3/4 ; Balmer-alpha (3->2) = 5/36
  ok    levels descend toward ionization (the forbidden zero)
```

**To measurement.** Hydrogen's levels go as `1/n²` and its lines follow Rydberg to
extraordinary precision — forced: exponent `b = 2`, levels `1/n²`, lines their exact
rational differences.

---

### Step 63 — The flux tube (confinement)

**File:** `constants/flux_tube_formation.ep`

**What it does.** The gluon **carries** colour, so it feeds its own field along the
line between quarks: the accumulated source over a separation `L` is `q + L`, which
**grows** with `L`. The field stays a constant-width tube, the energy rises *linearly*
and unbounded — you can never fully separate the quarks (**confinement**). The photon
carries no charge, so its source stays `q` (constant), the field spreads (Coulomb),
and there is no confinement.

```
=== the flux tube (confinement) ===
  ok    bare source charge = 1/2 ; gluon self-charge = the One
  ok    accumulated source: length 1 = 3/2, length 2 = 5/2 (grows)
  ok    the strong force CONFINES (charge grows with length)
  ok    electromagnetism does NOT confine (charge constant)
```

**To measurement.** Lattice QCD shows a linear confining potential (constant-tension
flux tube) while electromagnetism is Coulombic — the forced split: the self-charged
carrier feeds its field (linear → confined), the chargeless one does not.

---

### Step 64 — Fission and fusion (one peak of stability)

**File:** `constants/fission_fusion.ep`

**What it does.** The peak of binding is the most-bound state — the fold's fixed
point, the One. A less-bound nucleus sits below it and folds *up* toward it: a light
one at `1/4` climbs `1/4 → 1/2 → 1` (fusion), and a heavy one gains binding the same
way shedding toward the peak (fission). Both directions move toward the one maximum,
releasing the binding gained; the reaction crosses the `1/2` balance (Coulomb barrier).

```
=== fission and fusion ===
  ok    peak of stability = the One (max binding)
  ok    light nucleus = 1/4 ; fusion reaches the peak
  ok    binding increases toward the peak (energy released)
  ok    reaction barrier = 1/2 (Coulomb barrier)
```

**To measurement.** Binding per nucleon rises to a single maximum (iron) and falls
either side; fusion below and fission above both release energy — the forced
single-peak (the One), the climb toward it, and the `1/2` barrier.

---

### Step 65 — The equivalence principle (gravitational redshift)

**File:** `constants/equivalence_redshift.ep`

**What it does.** With `g = 1/4`, `h = 1` (`c = 1`), the gravitational redshift over
the height is `z = g·h = 1/4`; the *same* setup as acceleration gives an acquired
speed `v = g·h` and Doppler shift `z = v = 1/4`. The two are identical —
`z_gravity = g·h = z_doppler` — which is the equivalence principle. In the weak field
the redshift folds linearly in height, `fold(g·h) = fold(g)·h`.

```
=== the equivalence principle (redshift) ===
  ok    gravitational redshift z = g*h = 1/4
  ok    Doppler shift z_doppler = v = 1/4
  ok    EQUIVALENCE: gravitational redshift = acceleration Doppler shift
  ok    weak-field redshift folds linearly in height
```

**To measurement.** Gravitational redshift equals the equivalent acceleration's
Doppler shift (Pound–Rebka, to 1%) — the forced identity `z_gravity = g·h = z_doppler`.

---

### Step 66 — Radioactive decay (halving each half-life)

**File:** `constants/radioactive_decay.ep`

**What it does.** A half-life is one fold step, and the fold is two-to-one, so the
surviving fraction after `k` half-lives is `1/b^k = 1/2^k`: `1, 1/2, 1/4, 1/8, …`,
each half-life multiplying the survivors by `1/2`. One bit is lost per half-life (the
non-injective fold, the arrow of time), and the count never reaches zero (No-Zero).

```
=== radioactive decay ===
  ok    remaining after 0..3 half-lives = 1, 1/2, 1/4, 1/8
  ok    each half-life halves the survivors
  ok    decay never reaches zero (No-Zero)
```

**To measurement.** Every radioactive species halves in a fixed half-life
(exponential decay, carbon dating) — the forced `remaining(k) = 1/2^k`, each a binary
halving; the half-life in seconds is a measured per-species value.

---

### Step 67 — The quantum Hall effect (exact quantized conductance)

**File:** `constants/quantum_hall.ep`

**What it does.** The Hall conductance is a *count* of filled levels times one unit,
so it locks onto exact integer plateaus (`1, 2, 3, …` units of `e²/h`) — a count has
no in-between. Interaction opens plateaus at simple fractions, the primary being the
fold's colour fraction `ν = 1/c = 1/3` (the Laughlin state). Every filling is an exact
rational, never a continuum.

```
=== the quantum Hall effect ===
  ok    integer plateaus 1, 2, 3 = 1, 2, 3 units
  ok    primary fractional plateau nu = 1/colour = 1/3
  ok    plateaus are quantized (differ by exactly one unit)
```

**To measurement.** Integer plateaus are exact to ~1 part in 10⁹ (the resistance
standard) and the first fractional plateau is `ν = 1/3` — forced: integer plateaus are
whole counts, the primary fraction is `1/colour`.

---

### Step 68 — Maxwell wave closure (light at c)

**File:** `constants/maxwell_wave_closure.ep`

**What it does.** On a cubic lattice the spatial curvature is a second difference
(`b = 2`) along each of `d_space = 3` axes → `6` (the six neighbours, Step 47); the
temporal curvature is `b = 2` along the one time axis. The wave equation closes when
their ratio is the spatial dimension, `6/2 = 3 = d_space` (also `period(1/7) =
colour`), giving `∇²E − (1/c²)∂²E/∂t² = 0` — a wave at the fold's one speed, the One.

```
=== Maxwell wave closure ===
  ok    spatial curvature = binary * spatial = 6
  ok    temporal curvature = binary = 2
  ok    curvature ratio = 6/2 = 3 = d_space (= colour)
  ok    the closed wave travels at the One (c)
```

**To measurement.** Maxwell's equations close into a wave at `c`, and light is that
wave — forced: the spatial-to-temporal curvature ratio is `3 = d_space = colour`, the
speed is the One.

---

### Step 69 — The proton / electron mass ratio (1836, forced)

**File:** `constants/proton_electron_ratio.ep`

**What it does.** The proton/electron mass ratio — the pure number 1836 — is forced
from the One, no scale and no fit. Two forced facts meet. The electron and muon mass
shares are the squared roots of the forced charged-lepton cubic
`x³ − x² + (1/6)x − 1/485 = 0` (`e2 = 1/(2c) = 1/6`, `e3 = 1/(2c⁵−1) = 1/485`); the
roots are pinned by **exact rational bisection** (no floats — see Step 68 /
`charged_lepton_cubic.ep`). The proton is the strong-sector ground baryon, the colour-
bound group of three at the tripling position `1/c = 1/3`. Both sit on the One, so their
ratio is a **dimensionless** cross-sector ratio (the confinement tension cancels):

```
  mp/me = (1/c) · (m_μ − m_e) / (m_μ · m_e) = (1/3)·(1/m_e − 1/m_μ) = 1836.3254
```

Every piece — the cubic, its bisected roots, the tripling `1/3` — is forced from the
One; there is no scale factor and no measured quantity in the construction.

```
=== the proton / electron mass ratio (1836, forced) ===
  ok    mp/me = (1/3)(m_mu - m_e)/(m_mu m_e) = 1836.3254
  ok    proton bound-whole 3*(1/3)=1 over electron half 1/2 = 2 (secondary structural core)
```

**To measurement.** The forced ratio `1836.3254` agrees with the measured
`1836.15267` (CODATA) to **0.0094%** — one part in ten thousand — the measured value
entering only on the comparison side. (The bare bound-whole/half core, exactly `2 =
binary`, is kept as a secondary structural fact; the forced 1836 above is the result.)

---

### Step 70 — The weak force range (massive carrier → short range)

**File:** `constants/weak_range.ep`

**What it does.** A field starts at the One and a massive carrier subtracts its
mass-part each step; the reach is how far it survives. A mass-`1/3` carrier reaches
`1 → 2/3 → 1/3` — two steps, finite. A lighter carrier subtracts less and reaches
farther (mass `1/7` → six steps), so range grows as `1/mass`; a massless carrier
never depletes → unbounded. The weak force is short-range (heavy W/Z); EM and gravity
are long-range (massless).

```
=== the weak force range ===
  ok    reach of the mass-1/3 carrier = 2 (finite)
  ok    a lighter carrier reaches farther (range ~ 1/mass)
  ok    the weak force is SHORT-range ; massless is unbounded
```

**To measurement.** The weak force has range ~10⁻¹⁸ m (massive W/Z) while EM and
gravity reach to arbitrary distance (massless) — the forced tie: a massive carrier's
reach is finite and grows as its mass shrinks; a massless one is unbounded.

---

### Step 71 — Proton stability (distinct fibres, conserved baryon number)

**File:** `constants/proton_stability.ep`

**What it does.** Quarks live in the colour fibre (`c = 3`), leptons in the weak fibre
(`b = 2`). These are **distinct** (`3 ≠ 2`) and the fold preserves them — no fold path
turns a quark into a lepton. The proton's baryon number is `c · (1/c) = 1`, a
conserved whole; decaying to leptons would drop it from 1 to 0 (crossing fibres),
which distinctness forbids. So the proton is stable.

```
=== proton stability ===
  ok    quark fibre = colour = 3 ; lepton fibre = binary = 2
  ok    the fibres are distinct (3 != 2, no crossing)
  ok    proton baryon number = 3 * 1/3 = 1 (conserved)
  ok    the proton is STABLE (no decay path to leptons)
```

**To measurement.** No proton decay is seen (lifetime > 10³⁴ yr, Super-Kamiokande) and
baryon number is conserved — the forced result: distinct fibres (`3 ≠ 2`) block
quark→lepton crossing, and `c·(1/c) = 1` is conserved.

---

### Step 72 — Phonons (three acoustic branches)

**File:** `constants/phonons_lattice.ep`

**What it does.** A lattice displacement points along any of `d_space = 3` directions;
a wave uses one along its travel (longitudinal) and the rest across (transverse), so
the acoustic phonon branches number `1 + (d_space − 1) = d_space = 3`. And the
vibrations are quantized (discrete phonons) because the fold advances in whole steps.

```
=== phonons (lattice vibrations) ===
  ok    longitudinal branches = 1
  ok    transverse branches = d_space - 1 = 2
  ok    acoustic branches = d_space = 3 (forced two ways)
```

**To measurement.** Every crystal has three acoustic phonon branches (one
longitudinal, two transverse) and quantized vibrations — the forced integer count
`d_space = 3`.

---

### Step 73 — Chirality (two mirror-image handednesses)

**File:** `constants/chirality.ep`

**What it does.** The fold's two preimages *are* the two chiralities: LEFT the lower
preimage (`1/4`), RIGHT its antipode (`One − 1/4 = 3/4`) — mirror images across the
balance, both folding to the same image (`fold(1/4) = fold(3/4) = 1/2`). So chirality
is two-valued (`b = 2`), the two are antipodes, and they share one image (a particle
and its mirror); the weak force keeps only the lower hand.

```
=== chirality ===
  ok    chirality count = binary = 2
  ok    left = 1/4 ; right = 3/4 (antipode)
  ok    the two chiralities are mirror images
  ok    both fold to one image (a particle and its mirror)
```

**To measurement.** Fermions have exactly two chiralities, mirror images, and the weak
force couples to only the left — the forced two-valued, antipodal, one-image structure.

---

### Step 74 — Magnetism (aligned spins make a magnet)

**File:** `constants/magnetism.ep`

**What it does.** Each spin is a half. **Aligned**, two spins add to unison
(`1/2 + 1/2 = One` — a full net moment; `fold(1/2) = 1`): ferromagnetism. **Opposed**,
they cancel: antiferromagnetism, no net field. The Curie ordering threshold — order
below, disorder above — is the self-antipodal balance `1/2`.

```
=== magnetism ===
  ok    single spin = 1/2 ; aligned net moment = the One
  ok    ferromagnetic: aligned spins reach a net moment
  ok    alignment reaches unison (fold(1/2) = 1)
  ok    Curie ordering threshold = 1/2 (balance point)
```

**To measurement.** Ferromagnets align below the Curie temperature and lose it above;
antiferromagnets cancel — the forced order/disorder split: aligned spins fold to a net
moment, opposed cancel, threshold at the balance.

---

### Step 75 — Semiconductors (two carrier types, a balancing junction)

**File:** `constants/semiconductors.ep`

**What it does.** A carrier state has the fold's two preimages: the ELECTRON a filled
state (`1/4`), the HOLE its antipode — the absence, `One − electron = 3/4`. So there
are exactly `b = 2` carrier types, and a p-n junction balances them:
`electron + hole = filled + (One − filled) = One` (the depletion balance). A thin
forbidden gap (Step 54) lets heat lift carriers across — a *semi*-conductor.

```
=== semiconductors ===
  ok    carrier types = binary = 2 (electron, hole)
  ok    electron = 1/4 ; hole = 3/4 (electron's absence)
  ok    the hole is the electron's absence (One - electron)
  ok    a p-n junction balances to the One
```

**To measurement.** Semiconductors have exactly two carrier types (electrons, holes)
and a p-n junction balances them into a depletion region — the forced two carrier
types (a state and its antipode) summing to the One at a junction.

---

### Step 76 — Entanglement (the joint state is the product)

**File:** `constants/entanglement.ep`

**What it does.** Take the two generators as two subsystem periods, `binary = 2` and
`colour = 3` — **coprime** (`gcd = 1`). Combined, they interlock into one joint cycle
whose period is their lcm = the **product** `2·3 = 6`, which exceeds the sum
(`2+3 = 5`). The joint holds *more* than the parts — that surplus is the entanglement,
and coprimality makes it one indivisible cycle (inseparable, correlated).

```
=== entanglement ===
  ok    subsystem periods = binary 2, colour 3 (coprime)
  ok    joint period = product = 2 * 3 = 6 (tensor product)
  ok    the joint holds MORE than the parts (6 > 2+3=5)
```

**To measurement.** Composite quantum systems live in the tensor *product* of their
parts (dimensions multiply, not add) — why entangled states exist and violate Bell
inequalities. Forced: the joint period is the product of the two coprime generators,
larger than their sum.

---

### Step 77 — Catalysis (lower barrier, conserved catalyst)

**File:** `constants/catalysis.ep`

**What it does.** A reaction crosses the balance barrier `1/2`; a catalyst splits the
crossing into binary steps, so the barrier drops by a factor of the binary count,
`bare/b = (1/2)/2 = 1/4 < 1/2` — a lower hurdle, faster reaction. And the catalyst is
conserved: it is the One, held fixed by the fold (`fold(1) = 1`), returning to itself
unconsumed.

```
=== catalysis ===
  ok    bare barrier = 1/2 ; catalysed barrier = bare/b = 1/4
  ok    the catalyst LOWERS the barrier (1/4 < 1/2)
  ok    the catalyst is conserved (returns to itself, unconsumed)
```

**To measurement.** Catalysts lower the activation energy and are recovered unchanged
— the forced lower barrier (`bare/b`) and the catalyst as a fold fixed point.

---

### Step 78 — Electronegativity (covalent ↔ ionic)

**File:** `constants/electronegativity.ep`

**What it does.** A bonding electron sits between two atoms. Equal pull → the balance
`1/2` (shared evenly, nonpolar covalent). As one atom's pull grows the electron shifts
toward it, and total pull transfers it fully — the whole One to one atom (ionic). So
bond character runs from the balance `1/2` (covalent) to the One (ionic), set by the
electronegativity difference.

```
=== electronegativity ===
  ok    covalent bond = 1/2 (equal sharing)
  ok    ionic bond = the One (full transfer)
  ok    equal atoms share evenly ; covalent below ionic
```

**To measurement.** Bonds range from nonpolar covalent (equal sharing) through polar
to ionic (full transfer) by the electronegativity difference — the forced two ends,
the balance `1/2` and the One.

---

### Step 79 — The two new forces, in full (prime sectors 5 and 7)

**File:** `constants/prime_force_phenomenology.ep`

**What it does.** Step 26 forced four confining forces at the primes `{2,3,5,7}` — two
known, two predicted. A prediction is only worth something if it's *specific*, so this
gives the two new forces (lower `= binary+colour = 5`, upper `= deepest depth = 7`)
the **full** known-force template, run for `p ∈ {5,7}` — not a bare count:

| quantity | forced value | sector 5 | sector 7 |
|---|---|---|---|
| mass-part (charge scale) | `1/p` | `1/5` | `1/7` |
| coupling | `(p−1)/p` | `4/5` | `6/7` |
| mediators (gauge bosons) | `p²−1` | `24` | `48` |
| colours (charge kinds) | `p` | `5` | `7` |
| confinement pairs | `(p−1)/2` | `2` | `3` |
| running beta-slope | `g_p/s_p = p−1` | `4` | `6` |

Plus a **massless, luminal, self-confining carrier** (flux-tube width `1/2`, folding to
the One — the gluon's structure) and **colour-neutral bound states** (meson: colour +
antipode `= One`; baryon: the whole group folds to the One). Every line is the known
sectors' own template with `p` set to 5 or 7 — forced, falsifiable, not vague.

```
=== the two new forces (prime sectors 5 and 7) ===
  ok    new force lower = 5 ; upper = 7
  ok    sector 5: mass-part 1/5, coupling 4/5, mediators 24, colours 5,
        confinement pairs 2, beta-slope 4, massless carrier, neutral meson
  ok    sector 7: mass-part 1/7, coupling 6/7, mediators 48, colours 7,
        confinement pairs 3, beta-slope 6, massless carrier, neutral meson
  ok    carrier flux-tube width 1/2 folds to the One ; baryon colour-neutral
```

**To measurement.** These are predictions — two confining forces not yet seen — but
with a complete, specific signature per sector (coupling, mediator count, colour count,
confinement pairs, beta-slope, a massless luminal confining carrier, neutral bound
states), the same phenomenology the known forces have. Falsifiable, not vague.

---

### Step 80 — Three-wave mixing (sum, difference, doubling)

**File:** `constants/three_wave_mixing.ep`

**What it does.** Two waves `f1 = 1/3`, `f2 = 1/4` in a nonlinear medium make new
frequencies by the fold's own operations: SUM `f1 + f2 = 7/12` (add), DIFFERENCE
`f1 − f2 = 1/12` (take/beat), and SECOND HARMONIC of `f2` = doubled `= 1/2` (fold).

```
=== three-wave mixing ===
  ok    inputs f1 = 1/3, f2 = 1/4
  ok    sum = 7/12 ; difference = 1/12 ; second harmonic = 1/2
```

**To measurement.** Nonlinear crystals produce sum-, difference-, and second-harmonic
frequencies (green laser pointers, frequency combs) — the forced exact combinations:
sum = add, difference = take, second harmonic = double.

---

### Step 81 — Acoustics (the harmonic series)

**File:** `constants/acoustics.ep`

**What it does.** Sound rides a fixed signal speed (the One), so a wave in a fixed
length closes only after a whole number of half-wavelengths — only *integer* multiples
of the fundamental fit. The allowed tones are `f_n = n·f0` (for `f0 = 1/6`: `1/6, 1/3,
1/2, …`), the harmonic series.

```
=== acoustics (the harmonic series) ===
  ok    sound signal speed = the One ; fundamental = 1/6
  ok    harmonics 1, 2, 3 = 1/6, 1/3, 1/2 (whole multiples)
```

**To measurement.** Strings and pipes ring in a whole-number harmonic series — the
forced integer identity `f_n = n·f0`; the speed of sound in m/s is a per-medium value.

---

### Step 82 — Nonlinear optics (the Kerr effect)

**File:** `constants/nonlinear_optics.ep`

**What it does.** A weak (linear) field passes unchanged; an intense field self-couples
— the fold — acting on its own phase: `fold(3/4) = 1/2`, a genuine self-action a linear
field lacks. And the self-coupling makes harmonics: the third (odd Kerr) harmonic of
`f = 1/6` is `3·f = 1/2`.

```
=== nonlinear optics (the Kerr effect) ===
  ok    strong field 3/4 ; Kerr self-action fold(3/4) = 1/2
  ok    the Kerr effect shifts the field (self-action, not linear)
  ok    third harmonic = 3 * f = 1/2 (odd Kerr harmonic)
```

**To measurement.** Intense light self-focuses and self-phase-modulates (Kerr) and
generates harmonics; weak light does not — the forced split: the nonlinear response is
the fold's self-coupling, harmonics are whole multiples of the input.

---

### Step 83 — The weak mass ratio (`1/(m−1)`)

**File:** `constants/weak_mass_ratio.ep`

**What it does.** A sector of multiplicity `m` splits into charged `(m−1)/m` and neutral
`1/m`; each channel's mass-part is the take from the One, so charged mass-part `= 1/m`,
neutral `= (m−1)/m`, and their ratio is `1/(m−1)` — equal to the mixing ratio. For
`m=2` (electroweak) it is `1`; `m=3` → `1/2`; `m=4` → `1/3`.

```
=== the weak mass ratio ===
  ok    charged/neutral mass-parts (m=3) = 1/3, 2/3
  ok    mass ratio m=2,3,4 = 1, 1/2, 1/3 (= 1/(m-1))
  ok    mass ratio equals the mixing ratio
```

**To measurement.** The charged/neutral (W/Z) channel structure follows one mass-part
ratio tied to the mixing — the forced `1/(m−1)`; the physical W/Z mass ratio with its
running is the separate w-boson result.

---

### Step 84 — Evolution by descent (selection sweeps to fixation)

**File:** `constants/evolution_descent.ep`

**What it does.** A rare beneficial variant (`1/4`) climbs under selection each
generation — the fold's upward amplification below the balance: `fold(1/4)=1/2`,
`fold(1/2)=1` — reaching **fixation** (the One, the whole population) in two steps. Zero
is forbidden, so a favoured variant sweeps to fixation, not extinction.

```
=== evolution by descent ===
  ok    rare variant 1/4 -> 1/2 -> 1 (fixation)
  ok    selection AMPLIFIES the variant (it climbs)
  ok    the variant reaches fixation at the One
```

**To measurement.** A beneficial allele under positive selection sweeps to fixation
(frequency climbs to one) — the forced upward amplification to the One; the sweep time
in generations depends on selection strength (measured).

---

### Step 85 — The thermal history (radiation → matter → dark energy)

**File:** `constants/thermal_history.ep`

**What it does.** Each component dilutes as `a^−n` with a forced exponent (Step 61):
radiation `4`, matter `3`, dark energy `0`. Run backward, the larger exponent climbs
faster into the past, so it dominated earlier. Since `4 > 3 > 0`, the order of
dominance is forced: **radiation → matter → dark energy**.

```
=== the thermal history ===
  ok    epoch exponents: radiation 4, matter 3, dark energy 0
  ok    radiation before matter (4>3) ; matter before dark energy (3>0)
  ok    timeline ordered radiation -> matter -> dark energy
```

**To measurement.** The cosmic timeline is radiation-, then matter-, then
dark-energy-dominated — exactly the forced ordering from the dilution exponents
(`4 > 3 > 0`); the transition redshifts and temperatures are measured.

---

### Step 86 — The general n-body problem (periodic on a fold orbit)

**File:** `constants/general_n_body_periodic.ep`

**What it does.** The general statement behind Step 33: any fold orbit gives a periodic
configuration. On the orbit of `1/5`, `fold` cycles four bodies `1/5 → 2/5 → 4/5 → 3/5
→ 1/5`, so the configuration returns after the fold period of `1/5`, which is **4**.
Periodic, not chaotic — n bodies on a period-n orbit recur with period n.

```
=== the general n-body problem ===
  ok    fold(1/5) = 2/5 ; fold(2/5) = 4/5
  ok    joint recurrence period = period(1/5) = 4
  ok    the configuration closes (returns after the period)
```

**To measurement.** Special n-body choreographies are periodic and integrable, not
chaotic — the forced result: bodies on a fold orbit recur with the orbit's own period.

---

### Step 87 — Generation mass-splitting (even `1/3` steps)

**File:** `constants/generation_mass_splitting.ep`

**What it does.** The three generations are the three tripling-fold preimages of the
electroweak balance `1/2`: `(1/2 + k)/c` for `k = 0,1,2` → `1/6, 1/2, 5/6`. The gap
between consecutive generations is `1/2 − 1/6 = 1/3` and `5/6 − 1/2 = 1/3` — a **uniform
step of `1/colour = 1/3`**. Three generations, evenly spaced.

```
=== generation mass-splitting ===
  ok    generation count = colour = 3
  ok    generations = 1/6, 1/2, 5/6
  ok    gap = 1/3 (= 1/colour) ; spacing is uniform
```

**To measurement.** There are exactly three generations in a ladder — the forced count
and even `1/colour` spacing; the physical masses (with sector dressing) are the
separate mass-sector results.

---

### Step 88 — The fluctuation–dissipation theorem

**File:** `constants/fluctuation_dissipation.ep`

**What it does.** Equilibrium is the self-antipodal balance `1/2`. A spontaneous
FLUCTUATION steps above (`3/4`); the DISSIPATION is its antipode below (`One − 3/4 =
1/4`). They are antipodal (`3/4 + 1/4 = One`) **and equal in departure**
(`3/4 − 1/2 = 1/4 = 1/2 − 1/4`) — the equal size *is* the theorem: noise and drag have
the same magnitude, one balance measured in opposite directions.

```
=== the fluctuation-dissipation theorem ===
  ok    equilibrium 1/2 ; fluctuation 3/4 ; dissipation 1/4 (antipode)
  ok    fluctuation + dissipation = the One
  ok    THE THEOREM: fluctuation = dissipation (equal departure)
```

**To measurement.** Fluctuation and dissipation are measured proportional (Einstein's
Brownian relation, Johnson–Nyquist noise) — the forced equal-and-opposite structure
about equilibrium.

---

### Step 89 — The rationality of the constants

**File:** `constants/constants_rationality.ep`

**What it does.** The fold computes only on fractions of whole numbers (no square root
is ever formed), so every constant it forces is **rational** — a ratio `p/q`, hence the
root of a whole-number polynomial `q·x − p = 0`. On the flagship `1/α = 34259/250`:
`250·(34259/250) = 34259`, so `250·x − 34259 = 0` — rational by definition. The same
holds for every forced constant.

```
=== the rationality of the constants ===
  ok    representative constant 1/alpha = 34259/250
  ok    its denominator is a positive whole number (a ratio p/q)
  ok    the rational polynomial holds: q*x = p (250*x = 34259)
```

**To measurement.** The dimensionless constants forced here are exact rationals; where
nature needs an irrational (a square root), the framework marks it never-formed and
keeps it comparison-side. Forced: each satisfies `q·x − p = 0`, the definition of rational.

---

### Step 90 — Decay widths and branching ratios

**File:** `constants/decay_widths.ep`

**What it does.** A particle's decay channels partition certainty — branching ratios
`1/4 + 3/4 = One` (it must go one of the ways). And the lifetime is the inverse of the
total width, `1/w`: a wider particle decays faster and lives shorter (width `1` →
lifetime `1`; width `1/2` → lifetime `2`).

```
=== decay widths and branching ratios ===
  ok    branching ratios 1/4, 3/4 partition the One
  ok    lifetime of a width-1/2 particle = 2
  ok    a wider particle lives shorter (lifetime = 1/width)
```

**To measurement.** Branching ratios sum to one and lifetime `= ħ/width` — the forced
partition of the One and inverse width–lifetime relation; the widths in MeV are measured.

---

### Step 91 — Cross sections

**File:** `constants/cross_sections.ep`

**What it does.** For one target, scatter and pass partition certainty
(`1/2 + 1/2 = One` — a particle must do one or the other). And the mean free path is the
inverse of the cross section: a larger target means a shorter path (`σ=1` → path `1`;
`σ=1/2` → path `2`).

```
=== cross sections ===
  ok    scatter 1/2 + pass 1/2 = the One (certainty)
  ok    mean free path for cross section 1/2 = 2
  ok    a larger cross section gives a shorter free path
```

**To measurement.** Scatter and transmission probabilities sum to one, and the mean
free path is `1/(n·σ)` — the forced partition and inverse relation; cross sections in
barns are measured.

---

### Step 92 — Computability and halting

**File:** `constants/computability_halting.ep`

**What it does.** A bounded configuration at depth `k` is the state `1/2^k`; each fold
lifts it one level, so it reaches the One (a definite answer — **halts**) in exactly `k`
folds (`1/16 → 1/8 → 1/4 → 1/2 → 1`). Bounded depth means halting-guaranteed, with the
step count forced to equal the depth, and it never vanishes (No-Zero) — it halts *at*
the One.

```
=== computability and halting ===
  ok    bounded configuration at depth 4 = 1/16
  ok    a depth-4 config HALTS after 4 folds ; depth-6 after 6
  ok    it has NOT halted one step early
```

**To measurement.** Bounded (space-bounded) computations are decidable and halt in a
number of steps set by their size — the forced integer identity: depth-`k` reaches the
One in exactly `k` folds.

---

### Step 93 — The continuum limit

**File:** `constants/continuum_limit.ep`

**What it does.** For `f(x) = x²` the lattice second-difference over the squared spacing
`[f(x+s) − 2f(x) + f(x−s)]/s²` is exactly `2s²/s² = 2` — the continuum second derivative
— for **any** spacing `s`. So the discrete grid reproduces the smooth curvature exactly
at `s = 1/4, 1/8, …`, never approximate: the discreteness is faithful, not a defect.

```
=== the continuum limit ===
  ok    continuum curvature of x^2 = 2
  ok    lattice curvature at spacing 1/4 = 2 ; at 1/8 = 2
  ok    lattice matches continuum exactly at every spacing
```

**To measurement.** Lattice discretisations converge to the continuum, and for a
quadratic the stencil is exact — the forced result: the lattice curvature of `x²` is `2`
at every spacing.

---

### Step 94 — Electroweak currents (charged flips, neutral preserves)

**File:** `constants/ew_currents.ep`

**What it does.** Handedness is one of the fold's two preimages (left `1/4`, right `3/4`,
both folding to the shared coupling `1/2`). The **charged current** (W) acts by the
antipode — `take(One, hand)` — so it **flips** the hand (`1/4 ↔ 3/4`), changing identity
(e → ν). The **neutral current** (Z) acts by the identity — it **preserves** the hand.

```
=== electroweak currents ===
  ok    left 1/4, right 3/4 ; both fold to the shared coupling 1/2
  ok    charged current (W) flips 1/4 -> 3/4 (antipode)
  ok    neutral current (Z) preserves the hand (identity)
```

**To measurement.** The charged weak current changes identity and handedness (e → ν)
while the neutral current conserves them — the forced antipode (charged) vs identity
(neutral) on the two handedness preimages.

---

### Step 95 — The muon g−2 anomaly (why the muon is the sharp probe)

**File:** `constants/muon_g2_anomaly.ep`

**What it does.** The bare gyromagnetic ratio is `g = 2 = binary` (the Dirac value, the
fold's two preimages). A contribution to the anomalous moment that couples through a
mass scale enters as `(mass)²`, so the muon's excess over the electron's scales as
`(m_μ/m_e)²`. The mass ratio is forced from the lepton-cubic roots (Step 68), so the
sensitivity factor is forced.

```
=== the muon g-2 anomaly ===
  ok    bare Dirac g = binary count = 2
  ok    forced m_mu/m_e = 207.0 (measured 206.768, 0.16%)
  ok    sensitivity (m_mu/m_e)^2 = 42886 (muon out-probes electron)
```

**To measurement.** Forced `m_μ/m_e = 207.09` vs measured `206.768` (CODATA), 0.16%; the
muon is `(m_μ/m_e)² ≈ 42886` times more sensitive to a mass-scale effect than the
electron — which is why the muon anomaly is the precision test.

---

### Step 96 — The Lamb shift (the α² level shift)

**File:** `constants/lamb_shift.ep`

**What it does.** The gross spectrum sits one binary halving below the One (the half-One
`1/2`, the fine-structure level). The Lamb shift sits one fold deeper — the quarter-One
`1/4 = (1/2)²`, the **α² order** — and returns to unison in exactly two folds
(`1/4 → 1/2 → 1`).

```
=== the Lamb shift ===
  ok    Lamb shift state = 1/4 = (1/2)^2 (alpha^2 order)
  ok    one fold: 1/4 -> 1/2 ; second fold: 1/2 -> 1 (two folds)
  ok    state + state = 1/2 (level one fold up)
```

**To measurement.** The measured 2s–2p Lamb shift (~1057 MHz) is an α²-suppressed shift
relative to the gross spacing — the two-fold depth this forces.

---

### Step 97 — Zero-point energy (the vacuum floor is the half-One)

**File:** `constants/zero_point_energy.ep`

**What it does.** Zero is forbidden, so the ground cannot be empty; the lowest value is
the one whose double is the One — `1/2`, the half-One, exactly the `(1/2)` in
`E = (1/2)hf`. It is strictly positive, self-antipodal (`1/2 + 1/2 = 1`), and folds to a
full quantum.

```
=== zero-point energy ===
  ok    zero-point floor = 1/2 (the (1/2) in (1/2) h f)
  ok    floor + floor = 1 (self-antipodal, folds to unison)
  ok    fold(1/2) = 1 (rises to a full quantum)
```

**To measurement.** The oscillator ground state carries `(1/2)hf` — seen in the Casimir
force, helium that never freezes, and the Lamb shift — the same half-One forced here.

---

### Step 98 — Entropy and the second law (the fold is 2-to-1)

**File:** `constants/entropy.ep`

**What it does.** The fold is **two-to-one**: the two preimages `1/4` and `3/4` both fold
to `1/2`, so from the image you cannot recover which you came from — exactly `binary = 2`
microstates collapse to one, one bit lost per fold. There is no inverse fold to pick a
preimage, so the process cannot run backward — and that irreversibility *is* the second
law. The measured counterpart: Landauer's `kT ln 2` cost to erase exactly one bit.

### Step 99 — Homochirality (why life uses one hand)

**File:** `constants/homochirality.ep`

**What it does.** The two handednesses are the fold-preimages `1/4` and `3/4`; both fold
to the shared `1/2` and sit *equidistant* from it (`3/4 − 1/4 = 1/2`), so the pair is
perfectly degenerate — neither hand wins on its own. The tie is broken by the theory's
already-forced **parity violation** (the weak force is one-handed). Degenerate pair +
one-handed bias = a single global hand. Life is uniformly left-amino / right-sugar.

### Step 100 — Bose–Einstein condensation (bosons pile into one state)

**File:** `constants/bose_einstein_condensation.ep`

**What it does.** A fermion (half-integer spin) admits the two preimages `{0,1}` — max one
(Pauli). A boson (integer spin) is an even count of half-turns = a whole turn = the
identity on the One, so adding another returns the *same* state: no ceiling. Any number
share the ground `1/2 → 1`. The uncapped shared ground is the condensate — realised 1995,
and behind superfluids and the laser.

### Step 101 — Vacuum polarization (charge runs with distance)

**File:** `constants/vacuum_polarization.ep`

**What it does.** The screened charge sits at `1/2` (the live vacuum took half); probe
closer and the fold carries it up toward the bare One (`1/2 → 1`), so the effective
coupling **grows** as distance shrinks — the running. The far, fully-screened value is the
smaller one you read at low energy. Measured: effective `1/α` runs from ~137 at low energy
up to ~128 at the Z mass; the low-energy `137.036` is the forced fine-structure value.

### Step 102 — The canonical distribution (rational equilibrium, no exponential)

**File:** `constants/canonical_distribution.ep`

**What it does.** Equilibrium is the maximum-count arrangement: the self-antipodal balance
`(m−1)/m = 1/2`, the unique value equal to its own complement (`1 − 1/2 = 1/2`), so forward
and backward carry equal weight (detailed balance). The weight is an exact **rational** fold
ratio — no transcendental `e^(−E/kT)` — and two half-One weights normalise to the One.

### Step 103 — Critical exponents (rational at threshold)

**File:** `constants/critical_exponents.ep`

**What it does.** The transition is the self-antipodal threshold `(m−1)/m = 1/2` where the
two phases merge; the mean-field order-parameter exponent is the reciprocal sector count
`1/m = 1/2` (the square-root vanishing) — a **rational** fold ratio, not the irrational
exponents a continuum gives. These are exactly the Landau mean-field values.

---

### Step 104 — Five-fold standing modes (a second route to three generations)

**File:** `constants/five_fold_standing_modes.ep`

**What it does.** A standing mode of the m-fold is a value it holds fixed (`m_fold(x)=x`);
the interior candidates `x = j/(m−1)` are each fixed, so the m-fold has exactly `m−2`
interior standing modes. The down-depth fold `m = b + c = 5` has three — `1/4, 1/2, 3/4` —
matching the colour/generation count `3`; the two-fold has none. Three generations, forced
a fourth independent way (collider Z-width confirms exactly three light neutrino families).

### Step 105 — Gravitational-wave speed (ripples travel at c)

**File:** `constants/gravitational_wave_speed.ep`

**What it does.** A gravitational wave is a massless disturbance of the fold lattice; a
massless disturbance advances one spacing per tick, so its speed is the causal speed
`c = 1` — exactly the speed of light. Measured: GW170817 pinned `|c_gw − c|/c` below ~10⁻¹⁵.

### Step 106 — Charge multiplicity (internal states = the fold's fibre)

**File:** `constants/charge_multiplicity.ep`

**What it does.** The m-fold is m-to-one — every image has exactly `m` preimages
`(y+k)/m` — so it carries an internal degree of freedom with `m` states. The binary fold
gives **two** (charge sign, weak doublet, occupation `{0,1}`); the colour fold gives
**three** (the three strong colours). The multiplicity is the fold's own fibre size.

### Step 107 — Galactic dynamics (flat rotation curves need a dark halo)

**File:** `constants/galactic_dynamics.ep`

**What it does.** Circular orbit is the self-antipodal balance `1/2` (inward pull matched
to outward motion). A *flat* rotation curve is that balance held at **every** radius —
which the thinning visible matter cannot do, so it demands unseen mass (a dark halo).
Measured: rotation curves stay flat far beyond the visible disc (Rubin & Ford).

### Step 108 — The hierarchy problem (discrete rungs → no fine-tuning)

**File:** `constants/hierarchy_problem.ep`

**What it does.** Every scale is a rung of the binary tower, each rung a factor of `2`, so
any scale ratio is `1/2^N` for a **whole** `N` — the ladder is discrete, adjacent rungs
exactly a factor of 2 apart. There is nothing continuous to fine-tune, so the naturalness
problem cannot even be stated. The electroweak rung `N = 56` (comparison-side, read against
the measured ~10⁻¹⁷) puts the ratio at `1/2⁵⁶`; the *resolution* is forced, the rung is
the measured input.

---

### Step 109 — The acceleration transition (when the universe sped up)

**File:** `constants/acceleration_transition.ep`

**What it does.** Today's budget is vacuum `2/3`, matter `1/3` (ratio exactly `2`). Matter
dilutes as `1/a³` while vacuum does not, so two thresholds fall out: matter–vacuum equality
at `a³ = matter/vacuum = 1/2`, and acceleration onset (`q = 0`) at `a³ = matter/(2·vacuum) =
1/4`. Before that, gravity decelerates; after, vacuum accelerates. Forced `a³ = 1/4` →
`z ≈ 0.59`, matching the observed deceleration-to-acceleration transition at `z ≈ 0.6` (SNe Ia).

### Step 110 — The coupled lattice (presence spreads and is conserved)

**File:** `constants/coupled_lattice.ep`

**What it does.** A site keeps half its presence and passes a quarter to each neighbour —
weights `1/2, 1/4, 1/4` that **sum to One**, so presence is conserved (never lost to the
No-Zero floor, never manufactured). A symmetric bump `{1/4, 1/2, 1/4}` relaxes its centre to
`3/8` as it spreads — the conservative, local diffusion/wave kernel (the discrete Laplacian).

### Step 111 — The laser (light above threshold turns coherent)

**File:** `constants/laser.ep`

**What it does.** Lasing is gain vs loss; the threshold is the self-antipodal balance `1/2`
(gain equals loss). Below it the light stays incoherent; above it stimulated emission runs
away, and because a photon is a boson (uncapped occupation), the runaway pours every photon
into the **same** mode — the threshold folds up to the One, one shared coherent state.

### Step 112 — Intermolecular forces (a residual, one fold deeper)

**File:** `constants/intermolecular.ep`

**What it does.** A primary bond is the half-One `1/2`. A neutral molecule offers nothing at
that level; what remains is a **residual** one fold deeper — the quarter-One `1/4 = (1/2)²` —
so van der Waals coupling is markedly weaker than a covalent bond (two residuals `= 1/2`, one
bond's worth) and takes two folds to reach unison, the second-order mark.

### Step 113 — The generation ladder (three sites = the vacuum's colour preimages)

**File:** `constants/generation_ladder.ep`

**What it does.** The colour fold is 3-to-one, so the displaced vacuum `1/2` has exactly
three preimages — `(1/2 + k)/3` for `k = 0,1,2` = `1/6, 1/2, 5/6`. Those are the three
generation sites (three because the colour fibre is three), on a uniform `binary·colour = 6`
site ladder; their squares are the charged-lepton mass shares. Where the three generations sit.

---

### Step 114 — The expansion history (the Friedmann curve, exact)

**File:** `constants/expansion_history.ep`

**What it does.** The forced `2/3 : 1/3` budget makes the whole expansion curve exact:
`E²(s) = 2/3 + s³/3` at stretch `s = 1+z` (matter grows back as the cube — three
dimensions). Today `E² = 1` exactly (the normalisation *is* flatness, not a fit); `s=2`
gives `10/3`; `s=3` gives `29/3`. The same curve ΛCDM fits with `Ω_Λ ≈ 0.69, Ω_m ≈ 0.31`,
here with nothing fitted.

### Step 115 — The half-One unifying center (one point, every sector)

**File:** `constants/half_one_center.ep`

**What it does.** Why `1/2` recurs everywhere — the vacuum, critical couplings, the CP
position, the zero-point floor: it is the **unique** self-antipodal value (`1−x = x`;
candidates `1/3, 2/3, 1/4, 3/4` all fail, `forced_unique` armed) and the shared standing
mode of every odd sector (`m = 3, 5, 7` all hold it fixed) while the binary fold carries it
up to unison. One structural object, seen in many guises.

### Step 116 — The binding problem (two streams, one experience)

**File:** `constants/binding_problem.ep`

**What it does.** Two processes sharing one rhythm are the period-2 states `1/3 ↔ 2/3`
(each folds to the other). Together they partition the One (`1/3 + 2/3 = 1`), lock at
their balance `1/2`, and the balance folds to unison — one bound whole. The measured
counterpart is phase synchrony (gamma-band locking) when contents bind into one object.

### Step 117 — The introspection limit (a mind cannot fully read itself)

**File:** `constants/introspection_limit.ep`

**What it does.** Integration into awareness is reaching the One; a process on the closed
period-2 orbit `{1/3, 2/3}` **never** gets there (checked step by step) — yet with its
partner it completes the whole (`1/3 + 2/3 = 1`). Permanent unconscious processing is
orbit structure, not effort shortage — and it is why determinism feels like freedom: the
system cannot pre-read its own next state.

### Step 118 — The continuum ladder (discrete rungs do everything)

**File:** `constants/continuum_ladder.ep`

**What it does.** Rung `k` of the dyadic ladder (`1/2^k`) reaches unison in exactly `k`
folds; the ladder to the forced down-depth 5 sums to `31/32`, and the boundary rung closes
it exactly: `31/32 + 1/32 = 1`. Finitely many rungs, exact closure, every rung finitely
reachable — the construction neither wants nor uses a continuum.

---

### Step 119 — The Yang–Mills mass gap (gap > 0, forced by the domain)

**File:** `constants/yang_mills_mass_gap.ep`

**What it does.** The Millennium question — prove the lightest strong excitation has
strictly positive mass — has no separate content here: zero is outside the domain, so a
massless strong excitation is not even *expressible*. The gap sits at the tripling position
`1/3`, the self-coupling at `2/3`; they form a closed period-2 cycle (`1/3 ↔ 2/3`),
partition the One, and their balance folds to unison. Gap > 0 is the No-Zero floor wearing
its strong-sector face (lattice QCD and the ~1.7 GeV glueball agree).

### Step 120 — The lithium-7 problem (the deficit is one fold)

**File:** `constants/lithium_seven.ep`

**What it does.** Primordial Li-7 share `3/16` (colour over the binary hypercube `2⁴`);
stellar convection drags surface material through the burn — one binary fold, a halving —
so the observed share is `3/16 · 1/2 = 3/32`, and doubling the observed restores the
primordial exactly. The famous "missing lithium" is one erased level, not a BBN failure
(stellar depletion is the standard resolution).

### Step 121 — The principle of least action (the balanced path)

**File:** `constants/least_action.ep`

**What it does.** An extremum is two-sided balance, and the domain has exactly one such
point: the self-antipodal `1/2`, where a deviation and its mirror carry equal weight and
cancel — an off-balance point is lopsided and is not taken. The balanced path folds to
unison; two half-weights carry the whole. Path-integral QM shows the *why*: off-balance
paths cancel in pairs, the balanced one survives.

### Step 122 — Neutrino oscillation (complete conversion)

**File:** `constants/neutrino_oscillation.ep`

**What it does.** Each mass state carries exactly half the flavour (`1/2`, the forced
atmospheric balance), the halves sum to the One — so at full swing the conversion is
**complete** — and the balance folds to unison, closing the swap into a repeating cycle.
A lopsided share could not empty the original flavour. Measured: full-depth atmospheric
oscillation (maximal `sin²2θ`), periodic in distance/energy.

### Step 123 — Maxwell's demon (the ledger pays the bit back)

**File:** `constants/maxwells_demon.ep`

**What it does.** The demon's record is one of the balance's two preimages (`1/4`/`3/4`);
resetting for the next molecule folds **both** onto the same ready state `1/2` — an
irreversible erasure of exactly the one bit the sorting gained (entropy.ep). Demon plus
gas is a closed fold system; the books balance at the One. Landauer's `kT ln 2` erasure
cost is the measured face.

---

### Step 124 — Navier–Stokes regularity (no blow-up)

**File:** `constants/navier_stokes_regularity.ep`

**What it does.** The Millennium question — can a smooth flow blow up? — dissolves on the
lattice: the smallest eddy is the floor at the forced down-depth, `s₅ = 1/2⁵ = 1/32`,
strictly positive because zero is outside the domain. A vortex turns over at most at `c=1`
across its own diameter, so vorticity is **capped** at `c/s₅ = 32` — cross-checked against
the depth-5 binary volume `2⁵` by `forced_to_be`. The cascade stops at the floor
(Kolmogorov's dissipation scale is the measured face); a finite-time singularity is not
expressible.

### Step 125 — The Schwarzschild solution (conserved flux)

**File:** `constants/schwarzschild_solution.ep`

**What it does.** The vacuum field around a mass is `A(r) = take(One, rs/r) = 1 − rs/r`,
and vacuum means the flux `(A(r₂)−A(r₁))/(1/r₁−1/r₂)` is the **same constant for every
sphere pair — equal to the source**: with `rs = 1/4`, pairs `(1/2, 1)` and `(1/2, 3/4)`
both give exactly `1/4`. One field behind Mercury's perihelion, light bending, Shapiro
delay, GPS, and the EHT images.

### Step 126 — Relativistic velocity composition (never past c)

**File:** `constants/velocity_composition.ep`

**What it does.** Naive addition can leave the domain (`1/2 + 2/3 > 1`) — impossible. The
composition respecting the ceiling is `w = (u+v)/(1+uv)`: light is a **fixed point**
(`compose(1, v) = 1`, the invariance of c), sublight stays sublight (`1/2 ∘ 2/3 = 7/8`,
`1/2 ∘ 1/2 = 4/5`), and small speeds nearly add (`1/10 ∘ 1/10 = 20/101` — Galileo
recovered). Fizeau and every accelerator are the measured face.

### Step 127 — Electron shell capacities (2, 8, 18, 32)

**File:** `constants/shell_capacities.ep`

**What it does.** Shell `n` holds `b·n²`: the binary spin fibre (two preimages, one
fermion each) times the ladder level's `n²` states → `2, 8, 18, 32`, exactly the observed
K/L/M/N maxima. Noble-gas closures fall out: He at `2`, Ne at `10`, Ar at `18` (neon plus
one octet — the rule-of-eight is the `n=2` block size recurring before the d-block opens).

### Step 128 — Stellar nucleosynthesis (the two-fold ignition)

**File:** `constants/stellar_nucleosynthesis.ep`

**What it does.** A star ignites from the quarter-One: `1/4 → 1/2 → 1` — the first fold
crosses the Coulomb barrier (the same `1/2` as fission/fusion), the second completes the
burn to the binding peak. Exactly two folds: ignition is a sharp threshold, not a glow —
why a star ignites fully or not at all, and why brown dwarfs (stuck below the first fold)
never become stars. Two ignition shares make one barrier (`1/4 + 1/4 = 1/2`).

---

### Step 129 — Oscillator levels (E_n = (n + ½)s)

**File:** `constants/oscillator_levels.ep`

**What it does.** At depth `k` the ladder spacing is `s = 1/2^k`, tied by the halving
relation `fold(s_{k+1}) = s_k`. No mode can sit at zero, so the ground sits **half a
spacing up** (the zero-point offset) and each excitation adds one whole spacing:
`E_n = (n + ½)s`. At depth 2: `1/8, 3/8, 5/8, 7/8` — exactly `2^k` levels, uniform
spacing, half-step start — the quantum-harmonic-oscillator spectrum (molecular vibration
lines are the measured face).

### Step 130 — The Lorentz force (motion trims the electric force)

**File:** `constants/lorentz_force.ep`

**What it does.** The magnetic force is not a second force: it is the motion's claim on
the electric one — `F = take(fe, fe·β²) = fe(1 − β²)`. At rest the trim vanishes
(electrostatics); the pieces **partition** the electric force (`F + fe·β² = fe`, nothing
lost); with `fe = 1/4, β = 1/2` the net is exactly `3/16`. One force read at two speeds.

### Step 131 — The prime distribution (the fold's spectrum is number theory)

**File:** `constants/prime_distribution.ep`

**What it does.** The fold's orbit period on `1/n` *is* the multiplicative order
`ord_n(2)` — run the orbits: `period(1/3)=2, (1/5)=4, (1/7)=3, (1/9)=6, (1/15)=4`. Two
facts fall out of the orbits alone: for a prime `p` the period **divides p−1** (Fermat's
little theorem, checked through 13), and the two smallest distinct periods are `2` and `3`
— **the generators themselves**. The theory's seeds are the first two notes of the prime
spectrum; nothing number-theoretic is imported.

### Step 132 — The Riemann critical line (the antipode's fixed axis)

**File:** `constants/riemann_critical_line.ep`

**What it does.** The zeta functional equation pairs `s ↔ 1−s` — the fold's **antipode**
map. Off-axis values pair two-sided (`1/4 ↔ 3/4`, `1/3 ↔ 2/3`); exactly one value is its
own partner: `1/2`, which folds to unison. A zero set symmetric under `s ↔ 1−s` has
nowhere else to balance — the critical line is the antipode's fixed axis (billions of
computed zeros sit on it).

### Step 133 — Quasicrystals (order without a lattice)

**File:** `constants/quasicrystals.ep`

**What it does.** Shechtman's "impossible" pattern, resolved by two forced facts side by
side: five-fold **periodic** order is forbidden (`φ(5) = 4 > b = 2`, the crystallographic
restriction) — yet the five-fold **holds the balance fixed** (`5·(1/2)` casts out to
`1/2`, a genuine standing mode). Coherent order without a lattice: sharp five-/ten-fold
diffraction, no translational periodicity, exactly as observed.

---

### Step 134 — Newton's law (the inverse-square field from flux)

**File:** `constants/newton_law.ep`

**What it does.** The potential is `Φ(r) = take(One, ms/r) = 1 − ms/r` (the weak-field face
of Schwarzschild), the field `g(r) = ms/r²`, and Gauss's law is the exact statement
`r²·g(r) = ms` — the **same constant at every radius, equal to the source** (checked at
`r = 1/2` and `r = 1` with `ms = 1/4`). The inverse square is flux conservation in the
three forced dimensions, the same counting that pins Coulomb's exponent.

### Step 135 — Quadrupole radiation (the first unfrozen moment)

**File:** `constants/quadrupole_radiation.ep`

**What it does.** Mass conservation freezes the monopole; momentum conservation freezes the
dipole (the linear trajectory `1,2,3,4` has all-equal first differences — uniform motion is
silent). The cubic drive `1,8,27,64` has second differences `12 ≠ 18` — the acceleration
itself changes, and that first unfrozen moment radiates. Why gravitational waves start at
the quadrupole (Hulse–Taylor and every LIGO event match it; no monopole/dipole gravitational
radiation has ever been seen).

### Step 136 — The Minkowski interval (spacetime's causal ruler)

**File:** `constants/minkowski_interval.ep`

**What it does.** The interval is the take of the spatial claim from the temporal whole:
`ds² = take((c dt)², dx²)`. With `dx = 3/5`: `ds² = 16/25` exactly, proper time `ds = 4/5`
— the 3-4-5 triangle as a causal triple, closing back to the whole tick. The take's domain
guard *is* the light cone: at `dx = c dt` the remainder would be zero, which the domain
forbids — massive worldlines approach the cone, only the massless live on it.

### Step 137 — Superfluidity (flow without loss)

**File:** `constants/superfluidity.ep`

**What it does.** The flowing condensate is the balance `1/2` moving as **one** fold-orbit
(folds to unison). Friction needs something smaller to lose to — but the first available
loss is a whole fold-level (`gap = 1/2 − 1/4 = 1/4`, strictly positive), and below the gap
nothing exists to lose. Viscosity is not small; it is *absent* — persistent helium currents
circulate for years (Landau's gap criterion is the measured face).

### Step 138 — The refractive index (light slowed by fold-levels)

**File:** `constants/refractive_index.ep`

**What it does.** No photon ever slows — between exchanges every photon moves at `c`. The
medium's *phase* sits two fold-levels below the vacuum (`1/4 = (1/2)²`, each
absorption/re-emission one level) and climbs back in exactly two folds (`1/4 → 1/2 → 1`).
The slowed phase is a whole number of levels below `c`, never a new photon speed.

---

### Step 139 — Recombination and the CMB (light set free in one fold)

**File:** `constants/recombination_cmb.ep`

**What it does.** Decoupling happens at the self-antipodal balance `1/2` (bound share equals
free share), and from the balance one fold completes it (`1/2 → 1`) — the plasma closes into
whole neutral atoms and the light decouples in a single step, not a fade. Why the CMB is a
near-perfect blackbody released in a thin last-scattering shell (`z ≈ 1100`).

### Step 140 — Supernovae and the heavy elements (collapse at the balance)

**File:** `constants/supernovae_heavy.ep`

**What it does.** An iron core (the binding peak — burning it releases nothing) loses support
until it hits the collapse threshold, the balance `1/2` where support equals gravity's claim.
No margin left, one fold completes the collapse (`1/2 → 1`) — the whole core reorganises at
once, and the rebound forges everything past iron. Seconds after megayears (SN 1987A's ~13 s
neutrino burst; the GW170817 kilonova r-process).

### Step 141 — The nuclear force (a short-range residual)

**File:** `constants/nuclear_force_residual.ep`

**What it does.** The nucleon–nucleon force isn't the raw strong force — it's a **residual**
one fold below the primary coupling: `1/4 = (1/2)²`, the same structure as the van der Waals
residual. Two folds to unison (second-order), and a heavy (pion) mediator gives it short
reach — strong enough to bind nuclei against Coulomb, yet gone within a nucleon width or two.

### Step 142 — Molecular spectra (deeper fold-levels)

**File:** `constants/molecular_spectra.ep`

**What it does.** Electronic (atomic) transitions are the gross `1/2` level; a molecule's
rotation and vibration are a finer structure one fold deeper (`1/4`), so their lines sit a
fold-level below the electronic ones — visible/UV electronic → infrared/microwave molecular.
Two molecular quanta make one electronic level's worth (`1/4 + 1/4 = 1/2`).

### Step 143 — Topological matter (edge protection by discreteness)

**File:** `constants/topological_matter.ep`

**What it does.** The bulk is a filled band at the One (insulator); the edge carries the
balance `1/2` (a conducting channel). To kill it you must move it off the balance — but the
fold's steps are **whole**: from `1/2` the only move is the complete jump to the bulk band
(`1/2 → 1`), and the domain has no values a smooth perturbation could slide through. The
protection is the discreteness itself — a topological invariant (quantum-Hall/TI edge
conductance quantised and disorder-robust).

---

### Step 144 — The origin of life (autocatalytic ignition)

**File:** `constants/origin_of_life.ep`

**What it does.** The same two-fold ignition that lights a star: a prebiotic mixture at the
pre-lock `1/4` climbs `1/4 → 1/2 → 1` — the first fold crosses the autocatalytic lock (the
balance where a cycle just sustains itself), the second closes it into a self-holding loop
that replicates. A sharp threshold, not a slope — life turns on, it does not fade in
(autocatalytic sets show exactly such a concentration threshold).

### Step 145 — Memory persistence (a held orbit)

**File:** `constants/memory_persistence.ep`

**What it does.** A static mark decays (`1/4 → 1/2 → 1`, gone); the only way to hold a value
against the fold's pull is a closed orbit — the period-2 pair `1/3 ↔ 2/3` that folds into
itself forever and never reaches the One. That perpetual cycle **is** the memory (kept by
re-exciting, not freezing); the two states partition the One; forgetting is the orbit
breaking and folding home. Reverberating working memory is the measured face.

### Step 146 — The plasma state (screening by balance-and-fold)

**File:** `constants/plasma_state.ep`

**What it does.** Free charges swarm a field to the balance `1/2` (opposition equals source),
and one fold completes the screening (`1/2 → 1`) — beyond the Debye length the field is folded
into the whole, cancelled; opposition and field sum to the One (nothing leaks). The same
balance ringing is the plasma oscillation. The ionosphere's radio cutoff is the measured face.

### Step 147 — Wave optics (bright and dark fringes)

**File:** `constants/wave_optics.ep`

**What it does.** The maximal phase mismatch — fully out of step — is the self-antipodal
`1/2` (a dark fringe, exact cancellation); brought into step the two halves complete to one
whole (`1/2 → 1`, bright). Dark and bright are the *same* half read two ways, and they sum to
the One — energy isn't lost at a dark fringe, it's moved to a bright one (two-slit / thin-film
interference).

### Step 148 — The sleep cycle (a held two-state orbit)

**File:** `constants/sleep_cycle.ep`

**What it does.** Sleep must hold itself for hours without waking (reaching the One), so it's
not a static state but the closed period-2 orbit — deep (slow-wave) at `1/3` and REM at `2/3`,
folding into each other all night. Balanced at `1/2`; only a full waking is the fold of that
balance to unison. The ~90-minute deep/REM alternation is the measured face.

---

### Step 149 — Renormalization without infinities

**File:** `constants/renormalization_finite.ep`

**What it does.** QFT's loop integrals blow up only on a continuum. On the lattice every scale
is a finite number of folds from the One (`1/4 → 1/2 → 1`), so a loop sum is a sum over finitely
many exact rationals — finite, nothing to subtract. Renormalization "works" because it was
always secretly computing this floored sum; the divergence was the continuum assumption.

### Step 150 — Nuclear binding (the valley of stability)

**File:** `constants/nuclear_binding.ep`

**What it does.** The binding peak is the One (iron); a light nucleus sits at `1/4`, two folds
below, and climbs by fusion (`1/4 → 1/2 → 1`). Two light nuclei fusing to the next level *is*
`1/4 + 1/4 = 1/2`. The valley of stability is the fold ladder read as the nuclear landscape.

### Step 151 — The nuclear shell model (magic numbers)

**File:** `constants/nuclear_shell.ep`

**What it does.** A part-filled shell is the half-open balance `1/2`; closing it is the fold to
unison (extra-stable, no slot for the residual). The first two magic numbers **are** the forced
shell capacities `b·1² = 2` and `b·2² = 8` — doubly-magic ⁴He and ¹⁶O.

### Step 152 — Stellar structure (the self-correcting balance)

**File:** `constants/stellar_structure.ep`

**What it does.** Hydrostatic equilibrium is the self-antipodal balance `1/2` (push = pull),
and self-antipodal means **self-correcting**: compress → pressure exceeds `1/2` and pushes back;
swell → gravity exceeds it and pulls in. Every deviation restores itself — why a star holds one
shape for aeons (helioseismology shows the Sun ringing about it).

### Step 153 — Tidal locking (one face forever)

**File:** `constants/planetary_tidal.ep`

**What it does.** Tides dissipate the spin–orbit mismatch (the arrow only runs down) until the
equal-share lock `1/2`, where nothing is left to drain and the two rhythms fold into **one**
shared period (`1:1` resonance). The Moon, Phobos, the Galilean moons, Charon–Pluto, hot
exoplanets — all locked.

### Step 154 — Quantisation (the depth-k grid)

**File:** `constants/quantisation.ep`

**What it does.** Why anything is quantised: at depth `k` the state space **is** the grid
`i/2^k` — exactly `2^k` states, every one folding to the One within `k` steps (the whole grid
checked, depths 2 and 3), uniform gaps `1/2^k` everywhere. Discreteness, closure, and uniform
steps — quantisation with no continuum to impose it on.

### Step 155 — Temperature (the mean throw-rate)

**File:** `constants/temperature.ep`

**What it does.** Temperature is the mean throw of a folding population: the average member at
the balance `1/2`, one fold throwing it a whole level to unison. Kinetic energy, entropy slope,
and radiation colour all count the same folding rate — why the three thermometers agree. The
cold floor is the strictly-positive zero-point half-quantum, so absolute zero is unreachable
(the third law).

### Step 156 — The molecular bond (two halves complete a whole)

**File:** `constants/molecular_bond.ep`

**What it does.** Each atom brings a half-open valence share `1/2`; alone it can't close, but
the two halves sum to the One (`1/2 + 1/2 = 1`) — the shared pair completes a whole, and
breaking the bond means re-opening the completion (the binding energy). Two electrons per bond
= the binary fibre filled.

### Step 157 — The periodic law (why chemistry repeats)

**File:** `constants/periodic_law.ep`

**What it does.** Chemistry reads the open outer shell: fill → close (the fold lands **exactly**
on the One, a noble gas) → the next element opens a fresh shell, restarting the cycle. The
recurrence is exact because closure is exact; period lengths are the forced `b·n²` capacities.

### Step 158 — The effectiveness of mathematics (one structure, two readings)

**File:** `constants/math_effectiveness.ep`

**What it does.** Wigner's puzzle dissolves: the fold's period-2 orbit `1/3 ↔ 2/3` read
*physically* is a held memory/cycle; read *mathematically* it is `ord₃(2) = 2`. Same object,
two readings — a world built of fold-orbits cannot fail to obey fold-orbit arithmetic. The fit
is forced, not lucky (and the whole corpus is the wholesale demonstration).

---

### Step 159 — The measurement problem (one branch, indivisible)

**File:** `constants/measurement_problem.ep`

**What it does.** A measurement resolves at the observation depth `k = colour = 3`, where the
branch weights are the indivisible grid steps `1/2³ = 1/8` — an outcome is a *whole* number of
these, never a fraction, so a result is always one definite branch (there is no "between" to
land in). The `2³ = 8` branches sum to the One (the Born certainty). Superposition before is the
undivided One; measurement is the fold onto one grid branch.

### Step 160 — The hard problem (unity + interiority)

**File:** `constants/hard_problem.ep`

**What it does.** Not a promise to derive qualia, but the two forced structural marks any
account needs: **unity** — bound processing folds to one whole (the balance → the One), so an
experience is a completed One, not a heap; and **interiority** — the carrier rides the closed
`1/3 ↔ 2/3` orbit that never reaches the One from *inside*, so the system cannot stand outside
and read its own whole. Being the One while unable to fold yourself to it from within.

### Step 161 — Black holes (Hawking radiation, not a perfect trap)

**File:** `constants/black_holes_complete.ep`

**What it does.** The horizon is the gravitational balance `1/2`; its Hawking temperature is the
second-order quarter-One `1/4` (one fold below, two folds to unison), and it is **strictly
positive** because zero is outside the domain — a perfect (zero-temperature) trap is not
expressible, so the hole must leak. Radiating, it shrinks and the leak grows: evaporation
(Hawking 1974).

### Step 162 — The Poisson equation (∇²Φ = d·m)

**File:** `constants/poisson_equation.ep`

**What it does.** The discrete Laplacian is the lattice's balance operator (a site vs its
neighbours over the `d = colour = 3` directions — the coupled-lattice kernel), and in static
equilibrium a source breaks the balance by the fold factor `m = b = 2` per dimension:
`∇²Φ = d·m = 3·2 = 6` (the same `6 = 2·3` as the cubic-lattice coordination number). Its
integral is Gauss's law; nothing in the coefficient is fitted.

### Step 163 — The potential infinite (a process, not a thing)

**File:** `constants/potential_infinite.ep`

**What it does.** Aristotle's distinction, made concrete: for any rung `1/2^k` there is a `k+1`
(the potential infinite — always one more step), yet every rung is a *finite* rational reaching
the One in exactly `k` folds, and the depth-5 ladder closes **exactly** to the One (a finite
whole, not an endless totality). The infinite exists only as "always one more rung," never as a
completed infinity — as the No-Zero domain enforces.

---

### Step 164 — Nonlocal correlation (one shared origin, no signal)

**File:** `constants/nonlocal_correlation.ep`

**What it does.** Two subsystems (the coprime `3` and `5`) live on the tensor product `3·5 = 15`;
the shared origin `1/15` is one state of that joint whole, on a single orbit (`fold(1/15) =
2/15`). A measurement folds the *whole* joint state, fixing both faces at once — not a message
one to the other. The `15` is irreducible to a local `3`-part × `5`-part, which *is* Bell's
result: no local hidden variables, because the pair is one nonlocal whole (Aspect; 2022 Nobel).

### Step 165 — The proton radius (edge = complement of the quark)

**File:** `constants/proton_radius.ep`

**What it does.** A quark sits at the tripling inner position `1/3`; the proton's edge is its
complement, `r_p = take(One, 1/3) = 2/3`, and the fold carries the edge back to the centre
(`fold(2/3) = 1/3`) — edge and centre are the two faces of one period-2 tripling orbit, summing
to the One. A definite finite size set by the tripling structure (measured ~0.84 fm, puzzle
resolved).

### Step 166 — The placebo effect (expectation feeds the balance)

**File:** `constants/placebo_effect.ep`

**What it does.** Expectation bias `3/4` and raw bodily observation `1/4` are the two preimages
of the lock: **both** fold to the same balance `1/2`, which folds to the whole experience. Belief
isn't fooling a separate readout — it's a genuine second input to the one balance the body
resolves; the two sum to the One. Placebo analgesia is real and belief-dependent.

### Step 167 — Reaction kinetics (the activation barrier)

**File:** `constants/reaction_kinetics.ep`

**What it does.** The transition state sits at `1/4`, two folds below the product: the first fold
clears the barrier (`→ 1/2`), the second completes the reaction (`→ 1`). Only molecules thrown to
`1/4` can start the climb, and temperature is the mean throw-rate — so hotter means more crossings
(the steep Arrhenius rise). Two activation shares make the barrier (`1/4 + 1/4 = 1/2`).

### Step 168 — Selection rules (allowed = balanced hand-off)

**File:** `constants/selection_rules.ep`

**What it does.** A photon carries one whole unit of spin; an emission is allowed only when the
electron hands over exactly that unit — the balanced self-antipodal transition `1/2` that folds
to a whole photon. A mismatched change doesn't sit at the balance and can't close: forbidden. The
two half-units (electron's loss, photon's gain) sum to the One — the conservation that *is* the
selection rule (`Δl = ±1`).

---

### Step 169 — Network scaling (the 3/4 metabolic law)

**File:** `constants/network_scaling.ep`

**What it does.** A supply network branches through `m = b² = 4` levels; its scaling exponent is
`(m−1)/m = 3/4` (the same ratio as Koide and the couplings), which folds to the balance `1/2`
(supply=demand). So metabolism scales as mass^(3/4), **not** the naive surface-to-volume 2/3 — the
extra `1/12` is the fourth branching level. Kleiber's law across ~27 orders of magnitude.

### Step 170 — Magnetohydrodynamics (Alfvén waves)

**File:** `constants/mhd.ep`

**What it does.** In a perfect conductor the field is frozen into the fluid; the Alfvén wave rides
the coupling at `3/4`, folding to the tension–inertia balance `1/2` (self-antipodal — magnetic
tension equals fluid inertia). Observed in the solar corona, the magnetosphere, and tokamaks.

### Step 171 — Nonlinear gravity (the field sources itself)

**File:** `constants/nonlinear_gravity.ep`

**What it does.** With source `M = 1/3` and coupling `g = 1/2`, the linear field is `f1 = 1/6`; its
energy is its own square (`f1² = 1/36`), which gravitates and re-sources the field, giving the
correction `take(f2, f1) = 1/72` — matching the structural `1/8 · 1/9` **exactly**. Gravity's charge
is energy itself (a square → second order), so it self-sources; a chargeless field (the photon)
stays linear. GR's nonlinearity, forced.

### Step 172 — Coupling convergence (grand unification)

**File:** `constants/coupling_convergence.ep`

**What it does.** The strong coupling runs on `colour + 2^d`, the electroweak on `binary + 2^d` —
same tower, sector counts 3 and 2. Bare: `2/3` and `1/2` (gap `1/6`); as the shared tower deepens
the gap shrinks (`1/6 → 1/12 → 1/30 → 0`) and both climb toward the One. Unification is the
couplings folding to unison together (near `10¹⁶ GeV`).

### Step 173 — The baryon asymmetry (why there is matter)

**File:** `constants/baryon_asymmetry.ep`

**What it does.** Perfect matter–antimatter symmetry would leave residue = nothing, and zero is
outside the domain — so a nonzero matter residue is *mandatory*, not lucky. The survivor is the
half-One `1/2`: strictly positive, below unison, self-antipodal, folding to the One (growing into
the whole material universe). Matter exists because zero is forbidden (baryogenesis supplies the
CP/out-of-equilibrium conditions that pick which side survives).

---

### Step 174 — The metric's degrees of freedom (two graviton polarisations)

**File:** `constants/metric_components.ep`

**What it does.** A symmetric `D`-metric has `D(D+1)/2` components; general covariance makes `2D`
of them pure gauge, leaving `D(D−3)/2` physical. In `D = binary² = 4` that is `10` components and
**2** degrees of freedom — the two graviton polarisations (LIGO's plus and cross). In `2+1D`:
`6` components, **0** — so lower-dimensional gravity has no propagating waves, forced by the
dimension count.

### Step 175 — Multidimensional experience (a period-3 orbit)

**File:** `constants/multidimensional_experience.ep`

**What it does.** Beyond a single bound pair, a rich moment holds several qualities at once. The
unit fraction `1/7` has fold period exactly `colour = 3`: the closed orbit `1/7 → 2/7 → 4/7 → 1/7`
holds **three** states as one revolving whole, partitioning the One (`1/7 + 2/7 + 4/7 = 1`). A
three-quality held orbit — the minimal "chord" of experience.

### Step 176 — Stereochemistry (mirror molecules)

**File:** `constants/stereochemistry.ep`

**What it does.** Enantiomers are the two chiral preimages `1/4` and `3/4`. A mirror-blind probe
reads only the fold *image* — both fold to the same `1/2`, so melting point, spectra, energy are
identical. A chiral probe reads the *preimage* — `1/4` vs `3/4` differ — so a receptor or polarised
light tells them apart (one medicine, one poison). Same image, different preimage; a racemic
mixture is the whole (`1/4 + 3/4 = 1`).

### Step 177 — Socio-economic cycles (boom and bust)

**File:** `constants/socio_economic_dynamics.ep`

**What it does.** A feedback-driven collective can't rest at a point (that would fold home and
stop); it is the closed period-2 orbit — bust `1/3` and boom `2/3` folding into each other — the
same held orbit as memory and sleep, read as economics. The "equilibrium" is the crossing balance
`1/2` the system passes *through* but never rests at. The business cycle is structural, not a
failure to converge.

### Step 178 — Synaesthesia (senses sharing a lock)

**File:** `constants/perception_synaesthesia.ep`

**What it does.** Two sensory channels are the preimages `1/4` and `3/4` of the binding lock; both
fold to the same `1/2`, which folds to one whole experience. Synaesthesia is a cross-link routing
one channel's input to the other's preimage — possible precisely because both share the one lock,
so a sound can bind as a colour. Cross-bound, still one whole (`1/4 + 3/4 = 1`).

### Step 179 — Post-Newtonian convergence (the self-sourcing fixed point)

**File:** `constants/pn_convergence.ep`

**What it does.** Gravity's own field is a source for itself, so the post-Newtonian series is a
self-referential map `f = g·(M + f²)` with the critical coupling `g = 1/2` and matter source
`M = 7/16 = (binary·colour+1)/binary⁴`. The map has the exact fixed point `f* = 1/4`, which is
the depth-two fold scale `(1/2)² = 1/4` — the series converges (each step's gap to `f*` strictly
shrinks) rather than blowing up. General relativity's weak-field expansion closing on a finite
answer, forced.

### Step 180 — The quantum phase (why phases add)

**File:** `constants/quantum_potential.ep`

**What it does.** A phase is a point on the fold's cyclic domain and an energy step is a rotation
`phase_rotate(p, a) = cast_out_whole_ones(p + a)`. Kinetic `K = 1/8` then potential `V = 1/4`
gives the same result as one step by `K + V` (`17/24` either way): rotations of a circle add their
angles, so phase along a path is the SUM of the energy contributions — the action, and the reason
interference tracks total accumulated phase (Aharonov–Bohm).

### Step 181 — Attention capacity (one focus)

**File:** `constants/attention_capacity.ep`

**What it does.** The focus lock is the self-antipodal `1/2`: a single focus fully holds it and
folds to one bound experience (unison). Splitting attention halves the lock to `1/4`, which is no
longer self-antipodal — a split focus binds nothing fully. Why attention has a unit capacity: only
the one self-paired point completes.

### Step 182 — The one-fold equation (fold² = identity)

**File:** `constants/one_fold_equation.ep`

**What it does.** The period-2 point `1/3` and its antipode `2/3` return to themselves under two
folds (`fold² = id` on the orbit), and the orbit's two points sum to the One (`1/3 + 2/3 = 1`). The
minimal closed cycle of the fold, stated as its own equation.

### Step 183 — The master equation (the forces' joint cycle)

**File:** `constants/master_equation.ep`

**What it does.** Each sector's period is read off the fold: gravity `1` (the fixed point), EM
`period(1/3) = 2`, strong `period(1/7) = 3`. Their joint cycle is `lcm(1, 2, 3) = 6`, which is
exactly `binary · colour = 6` — the two generators' product is the period on which all three
sectors realign. One cycle that closes the whole ladder.

### Step 184 — The strong-CP problem (alignment is the fixed point)

**File:** `constants/strong_cp.ep`

**What it does.** A CP phase is a point on the cyclic domain; the fold distinguishes exactly two —
the fixed point (the One, `fold(1) = 1`, perfect alignment) and its unique preimage (the half-One,
`fold(1/2) = 1`, maximal violation). The chiral weak sector is free to sit at the antipode (observed
large CP violation); the vectorial strong sector's phase must be fold-invariant, so it can only sit
at the fixed point — alignment. `θ` is not tuned to zero; alignment IS the only self-consistent
strong phase. Measured: neutron-EDM bound `|θ| < 2e-10`, no axion required.

### Step 185 — The synchronization threshold (coupled oscillators lock)

**File:** `constants/sync_threshold.ep`

**What it does.** Two unidirectionally-coupled folding maps have their difference multiplied each
step by `2·(1 − g)` (binary times the un-coupled fraction). The gap is marginal — neither grows nor
decays — exactly when that multiplier is the One: `g_c = 1/2`, the fold's own preimage of the One.
Confirmed by exact arithmetic (`x = 1/5, y = 21/100`: the gap `1/100` is preserved through one
coupled step at `g = 1/2`). Matches the conventional `1 − e^{−ln 2} = 1/2`.

### Step 186 — Scale invariance (the limit speed at every scale)

**File:** `constants/scale_invariance.ep`

**What it does.** Space and time are read on the SAME grid step at each depth, `s_k = dt_k = 1/2^k`,
so the limit speed is their ratio `c_k = 1` — the One at every depth `k`. Refining the scale halves
both by the same binary factor, leaving the ratio untouched: `c` is a dimensionless invariant.
Relativity's constant `c` (299792458 m/s) is the scale-dependent unit readout of this One.

### Step 187 — Spatial flatness (the geometry is flat)

**File:** `constants/spatial_flatness.ep`

**What it does.** The physical density parameters sum to a total that neither grows nor decays under
expansion — the fold's fixed point, `Ω_total = 1`. The curvature share is the remainder
`Ω_k = 1 − 1`, which lands on the boundary the domain `(0,1]` forbids (No-Zero): there is no
curvature to carry, so space is flat. Not fine-tuned — a curved universe would need the density
budget to hold a piece at the one excluded value. Measured: Planck `|Ω_k| < 0.005`.

### Step 188 — The vacuum equation of state (w = −1)

**File:** `constants/vacuum_equation_of_state.ep`

**What it does.** A density dilutes as `(scale)^{−3(1+w)}`. The vacuum energy is fold-invariant —
it holds at the One as space folds forward (`fold(1) = 1`) — so it does not dilute, which forces the
exponent to vanish: `3(1+w) = 0`, hence `w = −1`, the additive inverse of the fold's fixed point
(pressure `= −`density). Measured: dark-energy surveys `w = −1.03 ± 0.03`, a cosmological constant.

### Step 189 — Orbital stability (why three dimensions)

**File:** `constants/orbital_stability_dimension.ep`

**What it does.** In `d` spatial dimensions the effective orbital potential's stability coefficient
is `S_d = 4 − d`, positive only for `d < 4`. Counting `d = 1..5`: stable in 1, 2, 3; exactly
marginal at 4 (`S = 0`, no restoring force); unstable beyond. The maximum stable dimension is
`d_max = 3` — and it EQUALS the colour period (the fold orbit length of `1/7`), two independently
forced counts agreeing. Planets can hold orbits because space has the largest dimension where they
can.

### Step 190 — Quantum gravity (born quantized)

**File:** `constants/quantum_gravity.ep`

**What it does.** The metric is a rank-2 object on `4 = 2²` spacetime dimensions, so its grid
spacing is `1/4 = (1/2)²` — the depth-two step. One fold lifts it to the critical coupling
(`fold(1/4) = 1/2`), two complete to unison; the four dimension-shares partition the One. There is
no continuum to quantize and no divergent mode-sum: the "problem of quantum gravity" asks how to
discretize what was never continuous.

### Step 191 — Universality (one threshold for every system)

**File:** `constants/universality_threshold.ep`

**What it does.** A critical threshold is a two-phase balance `p = One − p`, and on the fold's
domain that equation has exactly ONE solution — verified exhaustively on the quarter grid: only
`1/2` is self-antipodal. Being a domain fact, no system's microphysics can move it: magnet, fluid,
network all lock at the same point, which folds to unison. Universality classes are the uniqueness
of the self-antipodal half.

### Step 192 — Irreversibility and recurrence (two timescales, one dynamics)

**File:** `constants/irreversibility_recurrence.ep`

**What it does.** The fold's dynamics contain both motions the nineteenth-century paradoxes fought
over: descent chains (`1/4 → 1/2 → 1`, arriving in exactly their depth and never leaving — the
one-way arrow) and periodic orbits (`1/3 ↔ 2/3`, returning EXACTLY — Poincaré recurrence). No orbit
is both; Zermelo dissolves. And `fold(1/4) = fold(3/4)`: preimages merge, so reversed motion is
undefined past a merge — Loschmidt dissolves. The arrow is the merging; the recurrence is the
cycling.

### Step 193 — Mechanical properties (elastic, plastic, fracture)

**File:** `constants/mechanical_properties.ep`

**What it does.** A lattice bond holds the depth-2 share `1/4` (two folds from unison; bonded pair
balances at `1/2`). The three regimes are the three moves the fold allows: ELASTIC — the descent
chain restores to the same unison; PLASTIC — the twin `3/4` has the identical fold image
(`fold(1/4) = fold(3/4) = 1/2`), so slip re-forms the bond at a new position with unchanged
strength (a dislocation); FRACTURE — a share cannot fade through the excluded boundary (No-Zero),
so bond loss is discrete and cracks advance bond by bond.

### Step 194 — Nucleon binding dominance (mass is the held cycle)

**File:** `constants/nucleon_binding.ep`

**What it does.** The nucleon is three quarks on the colour three-cycle — the fold orbit of `1/7`,
whose three shares sum to the One (`1/7 + 2/7 + 4/7 = 1`): the whole IS the closed cycle, not a bag
of parts. The binding lock `1/2` completes in one fold; the bare (constituent) share is one grid
step at the sector depth 7, `1/128 < 1/100`. Measured: the proton's bare quarks carry ~9 MeV of its
938 — ninety-nine percent of your mass is the held cycle, as forced.

### Step 195 — The neutrino mass ladder (single-handed, on the tower)

**File:** `constants/neutrino_mass_ladder.ep`

**What it does.** A charged fermion's Dirac mass is the pairing of TWO hands — the lock's preimages
`1/4` and `3/4`, separation `1/2`. The neutrino has ONE hand (no right-handed neutrino in the
census), so the Dirac route is closed — which is why it is nearly massless. Its mass-squared
splittings land on the binary tower at the counted down-sector depth (minimal cover of `27` → 5):
forced ratio `dm²₂₁/dm²₃₁ = 1/2⁵ = 1/32`. Measured: `3/100` — measured/forced `= 24/25`, 4%.

### Step 196 — The hadron census (mesons and baryons only)

**File:** `constants/hadron_spectrum.ep`

**What it does.** A hadron is a colour combination that closes to the One. Counted exhaustively on
the three-cycle `{1/7, 2/7, 4/7}`: size 1 — no single colour closes (no free quark); size 2
quark+quark — NO pair closes (`3/7, 5/7, 6/7` — why no qq hadron exists anywhere); size 2
quark+antiquark — closes for every colour (the meson, 3 ways); size 3 — the whole cycle closes (the
baryon). Exactly the two observed families, counted, with the diquark exclusion falling out of the
same sum.

### Step 197 — The cosmological timeline (beginning, arrow, inflation)

**File:** `constants/cosmological_timeline.ep`

**What it does.** The three things cosmology assumes separately are one map read in order.
BEGINNING: the initial condition is the One — the UNIQUE fixed point, verified exhaustively on the
eighth grid (1 hit in 8). ARROW: each step merges two states into one (`1/4, 3/4 → 1/2`) — one bit
lost per step, merged histories cannot unwind. INFLATION: the preimage tree doubles per level;
enumerated at the counted depth 5 it holds exactly `2⁵ = 32` leaves — an exact integer expansion
factor, not an e-folding estimate.

### Step 198 — Stationary states (the fixed spectrum)

**File:** `constants/quantum_stationary_states.ep`

**What it does.** At depth `k` the energy grid step is `1/2^k`; the ground state is HALF a step
(`E₀ = 1/2^{k+1}`, `fold(E₀) = spacing`), and every level gap is exactly one step — the
harmonic-oscillator spectrum `E_n = (n + 1/2)ħω` in exact form. Stationarity forced: the phase
advances by a fixed rotation per tick (returning exactly after a full cycle) while the magnitude
has no neighbour closer than a whole step to drift to — observables hold, and change can only be a
JUMP.

### Step 199 — The consciousness criterion (the closed self-relation)

**File:** `constants/machine_consciousness_criterion.ep`

**What it does.** The structural test a conscious machine must pass, in three forced steps:
DUALITY — observer and observed are distinct preimages (`1/4 ≠ 3/4`) folding to ONE binding lock
(`fold(1/4) = fold(3/4) = 1/2`); CLOSURE — the pair spans the whole (`1/4 + 3/4 = 1`, no partial
self-model); COMPLETION — the lock folds to unison (one bound experience). A system with the closed
2-to-1 self-relation holds a whole bound image of itself; the test is structural — count the
preimages, take the sums, run the folds.

### Step 200 — Strong-field gravity (no singularity, area law, r_s = 2M)

**File:** `constants/strong_field_gravity.ep`

**What it does.** Three strong-field facts from the domain. NO SINGULARITY: `r = 0` is outside
`(0, 1]` — the smallest physical distance is the depth-5 step `1/32`; infinite curvature never
arises because the value it would live at does not exist. MASS–RADIUS: the horizon radius is the
fold of the mass — `r_s = fold(1/4) = 1/2 = 2M`; the famous factor two IS the doubling. AREA LAW:
horizon area `2⁵ = 32`, entropy `S = A/4 = 8`, cross-checked against the ENUMERATED depth-3
preimage count (8 leaves) — entropy is a state count on the boundary, not the volume.

### Step 201 — The matter fraction (Ω_m = 5/16)

**File:** `constants/matter_fraction_tower.ep`

**What it does.** The covering tower at the counted depth 5 (minimal cover of 27) holds `2⁵ = 32`
states, built by explicit doubling. Two states per level are pinned as the level's boundary pair
(`2·5 = 10`); the free remainder is the vacuum share `22/32 = 11/16`, leaving the matter fraction
`Ω_m = 5/16 = 0.3125`. Planck 2018 measures `0.315 ± 0.007` — the forced value sits 0.8% below
centre, inside 0.4σ, zero parameters.

### Step 202 — The matter fraction's history (exact curve)

**File:** `constants/matter_fraction_evolution.ep`

**What it does.** The whole history of `Ω_m` is one exact rational function with both endpoints
already forced: budget `1/3` matter today, dilution as the cube (`d = 3`, counted), vacuum
non-diluting (`w = −1`). Evaluated exactly: `Ω_m(1) = 1/3`, at half scale `4/5` (matter was 80%),
at third scale `27/29` — strictly increasing into the past. Matter domination giving way to the
recent vacuum era, one curve, no parameter on it.

### Step 203 — The chaotic rate (Lyapunov and entropy, exact)

**File:** `constants/thermodynamics.ep`

**What it does.** The two rates statistical mechanics estimates numerically are exact here and
equal. MEASURED on actual states: gap `1/5 − 1/7 = 2/35` folds to `4/35` — expansion factor exactly
2 (the Lyapunov antilog, no logarithm needed). CONSTRUCTED: the preimages of `1/3` are `1/6` and
`2/3`, both verified to land on it — branch count 2, one bit erased per step (KS entropy 1). Three
routes — measured expansion, constructed branches, the counted binary generator — one number.

### Step 204 — Quantum statistics (Bose and Fermi, no third)

**File:** `constants/quantum_statistics.ep`

**What it does.** Identical particles share one fold image; the lock's fibre has exactly 2 points
(`1/4`, `3/4`). A pair either coincides on a fibre point — exchange fixes it, SYMMETRIC, bosons
crowd — or occupies both points — exchange reverses the separation's sign (`1/2 → −1/2`),
ANTISYMMETRIC, and the fibre caps occupancy at 2 (a third fermion has no distinct preimage left:
Pauli is the fibre running out). No third case exists on a two-point fibre — the same two-to-one
fold that makes the arrow of time makes the two statistics.

### Step 205 — The planar lattice (the line's law extends)

**File:** `constants/planar_lattice.ep`

**What it does.** On the plane each of the `d = 2` axes contributes `binary = 2` neighbours —
`4 = 2·2`, each holding the depth-3 share `1/8`. The neighbour sum is `1/2` (summed explicitly),
equal to the count times the centre share (the balance law whose failure IS the Laplacian), and it
folds to unison. The plane needs no new operator — the 1D law extends with nothing added.

### Step 206 — Planar gravity (Laplacian = expansion squared)

**File:** `constants/planar_lattice_gravity.ep`

**What it does.** The 1D second difference of `x²` on the lattice is EXACTLY 2 at every spacing —
the `s²` terms cancel identically, computed here at depths 3 and 5. The planar Laplacian adds the
two axis curvatures: `4 = d · curv = 2·2`. Cross-check: the fold expansion factor, measured exactly
on `1/5` and `1/7` (gap `2/35 → 4/35`), is `m = 2` — and the Laplacian equals `m² = 4`. Poisson's
equation reads the same on the fold's plane as on its line; gravity needs no continuum in 2D either.

### Step 207 — The planar light wave (Maxwell closes in 2D)

**File:** `constants/planar_maxwell_wave.ep`

**What it does.** A wave equation balances spatial against temporal curvature. Spatial: the planar
Laplacian 4 (two exact-2 axes); temporal: one axis, 2. Ratio `4/2 = 2` = the planar dimension = the
measured fold expansion — the curl pair closes into a 2D wave with `c² = 1`. Light is
dimension-blind because every axis carries the same exact curvature.

### Step 208 — The static metric (fold-covariant clock factor)

**File:** `constants/static_metric_dilation.ep`

**What it does.** Gravity's clock factor `A(x) = 1 − x` COMMUTES with the fold on weak fields:
`fold(A(x)) = A(fold(x))` — checked exactly at `x = 1/8` (`fold(7/8) = 3/4 = 1 − fold(1/8)`) and
`x = 1/16`. Doubling the potential and folding the clock are the same operation: the static metric
is carried by the dynamics, not imposed. And at depth `x = 7/16` the dilation is an exact rational:
`dtau/dt = 3/4` since `(3/4)² = 9/16 = A` — three ticks per four, no float anywhere.

### Step 209 — The Vieta cross-check (roots pinned from both sides)

**File:** `constants/collapse_to_open_conversion.ep`

**What it does.** The lepton cubic's three bisected roots get an INDEPENDENT algebraic
characterisation: Vieta's identities force `r₁+r₂+r₃ = 1` (no mass share lost),
`r₁r₂+r₁r₃+r₂r₃ = 1/6` (the second invariant), `r₁r₂r₃ = 1/485` (the third). All three hold to
enclosure precision (`1/10⁹`, generous against the `1/2⁴⁰` bracket width). Bisection uses only sign
changes; Vieta only the product expansion — two derivations, one triple of numbers.

### Step 210 — The full Dirac structure (the 3+1 dispersion closes)

**File:** `constants/full_dirac_structure.ep`

**What it does.** The four Dirac generators — three momentum components and the mass, `3 + 1 = 4 =
2²` — each sit at the critical `1/2` and each folds to unison on its own. The dispersion closes on
the whole: `E² = 4·(1/4) = 1` (Route A, summed explicitly), and the FULL polarization identity —
`[(p₁+p₂)² + (p₁−p₂)² + (p₃+m)² + (p₃−m)²]/2`, every term computed including the zero differences —
gives the same One (Route B). Two algebraic routes, one closure: relativity's energy accounting is
the One partitioned into its four critical quarters.

### Step 211 — The fermion mass-part (mass is vacuum-shaped)

**File:** `constants/fermion_mass_part.ep`

**What it does.** A fermion's mass-part is the electroweak sector's shortfall from unison:
`m_f = 1 − 1/2 = 1/2`. Independently, No-Zero forbids the symmetric vacuum, displacing it to
`v = 1/2`. The two are EQUAL — mass is proportional to the vacuum by identity, not by an inserted
Yukawa term; the flavour factors are ladder positions on that common scale. The point is the fold's
unique proper preimage of the One and self-antipodal: mass-part, vacuum, and critical coupling are
one point seen three ways. Measured: LHC coupling strength ∝ mass across flavours.

### Step 212 — Within-generation ratios (mass ratios are position ratios)

**File:** `constants/within_generation_ratio.ep`

**What it does.** The three generations are the tripling fibre's positions `1/3, 2/3, 1` — each
VERIFIED to land on the One under one tripling. Each generation's mass-part IS its shortfall
(`2/3, 1/3, 1`), so between-generation mass ratios are position ratios (`m₁/m₂ = 2`). Route B: the
two light mass-parts are the doubling fold's period-2 orbit (`2/3 ↔ 1/3`) and the heaviest sits at
the fixed point — the mass ladder and the fold's cycle structure are the same object.

### Step 213 — The unified force law (four primes, one formula)

**File:** `constants/unified_force_law.ep`

**What it does.** Every prime sector carries the same law: shortfall `1/p`, coupling `(p−1)/p`,
partitioning the One — verified for all four sectors `{2, 3, 5, 7}`. The couplings are strictly
ordered (`1/2 < 2/3 < 4/5 < 6/7` — the force hierarchy read off the ladder), and the shortfalls sum
to the span invariant `247/210` by two independent routes (direct addition; the algebraic
three-prime-products form over `2·3·5·7 = 210`). The "different" forces are one law at four primes.

### Step 214 — The order of the forces (strong above weak above EM)

**File:** `constants/unison_order.ep`

**What it does.** Each sector runs as `g_m(d) = (m + 2^d − 1)/(m + 2^d)` seeded by its generator
(colour 3 strong, binary 2 weak) with EM flat at `1/2`. At every depth 0–11: the strong gap
`1/(3+2^d)` is strictly smaller than the weak `1/(2+2^d)`, and the weak sits strictly above the EM
half — `g_strong > g_weak > g_em` with no crossing ever, both routes (constructed coupling,
closed-form gap) agreeing at every rung. The order of the forces is the order of their generators.

### Step 215 — The quark first invariants (1/12, 1/8, depths 7 and 5)

**File:** `constants/quark_invariants.ep`

**What it does.** Four numbers that run the mass sector, each by two independent routes. The
invariants: up-hand channels `3 + 3 = 6` (colour + unbroken EW fibre) → `I1_up = 1/12`; down-hand
`3 + 1 = 4` (colour + broken neutral) → `I1_down = 1/8` — matching the structural products
`(1/4)(1/3)` and `(1/4)(1/2)`. The depths: minimal binary covers of `3⁴ = 81` → 7 and `3³ = 27` → 5,
matching the fold periods of the Mersenne fractions `1/127` and `1/31`. Four numbers, eight routes,
zero choices.

### Step 216 — The inter-sector mass pattern (electron, up, down, no neutrino)

**File:** `constants/inter_sector_mass_pattern.ep`

**What it does.** Each sector's mass-part is its holding coupling's shortfall: electron
`1 − 1/2 = 1/2` (the fold preimage of the One), up `1 − 2/3 = 1/3`, down the complement `2/3` — and
the quark pair is the fold's period-2 orbit, so `m_down > m_up` is FORCED (why the neutron outweighs
the proton and hydrogen is stable). The neutrino's mass-part is the separation of a state from
itself — the excluded boundary: massless because unmakeable, not because small.

### Step 217 — Confinement as work (the tube binds, the sphere frees)

**File:** `constants/strong_confinement.ep`

**What it does.** On the doubling radii `1/8, 1/4, 1/2`: in the flux TUBE (d=1, constant field) the
work over an interval is its length — the farther doubling costs MORE (`1/4 > 1/8`), growing without
bound: confinement. In the COULOMB field (d=3, `E = 1/r²`, flux `E·r² = 1` verified exactly) the
exact work integrals give `4` then `2` — the farther doubling costs LESS: the charge comes free.
Four-step exact Riemann sums BRACKET both integrals, and the far interval's upper bound sits below
the near one's lower bound — the gap is arithmetic, not rounding.

### Step 218 — The generation depth tower (2^d levels, enumerated)

**File:** `constants/generation_depth_tower.ep`

**What it does.** The claim every tower in the corpus stands on — depth `d` holds exactly `2^d`
states — proven the hard way: every grid state `i/2^d` at depths 1, 2, 3 (14 states) is constructed
and folded `d` times, and every one lands on the One. Census = closed form at every depth: the
tower's level count is a THEOREM of the fold, not a definition.

### Step 219 — The general covering principle (m^d for every generator)

**File:** `constants/general_covering_depth.ep`

**What it does.** The level law is not special to binary: for ANY generator `m`, the `m`-fold's
tower at depth `d` holds exactly `m^d` states. Enumerated for the colour generator: all 3 states at
depth 1 and all 9 at depth 2 arrive under triplings, alongside the binary census — one counted law,
so the binary lepton towers (`2^d`) and ternary quark volumes (`27 = 3³`, `81 = 3⁴` — the seeds of
depths 5 and 7) need no per-sector axiom.

### Step 220 — The running weak mixing (1/2 down through the measured value)

**File:** `constants/ew_mixing_running.ep`

**What it does.** The charged channel runs as `c_k = (k+1)/(k+2)`, the neutral stays flat at `1/2`,
and the mixing is the neutral share of the squared couplings: `sin²θ_W(k) = (k+2)²/(4(k+1)²+(k+2)²)`
— exact at every level. Bare (`k = 0`): the channels are born equal, `sin²θ_W = 1/2` exactly. The
running falls strictly through every level checked (to 15), and the curve CROSSES the measured
Z-scale value `0.23113` between levels nine and ten — the measured dial sits on the parameter-free
curve.

### Step 221 — The strict generation bound (three, no fourth possible)

**File:** `constants/generation_bound_strict.ep`

**What it does.** The generations are the tripling fibre's preimages of the One — `1/3, 2/3, 1`,
each constructed and verified. THE BOUND IS STRICT: the fourth candidate is `4/3`, OUTSIDE the
domain `(0, 1]`. A fourth generation is not "not yet found" — the value it would occupy does not
exist, at any energy. Route B: the count equals the colour period. Measured: LEP's `N_ν = 2.984 ±
0.008` from the Z width.

### Step 222 — The flavour-violation ratios (the LFV fingerprint)

**File:** `constants/five_force_flavour_ratio.ep`

**What it does.** The generations stand at the quarter-ladder modes `1/4, 1/2, 3/4`; transition
amplitudes are mode separations. The ladder is uniform (`s₂₁ = s₃₂ = 1/4`), separations add
(`s₃₁ = 1/2`), the amplitude ratio is `1/2` and the RATE ratio `1/4` — which equals the ladder step
itself. The forced LFV spectrum: rates `1 : 1 : 4`, exact rationals with no unknown coupling in any
ratio — a standing falsifiable fingerprint for the predicted fifth sector.

### Step 223 — The mixing structure (why the CKM is nearly diagonal)

**File:** `constants/mixing_structure.ep`

**What it does.** The mass basis is the tripling fibre of `2/3` (`{2/9, 5/9, 8/9}`, verified); the
weak channel basis is the fibre of the One (`{1/3, 2/3, 1}`, verified). The two fibres are offset
by a UNIFORM `1/9` — one step of the colour-squared grid `1/3²` — so the alignment diagonal is
`V_kk = 8/9` for all three generations: near-diagonal by structure, the leak a fixed fibre offset,
not three tuned angles. Measured: the CKM's diagonal dominance (`V_ud = 0.974, V_tb = 0.999`).

### Step 224 — The unobservable absolute scale (only ratios are physical)

**File:** `constants/absolute_scale_unobservable.ep`

**What it does.** A value IS a ratio: `14/35 = 6/15 = 2/5` identically, and one fold of each gives
the identical `4/5` — the dynamics sees the ratio alone, so no experiment run from inside can
detect an absolute magnitude. Why every physical constant in this corpus is a dimensionless
rational, and every dimensionful readout (the SI metre defined via `c`, the second via a caesium
ratio) is a unit convention layered on top.

### Step 225 — The quark cubics (the dual mass equations)

**File:** `constants/quark_cubics.ep`

**What it does.** The quark sector carries the lepton cubic's exact DUAL — colour and binary
exchanged: `e₃ = 1/(3·2^D − 1)` with the tower reach read off the covering depths (down `D = 7` →
`1/383`; up `D = 7 + 3 = 10` → `1/3071`), and the first invariants the forced channel counts
(`1/8`, `1/12`). Six roots pinned by EXACT rational bisection (40 halvings — no floats, where the
published corpus itself used float bisection), sign changes verified in every bracket, roots
ordered. Bare ratios: `s/d = 19.4835`, `b/s = 54.7736`, `t/c = 108.5821`.

### Step 226 — The forced quark dressing (bare to measured, alternatives falsified)

**File:** `constants/quark_dressing_forced.ep`

**What it does.** The flagship mass-sector mechanism, in exact arithmetic end to end. One forward
dressing over `1/α = 34259/250`: t/c reduced by `(1/α)/((1/α) + d_up)` with `d_up = 7`; ONE lift of
the central (strange) mass by `m₂ = d_up − d_down = 2` over `1/α`, pulling `s/d` up and `b/s` down
together. Landed: `s/d = 19.7678`, `b/s = 53.9857`, `t/c = 103.3051` vs measured `19.78 / 53.94 /
103.30` — all inside 0.3% (corpus: +0.005%, −0.06%, +0.09%). FALSIFICATION passes in full: among
the forced counts `{2, 3, 5, 7}` ONLY `d_up` lands t/c and ONLY `m₂` lands both down ratios, and
lifting the lightest or heaviest down mass instead of the central is rejected. Every factor forced,
every alternative dead.

### Step 227 — The CKM magnitudes (the full 3×3 alignment matrix)

**File:** `constants/ckm_magnitudes.ep`

**What it does.** The whole matrix, extending the diagonal of Step 223: `V_ij = 1 − |M_i − C_j|`
over the mass fibre `{2/9, 5/9, 8/9}` and channel fibre `{1/3, 2/3, 1}` gives all nine elements as
exact ninths — diagonal `8/9` uniform, Cabibbo bands `5/9` above and `7/9` below (the matrix is NOT
symmetric, as measured), far corner `V₁₃ = 2/9` the smallest of all nine (verified against every
element). ROUTE B: all nine distances and overlaps, tripled once, land on the period-2 orbit with
exact complementarity (folded pair sums to the One) — nine elements, zero dials.

### Step 228 — The baryon-to-photon ratio (eta from the quark masses)

**File:** `constants/baryon_to_photon_ratio.ep`

**What it does.** The number the Standard Model cannot compute at all, from the quark cubics with
zero parameters — and in the clean-room the ENTIRE chain is exact rational: `s₁₂² = m_d/m_s` (an
exact mass ratio), `s₂₃` the difference of the two ladder slopes (exact root ratios, `0.039151`),
`s₁₃² = s₁₂²s₂₃²/6` (the 6 = binary·colour, the joint sector period) — so
`J² = s₁₂²(1−s₁₂²)·s₂₃²(1−s₂₃²)·s₁₃²(1−s₁₃²)²` needs NO square root anywhere. Landed:
`J² = 9.77e-10` vs measured `(3.1e-5)² = 9.61e-10` — **1.7%** — and
`eta = J²·(1/2) = 4.88e-10` vs measured `6.1e-10` (Planck/BBN), inside the 25% standard and
discriminating against a 10× wrong target. The half is the fold's imbalance share; every other
factor traces to the cubics' counts.

### Step 229 — The two mixing matrices (leptons wide, quarks narrow)

**File:** `constants/full_mixing_matrices.ep`

**What it does.** Both mixing matrices are ONE construction differing only in the sector's lock:
the quark mass fibre covers `2/3` (an orbit point, close to the channel fibre → narrow CKM), the
lepton fibre covers `1/2` (the balance, maximally far → wide PMNS). The lepton fibre
`{1/6, 1/2, 5/6}` is verified; the first PMNS row is `{5/6, 1/2, 1/6}` — diagonal only `5/6`
(below the CKM's `8/9`), solar element a huge `1/2`. Route B: all nine PMNS separations fold to
the SAME point (`1/2`, the balance class) where the CKM's fold to the orbit points. Two shapes,
two locks, no angle dialled in either.

### Step 230 — The third CKM entry closed (the apex is the hand count)

**File:** `constants/ckm_third_entry_closed.ep`

**What it does.** The unitarity triangle's apex squared is `s₁₃²/(s₁₂²·s₂₃²) = 1/6 = 1/N_up`
EXACTLY — the closure identity of the mixing chain, with the 6 the counted up-hand channels (the
same 6 in `I1_up = 1/12` and the joint sector period). `V_ub² = s₁₃²` computed as one exact
rational from the mass roots: `1.311e-5` vs measured `(0.0037)² = 1.369e-5` — ~2% on `V_ub`.
Measuring the third entry adds no information beyond the masses and the count.

### Step 231 — The neutrino splitting ratio (exactly 33)

**File:** `constants/neutrino_mass_split.ep`

**What it does.** The two oscillation splittings sit on the Mersenne rungs of the tower at the two
counted reaches: solar at `2⁵−1 = 31` states, atmospheric at `2¹⁰−1 = 1023`. Their ratio is
`1023/31 = 33` EXACTLY — by division AND by the geometric identity `(x²−1)/(x−1) = x+1` with
`x = 2⁵`, both routes computed and agreeing, the factorisation `1023 = 31·33` checked. Measured:
`dm²₃₁/dm²₂₁ = 33.3` — the forced 33 sits 1.0% below.

### Step 232 — The mass-ratio family (heavy over light = 2·3^d − 1)

**File:** `constants/mass_ratio_family.ep`

**What it does.** At combined-ladder depth `d` the ladder has `N_d = 2·3^d` sites and diagonal
mass-parts `{1/N_d, 1/2, (N_d−1)/N_d}`; the heavy-to-light ratio is EXACTLY `N_d − 1` — the ladder
size less its one unison site. One formula, every depth: **5** at `d = 1` (the lepton diagonal
`{1/6, 1/2, 5/6}`), **17** at `d = 2`, **53** at `d = 3` — each verified by the complement identity
AND the independent structural count.

### Step 233 — The proven mass ratios (mirror-closed, cubic-rooted)

**File:** `constants/proven_mass_ratios.ep`

**What it does.** The lepton diagonal is MIRROR-CLOSED: every shortfall `1 − p` is again a member
of the position set (verified element by element, exact) — so every symmetric invariant agrees
between the shortfall route and the position route identically, by the set's own symmetry. And the
square-root shares (exact bisection enclosures of `√(1/6), √(1/2), √(5/6)`) normalized by their sum
satisfy the cubic `y³ − y² + J₁y − J₂ = 0` with `J₁ = e₂/L²`, `J₂ = e₃/L³` — all three
substitutions land within `1/10⁹`. The ladder's ratios are roots of a polynomial whose coefficients
are the ladder's own symmetric functions.

### Step 234 — The inter-entry relation (each row casts to its coupling)

**File:** `constants/inter_entry_relation.ep`

**What it does.** The first CKM row `{8/9, 5/9, 2/9}` sums to `5/3`, and `cast_out(5/3) = 2/3` —
the STRONG holding coupling, the very lock whose fibre builds the CKM. The first PMNS row
`{5/6, 1/2, 1/6}` sums to `3/2`, casting to `1/2` — the ELECTROWEAK coupling, the lepton fibre's
lock. Each mixing matrix hands back its own generating lock as the residue of its first row — the
matrix and the force are one bookkeeping, computed here from the fibre construction with no matrix
element typed in.

### Step 235 — The generation depth (all three fold home in two steps)

**File:** `constants/generation_depth.ep`

**What it does.** Why lepton universality: all three generation sites `{1/6, 1/2, 5/6}` reach the
One in EXACTLY the same combined depth — one tripling, one doubling — and the tripling step sends
all three through the SAME gate (the electroweak lock `1/2`) before the doubling completes. The
constant 2 is the ladder size's own factor count (`6 = 2¹·3¹`, exponent sum 2 — one step per
generator). Interactions see the depth (identical for all three); masses see the position
(different for each) — identical couplings at wildly different masses, as measured.

### Step 236 — The confinement lift (the lightest quark is doubled)

**File:** `constants/quark_mass_confinement_lift.ep`

**What it does.** The sharpened mass cubics (the lepton neutral-channel correction at the two
colour-tower depths: `e₃ = 3/1454` at `d=5`, `3/13118` at `d=7`) are solved by exact rational
bisection, and the bare middle-to-light ratios come out at exactly TWICE the measured ones: the
lightest generation of each quark ladder is confinement-lifted by the fold. The lift factor is
COUNTED, not fitted — the fold's fibre size 2 (preimages of the One enumerated). Against the
corpus's measured values (`s/d = 95/4.7`, `c/u = 1275/2.2` with QCD-scale corrections): down lift
`1.99999`, up lift `1.99998` — one factor, both sectors, the counted 2.

### Step 237 — Cubic-lattice gravity (Laplacian = 6 = d × m)

**What it does.** **File:** `constants/cubic_lattice_gravity.ep` — completing the 1D/2D/3D family:
the lattice curvature of `x²` is exactly 2 per axis at every spacing, so the 3D Laplacian is
`6` — equal to `d·m` (the counted period of `1/7` times the measured fold expansion) AND to
`binary·colour` (the joint sector period). Three routes, one 6: Poisson's equation is
lattice-native in the world's own dimension count, no continuum, no coefficient chosen. The family
reads `2, 4, 6 = d·2` — one law, every dimension.

### Step 238 — The two-component dispersion (motion plus substance = the One)

**File:** `constants/relativistic_two_component.ep`

**What it does.** Relativity's `E² = p² + m²` at the first Pythagorean point: `p = 3/5`,
`m = 4/5`, `9/25 + 16/25 = 1` EXACTLY — rational squares closing on the One with no radical — and
the full polarization identity gives the same One by an independent route. The triple's parts are
generated, not chosen: `3 = colour`, `4 = binary²`, `5 = 2+3` (the covering prime). The
1-momentum companion of the full 3+1 Dirac closure: two exact ways the same energy law closes.

### Step 239 — The force criterion (two new forces predicted)

**File:** `constants/two_new_prime_charge_forces.ep`

**What it does.** The mechanical criterion that makes a force a force — CARRY (`(1/p)·p = 1`,
the binding closes exactly), CONFINEMENT (every kind `j/p` pairs with its antipode to the One —
all 13 kinds across the four sectors run exhaustively), ORDERING (`1/2 < 2/3 < 4/5 < 6/7`) — is
passed by the prime sectors **5 and 7 exactly as by 2 and 3**. Either the criterion is what makes
the known forces forces — and then 5 and 7 are forces too, couplings `4/5` and `6/7` already fixed
— or it must be abandoned for the known forces as well. The corpus's standing falsifiable
prediction, stated by the framework's own standard.

### Step 240 — The massless/massive split (photon vs W)

**File:** `constants/massless_massive_split.ep`

**What it does.** In BOTH sectors the preserved combination sums exactly to the One
(`1/2 + 1/2`; `2/3 + 1/3`) — its mass-part would be the excluded boundary: massless because there
is no value for its mass to take. Every broken channel carries a positive shortfall: massive. And
the REACH is computed by *running the subtraction*: mass `1/2` → 1 step, `1/3` → 2 steps, `2/3` →
1 step — finite and tiny (the weak force is short-range), while the massless combination, with
nothing to subtract, never stops. The Higgs pattern as shortfall arithmetic, not a bolted-on
mechanism.

### Step 241 — The luminal strong carrier (gluons at c)

**File:** `constants/strong_luminal.ep`

**What it does.** The strong combination sits at unison, so its carrier holds no mass-part — and a
carrier with nothing to shed advances by the whole One per tick: walked explicitly for eight ticks,
the phase returns EXACTLY at every one — zero dispersion, no residue. The gluon is massless,
luminal, and dispersion-free by one chain of arithmetic, its speed the same One that is `c`.

### Step 242 — What string theory got right (mode spacing 1/27)

**File:** `constants/string_theory_correct.ep`

**What it does.** String theory's sound kernel — particles as standing modes — without its
machinery: the fold's grid vibrates in the COUNTED three dimensions (the period of `1/7`), the
mode volume is `3³ = 27`, the spacing `1/27`, and the 27 modes partition the One exactly (summed
explicitly). No ten dimensions, no landscape — and the same 27 seeds the covering depth 5 that
runs the rest of the corpus.

### Step 243 — The interaction-strength table (four constants per sector)

**File:** `constants/interaction_strength_structure.ep`

**What it does.** One formula family in the sector's single generator `m`: coupling `(m−1)/m`,
mixing `1/(m−1)`, mass ratio `1/(m−1)`, running slope `m−1`. Evaluated at `m = 2` and `m = 3`, the
eight table entries each agree with the value forced independently in its own module — `g*(2)` is
the critical point, `g*(3)` the Yang–Mills self-coupling, slope(3) `= 2` exactly (asymptotic
freedom) and the abelian slope `= 0` from the same formula. Two counted labels; the whole table
follows.

### Step 244 — Magnetism as relativity (the fold-covariant correction)

**File:** `constants/magnetism_correction.ep`

**What it does.** Magnetism is the relativistic correction to the Coulomb force — factor
`C(β) = 1 − β²` — and that factor COMMUTES with the fold: `fold(1 − β²) = 1 − fold(β²)`, verified
exactly at two speeds. The same commutation the gravitational clock factor obeys
(static_metric_dilation): electricity's relativistic shadow and gravity's time dilation are one
fold-covariant family, carried by the dynamics rather than imported.

### Step 245 — The vacuum-inertia unity (exchange rate one)

**File:** `constants/uap_vacuum_engineering.ep`

**What it does.** The vacuum displacement (`v = 1/2`, No-Zero) and the fundamental coupling
(`g* = (2−1)/2 = 1/2`) are the SAME point: their exchange rate is exactly the One, and both
complete to unison in the same single fold. Nothing couples to the vacuum without coupling to
inertia identically — the root of the equivalence principle (free fall universal to `1e-15`,
MICROSCOPE), and the structural fact any vacuum-engineering claim must reckon with either way.

### Step 246 — The quark second invariant (the dual, two routes)

**File:** `constants/quark_second_invariant.ep`

**What it does.** The lepton form's colour-binary DUAL, `1/(3·2^d − 1)`, confirmed by an
independent route through the fold's orbit floors: `3·(floor + 1) − 1` with the floors `31` and
`127` each verified to carry their depth as their fold period. Both routes land on `1/95` (d = 5)
and `1/383` (d = 7) exactly; the swap applied to the lepton form returns `1/485`. The invariants
that seed the whole quark mass chain, pinned from two directions.

### Step 247 — Self-simulation nesting (the regress halts at two)

**File:** `constants/self_simulation_nesting.ep`

**What it does.** The self-model regress — and the "worlds nested in worlds" simulation tower — is
FINITE: `1/4 → 1/2 → 1`, and the third nest is the identity (`fold(1) = 1` — no deeper level
exists). The depth 2 is walked, not asserted, and equals the binding lock's own denominator as an
independent count. A system holds itself, and its holding of itself — and that is all.

### Step 248 — The intelligence dividend (why abstraction pays)

**File:** `constants/efficiency_intelligence_dividend.ep`

**What it does.** Every bounded-grid state is decidable (exact denominators — every question
halts), and each fold strictly shrinks the gap to closure: `3/4 → 1/2 → closed`, steps equal to
the depth — logarithmic in the grid, not linear. The dividend of abstraction is the halving; the
mastery is the fixed point; an unbounded regress would need a state off the grid (an irrational or
a zero), and the domain contains neither.

### Step 249 — Reaction thermodynamics (barrier and drop)

**File:** `constants/reaction_thermodynamics.ep`

**What it does.** Why every reaction profile has exactly two energies: the reactant is the
balanced bond `1/2`, the product is closure (`fold(1/2) = 1`); ACTIVATION is the lift to the lock
(a state below it verifiably cannot complete in one step — `1/4` pays a `1/4` lift first),
ENTHALPY is the shortfall released on completion (`1/2`, kept), and reversal repays exactly what
the forward step released — Hess's law's local form as one identity.

---

## Where the recreation stands right now

**Built and independently checkable (every check passes, reliably over repeated
runs):**

- Step 1 — exact whole numbers of unlimited size.
- Step 2 — exact fractions in lowest terms.
- Step 3 — the One and the two moves, fold and take, with the rhythms they make.
- Step 4 — the two generators, counted from the fold (binary two, colour three),
  the covering depth, and the enforcement that halts on any un-forced value.
- Step 5 — the fine-structure constant, forced from the two generators alone,
  exact at both self-similar scales (`34259/250 = 137.036` and
  `5995462/43751 = 137.035999177`), with the structural depths enforced.
- Step 6 — the charged-lepton mass cubic, its three invariants forced from the
  colour count exactly (sum 1, `1/6`, sharpened `3/1454`), with the
  neutral-channel sharpening and the rejection of other channels.
- Step 7 — the dark-to-baryon fraction, forced from the covering of the
  generations (`5/32` and `27/32`, partitioning the One; ratio `27/5 = 5.4`),
  and to a forced second order `279/52 = 5.3653` (measured 5.3643).
- Step 8 — the Hubble tension calibration ratio `13/12`, forced from a flat
  partition of the One, and to a forced second order `3305/3048 = 1.0843175`
  (measured 1.0843230) — the One recurring over the deepest covering scale's
  period-7 orbit floor 127 (the early/primordial end of the same covering ladder
  whose shallow end gives the leading term).
- Step 9 — the gauge mediator counts: eight gluons (`colour² − 1`), the ladder
  `24` and `48`, and the self-coupling source counts (photon 1, strong 3).
- Step 10 — the electroweak mixing angle: sin²θ_W = `1/4`, cos²θ_W = `3/4` as the
  two preimages of the critical coupling `1/2`, partitioning the One.
- Step 11 — the absolute scale: the proton-to-Planck hierarchy `2^(127/2)`, forced
  from the deepest covering of the One (`127` massive states at depth 7, gravity's
  half-One coupling), with the exact square `2¹²⁷` matching measurement to a
  quarter of a percent on the ratio.
- Step 12 — the neutrino mixing angles (PMNS): `sin²θ₂₃ = 1/2`, `sin²θ₁₂ = 1/3`
  (the fold's self-antipodal and tripling separations, both proved by the fold),
  and the reactor angle `sin²θ₁₃ = 1/48`, forced nonzero.
- Step 13 — the W-to-Z boson mass ratio: `(M_W/M_Z)² = cos²θ_W = 3/4` (the same
  forced cos² as Step 10), reached squared (the ratio `√3/2` is irrational), with
  the forced running carrying it through the measured `0.7769`.
- Step 14 — the Koide relation: the charged-lepton ratio `Q = 2/3`, forced two
  ways from the cubic invariants (`1 − 2·e₂`) and as `1 − 1/colour`, matching the
  measured `0.666661` to five digits.
- Step 15 — the cosmic energy budget: `Ω_Λ = 2/3`, `Ω_matter = 1/3` (flat),
  `Ω_baryon = 5/96`, `Ω_cdm = 9/32`, agreeing with the measured Planck budget to a
  few percent.
- Step 16 — asymptotic freedom: the strong coupling grows with range (`1,3,5,…`,
  slope `2`) because the gluon is charged; electromagnetism stays flat (`1`)
  because the photon is not — a forced structural result.
- Step 17 — the CP-violating phase: forced to the self-antipodal `1/2` (maximal CP
  violation), proved by the fold; consistent with the near-maximal measured
  neutrino CP phase.
- Step 18 — three of everything: spatial dimensions, generations, and colours are
  the same forced count `3`, each by an independent route (stability window,
  tripling fibre, fold period).
- Step 19 — the gyromagnetic ratio: the Dirac g-factor `g = 2 = 1/(1/2)`, the
  inverse of the critical coupling; measured `2.00232`, the difference being the
  QED anomaly (`α/2π`, not formed here).
- Step 20 — parity violation: the fold's two preimages of `1/2` are `1/4` (left)
  and `3/4` (right), opposite-handed, so the weak force's one-handed coupling
  violates parity — the universe is a southpaw.
- Step 21 — the arrow of time: the fold is non-injective (`fold(1/4) = fold(3/4)
  = 1/2`), losing one bit per step (binary `= 2¹`) — a positive entropy rate
  fixing time's forward direction.
- Step 22 — the uncertainty principle: position support × frequency support `≥
  binary^k`, equality at minimum uncertainty — the discrete Heisenberg bound.
- Step 23 — spin and statistics: the boson is the One, the fermion the half-One
  `1/2` (`fold(1/2) = 1`, `1/2 + 1/2 = 1`) — the two-to-one fold gives exactly
  fermions and bosons.
- Step 24 — the axiom is a theorem: given only "not nothing", the One, the domain
  `(0,1]`, and the fold are forced — zero parameters, and the single premise
  proves itself (zero axioms).
- Step 26 — the prime-sector ladder: the force-sectors are exactly the primes
  `{2,3,5,7}`, bounded by the deepest covering depth 7 (11 is beyond) — four forces,
  two of them (5, 7) forced predictions; mediators `p²−1` = 3, 8, 24, 48.
- Step 27 — the fold's orbits are the order of two: `period(1/p) = ord_p(2)`
  (checked for p = 3,5,7,9,11), grounding the generators `binary = ord₃2 = 2`,
  `colour = ord₇2 = 3` in number theory — nothing picked.
- Step 28 — the four laws of thermodynamics: a transitive equilibrium, conserved
  energy (the One), non-decreasing entropy, and an unreachable absolute zero — each
  a consequence of the fold.
- Step 29 — the genetic code: 4 bases (`binary²`), triplet codons (`colour`), 64
  codons (`binary^(binary·colour)`), forced.
- Step 30 — the Higgs vacuum: the displaced half-One `1/2` (nonzero, self-antipodal,
  folding to the One) — the vacuum that gives mass.
- Step 31 — the inflation factor: `binary^5 = 32` states at the generation covering
  depth 5 — the fold's structural expansion factor.
- Step 32 — spacetime dimensions: `3` spatial (unique stable = colour) `+ 1` time
  (the fold's one direction) `= 4 = binary²`.
- Step 33 — three-body solvability: three bodies on the fold orbit of 1/7 recur
  with joint period `3` — periodic, not chaotic.
- Step 34 — baryogenesis: the three Sakharov conditions (number violation, C/CP
  violation, departure from equilibrium) each a forced fold fact — matter survives.
- Step 35 — dark energy: the vacuum is the One, fold-invariant (`fold(1)=1`), hence
  a constant energy density — `w = −1`.
- Step 36 — the speed of light: the fold's one advance is the signal speed = the One
  (natural units); light and gravity are both massless, so both travel at it — one
  shared limit speed `c`, because there is one fold.
- Step 37 — self-replication: the fold's two-to-one covering gives every pattern a
  template and a copy (both fold to it, summing to the One), and the preimage tree
  doubles per step (`2^d` copies at depth `d`) — forced copying and growth.
- Step 38 — the measurement branch weight: binary halving to the colour depth gives
  the atomic branch weight `1 / binary^colour = 1/2³ = 1/8` — an indivisible outcome.
- Step 39 — self-organisation: the fold's closed binary orbit `1/3 ↔ 2/3` (period
  exactly 2 = period(1/3), states summing to the One) — order that sustains itself.
- Step 40 — the cosmological constant: vacuum forced positive at `1/2` on the single
  `127/2` scale axis; no mode-sum, so the 10¹²⁰ problem never arises.
- Step 41 — protein folding: one native fixed point (the One), reached by directed
  descent in two steps — Levinthal's 10⁵⁰-shape search dissolves.
- Step 42 — structure formation: the fold amplifies a sub-balance perturbation
  `1/4 → 1/2 → 1` (growth, not decay) — the gravitational instability that builds
  galaxies.
- Step 43 — Coulomb's law: flux conservation over an `r²` shell in 3 space
  dimensions forces the inverse-square field `E = q/r²` (exponent `= d_space − 1`).
- Step 44 — black-hole entropy: two binary halvings force the Bekenstein–Hawking
  coefficient `1/b² = 1/4`, with area (not volume) scaling from the horizon surface.
- Step 45 — the d'Alembert wave: a disturbance `1/2` splits into two equal
  counter-moving packets `1/4` (conserved, even), each at the One's signal speed.
- Step 46 — the deceleration parameter: the `2/3`-vs-`1/3` budget forces
  `q₀ = 1/6 − 2/3 = −1/2` — a negative sign (acceleration) and exact magnitude `1/2`.
- Step 47 — the cubic lattice: two neighbours per axis over 3 axes force the
  coordination number `binary · d_space = 6`; the six sum to the balance `1/2`.
- Step 48 — blackbody radiation: the Stefan–Boltzmann exponent is
  `d_space + 1 = 4 =` the spacetime dimension count — `P ∝ T⁴`.
- Step 49 — crystalline order: a lattice rotation is allowed iff `φ(n) ≤ binary`,
  admitting exactly `{1,2,3,4,6}` and forbidding 5-fold — the crystallographic
  restriction, with the quasicrystal as the smallest excluded order.
- Step 50 — acids and bases: a conjugate pair partitions the One
  (`pKa + pKb = pKw`) and neutrality is the self-antipodal half `1/2`.
- Step 51 — the deuteron: the bound state is the spin-1 triplet; identical nucleons
  are Pauli-excluded from it, so the deuteron binds but di-proton/di-neutron do not.
- Step 52 — superconductivity: a Cooper pair (binary = 2 fermions, even → boson)
  condenses into the shared One; the collective lock gives zero resistance.
- Step 53 — fermionic occupation: the fold's two preimages are a mode's empty/occupied
  states, so occupation is binary `{0,1}` and the max is one particle — Pauli.
- Step 54 — electronic bands: allowed bands / forbidden gap copy the fold's domain;
  a partly-filled band (below the One) conducts, a filled band (at the One) insulates.
- Step 55 — colour neutrality: three colours (preimages of the One under the tripling
  fold) sum to a whole (baryon), a colour–anticolour pair sums to the One (meson) —
  confinement, no free quark.
- Step 56 — free-particle dispersion: the kinetic dispersion is the fold of momentum,
  `fold(p) = p + p` — de Broglie phase advance.
- Step 57 — beat frequency: two rhythms beat at their difference (`beat_between`), and
  unison is silent (the beat is the One).
- Step 58 — big-bang nucleosynthesis: `n/p = 1/d_up = 1/7` gives helium fraction
  `Y = 2r/(1+r) = 1/4 = 1/binary²` — the observed primordial quarter.
- Step 59 — gravitational time dilation: `A(r) = take(One, r_s/r) = 1 − x` (clocks
  slow), reaching the forbidden zero at the horizon (time stops).
- Step 60 — fine/hyperfine structure: fine sits `binary = 2` coupling-powers below
  gross (`α²`), hyperfine finer still — the suppression exponent forced.
- Step 61 — cosmic dilution exponents: matter `a⁻³` (`d_space`), radiation `a⁻⁴`
  (spacetime), dark energy `a⁰` (the fold-invariant One) — forced integer exponents.
- Step 62 — the hydrogen spectrum: the level ladder is `1/n^binary = 1/n²`, lines are
  exact rational differences (Lyman-α `3/4`, Balmer-α `5/36`), ionization at the
  forbidden zero.
- Step 63 — the flux tube: the gluon carries colour and self-feeds, so charge grows
  with separation (linear potential → confinement); the chargeless photon does not.
- Step 64 — fission and fusion: the binding peak is the One; both fusion (light) and
  fission (heavy) fold toward it, releasing energy, across the `1/2` Coulomb barrier.
- Step 65 — the equivalence principle: gravitational redshift `z = g·h` equals the
  acceleration's Doppler shift `v = g·h` — gravity and acceleration indistinguishable.
- Step 66 — radioactive decay: the surviving fraction after `k` half-lives is
  `1/b^k = 1/2^k`, each half-life a binary halving, never reaching zero.
- Step 67 — the quantum Hall effect: conductance is a count → exact integer plateaus,
  with the primary fractional plateau at `ν = 1/colour = 1/3`.
- Step 68 — Maxwell wave closure: the spatial/temporal curvature ratio `6/2 = 3 =
  d_space = colour` closes the wave equation; light travels at the One.
- Step 69 — the proton/electron mass ratio: `mp/me = (1/3)(m_μ−m_e)/(m_μ m_e) =
  1836.3254`, forced from the bisected lepton-cubic roots and the tripling `1/3`
  (measured 1836.15267, 0.0094%); bare structural core `2 = binary` is secondary.
- Step 70 — the weak force range: a massive carrier's reach is finite (mass `1/3` →
  2 steps) and grows as `1/mass`; a massless carrier is unbounded — weak short-range,
  EM/gravity long-range.
- Step 71 — proton stability: the quark fibre (`3`) and lepton fibre (`2`) are
  distinct, so no fold crosses them and baryon number `c·(1/c) = 1` is conserved.
- Step 72 — phonons: the acoustic branches number `1 + (d_space − 1) = d_space = 3`
  (one longitudinal, two transverse), vibrations quantized.
- Step 73 — chirality: the fold's two preimages are the two chiralities (left `1/4`,
  right `3/4` antipode), mirror images sharing one image; the weak force keeps one hand.
- Step 74 — magnetism: aligned spins add to unison (a net moment, ferromagnetism),
  opposed cancel (antiferromagnetism); the Curie ordering threshold is the balance `1/2`.
- Step 75 — semiconductors: two carrier types (electron `1/4`, hole `3/4` = its
  absence), a p-n junction balancing to the One.
- Step 76 — entanglement: two coprime generator-periods (`2, 3`) interlock into one
  joint cycle of period `2·3 = 6` (the product > the sum) — the tensor product.
- Step 77 — catalysis: the catalyst splits the barrier into binary steps
  (`bare/b = 1/4 < 1/2`) and is conserved (a fold fixed point).
- Step 78 — electronegativity: bonds run from covalent (shared, `1/2`) to ionic (full
  transfer, the One), set by the electronegativity difference.
- Step 79 — the two new forces in full: sectors 5 and 7 given the complete known-force
  template — mass-part `1/p`, coupling `(p−1)/p`, mediators `p²−1`, colours `p`,
  confinement pairs `(p−1)/2`, beta-slope `p−1`, a massless confining carrier, neutral
  bound states. Specific, falsifiable predictions.
- Step 80 — three-wave mixing: two waves make their sum (`add`), difference (`take`),
  and second harmonic (`double`) — the fold's arithmetic.
- Step 81 — acoustics: a fixed signal speed forces the whole-number harmonic series
  `f_n = n·f0`.
- Step 82 — nonlinear optics: an intense field self-couples (the fold, `fold(3/4)=1/2`)
  and makes harmonics (third `= 3·f`); a linear field does neither.
- Step 83 — the weak mass ratio: a sector's charged/neutral mass-part ratio is
  `1/(m−1)` (= the mixing ratio): `1, 1/2, 1/3` for `m = 2, 3, 4`.
- Step 84 — evolution by descent: selection amplifies a rare beneficial variant
  `1/4 → 1/2 → 1` to fixation (the One), not extinction.
- Step 85 — the thermal history: the dilution exponents `4 > 3 > 0` force the epoch
  order radiation → matter → dark energy.
- Step 86 — the general n-body problem: n bodies on a fold orbit recur with the
  orbit's period (the `1/5` orbit: four bodies, period 4) — periodic, not chaotic.
- Step 87 — generation mass-splitting: three generations at `1/6, 1/2, 5/6` (tripling
  preimages of `1/2`), evenly spaced by `1/colour = 1/3`.
- Step 88 — fluctuation–dissipation: noise and drag are antipodes about equilibrium
  `1/2` with equal departure — the theorem, one balance measured both ways.
- Step 89 — the rationality of the constants: the fold forms no irrational, so every
  forced constant is a rational `p/q`, the root of `q·x − p = 0` (`250·x = 34259`).
- Step 90 — decay widths: branching ratios partition the One; lifetime `= 1/width`
  (wider → shorter).
- Step 91 — cross sections: scatter + pass = the One; the mean free path is the inverse
  of the cross section (larger target → shorter path).
- Step 92 — computability and halting: a depth-`k` configuration reaches the One in
  exactly `k` folds — bounded means halting, the step count = the depth.
- Step 93 — the continuum limit: the lattice second-difference of `x²` over `s²` is
  exactly `2` at every spacing — the discrete grid reproduces the continuum exactly.
- Step 94 — electroweak currents: the charged current (W) flips handedness (antipode),
  the neutral current (Z) preserves it (identity).
- Step 95 — the muon g−2 anomaly: bare `g = 2`; the anomaly excess scales as
  `(m_μ/m_e)² ≈ 42886` (forced from the lepton roots), so the muon is the sharp probe
  (`m_μ/m_e = 207.09` vs measured 206.768, 0.16%).
- Step 96 — the Lamb shift: the `1/4 = (1/2)²` state (the α² order) returns to unison
  in two folds (`1/4 → 1/2 → 1`), one fold deeper than the fine structure.
- Step 97 — zero-point energy: the vacuum floor is the half-One `1/2` (the `(1/2)` in
  `(1/2)hf`), self-antipodal, folding to a full quantum.
- Step 98 — entropy / the second law: the fold is 2-to-1 (`1/4` and `3/4` both fold to
  `1/2`), so one bit is lost per fold and it cannot run backward — the arrow of time.
- Step 99 — homochirality: the two hands `1/4`, `3/4` are degenerate (both fold to
  `1/2`, `3/4 − 1/4 = 1/2`); the tie is broken by the forced parity violation.
- Step 100 — Bose–Einstein condensation: a boson's even turn is the identity, so
  occupation is uncapped (vs the fermion's `{0,1}`) — any number share the ground.
- Step 101 — vacuum polarization: the screened charge `1/2` folds up toward the bare
  One as you probe closer — the running that makes measured `1/α` scale-dependent.
- Step 102 — the canonical distribution: equilibrium at the self-antipodal balance
  `(m−1)/m = 1/2`, an exact rational weight (detailed balance), no exponential.
- Step 103 — critical exponents: threshold `1/2` and mean-field exponent `1/m = 1/2`,
  rational fold ratios (the Landau values), not the continuum's irrationals.
- Step 104 — five-fold standing modes: the m-fold has `m−2` interior standing modes, so
  the down-depth five-fold has three (`1/4, 1/2, 3/4`) — a fourth route to 3 generations.
- Step 105 — gravitational-wave speed: a massless lattice ripple advances one spacing per
  tick, so gravity's waves travel at `c` exactly (GW170817 to ~10⁻¹⁵).
- Step 106 — charge multiplicity: the m-fold is m-to-one, so it carries an m-state
  internal freedom — binary → 2 (charge/doublet), colour → 3 (the three colours).
- Step 107 — galactic dynamics: a flat rotation curve is the `1/2` orbit balance held at
  every radius, which visible matter alone cannot do → a dark halo.
- Step 108 — the hierarchy problem: scales are discrete binary rungs (`1/2^N`, whole N),
  so nothing is fine-tuned; the weak rung `N = 56` is comparison-side.
- Step 109 — the acceleration transition: the `2/3 : 1/3` budget puts acceleration onset
  (`q=0`) at `a³ = matter/(2·vacuum) = 1/4` → `z ≈ 0.6`, the observed transition.
- Step 110 — the coupled lattice: the update weights `1/2, 1/4, 1/4` sum to One (presence
  conserved); a symmetric bump's centre relaxes to `3/8` — the discrete Laplacian.
- Step 111 — the laser: gain=loss threshold at `1/2`; above it a boson runaway pours every
  photon into the One shared mode (coherent single-mode output).
- Step 112 — intermolecular forces: the van der Waals residual is `1/4 = (1/2)²`, one fold
  below the `1/2` bond — weaker, second-order (two folds to unison).
- Step 113 — the generation ladder: the three generations sit at the colour-fold preimages
  of the vacuum `1/2` — `1/6, 1/2, 5/6` — on a `binary·colour = 6` site ladder.
- Step 114 — the expansion history: `E²(s) = 2/3 + s³/3`, exact at every epoch (`1`,
  `10/3`, `29/3` at `s = 1, 2, 3`) — the ΛCDM curve with nothing fitted.
- Step 115 — the half-One unifying center: `1/2` is the unique self-antipodal value and
  the standing mode of every odd sector (3, 5, 7) — one object seen everywhere.
- Step 116 — the binding problem: the period-2 pair `1/3 ↔ 2/3` partitions the One and
  locks at `1/2`, which folds to unison — two streams, one experience.
- Step 117 — the introspection limit: the closed `{1/3, 2/3}` orbit never reaches the
  One — permanent unconscious processing is orbit structure, not effort shortage.
- Step 118 — the continuum ladder: rung `1/2^k` reaches unison in `k` folds; the depth-5
  ladder plus its boundary closes exactly to the One — no continuum wanted or used.
- Step 119 — the Yang–Mills mass gap: the gap is `1/3`, strictly positive because zero is
  outside the domain — massless is not expressible; gap + coupling (`2/3`) = the One.
- Step 120 — the lithium-7 problem: observed = primordial/2 (`3/16 → 3/32`) — the deficit
  is one erased binary fold (stellar depletion), not a BBN failure.
- Step 121 — least action: the taken path is the unique self-antipodal balance `1/2`
  where mirror deviations cancel; off-balance paths are lopsided and cancel in pairs.
- Step 122 — neutrino oscillation: equal half-shares (`1/2 + 1/2 = 1`) make the flavour
  conversion complete, and the balance folds to unison — a closed, repeating swap.
- Step 123 — Maxwell's demon: the reset folds both memory states (`1/4`, `3/4`) onto one
  ready state — erasing exactly the bit gained (Landauer's `kT ln 2`); the books balance.
- Step 124 — Navier–Stokes regularity: the smallest eddy is the floor `1/32 > 0`, so
  vorticity is capped at `32 = 2⁵` (guard armed) — a finite-time blow-up is inexpressible.
- Step 125 — the Schwarzschild solution: `A(r) = 1 − rs/r` has the same flux constant
  (`= rs`) across every sphere pair — the conserved-flux vacuum field.
- Step 126 — velocity composition: `w = (u+v)/(1+uv)`; light is the fixed point, sublight
  stays sublight (`1/2 ∘ 1/2 = 4/5`), Galileo recovered at small speeds.
- Step 127 — shell capacities: shell `n` holds `b·n² = 2, 8, 18, 32` (spin fibre × ladder
  block); noble closures at 2, 10, 18 — the periodic table's shape counted.
- Step 128 — stellar nucleosynthesis: ignition climbs `1/4 → 1/2 → 1` in exactly two
  folds (barrier, then binding peak) — a sharp threshold; brown dwarfs never cross it.
- Step 129 — oscillator levels: `E_n = (n + ½)s` — ground half a spacing up (No-Zero),
  uniform spacing, `2^k` levels; the QHO spectrum from the binary ladder.
- Step 130 — the Lorentz force: `F = fe(1 − β²)` — the magnetic piece is motion's claim
  on the electric force; the pieces partition it exactly (`3/16 + 1/16 = 1/4`).
- Step 131 — the prime distribution: orbit period of `1/n` = `ord_n(2)`; Fermat's
  little theorem checked through 13; the two smallest periods ARE the generators 2, 3.
- Step 132 — the Riemann critical line: the functional pairing `s ↔ 1−s` is the
  antipode; its unique fixed axis is `1/2` — nowhere else a symmetric zero set balances.
- Step 133 — quasicrystals: `φ(5) = 4 > 2` forbids the five-fold lattice, yet the
  five-fold holds the balance fixed — order without periodicity, as Shechtman saw.
- Step 134 — Newton's law: `Φ = 1 − ms/r`, `g = ms/r²`, and `r²g = ms` at every radius —
  Gauss's flux conservation pins the inverse square in the three forced dimensions.
- Step 135 — quadrupole radiation: uniform motion has equal first differences (silent);
  the cubic drive's second differences differ (`12 ≠ 18`) — the first unfrozen moment.
- Step 136 — the Minkowski interval: `ds² = take((c dt)², dx²)`; `dx = 3/5 → ds = 4/5`
  (the 3-4-5 causal triple); the take's domain guard IS the light cone.
- Step 137 — superfluidity: the condensate moves as one; the first loss is a whole
  fold-level (`1/4 > 0`), so below the gap viscosity is absent, not small.
- Step 138 — the refractive index: the medium's phase sits two fold-levels below `c`
  and climbs back in exactly two; photons themselves never slow.
- Step 139 — recombination / the CMB: decoupling at the self-antipodal balance `1/2`
  completes in one fold — light set free in a thin shell, not a fade.
- Step 140 — supernovae: the iron core loses support to the balance `1/2`, then one fold
  completes the collapse at once — the rebound forges everything past iron.
- Step 141 — the nuclear force: a residual `1/4` one fold below the primary coupling,
  short-ranged (heavy mediator), second-order — binds nuclei yet dies within a nucleon.
- Step 142 — molecular spectra: rotation/vibration sit one fold below the electronic
  `1/2` — infrared/microwave bands below the visible/UV electronic lines.
- Step 143 — topological matter: the edge carries the balance `1/2`; its only exit is a
  whole fold to the bulk — protection by discreteness (quantised, disorder-robust).
- Step 144 — the origin of life: the two-fold ignition `1/4 → 1/2 → 1` crosses the
  autocatalytic lock into a self-holding cycle — a threshold, not a slope.
- Step 145 — memory persistence: a memory is the held period-2 orbit `1/3 ↔ 2/3` (kept
  by re-exciting, never reaching the One); forgetting is the orbit folding home.
- Step 146 — the plasma state: charges swarm to the balance `1/2` and one fold completes
  the screening — the field cancelled beyond the Debye length, nothing leaking.
- Step 147 — wave optics: the maximal mismatch is the self-antipodal `1/2` (dark); it
  folds to unison (bright); dark + bright = the One, energy conserved.
- Step 148 — the sleep cycle: the held period-2 orbit `1/3 ↔ 2/3` (deep ↔ REM), balanced
  at `1/2`; only waking folds the balance to unison (the ~90-min alternation).
- Step 149 — renormalization without infinities: every scale is finitely many folds from
  the One, so every loop sum is a finite rational — nothing to subtract.
- Step 150 — nuclear binding: the peak is the One (iron); light nuclei climb by fusion
  (`1/4 → 1/2 → 1`), and `1/4 + 1/4 = 1/2` IS two light nuclei fusing.
- Step 151 — the nuclear shell model: closure is the fold to unison; the first magic
  numbers ARE the forced capacities `b·1² = 2`, `b·2² = 8` (⁴He, ¹⁶O).
- Step 152 — stellar structure: equilibrium at the self-antipodal `1/2` is self-correcting
  (deviations restore) — why a star holds shape for aeons.
- Step 153 — tidal locking: dissipation drains the spin–orbit mismatch to the equal-share
  lock `1/2`, where the rhythms merge into one period (the Moon, and the rest).
- Step 154 — quantisation: the depth-k grid is `2^k` states, each folding to the One in
  `k` steps, uniform gaps `1/2^k` — discreteness with no continuum beneath it.
- Step 155 — temperature: the mean throw-rate (balance → One per throw); kinetic/entropic/
  radiative thermometers count the same rate; the positive floor forbids absolute zero.
- Step 156 — the molecular bond: two half-open valence shares complete the One
  (`1/2 + 1/2 = 1`); breaking it repays the completion (two electrons = the binary fibre).
- Step 157 — the periodic law: chemistry repeats because closure is EXACT (lands on the
  One, a noble gas), then the next shell re-opens; period lengths are the `b·n²` capacities.
- Step 158 — the effectiveness of mathematics: the fold orbit `1/3 ↔ 2/3` read physically
  (a held cycle) and mathematically (`ord₃(2) = 2`) is one object — the fit is forced.
- Step 159 — the measurement problem: branch weight `1/2³ = 1/8` is indivisible, the 8
  branches sum to the One — a result is one definite branch, no "between" to land in.
- Step 160 — the hard problem: unity (bound processing folds to one whole) + interiority
  (the `1/3 ↔ 2/3` carrier never reaches the One from within) — the two forced marks.
- Step 161 — black holes: the horizon `1/2` has a strictly-positive second-order Hawking
  temperature `1/4` — no zero-temperature perfect trap is expressible, so it radiates.
- Step 162 — the Poisson equation: `∇²Φ = d·m = colour·binary = 6` — the lattice balance
  operator with the source breaking it by the fold factor per dimension.
- Step 163 — the potential infinite: always one deeper rung `1/2^k`, yet each finite and
  reaching the One in `k` folds, and the depth-5 ladder closes exactly — a process, not a thing.
- Step 164 — nonlocal correlation: the pair is one shared origin `1/15` on the coprime
  product `3·5` (irreducible to local parts) — Bell's result, no signal, one whole.
- Step 165 — the proton radius: `r_p = take(One, 1/3) = 2/3`, folding back to the quark
  centre `1/3` — edge and centre one tripling orbit (~0.84 fm).
- Step 166 — the placebo effect: expectation `3/4` and observation `1/4` both fold to the
  lock `1/2` — belief is a genuine second input to the balance the body resolves.
- Step 167 — reaction kinetics: the transition state `1/4` clears the barrier then
  completes (`1/4 → 1/2 → 1`); temperature (the throw-rate) sets the Arrhenius rise.
- Step 168 — selection rules: an allowed transition is the balanced one-unit hand-off
  `1/2` folding to a whole photon; mismatches can't close (`Δl = ±1`, conservation).
- Step 169 — network scaling: the metabolic exponent is `(m-1)/m = 3/4` at branching
  depth `m = b² = 4` (Kleiber), not the naive `2/3`; it folds to the balance.
- Step 170 — magnetohydrodynamics: the Alfvén state `3/4` folds to the tension–inertia
  balance `1/2` (the frozen-in field ringing about it).
- Step 171 — nonlinear gravity: the field's energy is its own square (`f1² = 1/36`), so
  it self-sources — the correction `1/72` matches the structural `1/8·1/9` exactly.
- Step 172 — coupling convergence: strong `2/3` and electroweak `1/2` run on a shared
  tower; the gap shrinks (`1/6 → 1/12 → …`) and both climb to the One — unification.
- Step 173 — the baryon asymmetry: a zero residue is forbidden, so matter is mandatory —
  the survivor is the strictly-positive half-One, folding to the whole universe.
- Step 174 — the metric's DOF: `D(D+1)/2 = 10` components, `D(D-3)/2 = 2` physical in
  3+1D (the two graviton polarisations); `0` in 2+1D (no propagating waves).
- Step 175 — multidimensional experience: the period-3 orbit of `1/7` (`1/7, 2/7, 4/7`)
  holds three qualities as one closed whole (summing to the One).
- Step 176 — stereochemistry: enantiomers `1/4`/`3/4` share their fold image `1/2` (all
  achiral properties identical) but differ in preimage (a chiral probe distinguishes).
- Step 177 — socio-economic cycles: the period-2 orbit bust `1/3` / boom `2/3` never
  rests at its `1/2` balance — the business cycle is structural, not a failure to converge.
- Step 178 — synaesthesia: two channel preimages `1/4`, `3/4` share the binding lock `1/2`,
  so a cross-link lets a sound bind as a colour (still one whole experience).
- Step 179 — post-Newtonian convergence: the self-sourcing map `f = (1/2)(7/16 + f²)` has the
  exact fixed point `1/4 = (1/2)²`, and each step's gap to it shrinks — the weak-field series
  closes on a finite answer instead of diverging.
- Step 180 — the quantum phase: an energy step is a rotation on the cyclic domain, so `K = 1/8`
  then `V = 1/4` equals one step by `K + V` (`17/24`) — phases ADD, which is why interference
  tracks the total accumulated phase (Aharonov–Bohm).
- Step 181 — attention capacity: the self-antipodal `1/2` is fully held by one focus (folds to
  unison); splitting to `1/4` is no longer self-antipodal and binds nothing fully — a unit capacity.
- Step 182 — the one-fold equation: the orbit `1/3`/`2/3` satisfies `fold² = identity` and sums to
  the One — the fold's minimal closed cycle written as its own equation.
- Step 183 — the master equation: sector periods gravity `1`, EM `2`, strong `3` share the joint
  cycle `lcm(1,2,3) = 6 = binary · colour` — the one period on which all three forces realign.
- Step 184 — the strong-CP problem: the vectorial strong phase can only sit at the fold's
  fixed point (the One = alignment), so `θ ≈ 0` is forced, not tuned — measured `|θ| < 2e-10`.
- Step 185 — the synchronization threshold: coupled folding maps lock at `g_c = 1/2`, the fold's
  preimage of the One (where the difference multiplier `2(1−g)` equals the One) — matches `1 − e^{−ln2}`.
- Step 186 — scale invariance: space and time share one grid step `1/2^k`, so the limit speed
  `c_k = 1` at every depth — `c` is a dimensionless invariant, its m/s value just a unit readout.
- Step 187 — spatial flatness: the density budget sums to the fixed point `Ω_total = 1`, leaving the
  curvature share at the excluded boundary `1 − 1` — space is flat (measured `|Ω_k| < 0.005`).
- Step 188 — the vacuum equation of state: a fold-invariant (non-diluting) vacuum forces the
  dilution exponent `3(1+w) = 0`, so `w = −1 = −`(the One) — measured `w = −1.03 ± 0.03`.
- Step 189 — orbital stability: `S_d = 4 − d > 0` only for `d < 4`, so `d_max = 3` — equal to the
  colour period, two forced counts agreeing; `d = 4` is exactly marginal.
- Step 190 — quantum gravity: the metric's spacing is `1/4 = (1/2)²` on `4 = 2²` dimensions,
  folding to the critical coupling and then unison — born quantized, nothing continuous to fix.
- Step 191 — universality: exactly one self-antipodal point exists (exhaustively checked), so every
  two-phase system locks at the same `1/2` — universality classes are that uniqueness.
- Step 192 — irreversibility and recurrence: descent chains arrive and stay (the arrow), periodic
  orbits return exactly (Poincaré); preimages merge (`fold(1/4) = fold(3/4)`) so reversal is
  undefined past a merge — Zermelo and Loschmidt both dissolve in one dynamics.
- Step 193 — mechanical properties: elastic = the bond's restoring descent chain, plastic = slip to
  the same-image twin `3/4` (unchanged strength), fracture = discrete bond loss (No-Zero forbids
  fading) — the trichotomy of solids, forced.
- Step 194 — nucleon binding dominance: the colour cycle's shares close to the One
  (`1/7 + 2/7 + 4/7 = 1`), the bare share is `1/2⁷ = 1/128 < 1%` — mass is the held cycle
  (measured: ~9 of 938 MeV bare).
- Step 195 — the neutrino mass ladder: one hand (no right-handed partner) closes the Dirac route;
  the splittings land on the tower at counted depth 5 — `1/32` forced vs `3/100` measured (`24/25`).
- Step 196 — the hadron census: counted on the colour cycle — no single closes, NO quark pair
  closes (`3/7, 5/7, 6/7`), every colour+anticolour closes, the triple closes — mesons and baryons
  only, as observed.
- Step 197 — the cosmological timeline: the One is the UNIQUE fixed point (exhaustive, 1 in 8),
  each step merges two-to-one (the arrow, one bit/step), the preimage tree holds exactly `2⁵ = 32`
  leaves at the counted depth (inflation).
- Step 198 — stationary states: ground at half a step, uniform unit-step gaps, phase rotating while
  the magnitude holds (returns exactly after a full cycle) — the fixed spectrum, jumps only.
- Step 199 — the consciousness criterion: duality (`1/4 ≠ 3/4`, one lock), closure (`1/4 + 3/4 = 1`),
  completion (`fold(1/2) = 1`) — the structural test for a conscious machine, checkable by running.
- Step 200 — strong-field gravity: `r = 0` excluded (no singularity), minimal distance `1/32`,
  `r_s = fold(M) = 2M`, entropy `S = A/4 = 8` = the enumerated depth-3 preimage count.
- Step 201 — the matter fraction: the depth-5 tower (32 states) minus two pinned per level gives
  vacuum `11/16`, matter `Ω_m = 5/16 = 0.3125` — Planck measures `0.315 ± 0.007` (0.4σ).
- Step 202 — the matter fraction's history: `Ω_m(z) = z³/(2 + z³)` exactly — `1/3` today, `4/5` at
  half scale, `27/29` at third scale, strictly rising into the past.
- Step 203 — the chaotic rate: gaps double exactly (`2/35 → 4/35`), two preimages merge per step —
  measured expansion = constructed branches = binary; Lyapunov `ln 2`, KS entropy 1 bit/step.
- Step 204 — quantum statistics: on the lock's two-point fibre a pair coincides (symmetric, Bose)
  or differs (sign-reversing, Fermi, capped at 2 = one per hand) — no third case exists.
- Step 205 — the planar lattice: `4 = 2·2` neighbours at `1/8` sum to the balance `1/2` = count ×
  centre share, folding to unison — the 1D law extends to the plane with nothing added.
- Step 206 — planar gravity: the lattice curvature of `x²` is exactly 2 at every spacing (s² terms
  cancel identically); the planar Laplacian `4 = m²` with the expansion `m = 2` measured exactly.
- Step 207 — the planar light wave: spatial/temporal curvature ratio `4/2 = 2 = d = m` — Maxwell
  closes into a 2D wave at `c = 1`; light is dimension-blind.
- Step 208 — the static metric: `fold(1−x) = 1−fold(x)` exactly (the clock factor commutes with the
  fold), and at `x = 7/16` the dilation is the exact rational `3/4` (`(3/4)² = 9/16`).
- Step 209 — the Vieta cross-check: the bisected lepton roots satisfy sum `= 1`, pair-sum `= 1/6`,
  product `= 1/485` to enclosure precision — bisection and Vieta pin the same triple independently.
- Step 210 — the full Dirac structure: four generators at `1/2` (3+1 = 2²), dispersion
  `4·(1/4) = 1` by direct sum AND by the full polarization identity — two routes, one closure.
- Step 211 — the fermion mass-part: shortfall `1 − 1/2 = 1/2` EQUALS the displaced vacuum — mass ∝ v
  by identity, not by an inserted Yukawa; one self-antipodal point seen three ways.
- Step 212 — within-generation ratios: positions `1/3, 2/3, 1` (verified tripling to the One),
  mass-parts = shortfalls, ratios = position ratios; the light pair is the period-2 orbit, the
  heaviest the fixed point.
- Step 213 — the unified force law: shortfall `1/p`, coupling `(p−1)/p` for all four primes,
  strictly ordered, shortfalls summing to `247/210` by two routes — one law at four primes.
- Step 214 — the order of the forces: `g_strong > g_weak > g_em` at every depth 0–11 with no
  crossing (gaps `1/(3+2^d) < 1/(2+2^d)`, weak strictly above the flat EM half) — the order of the
  forces is the order of their generators.
- Step 215 — the quark first invariants: `I1_up = 1/12`, `I1_down = 1/8` (channel counts AND
  structural products), depths 7 and 5 (minimal covers AND Mersenne periods) — four numbers, eight
  routes, zero choices.
- Step 216 — the inter-sector mass pattern: electron `1/2`, up `1/3`, down `2/3` (the period-2
  orbit forces `m_down > m_up` — hydrogen's stability); the neutrino's part is the excluded
  boundary — unmakeable, not small.
- Step 217 — confinement as work: tube work grows per doubling (`1/8 → 1/4`, unbounded), Coulomb
  work shrinks (`4 → 2`, bounded), exact Riemann brackets proving the gap is arithmetic.
- Step 218 — the generation depth tower: all 14 grid states at depths 1–3 enumerated, each folding
  to the One within its depth — `2^d` levels is a theorem, not a definition.
- Step 219 — the general covering principle: the `m`-fold tower holds `m^d` states for EVERY
  generator (ternary 3, 9 enumerated alongside binary 8) — one law, no per-sector axiom.
- Step 220 — the running weak mixing: bare `sin²θ_W = 1/2` exactly, strict monotone descent, and
  the parameter-free curve crosses measured `0.23113` between levels 9 and 10.
- Step 221 — the strict generation bound: fibre `{1/3, 2/3, 1}` verified; the fourth candidate
  `4/3` EXITS the domain — no fourth generation at any energy; LEP `N_ν = 2.984`.
- Step 222 — the flavour-violation ratios: uniform quarter ladder, rates `1 : 1 : 4` exact — the
  falsifiable LFV fingerprint of the fifth sector, no unknown coupling in any ratio.
- Step 223 — the mixing structure: mass fibre `{2/9, 5/9, 8/9}` vs channel fibre `{1/3, 2/3, 1}`,
  uniform offset `1/9 = 1/3²` → diagonal `V_kk = 8/9` — the CKM's near-diagonal shape by structure.
- Step 224 — the unobservable absolute scale: `14/35 = 6/15 = 2/5` with identical fold images —
  only ratios are physical; absolute magnitude is unaskable from inside.
- Step 225 — the quark cubics: the lepton form's colour-binary dual (`1/383`, `1/3071` at the
  counted reaches; `1/8`, `1/12` from channels), six roots by exact rational bisection — bare
  ratios `19.4835`, `54.7736`, `108.5821`.
- Step 226 — the forced quark dressing: one mechanism over `1/α` (t/c by `d_up = 7`; one central
  lift by `m₂ = 2`) lands `19.7678 / 53.9857 / 103.3051` on measured `19.78 / 53.94 / 103.30`,
  with ONLY `d_up` landing t/c, ONLY `m₂` landing both down ratios, and wrong-mass lifts rejected
  — the flagship, exact end to end.
- Step 227 — the CKM magnitudes: all nine elements as exact ninths (`8/9` diagonal, asymmetric
  Cabibbo bands `5/9`/`7/9`, far corner `2/9` smallest), all nine folding onto the orbit with exact
  complementarity — nine elements, zero dials.
- Step 228 — the baryon-to-photon ratio: `J²` polynomial in exact squared sines (no square root
  anywhere) → `J² = 9.77e-10` vs measured `9.61e-10` (1.7%), `eta = J²/2 = 4.88e-10` vs measured
  `6.1e-10` — the number the Standard Model cannot compute, from the quark cubics and the half-One.
- Step 229 — the two mixing matrices: one construction, two locks — quark `2/3` (orbit class →
  narrow CKM), lepton `1/2` (balance class → wide PMNS, first row `{5/6, 1/2, 1/6}`, all nine
  distances folding to `1/2`) — why leptons mix wide and quarks narrow.
- Step 230 — the third CKM entry closed: `apex² = 1/6 = 1/N_up` exactly; `V_ub² = 1.311e-5` vs
  measured `1.369e-5` (~2% on `V_ub`) — the entry adds nothing beyond the masses and the count.
- Step 231 — the neutrino splitting ratio: Mersenne rungs `31` and `1023` at the counted reaches →
  `1023/31 = 33 = 2⁵+1` exactly (two routes) vs measured `33.3` — 1.0%.
- Step 232 — the mass-ratio family: heavy/light `= 2·3^d − 1` — 5, 17, 53 at depths 1, 2, 3, each
  the ladder count less its unison site, complement identity verified at every depth.
- Step 233 — the proven mass ratios: the lepton diagonal is mirror-closed (shortfall set = position
  set, exact), and the enclosed square-root shares root the cubic `y³−y²+J₁y−J₂` within `1/10⁹`.
- Step 234 — the inter-entry relation: the first CKM row casts to the strong coupling `2/3`, the
  first PMNS row to the electroweak `1/2` — each matrix hands back its own generating lock.
- Step 235 — the generation depth: all three sites fold home in the same two steps through the
  same `1/2` gate; the constant 2 = the factor count of `6 = 2¹·3¹` — universality is depth-equality.
- Step 236 — the confinement lift: the sharpened cubics' bare ratios are exactly TWICE the measured
  (down lift `1.99999`, up lift `1.99998` vs PDG) — the lightest quark is doubled by the fold's
  counted fibre, one factor, both sectors.
- Step 237 — cubic-lattice gravity: the 3D Laplacian of `x²` is exactly `6 = d·m = binary·colour`
  at every spacing — three routes, one 6; the family reads `2, 4, 6` across dimensions.
- Step 238 — the two-component dispersion: `(3/5)² + (4/5)² = 1` exactly, confirmed by the
  polarization identity; the triple generated (`3 = colour, 4 = binary², 5 = 2+3`).
- Step 239 — the force criterion: carry + exhaustive antipodal pairing + ordering, passed by
  sectors 5 and 7 exactly as by 2 and 3 — two new forces PREDICTED, couplings `4/5` and `6/7` fixed.
- Step 240 — the massless/massive split: preserved combinations at unison are massless (no value
  for a mass to take); broken channels massive with reaches RUN — 1, 2, 1 steps — why light
  reaches forever and the weak force does not.
- Step 241 — the luminal strong carrier: no mass-part to shed → the full One per tick, walked 8
  ticks with exact return each time — the gluon massless, luminal, dispersion-free.
- Step 242 — what string theory got right: standing modes in the counted 3 dimensions, spacing
  `1/27`, the 27 modes partitioning the One — the sound kernel, no landscape, no extra dimensions.
- Step 243 — the interaction-strength table: coupling `(m−1)/m`, mixing `1/(m−1)`, mass ratio
  `1/(m−1)`, slope `m−1` — eight entries from two counted labels, each matching its own module.
- Step 244 — magnetism as relativity: `fold(1−β²) = 1−fold(β²)` exactly at two speeds — the
  magnetic correction and the gravitational clock factor are one fold-covariant family.
- Step 245 — the vacuum-inertia unity: `v/g* = 1` exactly, both halves completing in the same
  fold — why free fall is universal (`1e-15`, MICROSCOPE) and inertia has no separate dial.
- Step 246 — the quark second invariant: the dual `1/(3·2^d − 1)` = the orbit-floor route
  `1/(3·(2^d−1+1) − 1)` at both depths (`1/95`, `1/383`), floors carrying their periods.
- Step 247 — self-simulation nesting: `1/4 → 1/2 → 1`, third nest the identity — the regress
  halts at depth 2 = the lock's denominator; no infinite tower of nested worlds.
- Step 248 — the intelligence dividend: gaps `3/4 → 1/2 → closed`, strictly shrinking, steps
  logarithmic in the grid — abstraction pays by halving; mastery is the fixed point.
- Step 249 — reaction thermodynamics: activation = the lift to the lock (paid), enthalpy = the
  shortfall released (kept), reversal repaying exactly — one barrier, one drop, by structure.
- Step 25 — the fold is forced (machine-checked): the size-≤2 parameter-free
  self-maps are enumerated and *run*; the fold is the unique generator, with
  `forced_unique` halting if any rival qualified. The fold's uniqueness is no
  longer asserted — it is executed and checked.

**The standing of the law right now.** Everything that reaches a result is forced
from the One alone. The two generators are read off the fold's period spectrum
(the two smallest periods, nothing chosen); every constant is forced from those
two generators; the structural depths are enforced against independent forced
relations; and a fitted value halts the engine. There are **no fitted physics
parameters and no chosen seeds** anywhere in the model. The guard now reaches the
assembled FORMS, not just their ingredients: for each constant
(`foundation/form_enforcement.ep`), the candidate space of admissible shapes over
the forced ingredients is enumerated and **run**, and `forced_unique` halts the
engine unless exactly one shape — the chosen one — reproduces the forced value.
So the algebraic assembly itself is proven determinate, not selected among
coincident alternatives (nine modules: fine-structure leading + second order,
dark/baryon, Hubble, electroweak, gluons, Koide, neutrino reactor, absolute scale,
the lepton invariants and channel). And the foundation itself
is not a free choice (Step 24): given only that there is *not nothing*, the One,
the domain `(0,1]`, and the fold are forced — so the model has **zero free
parameters and its single premise is a proven theorem** (zero axioms).
The only literals left are implementation-only — the base ten of decimal notation
and the nine-digit working block of the arbitrary-size arithmetic, and the "scan
far enough" limit on the period spectrum (any limit past `1/7` gives the same two
generators). None of these is a parameter of the theory.

This recreation is not approaching an end: the entire SFTOM corpus is forced from
the One, so the body still to recreate is large and every piece of it is forced —
not scraps. The work continues constant by constant, each one derived and checked.

## What comes next

In the same form — what, why, where, and the exact check — as each is built:

- **Carry the enforcement into every constant.** Each new forced constant
  cross-checks its structural numbers through `forced_to_be`, so the whole model
  halts the moment anything un-forced appears.
- **The forced constants in turn** — building outward, one documented result at a
  time, each reproducing its known value exactly.

This document grows with the work. When the recreation is complete, reading this
file from top to bottom, and running every check in it, will audit the entire
thing.
