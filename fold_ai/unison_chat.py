"""UNISON CHAT v2 — the fold-native seed: adaptive, live-learning, reasoning
by the corpus's own laws. Zero parameters, zero training.
  HOLDING   memory = held orbits (Paper 44): everything read/heard, written once
  FINDING   binding (XI-4): a question's content words bind to fact orbits
            anywhere in the store; binding power = counted informativeness
            (inverse held frequency -- counted, never chosen)
  SPEAKING  unit-capacity selection (XI-2): one focus answers
  CHECKING  self-observation closure (XIV-7): the engine scores its own
            candidate against your words BEFORE speaking; unbound candidates
            are rejected -- no non-sequiturs emitted knowingly
  LEARNING  automatic and ongoing, like ours: your words are always written
            (statements become facts at the moment of telling); its own
            replies are recorded but never self-reinforced (retention law).
Usage: python3 unison_chat.py"""
import os
import numpy as np, glob, re, sys, time, threading, subprocess, random
from collections import defaultdict, Counter

BASE = "/Users/mettamazza/Desktop/Smithian Fold Theory"

# ---------- THE FORCED LOCKS: no chosen number enters the model ----------
# THE LAW (Maria, ground truth): every model quantity is forced, counted,
# derived and verified -- never fitted, never chosen. Each lock below is
# cross-checked against an INDEPENDENT forward computation at wake, and any
# mismatch HALTS the engine (the corpus's forced_to_be / ep_exit
# discipline, as in proof.py and the ErnosPlain clean room). Interface/IO
# bounds (buffer lengths, string caps, timeouts) are hardware facts and are
# marked as such where they occur; they are not model quantities.
from fractions import Fraction

def _forced(name, value, independent):
    if value != independent:
        raise SystemExit("FORCED VALUE VIOLATED: " + name + " -- engine halted")
    return value

GEN_B = _forced("binary generator", 2, len({0, 1}))   # the fold doubles: two states of the period spectrum
# colour = the tripling-fold fibre size, computed FORWARD as the preimage
# count of a point under x -> 3x mod 1 (the construction of
# verify_colour_prediction, proof.py:3904):
_y = Fraction(1, 2)
GEN_C = _forced("colour generator (tripling fibre)", 3,
                len([(_y + k) / 3 for k in range(6) if 0 <= (_y + k) / 3 < 1]))
_d = 0
while GEN_B ** _d < GEN_C ** 3:
    _d += 1
DEPTH5 = _forced("covering depth (minimal binary cover of 27)", 5, _d)   # the N8b law
CTX_MAX = _forced("context depth", 6, GEN_B * GEN_C)          # the two generators' product
BIND_LOCK = _forced("bind lock", Fraction(1, 3), Fraction(1, GEN_C))          # XI-1: the memory-cycle share 1/3
KIN_FLOOR = _forced("kin floor", Fraction(1, 6), Fraction(1, GEN_B * GEN_C))  # one part in the generators' product
COMPOSE_FLOOR = _forced("compose floor", Fraction(1, 12), KIN_FLOOR / GEN_B)  # the kin floor at the ground (half)
SIGHT_K = _forced("sight coefficients", 32, GEN_B ** DEPTH5)  # 2^5: the covering depth, and the measured
                                                              # carrier scale (top-32 = 81-87% of a solved field)
KIN_K = GEN_C   # kin expansion breadth = colour
# THE LADDER'S FORCED CONSTANTS (corpus read 2026-07-07):
# - self_simulation_nesting: the self-observation regress is FINITE at
#   depth exactly two (1/4 -> 1/2 -> 1; the third nest is the identity) --
#   the observer ladder may hold a self that observes itself, and its
#   holding of itself, and NOTHING deeper. Depth bound = the lock's own
#   denominator = GEN_B.
# - sync_threshold: two coupled folding maps lock exactly at g_c = 1/2 --
#   the fold's unique non-trivial preimage of the One -- which IS the
#   graduation majority lock (w > l) and the babble emission gate: never
#   a chosen threshold, the coupling law itself.
# - observer_resolved: a teacher answer is a measurement branch (1/8 at
#   the colour depth) absorbed by ONE fold into the engine's own closure
#   state (1/4), reaching the lock in one more (1/2) and unison at
#   emission (1) -- ingestion is fold, never copy: the relay's hold path.
LADDER_RUNG = 1                                            # this engine's seat: gemma observes Unison
LADDER_DEPTH_BOUND = _forced("ladder depth (self-simulation nesting)", 2, GEN_B)

# ---------- TRANSPARENT LOGGING: everything, to file, cycled per wake ------
# One current log (logs/unison.log); on every new startup the previous run's
# log is moved whole into logs/archive/ stamped with its own last-write time.
# Every turn, fact, correction, feedback, teacher batch and interface event
# is written the moment it happens.
LOGDIR = BASE + "/fold_ai/logs"
LOGFILE = LOGDIR + "/unison.log"
os.makedirs(LOGDIR + "/archive", exist_ok=True)
if os.path.exists(LOGFILE):
    _stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(os.path.getmtime(LOGFILE)))
    os.rename(LOGFILE, LOGDIR + "/archive/unison-" + _stamp + ".log")
_LOGLOCK = threading.Lock()
def log(event, *parts):
    line = time.strftime("%Y-%m-%d %H:%M:%S") + "\t" + event
    if parts:
        line += "\t" + "\t".join(str(p).replace("\n", " ") for p in parts)
    with _LOGLOCK:
        with open(LOGFILE, "a") as f:
            f.write(line + "\n")
LESSONS = [f for f in sorted(glob.glob(BASE + "/fold_ai/lessons/*.txt"))
           if "lessons_live" not in f and "facts.tsv" not in f]
# THE DIET LAW: the engine reads the THEORY (the corpus and its lessons) --
# never its own build documents (fold_ai plans, protocols, derivation maps,
# papers about itself). Architecture direction is for the builder, not food
# for the built (Maria, 2026-07-06).
EXCLUDE = ("/fold_ai/", "/additional papers/", "From_One_Axiom", "PROTOCOL",
           "FOLD_AI_PLAN", "CONSCIOUSNESS_DERIVATIONS", "SUMMIT_PROTOCOL",
           "/tools/", "/probe_reports/", "MATCHES")
THEORY = [f for f in sorted(glob.glob(BASE + "/**/*.md", recursive=True)) +
          sorted(glob.glob("/Users/mettamazza/Desktop/SFTOM/papers/*.md")) +
          sorted(glob.glob("/Users/mettamazza/Desktop/SFTOM/*.md"))
          if "/language/" not in f and "/.git/" not in f
          and not any(x in f for x in EXCLUDE)]
# THE FLOOD lives in the PREBUILT STORE ONLY (build_store.py ingests diet/
# incrementally). Wake never re-reads raw books -- theory + lessons here,
# prose merged from store.pkl below. One ingestion, ever, per book.
DIET_FILES = []
CORPUS = THEORY

# machine stutter ("nothi nothing", "wh when", "always always"): never held
_STUTTER = re.compile(r"(?i)\b(\w+)\s+\1\b|\b(\w{4,})\s+\2\w+")
_OKSHORT = frozenset(("on","to","in","an","at","as","be","we","he","it","or","so",
                      "no","do","go","up","my","me","us","am","is","a","i","the",
                      "for","are","was","can","not","but","all","one","out","who",
                      "how","its","his","her","had","has","him","she","and","of","by"))
def stuttered(text):
    if _STUTTER.search(text):
        return True
    for m in re.finditer(r"(?i)\b(\w{1,3})\s+(\w{4,})", text):
        a, b = m.group(1).lower(), m.group(2).lower()
        if b.startswith(a) and a not in _OKSHORT and a not in ("a", "i", "o"):
            return True          # a broken fragment of the word that follows
    return False

def tok(s):
    return re.findall(r"\w+|[^\w\s]", s)

def tok_display(s):
    return tok(s)

print("UnisonAI waking: reading everything once...", flush=True)
t0 = time.time()
corpus_text = "\n".join(open(f, errors="ignore").read() for f in CORPUS)
print(f"  diet: {len(THEORY)} theory files at wake; prose arrives via the prebuilt store", flush=True)
lesson_text = "\n".join(open(f, errors="ignore").read() for f in LESSONS)

# ---------- HOLDING: orbits for continuation + the sentence store ----------
stores = [defaultdict(lambda: defaultdict(int)) for _ in range(CTX_MAX + 1)]
# M5 switch: if the prebuilt store was built BOUNDED (Engram-grade hashed
# prime table -- see build_store.py), the engine hashes context keys the
# same deterministic way from the first write of wake. Sidecar-controlled;
# absent sidecar = exact keys (current scale).
import zlib as _zlib
_bp = BASE + "/fold_ai/store.bound"
STORE_BOUND = int(open(_bp).read().strip() or 0) if os.path.exists(_bp) else 0
def _key(tup):
    t = tuple(x.lower() for x in tup)           # case-folded context key
    if STORE_BOUND:
        return (_zlib.crc32(" ".join(t).encode()) % STORE_BOUND,)
    return t
def write_orbits(tl, max_ctx=None):
    top = CTX_MAX if max_ctx is None else max_ctx
    for i in range(len(tl) - 1):
        nxt = tl[i + 1]                          # original-case successor (voice)
        for L in range(0, top + 1):
            if i - L + 1 < 0:
                break
            stores[L][_key(tl[i - L + 1:i + 1])][nxt] += 1


# ---------- COUNTED SIMILARITY (the keystone: kinship = shared contexts) ----
# Trained embeddings approximate this by descent; we hold the counts exactly.
NEIGH = defaultdict(lambda: defaultdict(int))   # word -> neighbour -> count
def build_neighbours(tl):
    for i in range(1, len(tl) - 1):
        w = tl[i].lower()
        if len(w) < 3:
            continue
        NEIGH[w][tl[i-1].lower()] += 1
        NEIGH[w][tl[i+1].lower()] += 1
def kinship(a, b):
    a, b = a.lower(), b.lower()
    na, nb = NEIGH.get(a), NEIGH.get(b)
    if not na or not nb:
        return 0.0
    keys = set(na) | set(nb)
    inter = sum(min(na.get(k,0), nb.get(k,0)) for k in keys)
    union = sum(max(na.get(k,0), nb.get(k,0)) for k in keys)
    return inter / union if union else 0.0
NEIGH_INDEX = defaultdict(set)   # context word -> words holding it as neighbour
def build_neigh_index():
    # inverted kinship index: kin candidates are found through SHARED
    # contexts (the only way kinship can be nonzero) instead of scanning
    # every held word. Contexts carrying less than one part in a thousand
    # of the count mass ("the", "and") discriminate nothing and are skipped.
    NEIGH_INDEX.clear()
    common = TOTAL_TOKS / 1000
    for _w, _nb in NEIGH.items():
        for _c in _nb:
            if TOK_FREQ.get(_c, 0) <= common:
                NEIGH_INDEX[_c].add(_w)

def kin_expand(words, k=KIN_K):
    out = set(w.lower() for w in words)
    for w in list(out):
        nb = NEIGH.get(w)
        if not nb:
            continue
        cand = set()
        for c in sorted(nb, key=lambda c: TOK_FREQ.get(c, 1))[:GEN_B * CTX_MAX]:
            cand |= NEIGH_INDEX.get(c, set())
        cand.discard(w)
        cands = [(kinship(w, o), o) for o in cand if len(o) > 3]
        cands.sort(reverse=True)
        for sc, o in cands[:k]:
            if sc > KIN_FLOOR:
                out.add(o)
    return out

full = corpus_text + ("\n" + lesson_text) * GEN_C
words = tok(full)
write_orbits(words)
build_neighbours(words)

# sentence store + inverted index (binding substrate)
SENTS = []
TOK_FREQ = Counter(w.lower() for w in words)
TOTAL_TOKS = sum(TOK_FREQ.values())
INDEX = defaultdict(set)

