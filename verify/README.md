# Verify everything — with or without ErnosPlain

This directory lets anyone reproduce every result, two ways.

## Path 1 — just a C compiler (no ErnosPlain)

Each `test_*.c` here is the **self-contained output of the ErnosPlain compiler**
for one proof: it bundles its own runtime and includes only standard C headers, so
any C compiler can build it.

```sh
make check
```

This builds every proof and runs it, printing `ok` for each and `ALL PROOFS PASS`
at the end (or `FAIL` if any check does not hold). You need nothing but `cc`/`gcc`
or `clang` and `make`.

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

## What the proofs establish

Every fundamental constant is derived from the One and the fold with zero free
parameters; the engine halts on any fitted or chosen value. See the repository
[`README.md`](../README.md), the step-by-step [`OneFoldMaster.md`](../OneFoldMaster.md),
and the auditing rules in [`STANDARDS.md`](../STANDARDS.md).
