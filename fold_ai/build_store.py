"""BOUNDED fluency store. Prose gives GENERATIVE fluency via short-context
orbits (Markov over real English) + kinship + a sentence bank. Bounded so
it loads in seconds: prose context capped at PCTX, volume capped by budget."""
import os, glob, re, pickle, sys, zlib
from collections import defaultdict, Counter
BASE = "/Users/mettamazza/Desktop/Smithian Fold Theory"
STORE = BASE + "/fold_ai/store.pkl"
PCTX = 6                      # prose orbit context length (= context depth, CTX_MAX)
BUDGET_MB = int(sys.argv[1]) if len(sys.argv) > 1 else 90   # prose bytes to ingest
# M5, Engram-grade bounding -- INSPIRATION: DeepSeek Engram (arXiv
# 2601.07372): deterministically-hashed prime-sized tables keep O(1) exact
# lookup at bounded memory, and their verified null result shows collisions
# cost nothing. FOLD FORM: exact counts per cell, cells shared under a
# deterministic crc32 hash into a prime table. OFF by default (0 = exact
# keys); switch on at flood scale with a bucket count as argv[2].
BOUND = int(sys.argv[2]) if len(sys.argv) > 2 else 1000003 # Default to O(1) Prime Bounding
def next_prime(n):
    while True:
        n += 1
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            return n
BOUND = next_prime(BOUND) if BOUND else 0
def bkey(tup):
    if BOUND:
        return (zlib.crc32(" ".join(tup).encode()) % BOUND,)
    return tup
def tok(s): return re.findall(r"\w+|[^\w\s]", s)
def _ddint(): return defaultdict(int)
def well_formed(s):
    w = s.split()
    if not (4 <= len(w) <= 40): return False
    if not s[:1].isupper() or s[-1] not in ".!?": return False
    if w[0].lower() in ("no","but","and","because","so","then","yet","or"): return False
    return sum(c.isalpha() or c.isspace() for c in s)/max(len(s),1) >= 0.9

st = {"stores":[defaultdict(_ddint) for _ in range(PCTX+1)],
      "neigh":defaultdict(_ddint), "freq":Counter(), "sents":[], "ingested":[]}
budget = BUDGET_MB * 1_000_000
used = 0
for f in sorted(glob.glob(BASE + "/fold_ai/diet/*.txt")):
    text = open(f, errors="ignore").read()
    used += len(text)
    st["ingested"].append(f)
    words = tok(text)
    st["freq"].update(w.lower() for w in words)
    for i in range(len(words)-1):
        nxt = words[i+1]
        for L in range(PCTX+1):
            if i-L+1 < 0: break
            st["stores"][L][bkey(tuple(t.lower() for t in words[i-L+1:i+1]))][nxt] += 1
    for i in range(1, len(words)-1):
        w = words[i].lower()
        if len(w) >= 3:
            st["neigh"][w][words[i-1].lower()] += 1
            st["neigh"][w][words[i+1].lower()] += 1
    for s in re.split(r"(?<=[.!?])\s+", text):
        s = " ".join(s.split())
        if 8 <= len(s) <= 300 and "|" not in s and "`" not in s and well_formed(s):
            st["sents"].append((s, "prose"))
    print(f"  {used/1e6:.0f}/{BUDGET_MB}MB, {len(st['sents'])} sentences, {len(st['neigh'])} words", flush=True)
    if used > budget:
        break

st["bound"] = BOUND
with open(STORE + ".tmp","wb") as f: pickle.dump(st, f)
os.replace(STORE + ".tmp", STORE)
open(STORE.replace("store.pkl", "store.bound"), "w").write(str(BOUND))
print(f"STORE BUILT: {os.path.getsize(STORE)/1e6:.0f}MB from {len(st['ingested'])} books", flush=True)