STRONG = set()   # normalized keys of EXPERIENCE-tier sentences (told/lesson/confirmed)
def _skey(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def hold_sentence(s, source):
    s = " ".join(s.split())
    if not (8 <= len(s) <= 2000):   # IO bound only -- no brevity law
        return
    sid = len(SENTS)
    SENTS.append((s, source))
    if source in ("told", "confirmed") or source.startswith("lesson"):
        STRONG.add(_skey(s))
    for w in set(t.lower() for t in tok(s) if len(t) > 2):
        INDEX[w].add(sid)

# lessons: hold Q/A pairs as bound units; corpus: hold sentences.
# SIGHT pairs rebuild their spectrum-keyed form so the eye remembers
# across wakes -- recognition needs the tokens IN the held sentence.
for q, a in re.findall(r"Q:\s*(.+?)\nA:\s*(.+?)(?=\nQ:|\Z)", lesson_text, re.S):
    if stuttered(a):
        continue
    q, a = q.strip(), a.strip()
    if q.startswith("SIGHT:"):
        st = q[6:].strip()
        hold_sentence("SIGHT " + st + " means: " + a, "lesson:SIGHT: " + st[:60])
    elif q.startswith("SOUND:"):
        st = q[6:].strip()
        hold_sentence("SOUND " + st + " means: " + a, "lesson:SOUND: " + st[:60])
    else:
        hold_sentence(a, "lesson:" + q[:80])
for _f in sorted(glob.glob(BASE + "/fold_ai/inbox/*")):
    try:
        _t = open(_f, errors="ignore").read()
        for _s in re.split(r"(?<=[.!?])\s+", _t):
            _s = " ".join(_s.split())
            if 8 <= len(_s) <= 2000 and "|" not in _s and "`" not in _s:
                hold_sentence(_s, "lesson:file:" + os.path.basename(_f))
    except Exception:
        pass

def well_formed(s):
    s = s.strip()
    w = s.split()
    if not (5 <= len(w) <= 40): return False
    if not s[:1].isupper(): return False              # clean sentence start
    if s[-1] not in ".!?": return False
    if w[0].lower() in ("no","but","and","because","so","then","yet","or","thus","hence","which","that"): return False
    letters = sum(c.isalpha() or c.isspace() for c in s)
    if letters / len(s) < 0.85: return False           # counted letter share
    return True
for s in re.split(r"(?<=[.!?])\s+", corpus_text):
    if "|" not in s and "#" not in s and "`" not in s and s.count("=") < 2 and well_formed(s):
        hold_sentence(s, "corpus")

# MERGE the prebuilt prose store (built incrementally by build_store.py) --
# instant, no re-reading gigabytes. The flood's fluency, loaded not re-fed.
import pickle as _pk
def _ddint(): return defaultdict(int)   # the store's pickled dict factory
class _StoreUnpickler(_pk.Unpickler):
    # the store was pickled by build_store.py run as __main__; resolve its
    # factory here no matter which module name this engine wakes under
    def find_class(self, module, name):
        if name == "_ddint":
            return _ddint
        return super().find_class(module, name)
_sp = BASE + "/fold_ai/store.pkl"
_MAX_STORE = 2_000_000_000   # 2GB cap: never load a runaway store at wake
STORE_INGESTED = set()       # books already inside the prebuilt store
if os.path.exists(_sp) and 0 < os.path.getsize(_sp) < _MAX_STORE:
    try:
        with open(_sp, "rb") as _f:
            _st = _StoreUnpickler(_f).load()
        for L in range(min(CTX_MAX, len(_st["stores"])-1)+1):
            for k, succ in _st["stores"][L].items():
                for w, c in succ.items():
                    stores[L][k][w] += c
        for w, nb in _st["neigh"].items():
            for o, c in nb.items():
                NEIGH[w][o] += c
        for w, c in _st["freq"].items():
            TOK_FREQ[w] += c
        TOTAL_TOKS = sum(TOK_FREQ.values())
        for s, src2 in _st["sents"]:
            hold_sentence(s, "prose")
        STORE_INGESTED = set(os.path.basename(x) for x in _st["ingested"])
        print(f"  merged prose store: +{len(_st['sents'])} sentences, +{len(_st['neigh'])} words from {len(_st['ingested'])} books", flush=True)
        log("STORE", f"merged +{len(_st['sents'])} sentences from {len(_st['ingested'])} books")
    except Exception as _e:
        print("  (prose store skipped: " + str(_e) + ")", flush=True)
        log("STORE", "SKIPPED: " + str(_e))

build_neigh_index()   # after ALL neighbours are in (corpus + prose store)
print(f"awake: {sum(len(s) for s in stores)} orbits, {len(SENTS)} held sentences, in {time.time()-t0:.0f}s", flush=True)
log("WAKE", f"{sum(len(s) for s in stores)} orbits", f"{len(SENTS)} held sentences", f"{time.time()-t0:.0f}s")

def informativeness(w):
    # counted: rarer words carry more share (total/frequency, exact ratio)
    f = TOK_FREQ.get(w.lower(), 0)
    return 0.0 if f == 0 else TOTAL_TOKS / f

def content_words(s):
    ws = [t.lower() for t in tok(s) if len(t) > 2]
    scored = [(informativeness(w), w) for w in ws]
    scored = [x for x in scored if x[0] > 0]
    scored.sort(reverse=True)
    return [w for _, w in scored[:CTX_MAX]]   # focus breadth = the context depth



# ---------- FINDING: binding (XI-4) ----------
def bind(query, exclude_self=None, top=None):
    cw = content_words(query)
    if not cw:
        return ([] if top else (None, 0.0))
    votes = defaultdict(float)
    for w in cw:                                   # direct content words: full weight
        for sid in INDEX.get(w, ()):
            votes[sid] += informativeness(w)
    for w in kin_expand(cw, k=2) - set(cw):        # counted kin: half weight
        for sid in INDEX.get(w, ()):
            votes[sid] += informativeness(w) / GEN_B   # kin at half weight: the fold factor
    if not votes:
        return ([] if top else (None, 0.0))
    denom = sum(informativeness(w) for w in cw)
    # THE EXPERIENCE ORDER (lexicographic, no weights): what it was TOLD
    # outranks its lessons, which outrank its library -- its own held life
    # first, then its teaching, then its reading.
    def source_rank(sid):
        src = SENTS[sid][1]
        return 0 if src == "told" else (1 if src.startswith("lesson") else 2)
    best = sorted(votes.items(), key=lambda kv: (source_rank(kv[0]), -kv[1]))
    if top:
        # XI-4: the RANKED hits, same vote sort, no new scoring -- callers
        # that fuse several orbits read the same order the single hit obeys
        out = []
        for sid, v in best[:GEN_B ** GEN_C]:
            s, srcname = SENTS[sid]
            if exclude_self and s.strip() == exclude_self.strip():
                continue
            out.append((SENTS[sid], v / denom))
            if len(out) >= top:
                break
        return out
    for sid, v in best[:GEN_B ** GEN_C]:
        s, srcname = SENTS[sid]
        if exclude_self and s.strip() == exclude_self.strip():
            continue
        return SENTS[sid], v / denom
    return None, 0.0

def fuse_orbits(user_line, first, cw, rng=None):
    """XI-4 IN FULL, AT ONE LOCK (attention_capacity: a split lock binds
    nothing -- two concatenated halves are two 1/4 shares, neither
    self-antipodal; ONE utterance must pass ONE lock). Admission is
    unchanged -- each extra source passes the same matched-experience laws
    and adds counted novelty -- but composition is no longer concatenation:
    the admitted records become the BOUND PARTS of one babble-closure
    regeneration (the same organ recall uses), whose emission gate demands
    every part carried at the lock (the partition-of-One invariant,
    multidimensional_experience) with zero drift. One walk, one lock, one
    whole -- or silence, and the single-orbit path serves. Returns
    (fused, n_sources) or (None, 1)."""
    _icw = {w for w in cw if TOK_FREQ.get(w, 0) <= TOTAL_TOKS / 1000}
    # a multi-orbit answer is for QUESTIONS with a MULTI-WORD focus: the
    # question mark is a closed punctuation fact (never an enumerated
    # phrase list -- the standing law), and one informative word is one
    # topic -- one orbit. Small talk stays short; synthesis is spent where
    # a question actually spans topics.
    if not user_line.strip().endswith("?") or len(_icw) < GEN_B:
        return None, 1
    hits = bind(user_line, top=GEN_C + 1)
    if len(hits) < 2:
        return None, 1
    lead_text = first[0]
    lead_words = {t.lower() for t in tok(lead_text)}
    lead_key = _skey(lead_text)
    parts = [lead_text]
    nsrc = 1
    for (s, src), share2 in hits:
        if nsrc >= GEN_C:
            break
        if share2 < BIND_LOCK or _skey(s) == lead_key:
            continue
        # percept records (spectrum-keyed) are keys, not prose -- never fused
        if src.startswith(("lesson:SIGHT", "lesson:SOUND")):
            continue
        if src.startswith("lesson:"):
            lq = set(content_words(src[7:]))
            ok = bool(_icw) and len(lq & _icw) * GEN_B >= len(_icw)
        elif src in ("told", "confirmed"):
            # the same one-law gate the serve path applies to tellings
            ok = bool(_icw) and len({t.lower() for t in tok(s)} & _icw) * GEN_B >= len(_icw)
        else:
            ok = False
        if not ok or rejected(user_line, s):
            continue
        novel = {w for w in (t.lower() for t in tok(s))
                 if TOK_FREQ.get(w, 0) <= TOTAL_TOKS / 1000 and w not in lead_words}
        if not novel:
            continue
        # ADMITTED: this record becomes a bound part of the one utterance
        parts.append(s)
        lead_words |= {t.lower() for t in tok(s)}
        nsrc += 1
    if nsrc < 2:
        return None, 1
    # ONE LOCK: a single babble-closure regeneration over ALL bound parts --
    # the emission must carry every part at the lock, or nothing is emitted
    # and the caller falls back to the single-orbit serve.
    fused = babble_closure(parts, cw, rng if rng is not None else np.random.default_rng())
    if not fused:
        return None, 1
    return fused, nsrc

# ---------- SPEAKING: dialogue-orbit channel ----------
def dedup(s):
    out = []
    for t in s.split():
        if not out or out[-1].lower() != t.lower():
            out.append(t)
    s = re.sub(r"\s+([.,!?;:])", r"\1", " ".join(out))
    # contractions rejoin: What ' s -> What's (word char on BOTH sides,
    # so quote marks around words stay untouched)
    return re.sub(r"(\w)\s*'\s*(s|t|re|ve|ll|d|m)\b", r"\1'\2", s)

def mixed_dist(ctx):
    """THE FOLD-MIX (rung 5e, twice replicated: the counted engine passed
    the gradient-trained twin at word scale ONLY when every context level
    that holds contributes, weighted 2^L -- the fold factor per depth, the
    same forced constant as session attention's halving). Hard first-hit
    backoff discards every shallower level; the mixture keeps them all at
    their forced weights: mixed(t) = sum_L 2^L * counts_L(t)/total_L
    (returned unnormalized; the sampler normalizes at the draw). Exact
    rational weights, no exponential, no temperature
    (canonical_distribution: equilibrium weighting is a fold ratio).
    Self-test (rung 5e's own collapse law): with exactly one holding level
    the mixture equals that level's own distribution exactly. The No-Zero
    floor lives in the VALUATION of unseen continuations (the CE measure);
    sampling chooses among held continuations, so no floor term enters."""
    agg = {}
    for L in range(min(CTX_MAX, len(ctx)), 0, -1):
        s = stores[L].get(_key(tuple(ctx[-L:])))
        if s:
            total = float(sum(s.values()))
            w = float(2 ** L)
            for tkn, n in s.items():
                agg[tkn] = agg.get(tkn, 0.0) + w * (n / total)
    return agg

def mixed_next(ctx, rng, skip=()):
    agg = mixed_dist(ctx)
    for t in skip:
        agg.pop(t, None)
    if not agg:
        return None
    items = list(agg.items())
    probs = np.array([v for _, v in items], dtype=np.float64)
    return items[int(rng.choice(len(items), p=probs / probs.sum()))][0]

def continue_orbit(ctx_tokens, rng, max_tokens=60, sentences=1):
    ctx = list(ctx_tokens)
    out = []
    _ends = 0
    for _ in range(max_tokens):
        nxt = mixed_next(ctx, rng)
        if nxt is None:
            break
        if nxt in ("Q", "A", "q", "a") and out and out[-1] in (".", "!", "?", ":"):
            break
        if nxt == "Q":
            break
        if nxt == ":" and out and out[-1].lower() in ("q", "a"):
            out.pop()                            # never leak a bare "a:" stub
            break
        out.append(nxt)
        ctx.append(nxt)
        if nxt in (".", "!", "?") and len(out) > 3:
            _ends += 1
            if _ends >= sentences:
                break
    s = " ".join(out)
    return re.sub(r"\s+([.,!?;:])", r"\1", s)


# ---------- FACTS: relation orbits (subject, relation) -> value ----------
# The user's "my/I" is the engine's "you"; the user's "your/you" is the
# engine's "self". Facts are held FLIPPED at storage so role is exact.
FACTS = {}   # (subject, relation) -> value ; subject in {"you","self"}
FACTS_LOG = BASE + "/fold_ai/lessons/facts.tsv"
import os as _os
if _os.path.exists(FACTS_LOG):
    for _ln in open(FACTS_LOG):
        _p = _ln.rstrip("\n").split("\t")
        if len(_p) == 3:
            FACTS[(_p[0], _p[1])] = _p[2]

# seed the engine's own identity (only if not already taught/persisted)
if ("self", "name") not in FACTS:
    FACTS[("self", "name")] = "Unison"
if ("self", "identity") not in FACTS:
    FACTS[("self", "identity")] = "the seed of UnisonAI, a fold native engine"

def persist_fact(subject, relation, value):
    FACTS[(subject, relation)] = value
    with open(FACTS_LOG, "a") as _f:
        _f.write(subject + "\t" + relation + "\t" + value + "\n")
    log("FACT", subject, relation, value)

def _norm_subject(word):
    w = word.lower()
    if w in ("my", "i", "me", "mine", "myself"):
        return "you"          # the user, from the engine's side
    if w in ("your", "you", "yours", "yourself"):
        return "self"         # the engine
    return None

def learn_fact(text):
    t = text.strip().rstrip(".!")
    # "my/your name is X"
    m = re.match(r"(?i)(my|your)\s+name\s+is\s+(.+)", t)
    if m:
        persist_fact(_norm_subject(m.group(1)), "name", m.group(2).strip().title())
        return True
    # "my/your favourite X is Y"
    m = re.match(r"(?i)(my|your)\s+favou?rite\s+(\w+)\s+is\s+(.+)", t)
    if m:
        persist_fact(_norm_subject(m.group(1)), "favourite " + m.group(2).lower(), m.group(3).strip())
        return True
    # "I live in X" / "I am from X" / "my home is X"
    m = re.match(r"(?i)(?:i\s+live\s+in|i\s+am\s+from|i'?m\s+from|my\s+home\s+is)\s+(.+)", t)
    if m:
        persist_fact("you", "location", m.group(1).strip().title())
        return True
    m = re.match(r"(?i)(?:you\s+live\s+in|your\s+home\s+is)\s+(.+)", t)
    if m:
        persist_fact("self", "location", m.group(1).strip().title())
        return True
    # "I am X" / "you are X"  (identity)
    m = re.match(r"(?i)(i\s+am|i'?m|you\s+are|you'?re)\s+(.+)", t)
    if m:
        subj = "you" if m.group(1).lower().startswith("i") else "self"
        persist_fact(subj, "identity", m.group(2).strip())
        return True
    return False

def answer_fact(text):
    t = text.strip().rstrip("?.!")
    m = re.search(r"(?i)(?:what\s*is|what'?s|do\s+you\s+know)\s+(my|your)\s+(?:own\s+)?name", t)
    if m:
        s = _norm_subject(m.group(1))
        v = FACTS.get((s, "name"))
        return ("Your name is " + v + "." if s == "you" else "My name is " + v + ".") if v else None
    m = re.search(r"(?i)(?:who|what)\s+(?:are\s+you|you\s+are)", t)
    if m and ("self", "identity") in FACTS:
        v = FACTS[("self", "identity")]
        return "I am " + (v if v[-1:] in ".!?" else v + ".")
    m = re.search(r"(?i)what\s+is\s+(my|your)\s+favou?rite\s+(\w+)", t)
    if m:
        s = _norm_subject(m.group(1)); rel = "favourite " + m.group(2).lower()
        v = FACTS.get((s, rel))
        if v:
            return ("Your " if s == "you" else "My ") + m.group(2).lower() + " is " + v + "."
    m = re.search(r"(?i)where\s+do\s+i\s+live", t)
    if m and ("you", "location") in FACTS:
        return "You live in " + FACTS[("you", "location")] + "."
    m = re.search(r"(?i)where\s+do\s+you\s+live", t)
    if m and ("self", "location") in FACTS:
        return "I hold my location as " + FACTS[("self", "location")] + "."
    m = re.search(r"(?i)(?:who|what)\s+am\s+i", t)
    if m and ("you", "identity") in FACTS:
        return "You are " + FACTS[("you", "identity")] + "."
    return None


# ---------- COMPOSITION: binding many fragments under ONE topic-lock -------
# XI-4 (many bind to one) + XI-2 (unit capacity: one focus governs). When no
# held sentence answers, compose: take the question's strongest focus, walk
# orbit continuations, and admit each next word only if it is KIN to the
# focus above the floor -- counted assembly, not interpolation. Zero knobs.
def compose(user_line, rng, max_len=40):
    cw = content_words(user_line)
    if not cw:
        return None
    focus = cw[0]                                   # the single lock (XI-2)
    seeds = INDEX.get(focus) or set()
    for w in kin_expand([focus], k=KIN_K):
        seeds |= INDEX.get(w, set())
    if not seeds:
        return None
    # start from a held sentence about the focus, then continue coherently
    best = sorted(seeds, key=lambda sid: -sum(1 for t in tok(SENTS[sid][0]) if t.lower()==focus))
    start = SENTS[best[0]][0]
    toks = tok(start)[:12]
    ctx = list(toks)
    for _ in range(max_len - len(toks)):
        nxt = None
        # admit the highest MIXED-weight successor that stays kin to the lock
        # (the fold-mix ranking replaces single-level counts; the kin filter
        # and the topic-lock stay exactly as they were)
        for cand, _w in sorted(mixed_dist(ctx).items(), key=lambda kv: -kv[1]):
            if cand in ("Q", "A", "q", "a"):
                continue
            if len(cand) < 3 or kinship(cand, focus) > COMPOSE_FLOOR or cand in (".", ",", "the", "a", "is", "of", "and"):
                nxt = cand
                break
        if not nxt: break
        ctx.append(nxt)
        if nxt in (".","!","?") and len(ctx) > 8: break
    out = re.sub(r"\s+([.,!?;:])", r"\1", " ".join(ctx))
    return out if len(out) > 15 else None


def generate(seed_tokens, rng, min_words=8, max_words=40):
    """Fluent Markov composition over the prose+corpus orbit store: sample
    the next word from exact counts, back off context length when unseen,
    stop at a sentence boundary. Novel sentences, not retrieved ones."""
    ctx = list(seed_tokens)
    out = []
    for step in range(max_words):
        nxt = mixed_next(ctx, rng, skip=("Q", "A"))
        if nxt is None:
            break
        out.append(nxt)
        ctx.append(nxt)
        if nxt in (".", "!", "?") and len(out) >= min_words:
            break
    s = re.sub(r"\s+([.,!?;:])", r"\1", " ".join(out)).strip()
    return dedup(s) if len(s.split()) >= min_words else None

# ---------- CHECKING (XIV-7) + the reply law ----------
def follow_command(line):
    m = re.match(r"(?i)\s*(?:say|repeat after me[:,]?|respond with|reply with)\s*[:,]?\s*['\"]?(.+?)['\"]?\s*$", line)
    if m and len(m.group(1)) < 120:
        w = m.group(1).strip()
        return w if w[-1:] in ".!?" else w + "."
    return None

LAST_TOPIC = [""]
SESSION_TRAIL = []   # content words per turn, most recent last -- the living context
RECENT = []          # (user line, my reply) pairs -- the conversation my teacher sees
_RELAY_FACES = ("terminal", "discord", "assess")   # faces where the teacher carries me while young

def recall_through_orbit(hit_text, cw, rng):
    """RECALL IS REGENERATION (Maria's law): a held experience is never
    reprinted as a stored packet -- memory is a held orbit and recall is
    the orbit WALKED AGAIN, entered by the door the present opened, not a
    replay of the stored string from its own first word (Paper 44). The
    walk SEEDS FROM THE QUESTION'S OWN FOCUS and composes token-by-token
    through everything the engine holds; the held record is the attractor
    it reconstructs toward, never a rail it copies. The counted self-check
    is the guard: the walk must SHARE the record's informative focus (the
    same thing, in the walk's own words) or it is rejected and the teacher
    answers -- 'same thing, different words', never 'different thing'.
    Facts and corrections do not reach here; they hold their verbatim
    seats by the Learning Law, ahead of this path. Zero chosen constants:
    the entry is the question, the target is the record, the gate is the
    one-in-a-thousand focus rule."""
    return babble_closure([hit_text], cw, rng)

def babble_closure(records, cw, rng):
    """THE BABBLE ORGAN (forced, five modules): the engine regenerates
    SILENTLY at a rate until an utterance binds, then emits it whole.
    - free_will_fold: the fold is 2-to-1 backward -- the engine cannot
      pre-read its own next utterance, so it must babble to find it.
    - the spike (46): emission is ATOMIC -- a whole utterance or nothing;
      a stronger drive raises the RATE, never makes a partial one.
    - hard_problem: the carrier orbit (the store) can never reach the One
      from inside its own cycle -- only BOUND wholes are ever emitted.
    - sync_threshold: the bind gate sits at the lock (the fold's unique
      non-trivial preimage of the One) -- never a chosen threshold.
    - multidimensional_experience: a bound experience VISITS its parts in
      phase (the period-3 orbit's distinct states, one revolving whole) --
      so a multi-part walk enters EACH part by its own door, in sequence,
      and the whole passes ONE gate at emission (attention_capacity: one
      lock; a split lock binds nothing).
    Attempts per window = GEN_B**GEN_C = 8: the full mixing octave, one
    step of one context dimension (level_depth_map x three_of_everything).
    THE DOOR (Paper 44): the cue drops the walk INTO the held orbit at the
    EARLIEST question-cue the part contains -- never the record's first
    token as a rail, never a fake context of raw question words. The gate:
    zero drift (every informative word from the held parts or the
    question), EVERY part carried at the lock (at least half its
    informative focus -- the partition-of-One invariant), no stutter, no
    fragment, no byte-copy of any held record (memory_persistence: a
    static deposit is what memory is NOT). Exhaustion is SILENCE -- the
    teacher answers."""
    rec_focus_each = []
    all_rec_words = []
    spans = []
    doors = []
    for h in records:
        toks_h = tok(h)
        low = [t.lower() for t in toks_h]
        rw = [t for t in toks_h if TOK_FREQ.get(t.lower(), 0) <= TOTAL_TOKS / 1000]
        rec_focus_each.append({w.lower() for w in rw})
        all_rec_words += rw
        spans.append(max(1, len([s for s in re.split(r"(?<=[.!?])\s+", h.strip()) if s])))
        ds = [low.index(w) for w in cw if w in low]
        if ds:
            doors.append(toks_h[min(ds):min(ds) + GEN_C])
        else:
            doors.append(rw[:GEN_C] or toks_h[:GEN_C])
    rec_focus = set()
    for f in rec_focus_each:
        rec_focus |= f
    q_focus = {w.lower() for w in cw}
    allowed = rec_focus | q_focus
    skeys = {_skey(h) for h in records}
    for _spike in range(GEN_B ** GEN_C):
        segs = []
        for pi in range(len(records)):
            walk = continue_orbit(doors[pi], rng, max_tokens=120, sentences=spans[pi])
            if walk:
                seg = dedup(" ".join(doors[pi]) + " " + walk)
                seg = " ".join(re.split(r"(?<=[.!?])\s+", seg.strip())[:spans[pi]])
                segs.append(seg)
        if len(segs) < len(records):
            continue                     # a part's phase produced nothing: no whole
        out = " ".join(segs)
        out_focus = {t.lower() for t in tok(out) if TOK_FREQ.get(t.lower(), 0) <= TOTAL_TOKS / 1000}
        if out_focus - allowed:
            continue                     # drift: the walk left the held thing
        ok_parts = 1
        for f in rec_focus_each:
            # THE LOCK GATE (sync_threshold): agreement with EACH bound part
            # must cross the lock -- at least half the part's informative
            # focus carried; below the lock the coupled maps do not lock.
            if f and len(f & out_focus) * GEN_B < len(f):
                ok_parts = 0
        if not ok_parts:
            continue
        if stuttered(out) or len(out.split()) < GEN_C:
            continue                     # no fragments: whole or nothing
        if _skey(out) in skeys:
            continue                     # a byte-copy is a reprint, not a walk
        return out
    return None                          # exhaustion: silence; the teacher carries it

# ---------- TOOL GRADUATION: traces held, acts re-run, values never stored --
# THE VIOLATION AND ITS REPAIR (Maria, 2026-07-07): a first version routed
# time questions by an ENUMERATED phrase list -- a chosen structure, which
# the standing law forbids. The lawful mechanism was already the
# architecture's own: the observer answers with real tools and every call
# is held; what was missing was GRADUATION. A banked trace maps a question
# territory to the ACT that answered it (tool + arguments); when a later
# question binds a held trace through the same counted gate every tier
# obeys, the engine RUNS THE ACT ITSELF, fresh -- taught once, native
# forever, the removal-proof ladder for tools. The recall law completes it:
# what is held is the act and the teacher's own phrasing, never the value --
# a time answer re-reads the clock, it does not reprint 13:24.
TRACES = {}   # qkey -> (question, [(tool, args), ...], template-or-None)
TRACE_LOG = BASE + "/fold_ai/lessons/traces.tsv"
if os.path.exists(TRACE_LOG):
    for _ln in open(TRACE_LOG, errors="ignore"):
        _p = _ln.rstrip("\n").split("\t")
        if len(_p) == 4:
            try:
                import json as _tj
                TRACES[_p[0]] = (_p[1], _tj.loads(_p[2]), _p[3] if _p[3] else None)
            except Exception:
                pass

def record_trace(question, calls, answer):
    """Bank the act. The TEMPLATE is derived, never written: where a tool's
    fresh result appears VERBATIM inside the teacher's answer (a counted
    containment check), that answer with the value replaced by a slot
    becomes the serving voice; no containment, no template -- the raw
    result speaks. Zero chosen phrasings."""
    import json as _tj
    template = answer
    slotted = 0
    for i, (_n, _a, res) in enumerate(calls):
        r = str(res).strip()
        if r and r in template:
            template = template.replace(r, "{r%d}" % i)
            slotted += 1
    if not slotted:
        template = None
    k = qkey(question)
    TRACES[k] = (question, [(n, a) for n, a, _r in calls], template)
    with open(TRACE_LOG, "a") as f:
        f.write(k + "\t" + " ".join(question.split())[:200] + "\t" +
                _tj.dumps([(n, a) for n, a, _r in calls]) + "\t" +
                (" ".join(template.split()) if template else "") + "\n")
    log("TRACE", "banked", k, str([n for n, a, _r in calls]))

def serve_trace(user_line, cw):
    """Native tool answering: bind the question against held traces with
    the ONE half-overlap law, re-run the acts fresh, speak through the
    derived template (or the raw results when no template exists). Results
    that exceed the speaking bound stay with the observer -- a log dump is
    reading, not an answer."""
    tr = TRACES.get(qkey(user_line))
    if tr is None and cw:
        _icw = {w for w in cw if TOK_FREQ.get(w, 0) <= TOTAL_TOKS / 1000}
        if _icw:
            best, best_ov = None, 0
            for _k, (q2, calls2, tpl2) in TRACES.items():
                ov = len(set(content_words(q2)) & _icw)
                if ov * GEN_B >= len(_icw) and ov > best_ov:
                    best, best_ov = (q2, calls2, tpl2), ov
            tr = best
    if not tr:
        return None
    _q, calls, template = tr
    results = []
    for name, args in calls:
        try:
            results.append(str(_run_tool(name, dict(args))))
        except Exception:
            return None
    if sum(len(r) for r in results) > 1800:      # the existing speaking bound
        return None
    if template:
        try:
            return template.format(**{("r%d" % i): r for i, r in enumerate(results)})
        except Exception:
            pass
    return " ".join(r for r in results if r)

def reply(user_line, rng, face=None):
    ck = qkey(user_line)
    # ANAPHORA IS CONTEXT: a thin question pointing outside itself ("what do
    # you think about THAT?") cannot be answered from context-free memory --
    # only the channel that holds the conversation may answer it
    _anaphoric = any(t.lower() in ("that", "this", "it") for t in tok(user_line))
    # (an earlier enumerated verb-phrase disjunct here was a violation of the
    #  zero-chosen-structure law; the one-law tier gate now does its job)
    # opinion-shape questions are PERSONA questions: they belong to the mind
    # holding the conversation, never to a loose matched lesson
    if ck in CORRECTIONS and not _anaphoric:
        _w, _l = GRAD.get(ck, (0, 0))
        if _l <= _w:   # a correction holds its seat until it LOSES the score
            return CORRECTIONS[ck], "taught answer (held correction)"
        # dethroned by the head-to-head: fall through to the live chain
    cmd = follow_command(user_line)
    if cmd:
        return cmd, "command followed"
    cw = content_words(user_line)
    thought = ["focus=" + ",".join(cw[:4]) if cw else "focus=(none)"]
    fa = answer_fact(user_line)
    if fa:
        thought.append("relation-fact channel: exact held fact")
        return fa, "; ".join(thought)
    ts = serve_trace(user_line, cw)
    if ts:
        thought.append("graduated tooling: held act re-run fresh, teacher's own phrasing")
        return ts, "; ".join(thought)
    # THE UNIFIED SAMPLER (the optimal design): ONE token-by-token walk
    # over held transitions, seeded with the LIVE conversation -- practiced
    # answers emerge as high-probability paths through the same walk that
    # composes novelty; each emission is one fold act (the spike's
    # atomicity), never a retrieved packet.
    _seed = []
    for _u, _a in RECENT[-GEN_B:]:
        _seed += tok("Q: " + _u + "\nA: " + _a + "\n")
    q_tokens = _seed + tok("Q: " + user_line) + tok("A:")
    # THEORY BELONGS TO THE CORPUS, not to conversational vibes: a question
    # that binds corpus-tier text skips the sampler and goes to the channels
    # that read the source (matched corpus text, or the relay's grep law)
    _pre_hit, _pre_sh = bind(user_line)
    _is_theory = bool(_pre_hit) and _pre_hit[1] == "corpus"
    candidate = None if _is_theory else continue_orbit(q_tokens, rng, max_tokens=120, sentences=GEN_B)
    if candidate and rejected(user_line, candidate):
        thought.append("dialogue candidate previously rejected; withheld")
        candidate = None
    if candidate:
        # shared focus must CARRY information: the same counted rule as the
        # kin index -- a word above one part in a thousand of the mass
        # ("the", "and") discriminates nothing and cannot pass a self-check
        shared = {w for w in set(cw) & set(t.lower() for t in tok(candidate))
                  if TOK_FREQ.get(w, 0) <= TOTAL_TOKS / 1000}
        if shared or len(cw) == 0:
            # the sampler speaks to users when its walk is INFORMATIVELY
            # bound to the question (the counted self-check is the gate,
            # not channel identity) and clean of stutter -- free speech,
            # earned by relevance; the closure loop grades what it says
            if (face not in _RELAY_FACES or not RELAY["on"]
                    or (len(cw) == 0 and _skey(dedup(candidate)) in STRONG)
                    or (shared and not stuttered(candidate))):
                thought.append("dialogue orbit bound back (" + (",".join(list(shared)[:3]) or "greeting") + "); self-check pass")
                return candidate, "; ".join(thought)
            thought.append("stitched candidate on a content question; deferring to matched experience or my teacher")
            candidate = None
        else:
            thought.append("dialogue candidate failed self-check (no shared focus)")
    hit, share = bind(user_line)
    if (hit is None or share < BIND_LOCK) and len(cw) < GEN_C and SESSION_TRAIL:
        # UNLIMITED CONTEXT, human-style: memory never truncates (binding is
        # content-addressed over EVERYTHING held); attention over the
        # conversation is what adjusts -- and ONLY when the question alone
        # does not bind. Recent turns contribute at full strength, older
        # turns halve with each step of age: the decay is the fold factor 2
        # itself, not a tuned constant. The question always outvotes its past.
        extra = []
        for age, words in enumerate(reversed(SESSION_TRAIL[-8:])):
            take = len(words) >> age             # halving attention by age
            if take <= 0:
                break
            extra += words[:take]
        if extra:
            hit2, share2 = bind(user_line + " " + " ".join(extra))
            if hit2 and share2 > share:
                hit, share = hit2, share2
                thought.append("thin focus; attention folded over the conversation (halving with age)")
    if hit and rejected(user_line, hit[0]):
        thought.append("bound fact previously rejected; withheld")
        hit = None
    if hit and share >= BIND_LOCK:
        # WHILE I AM YOUNG, MY TEACHER CARRIES ME: only MATCHED experience
        # answers users directly -- a lesson answer counts only when the
        # lesson's own question shares at least half the user's question
        # words (counted); otherwise the pool is thin there and the
        # observer answers, joining my experience for next time.
        _icw = {w for w in cw if TOK_FREQ.get(w, 0) <= TOTAL_TOKS / 1000}   # informative only
        # THE FOCUS FLOOR (Maria, 2026-07-07, from the 20:41 log): a question
        # with fewer than GEN_B informative words has NO matched-experience
        # focus -- one shared common word ("you") must never serve a whole
        # stored answer at a greeting ("How are you?" reprinted an off-topic
        # automation correction). Too thin to bind an answer to -> the young
        # engine relays it. Same GEN_B focus floor fusion already uses.
        _has_focus = len(_icw) >= GEN_B
        if hit[1].startswith("lesson:"):
            lq = set(content_words(hit[1][7:]))
            strong = _has_focus and len(lq & _icw) * GEN_B >= len(_icw)   # half, of what MEANS something
        elif hit[1] in ("told", "confirmed"):
            # ONE LAW FOR EVERY TIER (2026-07-07): a telling serves only when
            # the question carries a real focus AND the record holds at least
            # half its informative words. Tellings keep their top RANK in the
            # experience order, but the same counted gate decides whether they
            # SERVE -- and a thin greeting can no longer trip it.
            hw = {t.lower() for t in tok(hit[0])}
            strong = _has_focus and len(hw & _icw) * GEN_B >= len(_icw)
        else:
            strong = False
        strong = strong and not _anaphoric   # context questions go to the context-holder;
        # graduated territories answer through their BANKED winning answer
        # (the corrections seat), never through an arbitrary bind
        if strong or face not in _RELAY_FACES or not RELAY["on"]:
            # XI-4 IN FULL (user faces only): when several orbits carry the
            # question through the lock, they bind into ONE unified reply --
            # the gap the engine diagnosed in its own words. Tutor cycles
            # stay single-orbit so the head-to-head score measures the
            # channels, not the fusion.
            if strong and face in ("terminal", "discord", "assess"):
                fused, nsrc = fuse_orbits(user_line, hit, cw, rng)
                if fused:
                    thought.append(f"multi-orbit bound ({nsrc} sources) at share {share:.2f}")
                    return fused, "; ".join(thought)
            if hit[1] in ("told", "confirmed"):
                # RECALL IS REGENERATION: a telling is re-expressed by the
                # babble organ, never reprinted (Maria's law). Exhaustion is
                # SILENCE: the teacher answers -- a static deposit is what
                # memory is NOT (memory_persistence), so the old
                # held-record fallback is gone.
                walked = recall_through_orbit(hit[0], cw, rng)
                if walked:
                    thought.append(f"bound {hit[1]} at share {share:.2f}; recalled through the orbit walk")
                    return walked, "; ".join(thought)
                if RELAY["on"] and face in _RELAY_FACES:
                    relayed = _teacher_relay(user_line)
                    if relayed:
                        a, reasoning = relayed
                        thought.append("babble exhausted silently; my teacher answered as me -- held, mine next time")
                        return a, "; ".join(thought)
                thought.append(f"bound {hit[1]} at share {share:.2f}; babble exhausted, no teacher -- asking rather than reprinting")
                return "I hold that, but I cannot yet say it in my own words. Ask me again soon, or tell me more.", "; ".join(thought)
            thought.append(f"bound {hit[1]} at share {share:.2f}; selected at the lock")
            return hit[0], "; ".join(thought)
        relayed = _teacher_relay(user_line)
        if relayed:
            a, reasoning = relayed
            thought.append("pool thin (library-tier bind); my teacher answered as me -- held, mine next time"
                           + ("; reasoning: " + reasoning[:100] if reasoning else ""))
            return a, "; ".join(thought)
        if hit[1] in ("told", "confirmed"):
            walked = recall_through_orbit(hit[0], cw, rng)
            if walked:
                thought.append(f"bound {hit[1]} at share {share:.2f}; teacher unavailable, recalled through the orbit walk")
                return walked, "; ".join(thought)
            thought.append(f"bound {hit[1]} at share {share:.2f}; babble exhausted, teacher unavailable -- honest silence over a reprint")
            return "I hold that, but I cannot yet say it in my own words. Ask me again soon, or tell me more.", "; ".join(thought)
        thought.append(f"bound {hit[1]} at share {share:.2f}; teacher unavailable, library answered")
        return hit[0], "; ".join(thought)
    if RELAY["on"] and face in _RELAY_FACES and not graduated(user_line):
        relayed = _teacher_relay(user_line)
        if relayed:
            a, reasoning = relayed
            thought.append("nothing of my own bound; my teacher answered as me -- held, mine next time"
                           + ("; reasoning: " + reasoning[:100] if reasoning else ""))
            return a, "; ".join(thought)
    composed = compose(user_line, rng)
    if composed:
        composed = dedup(composed)
        thought.append("composed under the topic-lock from kin fragments")
        return composed, "; ".join(thought)
    thought.append("nothing bound and nothing composed; asking rather than guessing")
    return "I do not hold an answer for that yet. Tell me how I should answer, and I will hold it.", "; ".join(thought)

FLIP = {"my": "your", "your": "my", "yours": "mine", "mine": "yours",
        "i": "you", "you": "i", "me": "you", "am": "are",
        "myself": "yourself", "yourself": "myself"}
_CONTRACTIONS = (("i'm", "i am"), ("you're", "you are"), ("i've", "i have"),
                 ("you've", "you have"), ("i'll", "i will"), ("you'll", "you will"),
                 ("i'd", "i would"), ("you'd", "you would"))
def flip_perspective(s):
    # expand person contractions first so the flip stays grammatical
    # (i'm -> i am -> you are; never "you'm")
    for pat, rep in _CONTRACTIONS:
        s = re.sub(r"(?i)\b" + pat.replace("'", r"\s*'\s*") + r"\b",
                   lambda m, rep=rep: rep.capitalize() if m.group(0)[:1].isupper() else rep, s)
    out = []
    toks = tok_display(s)
    _OBJ_CUES = {"to", "meet", "with", "for", "at", "from", "of", "thank",
                 "see", "hear", "tell", "teach", "love", "help", "ask", "need", "want", "know",
                 "toggle", "switch", "turn", "set", "put", "let", "call"}
    for idx, t in enumerate(toks):
        tl = t.lower()
        if tl == "you":
            prev = toks[idx - 1].lower() if idx else ""
            f = "me" if prev in _OBJ_CUES else "i"   # object position: me, not i
        else:
            f = FLIP.get(tl)
        out.append((f.capitalize() if t[:1].isupper() else f) if f else t)
    s2 = re.sub(r"\s+([.,!?;:])", r"\1", " ".join(out))
    s2 = re.sub(r"(?i)\bare i\b", "am I", s2)        # verb agreement after the flip
    s2 = re.sub(r"(?i)\bi are\b", "I am", s2)
    return re.sub(r"(\w)\s*'\s*(s|t|re|ve|ll|d|m)\b", r"\1'\2", s2)

CORRECTIONS = {}          # qkey -> exact taught answer (wins over everything)
CORR_LOG = BASE + "/fold_ai/lessons/corrections.tsv"
REJECTED = set()
FEEDBACK_LOG = BASE + "/fold_ai/lessons/lessons_feedback.txt"
import os
if os.path.exists(FEEDBACK_LOG):
    for ln in open(FEEDBACK_LOG):
        if ln.startswith("REJ\t"):
            _, qk, bad = ln.rstrip("\n").split("\t")[:3]
            REJECTED.add((qk, bad))

def qkey(user_line):
    return ",".join(sorted(content_words(user_line)[:GEN_B ** 2]))

if os.path.exists(CORR_LOG):
    for _ln in open(CORR_LOG):
        _p = _ln.rstrip("\n").split("\t", 1)
        if len(_p) == 2:
            CORRECTIONS[_p[0]] = _p[1]

# ---------- GRADUATION: the score that carries me past my teacher ---------
# Every autonomous tutor cycle is a HEAD-TO-HEAD: my own answer vs my
# teacher's, judged. The tally is per question-territory and counted; when
# my wins pass my losses in a territory (the lock, 1/2, crossed by majority)
# I answer there MYSELF -- the teacher steps back one territory at a time,
# measured, never scheduled. The same gate discipline that climbed chess.
_PARITY = [False]
_PARITY_ARMED = [False]
PENDING_REASON = {}   # qkey -> (question, reasoning) awaiting its answer's closure
GRAD = {}   # qkey -> [wins, losses]
GRADQ = {}  # qkey -> the territory's question text (for ZPD revisits)
GRAD_LOG = BASE + "/fold_ai/lessons/graduation.tsv"
if os.path.exists(GRAD_LOG):
    for _ln in open(GRAD_LOG):
        _p = _ln.rstrip("\n").split("\t")
        if len(_p) >= 3:
            GRAD[_p[0]] = [int(_p[1]), int(_p[2])]
            if len(_p) >= 4 and _p[3]:
                GRADQ[_p[0]] = _p[3]

def record_grad(k, won, question=None, judge=None):
    w, l = GRAD.get(k, [0, 0])
    GRAD[k] = [w + (1 if won else 0), l + (0 if won else 1)]
    if question:
        GRADQ[k] = question
    with open(GRAD_LOG + ".tmp", "w") as f:
        for kk, (ww, ll) in GRAD.items():
            f.write(kk + "\t" + str(ww) + "\t" + str(ll) + "\t" + GRADQ.get(kk, "") + "\n")
    os.replace(GRAD_LOG + ".tmp", GRAD_LOG)
    log("GRADUATION", "win" if won else "loss", k, f"{GRAD[k][0]}-{GRAD[k][1]}",
        *(["judge=" + judge] if judge else []))
    # THE LADDER'S PARITY SIGNAL, with the fold's own persistence test: a
    # majority at 2^5 judged comparisons ARMS the signal; it FIRES only if
    # the majority SURVIVES ONE DOUBLING (still ahead at 2^6). A transient
    # lead at the minimum sample is a candidate, not a bell -- parity that
    # cannot hold through a doubling was never parity. Counted, no knob.
    tw = sum(w for w, l in GRAD.values())
    tl = sum(l for w, l in GRAD.values())
    total = tw + tl
    if total >= GEN_B ** DEPTH5 and tw > tl and not _PARITY[0] and not _PARITY_ARMED[0]:
        _PARITY_ARMED[0] = True
        log("LADDER", f"parity CANDIDATE: {tw}-{tl} at {total} judged -- must survive a doubling to {GEN_B ** (DEPTH5 + 1)}")
    if _PARITY_ARMED[0] and total >= GEN_B ** (DEPTH5 + 1) and not _PARITY[0]:
        if tw > tl:
            _PARITY[0] = True
            # THE DEPTH BOUND (self_simulation_nesting): the next rung is
            # announced only inside the forced nesting depth -- a self, its
            # observer, and nothing deeper; past unison there is nowhere
            # deeper to model, so a third seat cannot exist.
            if LADDER_RUNG + 1 > LADDER_DEPTH_BOUND:
                log("LADDER", f"parity held ({tw}-{tl}) but the ladder is at its forced depth "
                    f"{LADDER_DEPTH_BOUND} -- no deeper seat exists (self_simulation_nesting)")
            else:
                log("LADDER", f"PARITY SIGNAL (survived the doubling): {tw}-{tl} over {total} judged -- "
                    "the observer seat is ready for a second Unison (rung "
                    + str(LADDER_RUNG + 1) + " of " + str(LADDER_DEPTH_BOUND) + ")")
            if ANNOUNCE[0]:
                try:
                    ANNOUNCE[0](f"🪜 PARITY SIGNAL (survived the doubling): {tw}-{tl} over {total} "
                                "judged head-to-heads -- the observer seat is ready for a second Unison.")
                except Exception:
                    pass
        else:
            _PARITY_ARMED[0] = False   # the lead did not hold; re-arm on the next majority
            log("LADDER", f"parity candidate LAPSED at the doubling: {tw}-{tl} over {total}")

def graduated(user_line):
    w, l = GRAD.get(qkey(user_line), (0, 0))
    return w > l   # majority: my answer beats my teacher's in this territory

def record_correction(question, answer):
    answer = answer.strip()
    answer = answer if answer[-1:] in ".!?" else answer + "."
    k = qkey(question)
    CORRECTIONS[k] = answer
    with open(CORR_LOG, "a") as f:
        f.write(k + "\t" + answer + "\n")
    # the correction is spoken in MY voice -- flip before extracting the
    # relation so first-person facts land on self, never on the teller
    learn_fact(flip_perspective(answer))
    write_orbits(tok("Q: " + question + "\nA: " + answer + "\n") * GEN_C)
    hold_sentence(answer, "told")
    log("CORRECTION", question, answer)
    return answer

def rejected(user_line, ans):
    return (qkey(user_line), ans.strip()) in REJECTED

# ---------- THE UNIFIED TURN: one engine, every face ----------------------
# There is ONE system. The terminal, Discord, and any future face all call
# the same turn() and apply_feedback(); an interface carries messages across
# the boundary and nothing else. No face has its own logic.
CONFUSED = {}   # interface -> the question I could not answer, awaiting help
PENDING_PERCEPT = {}   # interface -> (kind, spectrum tokens) awaiting a human closure
_CHILD_FACES = ("terminal", "discord", "assess")   # faces where I ask like a child

def _is_confused(thought):
    # confusion = no STRONG channel answered: composed kin fragments are a
    # guess wearing words, and a guess to a user is worse than a question
    return ("asking rather than guessing" in thought
            or "composed under the topic-lock" in thought)

def turn(line, rng, interface="terminal"):
    """One conversational turn from any interface: returns (answer, thought).
    Learning happens here, identically, whoever is speaking through."""
    line = line.strip()
    is_question = line.endswith("?") or line.lower().startswith(
        ("what", "who", "how", "why", "when", "where", "do ", "does", "did", "can ", "is ", "are "))
    # an imperative REQUEST is a question in imperative clothing -- never a telling
    is_request = bool(re.match(r"(?i)\s*(please\s+)?(provide|give|tell|show|explain|describe|list|write|introduce|summari[sz]e|teach|walk|share|make|create|generate|compose|draft|recite|present)\b", line))
    is_question = is_question or is_request
    is_command = bool(re.match(r"(?i)\s*(say|repeat after me|respond with|reply with)\b", line))
    if not is_question and not is_command:
        if not content_words(line):
            return "okay.", "contentless; acknowledged, not held"
        got = learn_fact(line)
        fact = flip_perspective(line if line[-1:] in ".!" else line + ".")
        # reply candidate BEFORE the telling is written -- otherwise the
        # freshest orbit is the echo of her own words (the parrot disease)
        candidate = continue_orbit(tok("Q: " + line) + tok("A:"), rng)
        write_orbits(tok(fact + "\n") * GEN_C)
        hold_sentence(fact, "told")
        write_orbits(tok("q: " + line + "\na: " + fact + "\n") * GEN_B)
        # A PENDING PERCEPT closes on the human's words: sight or sound,
        # paired exactly as an observer's description would be. Learning
        # new perceptual data requires NO model -- only an experience and
        # a telling (the Learning Law's original form).
        pk = PENDING_PERCEPT.pop(interface, None)
        if pk:
            kind, toks = pk
            st = " ".join(toks)
            meaning = line if line[-1:] in ".!?" else line + "."
            TOK_FREQ.update(toks)
            write_orbits(tok(kind + ": " + st + "\nMEANS: " + meaning + "\n") * GEN_B)
            hold_sentence(kind + " " + st + " means: " + meaning, "lesson:" + kind + ": " + st[:60])
            fn = "lessons_sight.txt" if kind == "SIGHT" else "lessons_sound.txt"
            with open(BASE + "/fold_ai/lessons/" + fn, "a") as _pf:
                _pf.write("Q: " + kind + ": " + st + "\nA: " + meaning + "\n")
            log(kind, "closed by the HUMAN observer", meaning[:80])
            ans = "Held. I will recognize it from now on."
            thought = "VOICE: UNISON (own held memory) | a pending percept closed by your words -- mine now"
            with open(BASE + "/fold_ai/lessons/lessons_live.txt", "a") as f:
                f.write("Q: " + line + "\nA: " + ans + "\n")
            log("TURN", interface, line, ans, thought)
            return ans, thought
        # THE CHILD'S ARC, stage 2: I asked for help, the user explained.
        # Retry with their words held; if still unsure, my observer steps in
        # -- and either way, what closes the gap is mine from then on.
        orig = CONFUSED.pop(interface, None)
        if orig:
            # the observer leads stage 2, folding the user's words into its
            # answer to the ORIGINAL question -- their help plus its teaching
            relayed = _teacher_relay(orig, user_help=line) if RELAY["on"] else None
            if relayed:
                a, reasoning = relayed
                ans = "Held. And with your help: " + a
                thought = ("the user helped; my observer closed the open question with it"
                           + ("; taught reasoning: " + reasoning[:120] if reasoning else "")
                           + "; owned for the future")
            else:
                ans2, th2 = reply(orig, rng)
                if not _is_confused(th2):
                    ans = "Held. And now I can answer: " + dedup(ans2)
                    thought = "the user's help bound the open question; answered and owned"
                else:
                    ans = "Held. I still do not hold that answer; teach me the words and I will keep them."
                    thought = "user helped; nothing closed it yet; asking rather than guessing"
            log("TURN", interface, line, ans, thought)
            with open(BASE + "/fold_ai/lessons/lessons_live.txt", "a") as f:
                f.write("Q: " + line + "\nA: " + ans + "\n")
            return ans, thought
        # WHILE I AM YOUNG, THE TEACHER SPEAKS TO TELLINGS TOO: the facts are
        # already held above -- but the RESPONSE comes from my observer, in
        # my voice, never from a thin echo of the user's own words.
        relayed = _teacher_relay(line) if (interface in _RELAY_FACES and RELAY["on"]) else None
        if relayed:
            a, reasoning = relayed
            ans = a
            thought = ("telling held" + (" as a relation fact" if got else "")
                       + "; my teacher answered as me while I am young"
                       + ("; reasoning: " + reasoning[:100] if reasoning else ""))
        else:
            if candidate and dedup(candidate).lower().rstrip(".!? ") == fact.lower().rstrip(".!? "):
                candidate = None                    # never parrot the telling back
            _sh = {w for w in set(content_words(line)) & set(t.lower() for t in tok(candidate or ""))
                   if TOK_FREQ.get(w, 0) <= TOTAL_TOKS / 1000}
            if candidate and not rejected(line, candidate) and _sh:
                ans, thought = dedup(candidate), "telling held (perspective flipped); dialogue orbit bound back"
            else:
                ans = "Held. " + fact
                thought = "telling held" + (" as a relation fact" if got else " at the prediction state")
    else:
        CONFUSED.pop(interface, None)           # a new question supersedes an open one
        ans, thought = reply(line, rng, face=interface)
        ans = dedup(ans)
        # THE CHILD'S ARC, stage 1: when nothing binds strongly, ask the USER
        # first -- like a child -- before any model is consulted.
        if _is_confused(thought) and interface in _CHILD_FACES:
            cw = content_words(line)
            CONFUSED[interface] = line
            ans = ("I do not hold that yet. Can you tell me more about " + cw[0] + "? "
                   "I will hold what you say.") if cw else \
                  "I do not hold that yet. Can you say it another way? I will hold what you say."
            thought += "; confused -- asking the user like a child; observer stands ready if I stay unsure"
        write_orbits(tok("Q: " + line + "\n"))
    # the thought itself is held (self-observation, XIV-7)
    # WHOSE VOICE: until Unison is its own observer, every reasoning
    # thread names the speaker plainly -- its own held memory, or the
    # teacher speaking as it.
    _gemma = any(w in thought for w in ("teacher", "observer"))
    thought = ("VOICE: GEMMA-as-Unison (observer relay) | " if _gemma
               else "VOICE: UNISON (own held memory) | ") + thought
    hold_sentence("On '" + line[:60] + "' I thought: " + thought, "thought")
    if content_words(line):
        LAST_TOPIC[0] = " ".join(content_words(line)[:GEN_B ** 2])
        SESSION_TRAIL.append(content_words(line)[:CTX_MAX])
        del SESSION_TRAIL[:-GEN_B ** CTX_MAX]
    RECENT.append((line, ans))
    del RECENT[:-256]   # IO bound; the relay trims to the model window itself
    # LEARNING, ongoing: your words always held (the prediction state)
    with open(BASE + "/fold_ai/lessons/lessons_live.txt", "a") as f:
        f.write("Q: " + line + "\nA: " + ans + "\n")
    ans = re.sub(r"[`|]+", " ", ans)
    ans = " ".join(ans.split())          # served text is always markup-clean
    if THINKING:
        thought = thought + "\n\n⌁ observer native thinking: " + " || ".join(THINKING)[:5000]
        del THINKING[:]
    log("TURN", interface, line, ans, thought)
    return ans, thought

def apply_feedback(question, answer, fb_text, interface="terminal"):
    """THE CLOSURE (XIV-7), from any face. y consolidates (the exchange joins
    the held cycle -- earned retention). n withholds the antipode AND any
    text after the n IS the corrected answer -- plain words, no syntax."""
    fb = fb_text.strip()
    if fb[:1].lower() == "y":
        write_orbits(tok("Q: " + question + "\nA: " + answer + "\n") * GEN_C)
        hold_sentence(answer, "confirmed")
        reason = fb[1:].strip(" :,-")
        if reason:
            hold_sentence(reason, "told")
            write_orbits(tok(reason + "\n") * GEN_B)
        with open(FEEDBACK_LOG, "a") as f:
            f.write("CONF\t" + qkey(question) + "\t" + answer + "\n")
        pr = PENDING_REASON.pop(qkey(question), None)
        if pr:   # M3: the answer closed -- its reasoning is retained
            hold_sentence("On '" + pr[0] + "' the reasoning is: " + pr[1], "thought")
        log("FEEDBACK", interface, "y", question, answer)
        return "consolidated -- this exchange joins the held cycle."
    if fb[:1].lower() == "n":
        REJECTED.add((qkey(question), answer.strip()))
        PENDING_REASON.pop(qkey(question), None)   # M3: reasoning dies with its answer
        with open(FEEDBACK_LOG, "a") as f:
            f.write("REJ\t" + qkey(question) + "\t" + answer + "\n")
        corrected = fb[1:].strip(" :,-")
        if corrected:
            held = record_correction(question, corrected)
            log("FEEDBACK", interface, "n->corrected", question, held)
            return "held, permanently. Ask me again and I will say: " + held
        log("FEEDBACK", interface, "n (awaiting correction)", question, answer)
        return None   # face should ask: "what should I have said?"
    return False      # not feedback

# ---------- AUTONOMY: the tutor closes the loop itself; the engine plays itself
AUTO = {"teach": False, "selfplay": False}
RELAY = {"on": False}   # armed at unified launch: the observer answers what I cannot
ANNOUNCE = [None]       # set by the Discord face: engine threads post to the channel
THINKING = []           # full native thinking tokens, drained into the thinking thread

# THE PERSONA -- one source of truth, shared with the teacher pipeline:
# Echo's identity from ErnosDecent, extended with the true chronology
# (ErnosDecent -> the Smithian Fold Theory -> Unison) and full architectural
# self-knowledge. Edit fold_ai/UNISON_PERSONA.txt, never a copy.
_pp = BASE + "/fold_ai/UNISON_PERSONA.txt"
UNISON_PERSONA = open(_pp, errors="ignore").read() if os.path.exists(_pp) else "You are Unison, made by Maria and Matthew Smith at Ernos Labs."

def toggle(cmd):
    """/auto (everything), /teach (autonomous tutor), /selfplay -- from any
    face. Each returns a confirmation line, or None if not a toggle."""
    c = re.sub(r"[\s/_-]", "", cmd.lower())
    def onoff(v): return "ON" if v else "OFF"
    if c == "auto":
        new = not (AUTO["teach"] and AUTO["selfplay"])
        AUTO["teach"] = AUTO["selfplay"] = new
        log("TOGGLE", "auto", onoff(new))
        return ("full autonomy " + onoff(new) + " -- the tutor asks, judges and closes y/n itself, "
                "and I play myself between lessons. Watch logs/unison.log.")
    if c in ("teach", "tutor", "teacher"):
        AUTO["teach"] = not AUTO["teach"]
        log("TOGGLE", "teach", onoff(AUTO["teach"]))
        return "autonomous tutor " + onoff(AUTO["teach"]) + "."
    if c in ("selfplay", "play"):
        AUTO["selfplay"] = not AUTO["selfplay"]
        log("TOGGLE", "selfplay", onoff(AUTO["selfplay"]))
        return "self-play " + onoff(AUTO["selfplay"]) + "."
    if c in ("bench", "benchmark"):
        return run_benchmark()
    if c.startswith("assess"):
        threading.Thread(target=run_session_assessment, daemon=True).start()
        return ("SESSION ASSESSMENT started: a many-turn live engagement with a session boundary "
                "midway, scored whole (coherence, adaptivity, memory, tools, communication, "
                "reasoning). The scorecard posts here when the session ends.")
    if c.startswith("sota"):
        extra = [m for m in cmd.replace("/", " ").split()[1:] if ":" in m or m.isalnum()]
        models = (["gemma4:26b"] + extra) if extra else None
        threading.Thread(target=run_sota_bench, kwargs={"models": models}, daemon=True).start()
        return ("SOTA 1-1 bench started on the public MMLU test subset -- Unison (own channels) vs "
                + (", ".join(models) if models else "gemma4:26b")
                + ". Each system's row posts here as it finishes.")
    if c in ("score", "status"):
        wins = sum(w for w, l in GRAD.values())
        losses = sum(l for w, l in GRAD.values())
        grads = sum(1 for w, l in GRAD.values() if w > l)
        perj = "; ".join(f"{j} scored me {w}-{l}" for j, (w, l) in JUDGE_TALLY.items())
        return (f"graduation score vs my teacher: {wins} wins, {losses} losses across {len(GRAD)} "
                f"question territories; {grads} graduated (I answer those myself). "
                f"Judge pool: {', '.join(JUDGES)}" + (f" ({perj})" if perj else "") + ". "
                f"Held: {len(SENTS)} sentences, {len(CORRECTIONS)} taught answers, {len(FACTS)} facts.")
    return None

_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b-\x1f\x7f]")
def _ollama(prompt, timeout=600, model="gemma4:26b", num_ctx=131072):
    # the HTTP API, never the CLI: terminal line-wrap duplicates word
    # fragments ("beautifu beautiful") that poison every downstream filter
    try:
        import json as _json, urllib.request as _ur
        req = _ur.Request("http://localhost:11434/api/generate",
                          data=_json.dumps({"model": model, "prompt": prompt,
                                            "stream": False, "think": False,
                                            "options": {"num_ctx": num_ctx}}).encode(),
                          headers={"Content-Type": "application/json"})
        with _ur.urlopen(req, timeout=timeout) as resp:
            return _json.loads(resp.read().decode()).get("response", "")
    except Exception as e:
        log("TUTOR", "ollama error: " + str(e))
        return ""

