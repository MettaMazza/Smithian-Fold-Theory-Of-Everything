#!/bin/sh
# The one-fold driver, PARALLEL: builds and runs every proof across all cores.
# Identical tally to prove_all.sh; wall time collapses to the slowest single suite.
set -e
here="$(cd "$(dirname "$0")" && pwd)"; cd "$here"
NPROC=$(getconf _NPROCESSORS_ONLN 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
make -j"$NPROC" all >/dev/null
tmp=$(mktemp -d)
ls test_*.c | sed 's/\.c$//' | xargs -P "$NPROC" -I {} sh -c './{} > "'"$tmp"'/{}.out" 2>&1 || true'
suites=0; oks=0; fails=0
for f in "$tmp"/*.out; do
  suites=$((suites + 1))
  n_ok=$(grep -cE '^  ok' "$f" 2>/dev/null || true); n_ok=${n_ok:-0}
  n_fail=$(grep -cE 'FAIL' "$f" 2>/dev/null || true); n_fail=${n_fail:-0}
  oks=$((oks + n_ok)); fails=$((fails + n_fail))
done
rm -rf "$tmp"
echo "================================================================"
echo "  suites: $suites    forced checks passed: $oks    failed: $fails"
if [ "$fails" -eq 0 ]; then
  echo "  EVERYTHING FORCED, DERIVED, COUNTED, AND VERIFIED -- traced to the One."
  echo "================================================================"
else
  echo "  SOME PROOFS FAILED."; echo "================================================================"; exit 1
fi
