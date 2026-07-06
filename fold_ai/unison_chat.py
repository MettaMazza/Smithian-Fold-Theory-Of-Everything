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

CTX_MAX = 6
BASE = "/Users/mettamazza/Desktop/Smithian Fold Theory"

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
    for m in re.finditer(r"(?i)\b(\w{2,3})\s+(\w{4,})", text):
        a, b = m.group(1).lower(), m.group(2).lower()
        if b.startswith(a) and a not in _OKSHORT:
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
def _key(tup):
    return tuple(t.lower() for t in tup)        # case-folded context key
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

def kin_expand(words, k=3):
    out = set(w.lower() for w in words)
    for w in list(out):
        nb = NEIGH.get(w)
        if not nb:
            continue
        cand = set()
        for c in sorted(nb, key=lambda c: TOK_FREQ.get(c, 1))[:12]:
            cand |= NEIGH_INDEX.get(c, set())
        cand.discard(w)
        cands = [(kinship(w, o), o) for o in cand if len(o) > 3]
        cands.sort(reverse=True)
        for sc, o in cands[:k]:
            if sc > 0.15:
                out.add(o)
    return out

full = corpus_text + ("\n" + lesson_text) * 3
words = tok(full)
write_orbits(words)
build_neighbours(words)

# sentence store + inverted index (binding substrate)
SENTS = []
TOK_FREQ = Counter(w.lower() for w in words)
TOTAL_TOKS = sum(TOK_FREQ.values())
INDEX = defaultdict(set)

def hold_sentence(s, source):
    s = " ".join(s.split())
    if not (8 <= len(s) <= 400):
        return
    sid = len(SENTS)
    SENTS.append((s, source))
    for w in set(t.lower() for t in tok(s) if len(t) > 2):
        INDEX[w].add(sid)

# lessons: hold Q/A pairs as bound units; corpus: hold sentences
for q, a in re.findall(r"Q:\s*(.+?)\nA:\s*(.+?)(?=\nQ:|\Z)", lesson_text, re.S):
    if not stuttered(a):
        hold_sentence(a.strip(), "lesson:" + q.strip()[:80])
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
    return [w for _, w in scored[:6]]



# ---------- FINDING: binding (XI-4) ----------
def bind(query, exclude_self=None):
    cw = content_words(query)
    if not cw:
        return None, 0.0
    votes = defaultdict(float)
    for w in cw:                                   # direct content words: full weight
        for sid in INDEX.get(w, ()):
            votes[sid] += informativeness(w)
    for w in kin_expand(cw, k=2) - set(cw):        # counted kin: half weight
        for sid in INDEX.get(w, ()):
            votes[sid] += 0.5 * informativeness(w)
    if not votes:
        return None, 0.0
    denom = sum(informativeness(w) for w in cw)
    # THE EXPERIENCE ORDER (lexicographic, no weights): what it was TOLD
    # outranks its lessons, which outrank its library -- its own held life
    # first, then its teaching, then its reading.
    def source_rank(sid):
        src = SENTS[sid][1]
        return 0 if src == "told" else (1 if src.startswith("lesson") else 2)
    best = sorted(votes.items(), key=lambda kv: (source_rank(kv[0]), -kv[1]))
    for sid, v in best[:8]:
        s, srcname = SENTS[sid]
        if exclude_self and s.strip() == exclude_self.strip():
            continue
        return SENTS[sid], v / denom
    return None, 0.0

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

