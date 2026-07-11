import sys
sys.path.append("fold_ai")
from unison_chat import *
record_correction("What is the capital of the fold?", "The capital of the fold is the One")
rng = np.random.default_rng(0)
cw = content_words("What is the capital of the fold?")
records = ["The capital of the fold is the One"]

# trace babble_closure
for h in records:
    toks_h = tok(h)
    low = [t.lower() for t in toks_h]
    rw = [t for t in toks_h if TOK_FREQ.get(t.lower(), 0) <= TOTAL_TOKS / (GEN_B ** 10)]
    print("rw:", rw)
    
ds = [low.index(w) for w in cw if w in low]
doors = [toks_h[min(ds):min(ds) + GEN_C]]
print("doors:", doors)

for _spike in range(8):
    walk = continue_orbit(doors[0], rng, max_tokens=120, sentences=1)
    seg = dedup(" ".join(doors[0]) + " " + walk) if walk else " ".join(doors[0])
    out = " ".join(re.split(r"(?<=[.!?])\s+", seg.strip())[:1])
    print(f"Spike {_spike}: walk={walk!r} -> out={out!r}")
    out_focus = {t.lower() for t in tok(out) if TOK_FREQ.get(t.lower(), 0) <= TOTAL_TOKS / (GEN_B ** 10)}
    f = {w.lower() for w in rw}
    ok_parts = not (f and len(f & out_focus) * GEN_B < len(f))
    print(f"  out_focus={out_focus}, ok_parts={ok_parts}")