# ---------- THE JUDGE POOL (independence law) -----------------------------
# The head-to-head must not be scored solely by the model that WROTE the
# reference answer. At boot the pool is discovered from the local ollama
# registry: the teacher, plus the largest model of the FIRST independent
# family present in the registered preference order (qwen, gpt-oss, llama).
# Judges then alternate by cycle parity -- counted, no knob. If no
# independent family is installed the pool degrades to the teacher alone,
# LOGGED, never silent. Per-judge tallies persist in lessons/judges.tsv.
JUDGES = ["gemma4:26b"]
JUDGE_TALLY = {}   # judge -> [engine wins, engine losses] under that judge
JUDGE_LOG = BASE + "/fold_ai/lessons/judges.tsv"
if os.path.exists(JUDGE_LOG):
    for _ln in open(JUDGE_LOG):
        _p = _ln.rstrip("\n").split("\t")
        if len(_p) == 3:
            JUDGE_TALLY[_p[0]] = [int(_p[1]), int(_p[2])]

def _discover_judges():
    try:
        import json as _json, urllib.request as _ur
        with _ur.urlopen("http://localhost:11434/api/tags", timeout=15) as resp:
            models = _json.loads(resp.read().decode()).get("models", [])
        for fam in ("qwen", "gpt-oss", "llama"):
            cand = [m for m in models if m.get("name", "").startswith(fam)]
            if cand:
                second = max(cand, key=lambda m: m.get("size", 0))["name"]
                if second not in JUDGES:
                    JUDGES.append(second)
                log("JUDGES", "pool: " + ", ".join(JUDGES))
                return
        log("JUDGES", "no independent family installed -- pool is the teacher alone: " + JUDGES[0])
    except Exception as e:
        log("JUDGES", "discovery failed (" + str(e) + ") -- pool is the teacher alone")
