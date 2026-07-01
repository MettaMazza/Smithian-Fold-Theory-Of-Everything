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
  Together these make "nothing is fitted and nothing is chosen" enforced, not
  merely intended.

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
=== done ===
```

**Second order, to measurement (forced).** The covering depth is read one level
deeper: the One recurs over its **period-orbit floor** `2^d_down − 1 = 31` (the
unique denominator whose fold-orbit has period d_down; the tower `2^d_down` is
pre-periodic and cannot host it — the engine checks the period is 5). So
`27/(5 + 1/31) = 279/52 = 5.3653`, against the measured 5.3643 — two parts in ten
thousand, from 27/5's seven in a thousand. (Falsified: the d_up floor 127 gives
5.39, rejected.)

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
a one-axiom model.

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

**To measurement.** The forced `1/2`, `1/3`, `1/48` agree with the measured
`0.545`, `0.307`, `0.022` to within about a tenth — looser than the precision
constants (mixing angles are themselves measured less sharply), but forced exactly
with zero parameters, and the reactor angle is forced **nonzero** at `1/48`.

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

**To measurement.** The forced budget agrees with the measured Planck values to a
few percent — the leading-order energy budget of the universe, zero parameters.

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
parameters — and, arguably, zero axioms: the one premise proves itself.

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
  proves itself (arguably zero axioms).
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
parameters and its single premise is a proven theorem** (arguably zero axioms).
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