def continue_orbit(ctx_tokens, rng, max_tokens=60):
    ctx = list(ctx_tokens)
    out = []
    for _ in range(max_tokens):
        s = None
        for L in range(min(CTX_MAX, len(ctx)), 0, -1):
            s = stores[L].get(_key(tuple(ctx[-L:])))
            if s:
                break
        if not s:
            break
        items = list(s.items())
        counts = np.array([n for _, n in items], dtype=np.float64)
        probs = counts / counts.sum()
        nxt = items[int(rng.choice(len(items), p=probs))][0]
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
    for w in kin_expand([focus], k=3):
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
        for L in range(min(CTX_MAX, len(ctx)), 0, -1):
            s = stores[L].get(_key(tuple(ctx[-L:])))
            if s:
                # admit the highest-count successor that stays kin to the lock
                for cand, _n in sorted(s.items(), key=lambda kv:-kv[1]):
                    if cand in ("Q","A","q","a"): continue
                    if len(cand) < 3 or kinship(cand, focus) > 0.05 or cand in (".",",","the","a","is","of","and"):
                        nxt = cand; break
                if nxt: break
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
        succ = None
        for L in range(min(CTX_MAX, len(ctx)), 0, -1):
            succ = stores[L].get(_key(tuple(ctx[-L:])))
            if succ and (len(succ) > 1 or L == 1):
                break
        if not succ:
            break
        items = [(w, c) for w, c in succ.items() if w not in ("Q", "A")]
        if not items:
            break
        ws = np.array([c for _, c in items], dtype=np.float64)
        nxt = items[int(rng.choice(len(items), p=ws / ws.sum()))][0]
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
def reply(user_line, rng):
    ck = qkey(user_line)
    if ck in CORRECTIONS:
        return CORRECTIONS[ck], "taught answer (held correction)"
    cmd = follow_command(user_line)
    if cmd:
        return cmd, "command followed"
    cw = content_words(user_line)
    thought = ["focus=" + ",".join(cw[:4]) if cw else "focus=(none)"]
    fa = answer_fact(user_line)
    if fa:
        thought.append("relation-fact channel: exact held fact")
        return fa, "; ".join(thought)
    q_tokens = tok("Q: " + user_line) + tok("A:")
    candidate = continue_orbit(q_tokens, rng)
    if candidate and rejected(user_line, candidate):
        thought.append("dialogue candidate previously rejected; withheld")
        candidate = None
    if candidate:
        shared = set(cw) & set(t.lower() for t in tok(candidate))
        if shared or len(cw) == 0:
            thought.append("dialogue orbit bound back (" + (",".join(list(shared)[:3]) or "greeting") + "); self-check pass")
            return candidate, "; ".join(thought)
        thought.append("dialogue candidate failed self-check (no shared focus)")
    probe_line = user_line
    if len(cw) == 0 and LAST_TOPIC[0]:
        probe_line = user_line + " " + LAST_TOPIC[0]
        thought.append("contextless follow-up; binding through the last topic")
    hit, share = bind(probe_line)
    if hit and rejected(user_line, hit[0]):
        thought.append("bound fact previously rejected; withheld")
        hit = None
    if hit and share >= 0.34:
        thought.append(f"bound {hit[1]} at share {share:.2f}; selected at the lock")
        return hit[0], "; ".join(thought)
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
    for t in tok_display(s):
        f = FLIP.get(t.lower())
        out.append((f.capitalize() if t[:1].isupper() else f) if f else t)
    s2 = re.sub(r"\s+([.,!?;:])", r"\1", " ".join(out))
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
    return ",".join(sorted(content_words(user_line)[:4]))

if os.path.exists(CORR_LOG):
    for _ln in open(CORR_LOG):
        _p = _ln.rstrip("\n").split("\t", 1)
        if len(_p) == 2:
            CORRECTIONS[_p[0]] = _p[1]

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
    write_orbits(tok("Q: " + question + "\nA: " + answer + "\n") * 3)
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
_CHILD_FACES = ("terminal", "discord")   # faces where I ask like a child

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
    is_command = bool(re.match(r"(?i)\s*(say|repeat after me|respond with|reply with)\b", line))
    if not is_question and not is_command:
        if not content_words(line):
            return "okay.", "contentless; acknowledged, not held"
        got = learn_fact(line)
        fact = flip_perspective(line if line[-1:] in ".!" else line + ".")
        # reply candidate BEFORE the telling is written -- otherwise the
        # freshest orbit is the echo of her own words (the parrot disease)
        candidate = continue_orbit(tok("Q: " + line) + tok("A:"), rng)
        write_orbits(tok(fact + "\n") * 3)
        hold_sentence(fact, "told")
        write_orbits(tok("q: " + line + "\na: " + fact + "\n") * 2)
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
        if candidate and dedup(candidate).lower().rstrip(".!? ") == fact.lower().rstrip(".!? "):
            candidate = None                    # never parrot the telling back
        if candidate and not rejected(line, candidate) and (set(content_words(line)) & set(t.lower() for t in tok(candidate))):
            ans, thought = dedup(candidate), "telling held (perspective flipped); dialogue orbit bound back"
        else:
            ans = "Held. " + fact
            thought = "telling held" + (" as a relation fact" if got else " at the prediction state")
    else:
        CONFUSED.pop(interface, None)           # a new question supersedes an open one
        ans, thought = reply(line, rng)
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
    hold_sentence("On '" + line[:60] + "' I thought: " + thought, "thought")
    if content_words(line):
        LAST_TOPIC[0] = " ".join(content_words(line)[:4])
    # LEARNING, ongoing: your words always held (the prediction state)
    with open(BASE + "/fold_ai/lessons/lessons_live.txt", "a") as f:
        f.write("Q: " + line + "\nA: " + ans + "\n")
    log("TURN", interface, line, ans, thought)
    return ans, thought

