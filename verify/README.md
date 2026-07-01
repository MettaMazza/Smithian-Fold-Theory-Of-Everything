# Verify everything — with or without ErnosPlain

This directory lets anyone reproduce every result, two ways.

## Path 1 — just a C compiler (no ErnosPlain)

Each `test_*.c` here is the **self-contained output of the ErnosPlain compiler**
for one proof: it bundles its own runtime and includes only standard C headers, so
any C compiler can build it. (One line is post-processed — `ep_gc_enabled` is set to
`0` — to disable the runtime garbage collector; see the note below. Nothing else is
touched, and no computed value depends on it.)

```sh
make prove      # THE unified driver: enumerate every forced value + a grand tally
make check      # or: build & run every proof, one ok / FAIL line per suite
```

`make prove` runs the top-level driver (`prove_all.sh`): it builds and runs every
proof in one pass, prints each forced constant and scale with its value, and ends with
a grand tally — `EVERYTHING FORCED, DERIVED, COUNTED, AND VERIFIED — from the One`.
`make check` is the terser per-suite `ok`/`ALL PROOFS PASS` form. Each proof is its own
self-contained compilation unit, so running them together is exactly running them one
by one — no cross-module clash. You need nothing but `cc`/`gcc` or `clang` and `make`.

Each proof prints, line by line, the forced value it computed and whether it
matches — so you are checking the derivations themselves, not taking a summary on
trust.

## Path 2 — from the ErnosPlain source

The C above is generated; the real source is the readable `.ep` in `foundation/`
and `constants/`. To confirm the C is genuinely the compiler's output, install the
ErnosPlain compiler (`ernos`) and regenerate it:

```sh
./build_from_source.sh      # rebuilds verify/*.c from the .ep sources via ernos
make check                  # then build and run as above
```

Or run a single `.ep` proof directly with the compiler:

```sh
ernos ../tests/test_fine_structure_constant.ep && ../tests/test_fine_structure_constant
```

`build_from_source.sh` re-applies the one-line GC-disable after regenerating (each
proof's `.c` gets `ep_gc_enabled = 0`).

## The garbage-collector note

The runtime's precise collector can free a live-but-unrooted argument temporary in
the middle of an expression (a heap-use-after-free), which surfaces as spurious
failures or a segfault. These verifiers are bounded, one-shot programs — ~18 MB peak,
finishing in a fraction of a second — so simply never collecting is harmless and no
computed value depends on the GC. That is why the generated C is post-processed to
set `ep_gc_enabled = 0`. This is a workaround in the emitted proofs only; the proper
fix is upstream (codegen roots each argument temporary, or the collector
conservatively scans its own C stack), and `ep_gc_enabled = 0` must **not** become a
compiler default for real programs.

## What the proofs establish

Every fundamental constant is derived from the One and the fold with zero free
parameters; the engine halts on any fitted or chosen value. See the repository
[`README.md`](../README.md), the step-by-step [`OneFoldMaster.md`](../OneFoldMaster.md),
and the auditing rules in [`STANDARDS.md`](../STANDARDS.md).
