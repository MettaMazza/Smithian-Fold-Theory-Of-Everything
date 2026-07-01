#!/bin/sh
# Regenerate the committed C in this directory from the ErnosPlain sources, to
# confirm the C really is the compiler's output (not something hand-edited).
#
# Uses the ErnosPlain compiler `ernos`. The compiler is bundled in ../compiler/, so if
# `ernos` is not on your PATH this script builds it from there (needs cargo). After
# running this, the files verify/test_*.c are exactly what `ernos` emits for
# tests/test_*.ep, and `make check` builds and runs them. If you have neither ernos nor
# cargo, skip this and just run `make check` on the committed C directly.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/.." && pwd)"
cd "$root"

if command -v ernos >/dev/null 2>&1; then
  ERNOS=ernos
elif [ -x "$root/compiler/target/release/ernos" ]; then
  ERNOS="$root/compiler/target/release/ernos"
elif command -v cargo >/dev/null 2>&1; then
  echo "ernos not on PATH; building the bundled compiler (compiler/) ..."
  cargo build --release --manifest-path "$root/compiler/Cargo.toml" >/dev/null
  ERNOS="$root/compiler/target/release/ernos"
else
  echo "ernos not found and cargo not installed. Build the bundled compiler with"
  echo "  cargo build --release --manifest-path compiler/Cargo.toml"
  echo "or just run  make -C verify check  on the committed C (no ernos required)."
  exit 1
fi

for t in tests/test_*.ep; do
  name=$(basename "$t" .ep)
  "$ERNOS" "$t" >/dev/null
  cp "tests/${name}_compiled.c" "verify/${name}.c"
done
# tidy the build artifacts ernos leaves next to the sources
find tests -type f ! -name '*.ep' -delete

# NOTE: the GC-disable post-processing step that used to live here is GONE. The root
# cause was fixed in the compiler runtime (bundled in ../compiler/): minor collections
# now conservatively scan the collecting thread's own C stack, so freshly-allocated
# argument temporaries can no longer be freed mid-expression. The proofs run with the
# GC ON -- bounded memory (a few MB per suite, where the exact-bisection proofs
# previously peaked at gigabytes with the GC disabled) and no use-after-free.

echo "Regenerated verify/*.c from the .ep sources (GC on; fixed compiler)."
echo "Now run: make -C verify check"