def apply_feedback(question, answer, fb_text, interface="terminal"):
    """THE CLOSURE (XIV-7), from any face. y consolidates (the exchange joins
    the held cycle -- earned retention). n withholds the antipode AND any
    text after the n IS the corrected answer -- plain words, no syntax."""
    fb = fb_text.strip()
    if fb[:1].lower() == "y":
        write_orbits(tok("Q: " + question + "\nA: " + answer + "\n") * 3)
        hold_sentence(answer, "confirmed")
        reason = fb[1:].strip(" :,-")
        if reason:
            hold_sentence(reason, "told")
            write_orbits(tok(reason + "\n") * 2)
        with open(FEEDBACK_LOG, "a") as f:
            f.write("CONF\t" + qkey(question) + "\t" + answer + "\n")
        log("FEEDBACK", interface, "y", question, answer)
        return "consolidated -- this exchange joins the held cycle."
    if fb[:1].lower() == "n":
        REJECTED.add((qkey(question), answer.strip()))
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

UNISON_PERSONA = ("You ARE UnisonAI (\"Unison\") -- the seed of a fold-native engine built on the "
                  "Smithian Fold Theory. You hold no trained weights: everything you know is written "
                  "as exact held orbits, and you learn from every telling the moment it is said. Your "
                  "voice is warm, steady, plain-spoken, first-person, never hedging, never corporate.")

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
    return None

_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b-\x1f\x7f]")
def _ollama(prompt, timeout=600):
    # the HTTP API, never the CLI: terminal line-wrap duplicates word
    # fragments ("beautifu beautiful") that poison every downstream filter
    try:
        import json as _json, urllib.request as _ur
        req = _ur.Request("http://localhost:11434/api/generate",
                          data=_json.dumps({"model": "gemma4:26b", "prompt": prompt,
                                            "stream": False, "think": False}).encode(),
                          headers={"Content-Type": "application/json"})
        with _ur.urlopen(req, timeout=timeout) as resp:
            return _json.loads(resp.read().decode()).get("response", "")
    except Exception as e:
        log("TUTOR", "ollama error: " + str(e))
        return ""

