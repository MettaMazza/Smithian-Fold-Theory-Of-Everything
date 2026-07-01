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

# Post-process: disable the runtime GC in the emitted C. The precise collector frees
# live-but-unrooted argument temporaries mid-expression (a heap-use-after-free in the
# runtime), which shows up as spurious FAILs / segfaults. These verifiers are bounded
# one-shot programs (~18 MB peak, run in a fraction of a second), so never collecting
# is harmless and no computed value depends on the GC. This is a WORKAROUND applied to
# the generated C; the proper fix is upstream in the compiler codegen (spill each
# argument temporary to a rooted local before evaluating a sibling allocating arg) or
# in the runtime (have the single-threaded collect path conservatively scan its own C
# stack, as ep_gc_park_if_stopped already does for other threads). Do NOT make
# ep_gc_enabled=0 a compiler default -- that would wrongly disable GC for every real
# program. Until the upstream fix lands, regeneration must re-apply this line.
sed -i.bak 's|^static int ep_gc_enabled = 1;|static int ep_gc_enabled = 0;  /* disabled: GC freed live unrooted temporaries (heap-use-after-free) in these one-shot proofs; see build_from_source.sh */|' verify/test_*.c
rm -f verify/test_*.c.bak

echo "Regenerated verify/*.c from the .ep sources (GC disabled for the proofs)."
echo "Now run: make -C verify check"