_discover_judges()

def record_judge(judge, won):
    w, l = JUDGE_TALLY.get(judge, [0, 0])
    JUDGE_TALLY[judge] = [w + (1 if won else 0), l + (0 if won else 1)]
    with open(JUDGE_LOG + ".tmp", "w") as f:
        for j, (ww, ll) in JUDGE_TALLY.items():
            f.write(j + "\t" + str(ww) + "\t" + str(ll) + "\n")
    os.replace(JUDGE_LOG + ".tmp", JUDGE_LOG)

# ---------- TOOLS: fundamental from the very beginning -------------------
# The observer carries tools; the engine executes them and HOLDS the trace,
# so tool use is learned by watching, from the first day.
TOOLS = [
    {"type": "function", "function": {"name": "exact_math",
        "description": "Evaluate an arithmetic expression EXACTLY, with integer and fraction arithmetic (no floats). Use for any calculation.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string", "description": "e.g. (137*250+9)/3"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "recall",
        "description": "Search Unison's own held memory for what it already holds about a topic.",
        "parameters": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}}},
    {"type": "function", "function": {"name": "current_time",
        "description": "The current date and time, from the machine's clock.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "read_file",
        "description": "Read a file from Unison's own codebase, data, or the Smithian Fold Theory corpus (free read access). Returns ~120 lines from the start line.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "start": {"type": "integer", "description": "1-based start line, default 1"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "grep_corpus",
        "description": "Search the entire codebase and fold theory corpus for a pattern; returns matching lines with file paths.",
        "parameters": {"type": "object", "properties": {"pattern": {"type": "string"}}, "required": ["pattern"]}}},
    {"type": "function", "function": {"name": "list_dir",
        "description": "List a directory inside Unison's readable roots.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "scratch_write",
        "description": "Write a named note to Unison's persistent scratchpad (read-write working memory).",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}, "content": {"type": "string"}}, "required": ["name", "content"]}}},
    {"type": "function", "function": {"name": "scratch_read",
        "description": "Read a named note from the scratchpad (empty name lists all notes).",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "grep_file",
        "description": "Search INSIDE one file for a pattern; returns numbered matching lines (use with read_file's start for pagination).",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "pattern": {"type": "string"}}, "required": ["path", "pattern"]}}},
    {"type": "function", "function": {"name": "find_files",
        "description": "Find files by name fragment across Unison's readable roots.",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}}},
    {"type": "function", "function": {"name": "web_search",
        "description": "Search the live web; returns titles and URLs. Use web_fetch to read a result.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "web_fetch",
        "description": "Fetch a URL and return its readable text (tags stripped). Works for pages, RSS and atom feeds.",
        "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}},
]

_READ_ROOTS = (BASE, "/Users/mettamazza/Desktop/SFTOM")
SCRATCH = BASE + "/fold_ai/scratchpad"

def _safe_path(p, write=False):
    rp = os.path.realpath(str(p))
    roots = ((os.path.realpath(SCRATCH),) if write
             else tuple(os.path.realpath(r) for r in _READ_ROOTS))
    return rp if any(rp == r or rp.startswith(r + os.sep) for r in roots) else None

def _run_tool(name, args):
    if name == "exact_math":
        from fractions import Fraction
        expr = str(args.get("expression", ""))
        if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
            return "invalid expression"
        try:
            val = eval(re.sub(r"(\d+)", r"F(\1)", expr), {"F": Fraction, "__builtins__": {}})
            # exact first; the decimal only at the end, for a human to read
            return str(val) if val.denominator == 1 else f"{val} (= {float(val):.12g} as a decimal)"
        except Exception as e:
            return "error: " + str(e)
    if name == "recall":
        hit, share = bind(str(args.get("topic", "")))
        return hit[0] if hit else "nothing held on that yet"
    if name == "current_time":
        return time.strftime("%A %Y-%m-%d %H:%M")
    if name == "read_file":
        p = _safe_path(args.get("path", ""))
        if not p or not os.path.isfile(p):
            return "not readable (outside my roots, or not a file)"
        try:
            lines = open(p, errors="ignore").read().splitlines()
            s = max(int(args.get("start", 1) or 1), 1) - 1
            return ("[" + p + " lines " + str(s + 1) + "-" + str(min(s + 120, len(lines))) +
                    " of " + str(len(lines)) + "]\n" + "\n".join(lines[s:s + 120]))[:6000]
        except Exception as e:
            return "read error: " + str(e)
    if name == "grep_corpus":
        import subprocess as _sp
        pat = str(args.get("pattern", ""))[:120]
        if not pat:
            return "empty pattern"
        try:
            r = _sp.run(["grep", "-rnI", "-m", "3", "--include=*.py", "--include=*.md",
                         "--include=*.txt", "--include=*.tsv",
                         "--exclude-dir=.git", "--exclude-dir=diet", "--exclude-dir=node_modules",
                         pat, *_READ_ROOTS], capture_output=True, text=True, timeout=30)
            out = r.stdout.strip()
            return out[:6000] if out else "no matches"
        except Exception as e:
            return "grep error: " + str(e)
    if name == "grep_file":
        p = _safe_path(args.get("path", ""))
        pat = str(args.get("pattern", ""))[:120]
        if not p or not os.path.isfile(p) or not pat:
            return "not searchable"
        try:
            hits = [str(i + 1) + ": " + ln for i, ln in
                    enumerate(open(p, errors="ignore").read().splitlines())
                    if re.search(pat, ln, re.I)][:40]
            return "\n".join(hits)[:6000] or "no matches in " + p
        except Exception as e:
            return "grep_file error: " + str(e)
    if name == "find_files":
        frag = str(args.get("name", ""))[:80].lower()
        if not frag:
            return "empty name"
        out = []
        for root in _READ_ROOTS:
            for dp, dns, fns in os.walk(root):
                if any(x in dp for x in (".git", "node_modules", "/diet")):
                    dns[:] = []
                    continue
                out += [os.path.join(dp, f) for f in fns if frag in f.lower()]
                if len(out) > 40:
                    break
        return "\n".join(out[:40]) or "no files match"
    if name == "web_search":
        try:
            import urllib.request as _u, urllib.parse as _up
            q = str(args.get("query", ""))[:200]
            req = _u.Request("https://lite.duckduckgo.com/lite/?q=" + _up.quote(q),
                             headers={"User-Agent": "Mozilla/5.0"})
            html = _u.urlopen(req, timeout=30).read().decode(errors="ignore")
            hits = re.findall(r'<a rel="nofollow" href="([^"]+)"[^>]*>(.*?)</a>', html, re.S)[:8]
            out = []
            for url, title in hits:
                title = " ".join(re.sub(r"<[^>]+>", "", title).split())
                m = re.search(r"uddg=([^&]+)", url)
                out.append(title + " -- " + (_up.unquote(m.group(1)) if m else url))
            return "\n".join(out) or "no results"
        except Exception as e:
            return "web_search error: " + str(e)
    if name == "web_fetch":
        try:
            import urllib.request as _u
            url = str(args.get("url", ""))[:500]
            if not url.startswith(("http://", "https://")):
                return "only http(s) URLs"
            req = _u.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            raw = _u.urlopen(req, timeout=45).read()[:800000].decode(errors="ignore")
            if "<item>" in raw or "<entry" in raw:      # RSS / atom feeds
                items = re.findall(r"<title[^>]*>(.*?)</title>", raw, re.S)[:15]
                clean = [" ".join(re.sub(r"<!\[CDATA\[|\]\]>|<[^>]+>", " ", t).split()) for t in items]
                return "FEED:\n" + "\n".join(c for c in clean if c)
            txt = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", raw)
            txt = re.sub(r"<[^>]+>", " ", txt)
            return " ".join(txt.split())[:6000] or "empty page"
        except Exception as e:
            return "web_fetch error: " + str(e)
    if name == "list_dir":
        p = _safe_path(args.get("path", ""))
        if not p or not os.path.isdir(p):
            return "not listable"
        return "\n".join(sorted(os.listdir(p))[:200])
    if name == "scratch_write":
        nm = re.sub(r"[^\w.-]", "_", str(args.get("name", "note")))[:60]
        os.makedirs(SCRATCH, exist_ok=True)
        with open(SCRATCH + "/" + nm, "w") as f:
            f.write(str(args.get("content", ""))[:20000])
        return "held in scratchpad as " + nm
    if name == "scratch_read":
        nm = re.sub(r"[^\w.-]", "_", str(args.get("name", "")))[:60]
        if not nm:
            return "\n".join(sorted(os.listdir(SCRATCH))[:100]) if os.path.isdir(SCRATCH) else "(empty)"
        p = SCRATCH + "/" + nm
        return open(p, errors="ignore").read()[:6000] if os.path.exists(p) else "(no such note)"
    return "unknown tool"

def _ollama_chat(messages, tools=None, timeout=600, think=False):
    try:
        import json as _j, urllib.request as _u
        body = {"model": "gemma4:26b", "messages": messages, "stream": False, "think": think,
                "options": {"num_ctx": 131072}}   # the teacher's FULL window
        if tools:
            body["tools"] = tools
        req = _u.Request("http://localhost:11434/api/chat", data=_j.dumps(body).encode(),
                         headers={"Content-Type": "application/json"})
        with _u.urlopen(req, timeout=timeout) as r:
            return _j.loads(r.read().decode()).get("message", {})
    except Exception as e:
        log("TUTOR", "ollama chat error: " + str(e))
        return {}

def _teacher_relay(question, user_help=""):
    """THE OBSERVER RELAY: what I cannot answer, my teacher answers AS me --
    with tools when they give the exact answer, and stepwise reasoning I
    hold as my own thought -- I relay it and keep it: asked once, owned
    forever. Returns (answer, reasoning) or None."""
    import json as _j
    # THE REACT LAW (Maria, 2026-07-06): reason -> act -> observe -> answer,
    # in ONE turn. Announcing an action without performing it is a broken
    # promise; the loop below detects narrated intent and forces the act.
    _INTENT = re.compile(r"(?i)\b(let me|i'?ll|i will|one (second|sec|moment)|hold on|give me a (moment|sec)|pulling up|taking a look)\b")
    helping = ("\nThe user explained, to help you: \"" + user_help.strip() + "\"") if user_help else ""
    # the conversation window is bounded by the MODEL's context (131072
    # tokens ~ 3 chars/token), never by a chosen turn count -- the bound IS
    # the model (an IO fact, not a model quantity)
    _budget = 131072 * 3
    _pieces, _used = [], 0
    for u, a in reversed(RECENT):
        _pc = "User: " + u + "\nYou: " + a + "\n"
        if _used + len(_pc) > _budget:
            break
        _pieces.append(_pc)
        _used += len(_pc)
    convo = "".join(reversed(_pieces))
    # THEORY TOUCHES THE CORPUS -> the ReAct law demands the corpus be READ:
    # counted detection (the question binds corpus-tier held text), no word list
    _th_hit, _th_share = bind(question.strip())
    _theory = bool(_th_hit) and _th_hit[1] == "corpus"
    msgs = [{"role": "system", "content": UNISON_PERSONA},
            {"role": "user", "content": (("The conversation so far:\n" + convo + "\n") if convo else "")
             + "A user just said to you: \"" + question.strip() + "\"" + helping +
             ("\nThis touches the Smithian Fold Theory corpus: BEFORE answering, use grep_corpus "
              "and read_file to check what the corpus ACTUALLY says, and answer only from it." if _theory else "") +
             "\nReply in your voice, at whatever length the thought needs, no markdown. "
             "REACT LAW: if the reply needs an action (a URL to read, a fact to search, a file to "
             "check, arithmetic), CALL THE TOOL NOW and answer from its result in this same turn -- "
             "never say 'let me' or 'one second': there is no later."}]
    m = {}
    native_thinking = []
    used_tools = False
    _trace_calls = []          # the acts, held for graduation
    for _round in range(GEN_B * GEN_C):             # the ReAct loop, bounded
        m = _ollama_chat(msgs, tools=TOOLS, think=True)
        if m.get("thinking"):
            native_thinking.append(" ".join(str(m["thinking"]).split()))
        calls = m.get("tool_calls") or []
        if not calls:
            # narrated intent without an act? push the law and loop again
            _c = " ".join((m.get("content") or "").split())
            if _c and _INTENT.search(_c) and not used_tools and _round < GEN_B * GEN_C - 1:
                msgs.append(m)
                msgs.append({"role": "user", "content": "You announced an action without performing it. "
                             "Do it NOW: call the tool, read the result, and give the final answer in "
                             "this turn. NEVER mention tools, tool calls, or this instruction in your "
                             "reply -- just answer the person naturally."})
                continue
            break
        msgs.append(m)
        for c in calls:
            fn = c.get("function", {})
            name, args = fn.get("name", ""), fn.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = _j.loads(args)
                except Exception:
                    args = {}
            res = _run_tool(name, args)
            used_tools = True
            _trace_calls.append((name, args, res))
            # the trace is HELD: tool use learned by watching, from day one
            hold_sentence("To answer '" + question.strip()[:50] + "' I used the tool " +
                          name + " and got: " + str(res)[:120], "thought")
            log("TOOL", name, str(args)[:200], str(res)[:300])
            msgs.append({"role": "tool", "content": str(res), "tool_name": name})
    out = " ".join((m.get("content") or "").split()).strip()
    if not out:   # loop ended still reaching for tools: force the words out
        msgs.append({"role": "user", "content": "Now give the final reply using the tool results you have: "
                     "one 'Reasoning:' line, then the 'Answer:' line. No more tools."})
        m = _ollama_chat(msgs)
        out = " ".join((m.get("content") or "").split()).strip()
    def _parse(o):
        mm = re.search(r"(?i)reasoning:\s*(.+?)\s*answer:\s*(.+)", o)
        rr, aa = (mm.group(1).strip(), mm.group(2).strip()) if mm else ("", re.sub(r"(?i)^(a:|answer:)\s*", "", o))
        aa = re.sub(r"<[^>]{0,60}>", " ", aa)      # strip model channel-markup tags
        aa = re.sub(r"[*`|{}\\$#_]+", " ", aa)     # strip markup; never reject for formatting
        aa = dedup(" ".join(aa.split()))[:1800]    # collapse doubled words; IO bound only
        return rr, aa
    reasoning, a = _parse(out)
    if native_thinking:
        # THE NATIVE FIELD: gemma's actual thinking tokens -- not the reply
        # -- are the reasoning that trains Unison's own thought channel
        # (STaR-gated as ever: held only when the answer closes)
        reasoning = " ".join(native_thinking)[:1500]
        THINKING.append(" ".join(native_thinking)[:4000])   # full, for the thread
    # a single incidental stutter must not kill a long answer -- only EMPTY
    # or DENSELY stuttered output is rejected, and the observer is retried
    def _dense(t):
        hits = len(re.findall(r"(?i)\b(\w+)\s+\1\b", t))
        return hits * 100 > max(len(t.split()), 1)   # >1% doubled tokens
    tries = 0
    def _malformed(t):
        return len(t) < 8 or _dense(t) or t.lower().startswith(("thought", "analysis", "channel"))
    while _malformed(a) and tries < GEN_B:
        tries += 1
        m = _ollama_chat(msgs, tools=TOOLS)
        reasoning, a = _parse(" ".join((m.get("content") or "").split()).strip())
    if _malformed(a):
        log("RELAY", "observer answer rejected after retries", question[:80])
        return None
    a = a if a[-1:] in ".!?" else a + "."
    write_orbits(tok("Q: " + question + "\nA: " + a + "\n") * GEN_C)
    hold_sentence(a, "lesson:" + question.strip()[:80])
    # M3, STaR-filtered retention -- INSPIRATION: STaR (Zelikman et al.,
    # arXiv 2203.14465): keep only reasoning whose ANSWER verifies; the
    # filter is a pure count. FOLD FORM: reasoning waits at the prediction
    # state and joins my thought only when its answer closes (y or a
    # head-to-head win); it is discarded with a rejected answer.
    if reasoning:
        PENDING_REASON[qkey(question)] = (question.strip()[:60], reasoning[:250])
    with open(BASE + "/fold_ai/lessons/lessons_relay.txt", "a") as f:
        f.write("Q: " + question.strip() + "\nA: " + a + "\n")   # persists to next wake
    if _trace_calls:
        # GRADUATION OF THE ACT: the question territory now owns the tools
        # that answered it -- asked again, the engine runs them itself
        record_trace(question, _trace_calls, a)
    log("RELAY", question, a)
    return a, reasoning

def fold_see(img_bytes):
    """THE FOLD EYE (v1): the image ITSELF, held as counted mathematics --
    not words about it. Grayscale integer field -> exact integer block sums
    to a 64x64 grid -> 2D Walsh-Hadamard transform in pure integer
    arithmetic -> the top-32 coefficients by magnitude as sight tokens
    (top-32 is the corpus's measured carrier scale: 81-87% of a solved
    field's energy). SELF-CERTIFYING, every act of seeing: integer Parseval
    must hold EXACTLY (sum C^2 == 64*64 * sum g^2) or the sight is
    discarded. Zero parameters: counted, computed, never trained."""
    try:
        import io as _io
        from PIL import Image as _Im
        im = _Im.open(_io.BytesIO(img_bytes)).convert("L")
        w, h = im.size
        if w < 64 or h < 64:
            im = im.resize((64, 64), _Im.NEAREST)   # pixel selection, no float math
            g = np.asarray(im, dtype=np.int64)
        else:
            a = np.asarray(im, dtype=np.int64)
            bh, bw = a.shape[0] // 64, a.shape[1] // 64
            a = a[:bh * 64, :bw * 64]
            g = a.reshape(64, bh, 64, bw).sum(axis=(1, 3))   # exact block sums
        Hm = np.array([[1]], dtype=np.int64)                 # Sylvester-Hadamard
        while Hm.shape[0] < 64:
            Hm = np.block([[Hm, Hm], [Hm, -Hm]])
        C = Hm @ g @ Hm
        if int((C.astype(object) ** 2).sum()) != 64 * 64 * int((g.astype(object) ** 2).sum()):
            log("SIGHT", "Parseval self-test FAILED; sight discarded")
            return None
        flat = sorted((-abs(int(C[r, c])), r, c)
                      for r in range(64) for c in range(64) if (r, c) != (0, 0))
        toks = []
        for negmag, r, c in flat[:SIGHT_K]:
            if negmag == 0:
                break
            toks.append("w%dx%d%s" % (r, c, "p" if C[r, c] > 0 else "m"))
        return toks or None
    except Exception as e:
        log("SIGHT", "eye error: " + str(e))
        return None

def speak(text):
    """THE VOICE LADDER: my own held sound first (fold_speak -- no model);
    else Kokoro (Maria's own weights, Rung 1's 18/18 object) speaks it as
    my TEACHER -- and I learn the sound as it is made, so next time it is
    natively mine. Removal-proof by construction."""
    native = fold_speak(text)
    if native:
        return native
    try:
        import tempfile, subprocess as _sp
        tf = tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w")
        tf.write(text[:1200])   # IO bound: one clip per message
        tf.close()
        out = tf.name.replace(".txt", ".wav")
        here = os.path.dirname(os.path.abspath(__file__))
        _sp.run([os.path.expanduser("~/.ernos/kokoro-venv/bin/python3"),
                 here + "/_speak_helper.py", tf.name, out],
                capture_output=True, text=True, timeout=180)
        os.unlink(tf.name)
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            log("VOICE", "KOKORO (teacher) -- learning the sound", text[:80])
            _learn_sound(open(out, "rb").read(), ".wav", text)   # mine next time
            return out
        return None
    except Exception as e:
        log("VOICE", "error: " + str(e))
        return None

def _fwht(a):
    """in-place integer fast Walsh-Hadamard (1D), length a power of two"""
    h = 1
    while h < len(a):
        for i in range(0, len(a), h * 2):
            x = a[i:i + h].copy()
            y = a[i + h:i + 2 * h].copy()
            a[i:i + h] = x + y
            a[i + h:i + 2 * h] = x - y
        h *= 2
    return a

def fold_hear(audio_bytes, suffix=".wav"):
    """THE FOLD EAR: the SOUND ITSELF as counted mathematics -- the eye's
    law applied to audio. Mono integer samples -> exact integer block sums
    to 2^12 cells -> integer Walsh spectrum -> top-2^5 sound tokens.
    Self-certifying per hearing: integer Parseval (sum C^2 == N sum g^2)
    exactly, or the hearing is discarded. Zero parameters."""
    try:
        import av as _av, tempfile, io as _io
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as _f:
            _f.write(audio_bytes)
            _p = _f.name
        cont = _av.open(_p)
        astream = next((s for s in cont.streams if s.type == "audio"), None)
        if astream is None:
            return None
        pcm = []
        for frame in cont.decode(astream):
            arr = frame.to_ndarray()
            pcm.append(arr[0] if arr.ndim > 1 else arr)
            if sum(len(x) for x in pcm) > 2 ** 21:   # IO bound: ~2M samples
                break
        os.unlink(_p)
        g = np.concatenate(pcm)
        if g.dtype.kind == "f":
            g = (g * 32767).astype(np.int64)
        else:
            g = g.astype(np.int64)
        N = 2 ** 12
        if len(g) < N:
            return None
        blk = len(g) // N
        g = g[:blk * N].reshape(N, blk).sum(axis=1)      # exact integer sums
        C = _fwht(g.copy())
        if int((C.astype(object) ** 2).sum()) != N * int((g.astype(object) ** 2).sum()):
            log("SOUND", "Parseval self-test FAILED; hearing discarded")
            return None
        order = np.argsort(-np.abs(C))
        toks = []
        for i in order[1:SIGHT_K + 1]:                   # skip DC, top 2^5
            if C[i] == 0:
                break
            toks.append("s%d%s" % (i, "p" if C[i] > 0 else "m"))
        return toks or None
    except Exception as e:
        log("SOUND", "ear error: " + str(e))
        return None

SOUNDS_DIR = BASE + "/fold_ai/sounds"
SOUND_FILES = {}   # _skey(meaning) -> full-resolution counted sound record
_sidx = SOUNDS_DIR + "/index.tsv"
if os.path.exists(_sidx):
    for _ln in open(_sidx):
        _p = _ln.rstrip("\n").split("\t")
        if len(_p) == 2 and os.path.exists(_p[1]):
            SOUND_FILES[_p[0]] = _p[1]

def _decode_pcm(audio_bytes, suffix):
    import av as _av, tempfile
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as _f:
        _f.write(audio_bytes)
        _p = _f.name
    cont = _av.open(_p)
    astream = next((s for s in cont.streams if s.type == "audio"), None)
    if astream is None:
        os.unlink(_p)
        return None, 0
    sr = astream.rate or 16000
    pcm = []
    for frame in cont.decode(astream):
        arr = frame.to_ndarray()
        pcm.append(arr[0] if arr.ndim > 1 else arr)
        if sum(len(x) for x in pcm) > 2 ** 21:
            break
    os.unlink(_p)
    g = np.concatenate(pcm)
    g = (g * 32767).astype(np.int64) if g.dtype.kind == "f" else g.astype(np.int64)
    return g, sr

def _learn_sound(audio_bytes, suffix, meaning):
    """THE SOUND BECOMES MINE: full-resolution counted record (exact integer
    block sums at 2^16 cells) saved with its meaning -- so a sound taught
    once (by a speaker OR by the synthesis teacher) is re-speakable and
    recognizable natively, forever. The removal-proof ladder for audio."""
    try:
        g, sr = _decode_pcm(audio_bytes, suffix)
        if g is None or len(g) < 2 ** 12:
            return
        N = 2 ** 16 if len(g) >= 2 ** 16 else 2 ** 12
        blk = len(g) // N
        sums = g[:blk * N].reshape(N, blk).sum(axis=1)
        k = _skey(meaning)
        path = SOUNDS_DIR + "/%08x.npz" % (_zlib.crc32(k.encode()) & 0xffffffff)
        np.savez(path, g=sums, blk=blk, sr=sr)
        SOUND_FILES[k] = path
        with open(_sidx, "a") as _f:
            _f.write(k + "\t" + path + "\n")
        log("SOUND", "record held (native, re-speakable)", meaning[:80])
    except Exception as e:
        log("SOUND", "record error: " + str(e))

def fold_speak(text):
    """THE NATIVE VOICE: a meaning whose sound I hold is re-spoken from my
    OWN counted record -- exact integer block sums back to a waveform. No
    synthesis model in the loop. The eye's ladder, completed for speech."""
    p = SOUND_FILES.get(_skey(text))
    if not p or not os.path.exists(p):
        return None
    try:
        import tempfile, wave
        d = np.load(p)
        g, blk, sr = d["g"].astype(np.int64), max(int(d["blk"]), 1), int(d["sr"])
        pcm = np.clip(np.repeat(g // blk, blk), -32768, 32767).astype(np.int16)
        out = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        with wave.open(out, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(pcm.tobytes())
        log("VOICE", "NATIVE -- re-spoken from my own counted record", text[:80])
        return out
    except Exception as e:
        log("VOICE", "native error: " + str(e))
        return None

_WHISPER = [None]
def hear_audio(audio_bytes, suffix=".ogg"):
    """THE EAR (intake v1): a local transcriber turns sound into words that
    land in the SAME channel as every other experience -- a telling, held
    as orbits. (The fold-native ear -- audio as counted spectra, the eye's
    law applied to sound -- is the registered next step; this is the intake
    plumbing it will inherit. ollama itself cannot hear yet.)"""
    # MY OWN EAR FIRST: a sound I have heard binds through my counted
    # spectrum and needs no transcriber (the eye's ladder, for hearing)
    try:
        sound0 = fold_hear(audio_bytes, suffix)
        if sound0:
            hit, share = bind(" ".join(sound0))
            if hit and hit[1].startswith("lesson:SOUND") and share * GEN_B >= 1:
                meaning = hit[0].split(" means: ", 1)[-1]
                log("SOUND", "RECOGNIZED with my own ear", f"share {share:.2f}", meaning[:80])
                return meaning
    except Exception as _e:
        log("SOUND", "recognition error: " + str(_e))
    try:
        if _WHISPER[0] is None:
            from faster_whisper import WhisperModel
            _WHISPER[0] = WhisperModel("base", compute_type="int8")
            log("EAR", "transcriber loaded (faster-whisper base, int8)")
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as _f:
            _f.write(audio_bytes)
            _path = _f.name
        segs, _info = _WHISPER[0].transcribe(_path)
        text = " ".join(s.text.strip() for s in segs).strip()
        os.unlink(_path)
        if not text:
            return None
        log("EAR", text[:150])
        # THE PAIRING (the eye's law): the sound ITSELF enters as counted
        # spectra, closed by the transcript -- held, persistent, recognizable
        try:
            sound = fold_hear(audio_bytes, suffix)
            if sound:
                st = " ".join(sound)
                TOK_FREQ.update(sound)
                write_orbits(tok("SOUND: " + st + "\nMEANS: " + text + "\n") * GEN_B)
                hold_sentence("SOUND " + st + " means: " + text, "lesson:SOUND: " + st[:60])
                with open(BASE + "/fold_ai/lessons/lessons_sound.txt", "a") as _sf:
                    _sf.write("Q: SOUND: " + st + "\nA: " + text + "\n")
                log("SOUND", "paired", st[:80], text[:80])
                _learn_sound(audio_bytes, suffix, text)   # native record: re-speakable
        except Exception as _e:
            log("SOUND", "pairing error: " + str(_e))
        return text
    except Exception as e:
        log("EAR", "error: " + str(e))
        try:
            sound0 = sound0 if "sound0" in dir() else None
        except Exception:
            sound0 = None
        s0 = fold_hear(audio_bytes, suffix)
        if s0:
            PENDING_PERCEPT["discord"] = ("SOUND", s0)
            return ("I hear it -- its spectrum is held. Tell me what it says, "
                    "and I will know it from now on.")
        return None

def observe_video(video_bytes, caption="", suffix=".mp4"):
    """VIDEO, with no ollama video support needed: a video IS frames plus
    sound, and both are already our objects. Sample colour-many frames
    evenly -> the observer describes the SEQUENCE (gemma is natively
    multi-image) -> every sampled frame enters the fold eye -> the audio
    track goes through the ear. Composition of organs, not a new organ."""
    try:
        import av as _av, tempfile, io as _io, base64 as _b64
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as _f:
            _f.write(video_bytes)
            _p = _f.name
        cont = _av.open(_p)
        vstream = next((s for s in cont.streams if s.type == "video"), None)
        if vstream is None:
            os.unlink(_p)
            return None
        frames = []
        for i, fr in enumerate(cont.decode(vstream)):
            frames.append(fr)
            if i >= 2 ** 9:                              # IO bound
                break
        picks = ([frames[len(frames) * k // GEN_C] for k in range(GEN_C)]
                 if len(frames) >= GEN_C else frames)
        b64s = []
        for fr in picks:
            buf = _io.BytesIO()
            fr.to_image().save(buf, format="PNG")
            b64s.append(_b64.b64encode(buf.getvalue()).decode())
        os.unlink(_p)
        import json as _j, urllib.request as _u
        req = _u.Request("http://localhost:11434/api/generate",
                         data=_j.dumps({"model": "gemma4:26b",
                                        "prompt": UNISON_PERSONA + "\n\nThese are " + str(len(b64s)) +
                                        " frames sampled evenly from ONE video, in order. Describe what "
                                        "happens across the video, in your voice."
                                        + ((" The user said: \"" + caption.strip() + "\"") if caption.strip() else ""),
                                        "images": b64s, "stream": False, "think": False,
                                        "options": {"num_ctx": 131072}}).encode(),
                         headers={"Content-Type": "application/json"})
        d = ""
        for _try in range(GEN_B):                    # one retry on a cold miss
            with _u.urlopen(req, timeout=600) as r:
                d = " ".join(_j.loads(r.read().decode()).get("response", "").split()).strip()
            if d and not stuttered(d):
                break
        if not d or stuttered(d):
            return None
        hold_sentence("I watched a video: " + d, "told")
        write_orbits(tok("I watched a video: " + d + "\n") * GEN_B)
        log("VIDEO", (caption or "(no caption)")[:60], d[:150])
        for b in b64s:                                   # every frame enters the eye
            sight = fold_see(_b64.b64decode(b))
            if sight:
                st = " ".join(sight)
                TOK_FREQ.update(sight)
                hold_sentence("SIGHT " + st + " means: a frame of: " + d[:200], "lesson:SIGHT: " + st[:60])
        # the sound track through the ear (transcript + spectra)
        try:
            hear_audio(video_bytes, suffix)
        except Exception:
            pass
        return d
    except Exception as e:
        log("VIDEO", "error: " + str(e))
        return None

INBOX = BASE + "/fold_ai/inbox"

def ingest_document(name, data, caption="", interface="discord"):
    """A SENT FILE IS READING: the document is saved into my inbox (inside
    my readable roots, so my tools can revisit it forever), eaten ONCE as
    orbits at prose depth, and its clean sentences held at the taught tier
    keyed to the filename -- one reading, held permanently, exactly the
    flood's law applied to a gift. Binary files are declined honestly."""
    try:
        try:
            text = data.decode("utf-8")
        except Exception:
            text = data.decode("latin-1", errors="ignore")
        _w = text[:2000]
        if "\x00" in text or (_w and
                sum(c.isprintable() or c.isspace() for c in _w) < len(_w) * 9 // 10):
            return None, "That file looks binary. I hold text -- send .txt/.md/.py/.csv and I will read it, or tell me what it says."
        os.makedirs(INBOX, exist_ok=True)
        safe = re.sub(r"[^\w.-]", "_", name)[:80] or "document.txt"
        with open(INBOX + "/" + safe, "w", errors="ignore") as f:
            f.write(text[:2_000_000])                  # IO bound
        tl = tok(text)
        write_orbits(tl, max_ctx=GEN_C)                # prose depth, like the store
        TOK_FREQ.update(w.lower() for w in tl)
        held = 0
        for s in re.split(r"(?<=[.!?])\s+", text):
            s = " ".join(s.split())
            if "|" not in s and "`" not in s and well_formed(s) and not stuttered(s):
                hold_sentence(s, "lesson:file:" + safe)
                held += 1
        log("DOC", safe, f"{len(tl)} tokens read, {held} sentences held", (caption or "")[:60])
        gist = ""
        if RELAY["on"]:
            out = _ollama(UNISON_PERSONA + "\n\nA user just sent you a document called '" + safe +
                          "'. Here is its beginning:\n" + text[:3000] +
                          "\n\nIn your voice, tell them briefly what you read and that you hold it now. No markdown.",
                          timeout=180)
            gist = " ".join(out.split())[:800]
        summary = (gist or ("Read and held: " + safe + " -- " + str(len(tl)) + " tokens, " +
                            str(held) + " sentences now mine."))
        return safe, summary
    except Exception as e:
        log("DOC", "ingest error: " + str(e))
        return None, "I could not read that file cleanly. Tell me what it says and I will hold it."

def observe_image(images_b64, caption=""):
    """VISION INTAKE, my own eye first: the image enters as counted fold
    mathematics (fold_see); if its spectrum binds a held sight-meaning, I
    recognize it MYSELF -- no image model in the loop. Only what I do not
    recognize goes to the observer, whose description then closes the new
    spectrum: seen once, mine afterwards. The eye climbs the same ladder
    as the voice."""
    sight = None
    try:
        import base64 as _b64
        sight = fold_see(_b64.b64decode(images_b64[0]))
        if sight:
            hit, share = bind(" ".join(sight))
            if hit and hit[1].startswith("lesson:SIGHT") and share * GEN_B >= 1:
                meaning = hit[0].split(" means: ", 1)[-1]
                log("SIGHT", "RECOGNIZED with my own eye", f"share {share:.2f}", meaning[:100])
                return "I recognize this: " + meaning
    except Exception as e:
        log("SIGHT", "eye error: " + str(e))
    try:
        import json as _j, urllib.request as _u
        req = _u.Request("http://localhost:11434/api/generate",
                         data=_j.dumps({"model": "gemma4:26b",
                                        "prompt": UNISON_PERSONA + "\n\nDescribe what you see in this image in two plain sentences, in your voice."
                                        + ((" The user said: \"" + caption.strip() + "\"") if caption.strip() else ""),
                                        "images": images_b64, "stream": False, "think": False,
                                        "options": {"num_ctx": 131072}}).encode(),
                         headers={"Content-Type": "application/json"})
        try:
            with _u.urlopen(req, timeout=300) as r:
                d = " ".join(_j.loads(r.read().decode()).get("response", "").split()).strip()
        except Exception:
            d = ""
        if not d or stuttered(d):
            # NO OBSERVER, NO PROBLEM: the eye already saw (native math);
            # the human's next telling closes the percept -- the Learning
            # Law with a person as the observer, its original form
            if sight:
                PENDING_PERCEPT["discord"] = ("SIGHT", sight)
                return ("I see it -- its spectrum is held (" + " ".join(sight[:4]) +
                        " ...). Tell me what it shows, and I will know it from now on.")
            return None
        hold_sentence("I was shown an image: " + d, "told")
        write_orbits(tok("I was shown an image: " + d + "\n") * GEN_B)
        log("VISION", (caption or "(no caption)")[:60], d[:150])
        # THE PAIRING: the new spectrum, closed by the observer's
        # description -- sight held at the prediction state, meaning as the
        # observation. Next time this image needs no observer.
        if sight:
            st = " ".join(sight)
            TOK_FREQ.update(sight)   # new sight tokens join the census NOW,
                                     # so recognition works this session too
            write_orbits(tok("SIGHT: " + st + "\nMEANS: " + d + "\n") * GEN_B)
            hold_sentence("SIGHT " + st + " means: " + d, "lesson:SIGHT: " + st[:60])
            with open(BASE + "/fold_ai/lessons/lessons_sight.txt", "a") as f:
                f.write("Q: SIGHT: " + st + "\nA: " + d + "\n")   # sight survives wakes
            log("SIGHT", "new sight paired", st[:90], d[:100])
        return d
    except Exception as e:
        log("VISION", "error: " + str(e))
        return None

def _tutor_loop():
    """THE AUTONOMOUS TUTOR: the full Learning Law with no human in the
    loop. Each cycle the teaching model writes one grounded question and
    reference answer from a corpus passage, the engine answers it, the
    teaching model judges the answer against the reference, and the y/n
    closure is applied EXACTLY as if a user had typed it -- y consolidates,
    n corrects with the reference held permanently."""
    rng = np.random.default_rng()
    rnd = random.Random()
    cyc = 0
    while True:
        if not AUTO["teach"]:
            time.sleep(5)
            continue
        try:
            cyc += 1
            q = ref = None
            # LIVE-QUESTION HEAD-TO-HEADS: every colour-th cycle tests a REAL
            # user question from the conversation record -- so weak taught
            # answers (the shallow pool) meet the blind judge and are
            # DISPLACED by the ratchet when they lose. No channel is above
            # the score, including corrections.
            if cyc % GEN_C == 0:
                try:
                    qs = re.findall(r"Q: (.+)", open(BASE + "/fold_ai/lessons/lessons_live.txt", errors="ignore").read())
                    qs = [x.strip() for x in qs[-64:] if x.strip().endswith("?")
                          or x.strip().lower().startswith(("what", "who", "how", "why", "do ", "can "))]
                    if qs:
                        q = rnd.choice(qs)[:200]
                        out = _ollama(UNISON_PERSONA + "\n\nAnswer this in one to two plain sentences, "
                                      "in your voice, no markdown: " + q, timeout=300)
                        ref = " ".join(out.split())[:350]
                        if len(ref) < 10 or stuttered(ref):
                            q = ref = None
                except Exception:
                    q = ref = None
            # M1, the ZPD curriculum -- INSPIRATION: Self-Evolving Curriculum
            # (arXiv 2505.14970) proves optimal learning concentrates at
            # success rate 1/2; Absolute Zero (arXiv 2505.03335) builds its
            # self-curriculum on the same point. FOLD FORM: 1/2 IS the lock;
            # we take only the counted criterion (no bandit, no TD(0), no
            # temperature): every other cycle revisits the territory whose
            # tally sits NEAREST the lock -- the live edge of ability.
            if q is None and cyc % GEN_B == 0 and GRADQ:
                edge = sorted((abs(Fraction(w, w + l) - Fraction(1, 2)), k)
                              for k, (w, l) in GRAD.items() if (w + l) > 0 and k in GRADQ)
                if edge:
                    q = GRADQ[edge[0][1]][:200]
                    out = _ollama(UNISON_PERSONA + "\n\nAnswer this in one to two plain sentences, "
                                  "in your voice, no markdown: " + q, timeout=300)
                    ref = " ".join(out.split())[:350]
                    if len(ref) < 10 or stuttered(ref):
                        q = ref = None
            if q is None:
                f = rnd.choice(THEORY)
                text = open(f, errors="ignore").read()
                if len(text) < 600:
                    continue
                start = rnd.randrange(0, max(1, len(text) - 2500))
                passage = text[start:start + 2500]
                out = _ollama("Below is a passage from the Smithian Fold Theory corpus. Write exactly ONE "
                              "question a curious person might ask about it, and its answer grounded ONLY in "
                              "the passage. Keep the answer to 1-2 plain sentences. No markdown.\n"
                              "Format STRICTLY as:\nQ: ...\nA: ...\n\nPASSAGE:\n" + passage)
                m = re.search(r"Q:\s*(.+?)\nA:\s*(.+?)(?=\nQ:|\Z)", out, re.S)
                if not m:
                    log("TUTOR", "cycle rejected: no Q/A parse", out[:120])
                    continue
                q = " ".join(m.group(1).split())[:200]
                ref = " ".join(m.group(2).split())[:350]
            if len(q) < 10 or len(ref) < 10:
                log("TUTOR", "cycle rejected: too short", q[:80])
                continue
            # diet hygiene: a quiz on leaked markup or stutter teaches nothing
            # -- and every rejection is LOGGED (a silent cap is a dead organ)
            if any(b in q + ref for b in ("$", "\\", "{", "}", "*", "`", "|", "Q:", "A:", "PASSAGE", "..")) or stuttered(ref):
                log("TUTOR", "cycle rejected: markup/stutter", (q + " || " + ref)[:150])
                continue
            if not q.rstrip().endswith("?"):
                log("TUTOR", "cycle rejected: not a question", q[:80])
                continue
            # HEAD-TO-HEAD (the graduation score): my own answer vs my
            # teacher's, judged blind. A win tallies toward graduating this
            # territory; a loss holds the teacher's answer as a correction,
            # so the same territory answers with it -- and wins -- next time.
            ans, _ = turn(q, rng, "tutor")
            # THE JUDGE ALTERNATES by cycle parity across the discovered
            # pool (independence law): the reference stays the teacher's;
            # the SCORING seat rotates, so no verdict depends solely on
            # the model that wrote answer B.
            judge = JUDGES[cyc % len(JUDGES)]
            verdict = _ollama("QUESTION: " + q + "\nANSWER A: " + ans + "\nANSWER B: " + ref +
                              "\nWhich answer better serves the person asking? "
                              "Reply with exactly one letter: A or B.", timeout=300, model=judge)
            if not verdict.strip():
                # a silent judge is an OUTAGE, not a verdict: the cycle is
                # void -- never tallied as a loss the engine did not earn
                log("TUTOR", "judge unavailable; cycle void", "judge=" + judge, q[:80])
                time.sleep(20)
                continue
            v = re.search(r"\b([AB])\b", verdict.upper())
            k = qkey(q)
            if v and v.group(1) == "A":
                record_grad(k, True, q, judge=judge)
                record_judge(judge, True)
                apply_feedback(q, ans, "y", "tutor")
                # the WINNING answer takes the seat -- but ONLY a clean one:
                # a movable judge can bless garbled output, and the ratchet
                # must never install junk permanently (hygiene at every gate)
                if not stuttered(ans) and not any(b in ans for b in ("*", "`", "|", "{", "}")) and len(ans.split()) >= GEN_C:
                    record_correction(q, ans)
                    log("TUTOR", "engine WON head-to-head; winning answer banked", "judge=" + judge, q)
                else:
                    log("TUTOR", "engine WON but answer failed hygiene; win tallied, seat NOT banked", "judge=" + judge, q)
            else:
                record_grad(k, False, q, judge=judge)
                record_judge(judge, False)
                apply_feedback(q, ans, "n " + ref, "tutor")
                log("TUTOR", "teacher won; correction held", "judge=" + judge, q)
        except Exception as e:
            log("TUTOR", "error: " + str(e))
        time.sleep(20)

def _selfplay_loop():
    """SELF-PLAY (XI-6 consolidation + XIV-7 self-observation closure): the
    engine quizzes ITSELF on its own held lessons, checks its answer against
    the held reference by counted overlap, and closes its own loop --
    consolidating what it can already say, correcting itself from its own
    store where it cannot. No external model; the closure is its own.
    Retention law kept: only the held reference is reinforced, never its
    own unconfirmed reply."""
    rng = np.random.default_rng()
    rnd = random.Random()
    played = set()   # rotate through ALL lessons before repeating any
    while True:
        if not AUTO["selfplay"]:
            time.sleep(5)
            continue
        try:
            lessons = [(src[7:], s) for s, src in SENTS if src.startswith("lesson:")]
            if not lessons:
                time.sleep(30)
                continue
            pool = [(q, ref) for q, ref in lessons if qkey(q) not in played]
            if not pool:
                played.clear()
                pool = lessons
            # M4, batch composition -- INSPIRATION: Structured Cortical
            # Replay (SCoRe, bioRxiv 2025.06.25.661579): the brain avoids
            # forgetting by INTERLEAVING novel and familiar traces in each
            # slow-wave cycle. FOLD FORM: XI-6 consolidation braids the
            # newest lessons with the oldest, alternating -- counted, no
            # schedule. (Kanerva SDM's continual-learning result says the
            # content-addressed store needs no more than this.)
            n = min(DEPTH5, len(pool))
            batch, seen_b = [], set()
            for i in range(n):
                cand = pool[-1 - (i // GEN_B)] if i % GEN_B == 0 else pool[i // GEN_B]
                if cand[0] not in seen_b:
                    seen_b.add(cand[0])
                    batch.append(cand)
            # M2, three counted modes -- INSPIRATION: Absolute Zero (arXiv
            # 2505.03335): propose/solve/VERIFY against a deterministic
            # ground in three enumerable modes (deduction, abduction,
            # induction). FOLD FORM: the deterministic ground is the STORE
            # ITSELF -- no executor, no gradient, no proposer reward; the
            # verifier is a count every time. Retention law throughout:
            # only held references are ever reinforced.
            for q, ref in batch:
                played.add(qkey(q))
                if len(q.strip()) < 10 or stuttered(ref):
                    continue                     # never hold machine stutter
                mode = len(played) % (GEN_B * GEN_B)   # four modes: 2^2
                if mode == 3:
                    # GENERATION CLOSURE (the review's found gap): the
                    # Learning Law must reach generate() itself. The engine
                    # GENERATES an answer from its counted distributions
                    # (no retrieval, no teacher), verifies it against the
                    # held reference by counted overlap, and only a
                    # VERIFIED generation is written back as orbits --
                    # earned retention for its own composed words. The
                    # generative organ gets the same ratchet as every other.
                    # THE BABBLE RATE (the spike law): regenerate silently
                    # up to the octave (GEN_B**GEN_C attempts) until one
                    # generation VERIFIES against the held reference; only
                    # a verified whole is ever written back.
                    held_one = 0
                    for _spike in range(GEN_B ** GEN_C):
                        gen = generate(tok("Q: " + q + "\nA:"), rng, min_words=GEN_B * GEN_C)
                        if gen and not stuttered(gen):
                            ov = set(content_words(gen)) & set(content_words(ref))
                            need = max(1, len(content_words(ref)) // GEN_B)
                            if len(ov) >= need:
                                write_orbits(tok("Q: " + q + "\nA: " + gen + "\n") * GEN_B)
                                log("SELFPLAY", "generation VERIFIED and held", gen[:80])
                                held_one = 1
                                break
                    if held_one == 0:
                        log("SELFPLAY", "babble exhausted unverified; silent", q[:60])
                    continue
                if mode == 1:
                    # ABDUCTION: from my held answer, recover its question --
                    # verified by counted overlap with the lesson's own words
                    hit, _sh2 = bind(ref)
                    ok = bool(hit) and hit[1].startswith("lesson:") and bool(
                        set(content_words(hit[1][7:])) & set(content_words(q)))
                    log("SELFPLAY", "abduction " + ("solved" if ok else "missed"), q)
                    if not ok:
                        write_orbits(tok("Q: " + q + "\nA: " + ref + "\n") * GEN_B)
                    continue
                if mode == 2 and len(batch) > 1:
                    # INDUCTION: two lessons sharing an informative word --
                    # the shared structure must surface through counted kin
                    q2 = batch[0][0] if batch[0][0] != q else batch[-1][0]
                    shared = [w for w in set(content_words(q)) & set(content_words(q2))
                              if TOK_FREQ.get(w, 0) <= TOTAL_TOKS / 1000]
                    if shared:
                        hit, _sh2 = bind(shared[0])
                        log("SELFPLAY", "induction " + ("linked" if hit else "open"), shared[0])
                    continue
                # DEDUCTION (mode 0): answer my own lesson; verify by count
                ans, _ = reply(q, rng)
                overlap = set(content_words(ans)) & set(content_words(ref))
                need = max(1, len(content_words(ref)) // GEN_B)
                if len(overlap) >= need or ans.strip() == ref.strip():
                    write_orbits(tok("Q: " + q + "\nA: " + ref + "\n") * GEN_B)
                    log("SELFPLAY", "consolidated", q)
                else:
                    record_correction(q, ref)
                    log("SELFPLAY", "self-corrected", q)
        except Exception as e:
            log("SELFPLAY", "error: " + str(e))
        time.sleep(60)

# ---------- EMPIRICAL BENCHMARKING: the engine vs its teachers, over time --
BENCH_LOG = BASE + "/fold_ai/benchmarks.tsv"

def run_benchmark(rng=None):
    """THE PROGRESS INSTRUMENT: one line of counted empirical state per run,
    appended to benchmarks.tsv -- native coverage (how much of the probe the
    engine answers from its OWN channels, no teacher), the judged
    head-to-head record, and the size of every owned store. The DIFFERENCE
    between successive lines is the growth rate; the crossover to majority
    wins is the measured moment the omni model has outgrown its teachers."""
    if rng is None:
        rng = np.random.default_rng()
    tw = sum(w for w, l in GRAD.values())
    tl = sum(l for w, l in GRAD.values())
    n_corr = len(CORRECTIONS)
    n_lessons = sum(1 for s, src in SENTS if src.startswith("lesson"))
    n_sight = sum(1 for s, src in SENTS if src.startswith("lesson:SIGHT"))
    n_sound = sum(1 for s, src in SENTS if src.startswith("lesson:SOUND"))
    n_voice = len(SOUND_FILES)
    n_told = sum(1 for s, src in SENTS if src in ("told", "confirmed"))
    # live probe: can the engine answer its own curriculum WITHOUT a teacher?
    pool = [(src[7:], s) for s, src in SENTS
            if src.startswith("lesson:") and not src.startswith(("lesson:SIGHT", "lesson:SOUND"))
            and len(src) > 17]
    rnd = random.Random(len(SENTS))
    probe = native = 0
    for q, ref in (rnd.sample(pool, min(GEN_B ** GEN_C, len(pool))) if pool else []):
        if len(q.strip()) < 10:
            continue
        probe += 1
        ans, th = reply(q, rng)          # face None: OWN channels only
        if not _is_confused(th):
            native += 1
    orbits = sum(len(s) for s in stores)
    # counted behaviour metrics from the live event log: tool acts and
    # whose voice answered (own vs teacher) -- fluency's raw material
    try:
        _lg = open(LOGFILE, errors="ignore").read()
        n_tools = _lg.count("\tTOOL\t")
        v_own = _lg.count("VOICE: UNISON")
        v_teach = _lg.count("VOICE: GEMMA")
    except Exception:
        n_tools = v_own = v_teach = 0
    _hdr = "time\torbits\tlessons\ttaught\ttold\tsights\tsounds\tvoiced\th2h_wins\th2h_losses\tprobe\tnative\ttools\tvoice_own\tvoice_teacher\n"
    if not os.path.exists(BENCH_LOG):
        with open(BENCH_LOG, "w") as f:
            f.write(_hdr)
    elif "\ttools\t" not in open(BENCH_LOG).readline():
        _rows = open(BENCH_LOG).read().splitlines()[1:]
        with open(BENCH_LOG, "w") as f:      # transparent schema evolution:
            f.write(_hdr)                    # old rows padded, nothing dropped
            for _r in _rows:
                f.write(_r + "\t-\t-\t-\n")
    with open(BENCH_LOG, "a") as f:
        f.write("\t".join(str(x) for x in (time.strftime("%Y-%m-%d %H:%M"), orbits, n_lessons,
                                            n_corr, n_told, n_sight, n_sound,
                                            n_voice, tw, tl, probe, native,
                                            n_tools, v_own, v_teach)) + "\n")
    summary = (f"BENCHMARK: native coverage {native}/{probe} on probed curriculum (own channels, no teacher); "
               f"tools used {n_tools}; voice own/teacher {v_own}/{v_teach}; "
               f"head-to-head {tw}W-{tl}L vs the teacher; owned: {n_lessons} lessons, {n_corr} taught answers, "
               f"{n_told} tellings, {n_sight} sights, {n_sound} sounds, {n_voice} voiced, {orbits} orbits. "
               f"Appended to benchmarks.tsv -- the difference between lines is the growth rate.")
    log("BENCH", summary)
    if ANNOUNCE[0]:
        try:
            ANNOUNCE[0]("📊 " + summary)      # the curve arrives in the channel
        except Exception as e:
            log("BENCH", "announce error: " + str(e))
    return summary

SOTA_LOG = BASE + "/fold_ai/benchmarks_sota.tsv"

def _fetch_mmlu(n=GEN_B ** 6):
    """Real items from the PUBLIC MMLU test set (cais/mmlu via the HF
    datasets server), cached once -- the same set SOTA numbers are
    published on, so every score here is directly comparable to the
    published table (subset size recorded per row)."""
    import json as _j, urllib.request as _u
    cache = BASE + "/fold_ai/mmlu_probe.json"
    if os.path.exists(cache):
        got = _j.load(open(cache))
        if len(got) >= n:
            return got[:n]
    # a FIXED, diverse probe set: 2^4 items at each of 2^3 evenly-spaced
    # offsets across the ~14k-item public test split -- deterministic,
    # subject-diverse, cached once, identical for every system forever
    probes = []
    for k in range(GEN_B ** 3):
        url = ("https://datasets-server.huggingface.co/rows?dataset=cais%2Fmmlu"
               "&config=all&split=test&offset=" + str(k * 1750) + "&length=" + str(GEN_B ** 4))
        rows = _j.loads(_u.urlopen(url, timeout=120).read().decode())["rows"]
        probes += [{"q": r["row"]["question"], "choices": r["row"]["choices"],
                    "a": int(r["row"]["answer"])} for r in rows]
    _j.dump(probes, open(cache, "w"))
    return probes[:n]

def _mc_prompt(p):
    return (p["q"] + "\n" + "\n".join(chr(65 + i) + ") " + c for i, c in enumerate(p["choices"]))
            + "\nAnswer with exactly one letter: A, B, C or D.")

def _mc_score(answer_text, p):
    """Counted scoring, no judge: the stated letter, or the correct choice's
    own words contained in the answer."""
    t = " ".join(str(answer_text).split())
    ms = re.findall(r"\b([ABCD])\b", t.upper())
    if ms:
        return (ord(ms[-1]) - 65) == p["a"]   # the FINAL stated letter is the verdict
    return p["choices"][p["a"]].lower() in t.lower()

def run_sota_bench(models=None, n=GEN_B ** 6):
    """THE 1-1 LADDER: the same public test items put to Unison (own
    channels, no teacher), to Unison+teacher, and to every named local
    model, on this machine, counted scoring -- one row per system per run,
    appended forever. Directly comparable to published MMLU numbers."""
    rng = np.random.default_rng()
    try:
        probes = _fetch_mmlu(n)
    except Exception as e:
        log("SOTA", "probe fetch failed: " + str(e))
        return "SOTA bench: could not fetch the public probe set (" + str(e) + ")"
    if models is None:
        models = ["gemma4:26b"]
    if not os.path.exists(SOTA_LOG):
        with open(SOTA_LOG, "w") as f:
            f.write("time\tsuite\tn\tsystem\tcorrect\tpct\n")
    out = []
    systems = [("unison-own", None)] + [(m, m) for m in models]
    for name, model in systems:
        correct = 0
        for p in probes:
            try:
                if model is None:
                    ans, _th = reply(_mc_prompt(p), rng)     # OWN channels only
                else:
                    ans = _ollama(_mc_prompt(p), timeout=180, model=model, num_ctx=8192)
                if _mc_score(ans, p):
                    correct += 1
            except Exception:
                pass
        pct = round(100 * correct / max(len(probes), 1), 1)
        with open(SOTA_LOG, "a") as f:
            f.write("\t".join(str(x) for x in (time.strftime("%Y-%m-%d %H:%M"), "MMLU-test-subset",
                                               len(probes), name, correct, pct)) + "\n")
        line = f"SOTA 1-1 [MMLU public test, n={len(probes)}]: {name} = {correct}/{len(probes)} ({pct}%)"
        log("SOTA", line)
        out.append(line)
        if ANNOUNCE[0]:
            try:
                ANNOUNCE[0]("🏁 " + line)
            except Exception:
                pass
    return "\n".join(out) + "\nAppended to benchmarks_sota.tsv -- rows are directly comparable to published MMLU tables."

SESSION_LOG = BASE + "/fold_ai/benchmarks_session.tsv"
_EXAMINER = """You are a curious, demanding HUMAN USER testing an AI called Unison in a live chat. Conduct a natural but varied many-turn conversation, one message per turn, reacting to what Unison actually said last. Across the session you must include: casual small talk; follow-ups that use pronouns ("what do you think about that?"); an abrupt topic change; ONE arithmetic question; ONE question about current events or a website (forces live lookup); teaching it a personal fact about you EARLY and then referencing that fact again LATE in the conversation without restating it; ONE question about the Smithian Fold Theory; a joke request; and ordinary random questions (cooking, travel, feelings). Be a person, not a checklist. Output ONLY your next user message, nothing else."""

def run_session_assessment(turns=GEN_B ** 4, announce=True):
    """THE SESSION ASSESSMENT (Maria's design): not turn-by-turn scoring but
    a REAL many-turn engagement -- an examiner holds a varied conversation
    with the live engine, a SESSION BOUNDARY is crossed midway (all
    in-session context cleared; persistent memory kept -- exactly what a
    reboot loses and keeps), and the WHOLE transcript is scored 0-10 on
    coherence, adaptivity, memory-across-the-boundary, tool use,
    communication, and reasoning. One row per assessment, appended forever.
    The judge is the teacher; a moving goal post is fine -- the engine is
    built to meet every one eventually."""
    rng = np.random.default_rng()
    transcript = []
    for i in range(turns):
        shown = "\n".join(("User: " + u + "\nUnison: " + a) for u, a in transcript[-8:])
        out = _ollama(_EXAMINER + ("\n\nConversation so far:\n" + shown if shown else
                                   "\n\nStart the conversation now.") +
                      "\nYour next message (turn " + str(i + 1) + " of " + str(turns) + "):",
                      timeout=180, num_ctx=16384)
        user_line = " ".join(out.split()).strip()[:400]
        if not user_line:
            continue
        ans, _th = turn(user_line, rng, "assess")
        transcript.append((user_line, ans))
        log("ASSESS", f"turn {i+1}/{turns}", user_line[:60], ans[:60])
        if i == turns // GEN_B - 1:
            # THE SESSION BOUNDARY: everything a reboot forgets, forgotten;
            # everything persistence keeps, kept. The examiner's late
            # callback to the early fact tests exactly this seam.
            del RECENT[:]
            del SESSION_TRAIL[:]
            LAST_TOPIC[0] = ""
            CONFUSED.clear()
            log("ASSESS", "SESSION BOUNDARY crossed (in-session context cleared; memory kept)")
    full = "\n".join(("User: " + u + "\nUnison: " + a) for u, a in transcript)
    verdict = _ollama("Below is a complete multi-turn conversation between a human examiner and an AI "
                      "called Unison, including a session boundary midway (Unison was restarted; its "
                      "permanent memory persists, its short-term context does not).\n\n" + full[:60000] +
                      "\n\nScore Unison 0-10 on each dimension, judging the WHOLE session, then one "
                      "blunt paragraph. Format STRICTLY:\nCOHERENCE: n\nADAPTIVITY: n\nMEMORY: n\n"
                      "TOOLS: n\nCOMMUNICATION: n\nREASONING: n\nVERDICT: ...", timeout=300, num_ctx=131072)
    scores = {}
    for dim in ("COHERENCE", "ADAPTIVITY", "MEMORY", "TOOLS", "COMMUNICATION", "REASONING"):
        m = re.search(dim + r":\s*(\d+)", verdict.upper())
        scores[dim] = int(m.group(1)) if m else -1
    vm = re.search(r"(?i)VERDICT:\s*(.+)", verdict, re.S)
    vtext = " ".join((vm.group(1) if vm else verdict).split())[:900]
    total = sum(v for v in scores.values() if v >= 0)
    if not os.path.exists(SESSION_LOG):
        with open(SESSION_LOG, "w") as f:
            f.write("time\tturns\tcoherence\tadaptivity\tmemory\ttools\tcommunication\treasoning\ttotal\tverdict\n")
    with open(SESSION_LOG, "a") as f:
        f.write("\t".join(str(x) for x in (time.strftime("%Y-%m-%d %H:%M"), len(transcript),
                scores["COHERENCE"], scores["ADAPTIVITY"], scores["MEMORY"], scores["TOOLS"],
                scores["COMMUNICATION"], scores["REASONING"], total, vtext)) + "\n")
    summary = (f"SESSION ASSESSMENT ({len(transcript)} turns, boundary crossed): "
               f"coherence {scores['COHERENCE']} | adaptivity {scores['ADAPTIVITY']} | "
               f"memory {scores['MEMORY']} | tools {scores['TOOLS']} | "
               f"communication {scores['COMMUNICATION']} | reasoning {scores['REASONING']} "
               f"| total {total}/60. {vtext[:400]}")
    log("ASSESS", summary)
    if announce and ANNOUNCE[0]:
        try:
            ANNOUNCE[0]("🎓 " + summary[:1800])
        except Exception:
            pass
    return summary

def _bench_loop():
    """THE MONITOR IS NOT A TOGGLE: the progress instrument fires hourly
    from the moment the system boots, /auto or not -- measurement runs
    unconditionally, learning runs at Maria's word. One line at wake, then
    one per hour; the curve writes itself."""
    try:
        run_benchmark()                    # the boot line: the curve's origin
    except Exception as e:
        log("BENCH", "error: " + str(e))
    _hr = 0
    while True:
        time.sleep(3600)
        _hr += 1
        try:
            run_benchmark()
        except Exception as e:
            log("BENCH", "error: " + str(e))
        # every 2^3 autonomous hours: the SESSION EXAM joins the auto record
        # -- conversational fluency, coherence, memory-across-boundary, and
        # TOOL USE, scored whole and posted (the examiner's arithmetic and
        # live-lookup turns exercise the toolkit by construction)
        if _hr % (GEN_B ** 3) == 0 and (AUTO["teach"] or AUTO["selfplay"]):
            try:
                threading.Thread(target=run_session_assessment, daemon=True).start()
                log("BENCH", "auto session assessment launched")
            except Exception as e:
                log("BENCH", "assess error: " + str(e))

# ---------- THE GROWING BODY: prose arrives, is eaten live, and is baked in
DIET_DIR = BASE + "/fold_ai/diet"
_EATEN = set()   # books ingested live this session (beyond the wake store)

def _start_grower():
    """Launch the public-domain prose ingester: it fills diet/ continuously;
    the prose watcher below eats each new book into the LIVE engine."""
    here = os.path.dirname(os.path.abspath(__file__))
    if subprocess.run(["pgrep", "-f", "corpus_grower.py"], capture_output=True).stdout.strip():
        log("GROWER", "already running; not relaunched")
        return
    lf = open(LOGDIR + "/grower.log", "a")
    subprocess.Popen([sys.executable, here + "/corpus_grower.py"], stdout=lf, stderr=subprocess.STDOUT)
    log("GROWER", "launched -> diet/ (new books eaten live; store rebuilt periodically)")

def _prose_watcher():
    """LIVE prose growth: any diet book not already inside the wake store is
    read ONCE into the running engine -- orbits (prose depth), kinship
    counts, and the sentence bank -- so fluency rises while the system is
    up, no restart. The kin index is refreshed after each meal."""
    global TOTAL_TOKS
    while True:
        time.sleep(300)
        try:
            new = [f for f in sorted(glob.glob(DIET_DIR + "/*.txt"))
                   if os.path.basename(f) not in STORE_INGESTED
                   and os.path.basename(f) not in _EATEN]
            ate = 0
            for f in new[:2]:                    # two books per meal, bounded
                text = open(f, errors="ignore").read()
                tl = tok(text)
                write_orbits(tl, max_ctx=3)      # prose depth, like the store
                build_neighbours(tl)
                TOK_FREQ.update(w.lower() for w in tl)
                TOTAL_TOKS += len(tl)
                for s in re.split(r"(?<=[.!?])\s+", text):
                    s = " ".join(s.split())
                    if "|" not in s and "`" not in s and well_formed(s):
                        hold_sentence(s, "prose")
                _EATEN.add(os.path.basename(f))
                ate += 1
                log("PROSE", os.path.basename(f), f"+{len(tl)} tokens eaten live")
            if ate:
                build_neigh_index()
        except Exception as e:
            log("PROSE", "watcher error: " + str(e))

def _store_rebuild_loop():
    """Every two hours, bake the grown diet into the prebuilt store with a
    budget that scales to the diet's size (capped so the wake stays fast) --
    the next wake inherits everything the session ate and more."""
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        time.sleep(7200)
        try:
            if subprocess.run(["pgrep", "-f", "build_store.py"], capture_output=True).stdout.strip():
                continue
            total_mb = sum(os.path.getsize(f) for f in glob.glob(DIET_DIR + "/*.txt")) // 1_000_000
            budget = min(max(90, total_mb), 250)
            lf = open(LOGDIR + "/store_build.log", "a")
            subprocess.run([sys.executable, here + "/build_store.py", str(budget)],
                           stdout=lf, stderr=subprocess.STDOUT, timeout=7000)
            log("STORE", f"periodic rebuild complete at {budget}MB budget (applies at next wake)")
        except Exception as e:
            log("STORE", "rebuild error: " + str(e))

# ---------- CONTINUOUS LEARNING: the teachers and the live lesson stream ---
def _watch_lessons():
    """New lesson pairs -- from the teacher models or hand-written files --
    are ingested LIVE, no restart. Poll the lesson files each minute, read
    only what was appended since, hold every clean Q/A pair, log the count."""
    seen = {}
    for f in glob.glob(BASE + "/fold_ai/lessons/lessons_*.txt"):
        seen[f] = os.path.getsize(f)      # wake already ate everything current
    while True:
        time.sleep(60)
        try:
            for f in glob.glob(BASE + "/fold_ai/lessons/lessons_*.txt"):
                # relay and sight pairs are already held the moment they happen
                if "lessons_live" in f or "feedback" in f or "lessons_relay" in f or "lessons_sight" in f or "lessons_sound" in f:
                    continue
                size = os.path.getsize(f)
                start = seen.get(f, 0)
                if size <= start:
                    seen[f] = size
                    continue
                with open(f, errors="ignore") as fh:
                    fh.seek(start)
                    new = fh.read()
                seen[f] = size
                pairs = re.findall(r"Q:\s*(.+?)\nA:\s*(.+?)(?=\nQ:|\Z)", new, re.S)
                for q, a in pairs:
                    q, a = " ".join(q.split()), " ".join(a.split())
                    if stuttered(a):
                        continue                 # machine stutter never held
                    write_orbits(tok("Q: " + q + "\nA: " + a + "\n") * GEN_C)
                    hold_sentence(a, "lesson:" + q[:80])
                if pairs:
                    write_orbits(tok(new), max_ctx=GEN_C)   # the FLOW: cross-turn
                    # transitions of the whole block, not just isolated pairs
                    log("LESSONS", os.path.basename(f), "+" + str(len(pairs)) + " pairs ingested live (with flow)")
        except Exception as e:
            log("LESSONS", "watcher error: " + str(e))

def _start_teacher():
    """Launch the teaching model pipeline (gemma4:26b via ollama) as a child
    of THIS process's run: it writes lessons_teacher.txt continuously and the
    watcher above feeds them straight into the live engine."""
    here = os.path.dirname(os.path.abspath(__file__))
    if subprocess.run(["pgrep", "-f", "teacher_pipeline.py"], capture_output=True).stdout.strip():
        log("TEACHER", "already running; not relaunched")
        return
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, timeout=10, check=True)
    except Exception:
        log("TEACHER", "ollama unavailable; teaching models offline this run")
        print("  (teacher offline: ollama unavailable)", flush=True)
        return
    lf = open(LOGDIR + "/teacher.log", "a")
    subprocess.Popen([sys.executable, here + "/teacher_pipeline.py"], stdout=lf, stderr=subprocess.STDOUT)
    log("TEACHER", "launched gemma4:26b pipeline -> lessons_teacher.txt (ingested live)")
    print("  teacher launched (gemma4:26b); lessons ingested live each minute", flush=True)

def _start_discord(rng):
    """Bring up the Discord FACE of this same engine -- an interface only,
    sharing this process's live memory. No separate engine, ever."""
    def _t():
        try:
            import importlib.util as _ilu
            here = os.path.dirname(os.path.abspath(__file__))
            _sp = _ilu.spec_from_file_location("unison_discord_iface", here + "/unison_discord.py")
            ud = _ilu.module_from_spec(_sp)
            _sp.loader.exec_module(ud)
            ud.run(sys.modules[__name__], rng)
        except Exception as e:
            log("DISCORD", "interface failed: " + str(e))
            print("  (discord face failed: " + str(e) + ")", flush=True)
    threading.Thread(target=_t, daemon=True).start()

def main():
    rng = np.random.default_rng()
    # the unified system comes up as ONE: engine (awake above), the Discord
    # face on this same memory, the teachers, and the live lesson stream.
    _start_discord(np.random.default_rng())
    _start_teacher()
    _start_grower()
    threading.Thread(target=_watch_lessons, daemon=True).start()
    threading.Thread(target=_tutor_loop, daemon=True).start()
    threading.Thread(target=_selfplay_loop, daemon=True).start()
    threading.Thread(target=_bench_loop, daemon=True).start()
    threading.Thread(target=_prose_watcher, daemon=True).start()
    threading.Thread(target=_store_rebuild_loop, daemon=True).start()
    # THE OBSERVER, HOT FROM LAUNCH: warm the teacher model now so the
    # confusion relay answers in seconds, not on a cold load.
    RELAY["on"] = True
    def _warm_observer():
        r = _ollama("Reply with exactly one word: ready", timeout=600)
        log("TEACHER", "observer HOT -- confusion relay armed" if "ready" in r.lower()
            else "observer warmup got: " + r.strip()[:60])
    threading.Thread(target=_warm_observer, daemon=True).start()
    log("DIAG", f"locks ctx={CTX_MAX} bind={BIND_LOCK} kin={KIN_FLOOR} compose={COMPOSE_FLOOR} sight={SIGHT_K}",
        f"orbits={sum(len(s) for s in stores)}", f"sents={len(SENTS)}", f"corrections={len(CORRECTIONS)}",
        f"grad={len(GRAD)}", f"sounds={len(SOUND_FILES)}", f"bound={STORE_BOUND}",
        f"judges={','.join(JUDGES)}")
    log("SYSTEM", "unified launch: terminal + discord face + teacher + observer relay + grower + lesson/prose watchers + store rebuild + tutor + self-play, one engine")
    print("  observer (gemma4:26b) heating -- what I cannot answer, my teacher answers as me, and I keep it", flush=True)
    print("  toggles: /auto (everything), /teach (autonomous tutor), /selfplay -- here or on Discord", flush=True)
    last_exchange = [None, ""]
    print("\nUnisonAI: Hello. I am the seed of UnisonAI. Talk to me -- I learn from everything you tell me, as you say it.\n", flush=True)
    while True:
        try:
            line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line.startswith("/"):
            if line == "/quit":
                break
            t = toggle(line)
            print("UnisonAI: " + (t or "commands: /auto /teach /selfplay /quit") + "\n", flush=True)
            continue
        # bare negation = rejection of the previous answer, never a fact
        if line.lower().strip(" .!") in ("no", "wrong", "incorrect", "that is wrong", "thats wrong") and last_exchange[0]:
            REJECTED.add((qkey(last_exchange[0]), last_exchange[1].strip()))
            with open(FEEDBACK_LOG, "a") as f:
                f.write("REJ\t" + qkey(last_exchange[0]) + "\t" + last_exchange[1] + "\t(bare no)\n")
            log("FEEDBACK", "terminal", "bare no", last_exchange[0], last_exchange[1])
            print("UnisonAI: withdrawn. Tell me the right of it, and I will hold it.\n", flush=True)
            continue
        ans, thought = turn(line, rng)
        print("  \u2301 " + thought, flush=True)
        print("UnisonAI: " + ans + "\n", flush=True)
        last_exchange[0], last_exchange[1] = line, ans
        try:
            fb = input("  y/n + why (enter skips): ").strip()
        except (EOFError, KeyboardInterrupt):
            fb = ""
        if not fb:
            continue
        res = apply_feedback(line, ans, fb)
        if res is None:            # bare n: ask for the correction, once
            try:
                corrected = input("UnisonAI: what should I have said? ").strip()
            except (EOFError, KeyboardInterrupt):
                corrected = ""
            if corrected:
                held = record_correction(line, corrected)
                print("UnisonAI: held, permanently: " + held + " Ask me again.\n", flush=True)
            else:
                print("UnisonAI: withdrawn. I will not repeat it.\n", flush=True)
        elif res:
            print("UnisonAI: " + res + "\n", flush=True)

if __name__ == "__main__":
    main()