def _teacher_relay(question, user_help=""):
    """THE OBSERVER RELAY: what I cannot answer, my teacher answers AS me --
    with stepwise reasoning I hold as my own thought -- I relay it and keep
    it: asked once, owned forever (the Learning Law, closed by a second
    observer instead of left open). Returns (answer, reasoning) or None."""
    helping = ("\nThe user explained, to help you: \"" + user_help.strip() + "\"") if user_help else ""
    out = _ollama(UNISON_PERSONA + "\n\nA user just asked you: \"" + question.strip() + "\"" + helping +
                  "\nFirst write ONE short line of stepwise reasoning beginning exactly 'Reasoning:'. "
                  "Then the reply beginning exactly 'Answer:' -- one to two plain sentences, in your "
                  "voice, no markdown.", timeout=180)
    out = " ".join(out.split()).strip()
    m = re.search(r"(?i)reasoning:\s*(.+?)\s*answer:\s*(.+)", out)
    reasoning, a = (m.group(1).strip(), m.group(2).strip()) if m else ("", re.sub(r"(?i)^(a:|answer:)\s*", "", out))
    a = " ".join(re.split(r"(?<=[.!?])\s+", a)[:2])[:350]      # at most two sentences
    if len(a) < 8 or stuttered(a) or any(b in a for b in ("$", "\\", "{", "}", "*", "`", "|")):
        log("RELAY", "observer answer rejected", question[:80])
        return None
    a = a if a[-1:] in ".!?" else a + "."
    write_orbits(tok("Q: " + question + "\nA: " + a + "\n") * 3)
    hold_sentence(a, "lesson:" + question.strip()[:80])
    if reasoning:                                   # taught reasoning joins MY thought
        hold_sentence("On '" + question.strip()[:60] + "' the reasoning is: " + reasoning[:250], "thought")
    with open(BASE + "/fold_ai/lessons/lessons_relay.txt", "a") as f:
        f.write("Q: " + question.strip() + "\nA: " + a + "\n")   # persists to next wake
    log("RELAY", question, a)
    return a, reasoning

def observe_image(images_b64, caption=""):
    """VISION INTAKE: the observer describes what is shown, in my voice; the
    description is held as a telling -- the image becomes memory."""
    try:
        import json as _j, urllib.request as _u
        req = _u.Request("http://localhost:11434/api/generate",
                         data=_j.dumps({"model": "gemma4:26b",
                                        "prompt": UNISON_PERSONA + "\n\nDescribe what you see in this image in two plain sentences, in your voice."
                                        + ((" The user said: \"" + caption.strip() + "\"") if caption.strip() else ""),
                                        "images": images_b64, "stream": False, "think": False}).encode(),
                         headers={"Content-Type": "application/json"})
        with _u.urlopen(req, timeout=300) as r:
            d = " ".join(_j.loads(r.read().decode()).get("response", "").split()).strip()
        if not d or stuttered(d):
            return None
        hold_sentence("I was shown an image: " + d, "told")
        write_orbits(tok("I was shown an image: " + d + "\n") * 2)
        log("VISION", (caption or "(no caption)")[:60], d[:150])
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
    while True:
        if not AUTO["teach"]:
            time.sleep(5)
            continue
        try:
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
            ans, _ = turn(q, rng, "tutor")
            verdict = _ollama("QUESTION: " + q + "\nREFERENCE ANSWER: " + ref +
                              "\nSTUDENT ANSWER: " + ans +
                              "\nDoes the student answer convey the reference answer's meaning? "
                              "Reply with exactly one word: YES or NO.", timeout=300)
            if re.search(r"\bYES\b", verdict.upper()):
                apply_feedback(q, ans, "y", "tutor")
                log("TUTOR", "y", q)
            else:
                apply_feedback(q, ans, "n " + ref, "tutor")
                log("TUTOR", "n->corrected", q, ref)
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
            for q, ref in rnd.sample(pool, min(5, len(pool))):
                played.add(qkey(q))
                if len(q.strip()) < 10 or stuttered(ref):
                    continue                     # never hold machine stutter
                ans, _ = reply(q, rng)
                overlap = set(content_words(ans)) & set(content_words(ref))
                need = max(1, len(content_words(ref)) // 2)
                if len(overlap) >= need or ans.strip() == ref.strip():
                    write_orbits(tok("Q: " + q + "\nA: " + ref + "\n") * 2)
                    log("SELFPLAY", "consolidated", q)
                else:
                    record_correction(q, ref)
                    log("SELFPLAY", "self-corrected", q)
        except Exception as e:
            log("SELFPLAY", "error: " + str(e))
        time.sleep(60)

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
                # relay pairs are already held the moment they happen
                if "lessons_live" in f or "feedback" in f or "lessons_relay" in f:
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
                    write_orbits(tok("Q: " + q + "\nA: " + a + "\n") * 3)
                    hold_sentence(a, "lesson:" + q[:80])
                if pairs:
                    log("LESSONS", os.path.basename(f), "+" + str(len(pairs)) + " pairs ingested live")
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
