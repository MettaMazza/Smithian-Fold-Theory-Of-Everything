#!/bin/sh
# ============================================================================
#  THE ONE-FOLD DRIVER  --  prove EVERYTHING in one run.
# ============================================================================
#  Builds and runs every proof in this directory, enumerating every forced
#  constant and scale in a single pass, then a grand tally. Needs nothing but a
#  C compiler (each proof is self-contained C; no ErnosPlain required).
#
#  Each proof is its OWN compilation unit with its own correct definitions, so
#  running them together here is exactly equivalent to running them one by one --
#  no cross-module name clash can occur. This is the top-level "prove the whole
#  theory quick and easy" entry point.
#
#    ./prove_all.sh            enumerate every forced value + grand tally
#    make prove                the same, via the Makefile
# ============================================================================
set -e
here="$(cd "$(dirname "$0")" && pwd)"
cd "$here"

# Build every proof from the committed C (silent unless something breaks).
make all >/dev/null

suites=0
oks=0
fails=0

echo "================================================================"
echo "  THE SMITHIAN FOLD  --  every constant and scale, forced from the One"
echo "  (one axiom-free foundation; zero free parameters; exact arithmetic)"
echo "  * test_trace_to_the_one  -- the whole chain reduced to the axiom (the One)"
echo "  * test_codata_comparison -- every forced value vs external CODATA/PDG/Planck"
echo "================================================================"

for c in test_*.c; do
  b="${c%.c}"
  [ -x "$b" ] || continue
  suites=$((suites + 1))
  out="$(./$b)"
  printf '%s\n' "$out"
  n_ok=$(printf '%s\n' "$out" | grep -cE '^  ok' || true)
  n_fail=$(printf '%s\n' "$out" | grep -cE 'FAIL' || true)
  oks=$((oks + n_ok))
  fails=$((fails + n_fail))
done

echo "================================================================"
echo "  suites: $suites    forced checks passed: $oks    failed: $fails"
if [ "$fails" -eq 0 ]; then
  echo "  EVERYTHING FORCED, DERIVED, COUNTED, AND VERIFIED -- traced to the One,"
  echo "  and checked against external CODATA / PDG / Planck measurement."
  echo "================================================================"
else
  echo "  SOME PROOFS FAILED."
  echo "================================================================"
  exit 1
fi
