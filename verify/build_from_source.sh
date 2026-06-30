#!/bin/sh
# Regenerate the committed C in this directory from the ErnosPlain sources, to
# confirm the C really is the compiler's output (not something hand-edited).
#
# Requires the ErnosPlain compiler `ernos` on your PATH. After running this, the
# files verify/test_*.c are exactly what `ernos` emits for tests/test_*.ep, and
# `make check` builds and runs them. If `ernos` is not installed you can skip this
# and just run `make check` on the committed C directly.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/.." && pwd)"
cd "$root"

if ! command -v ernos >/dev/null 2>&1; then
  echo "ernos not found on PATH. Install the ErnosPlain compiler, or just run"
  echo "  make -C verify check"
  echo "on the committed C (no ernos required)."
  exit 1
fi

for t in tests/test_*.ep; do
  name=$(basename "$t" .ep)
  ernos "$t" >/dev/null
  cp "tests/${name}_compiled.c" "verify/${name}.c"
done
# tidy the build artifacts ernos leaves next to the sources
find tests -type f ! -name '*.ep' -delete
echo "Regenerated verify/*.c from the .ep sources. Now run: make -C verify check"
