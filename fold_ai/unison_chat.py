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
import numpy as np, glob, re, sys, time
from collections import defaultdict, Counter

CTX_MAX = 6
BASE = "/Users/mettamazza/Desktop/Smithian Fold Theory"
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
def write_orbits(tl):
    for i in range(len(tl) - 1):
        nxt = tl[i + 1]                          # original-case successor (voice)
        for L in range(0, CTX_MAX + 1):
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
def kin_expand(words, k=3):
    out = set(w.lower() for w in words)
    for w in list(out):
        cands = [(kinship(w, o), o) for o in NEIGH if o != w and len(o) > 3]
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
_sp = BASE + "/fold_ai/store.pkl"
_MAX_STORE = 600_000_000   # 250MB cap: never load a runaway store at wake
if os.path.exists(_sp) and 0 < os.path.getsize(_sp) < _MAX_STORE:
    try:
        with open(_sp, "rb") as _f:
            _st = _pk.load(_f)
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
        print(f"  merged prose store: +{len(_st['sents'])} sentences, +{len(_st['neigh'])} words from {len(_st['ingested'])} books", flush=True)
    except Exception as _e:
        print("  (prose store skipped: " + str(_e) + ")", flush=True)

print(f"awake: {sum(len(s) for s in stores)} orbits, {len(SENTS)} held sentences, in {time.time()-t0:.0f}s", flush=True)

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
    return re.sub(r"\s+([.,!?;:])", r"\1", " ".join(out))

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
def flip_perspective(s):
    out = []
    for t in tok_display(s):
        f = FLIP.get(t.lower())
        out.append((f.capitalize() if t[:1].isupper() else f) if f else t)
    s2 = " ".join(out)
    return re.sub(r"\s+([.,!?;:])", r"\1", s2)

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
    # also learn it as a relation fact if it is one (self/your name etc.)
    learn_fact(answer)
    write_orbits(tok("Q: " + question + "\nA: " + answer + "\n") * 3)
    hold_sentence(answer, "told")
    return answer

def rejected(user_line, ans):
    return (qkey(user_line), ans.strip()) in REJECTED

def main():
    rng = np.random.default_rng()
    last_exchange = [None, ""]
    print("\nUnisonAI: Hello. I am the seed of UnisonAI. Talk to me -- I learn from everything you tell me, as you say it.\n", flush=True)
    while True:
        try:
            line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line == "/quit":
            break
        is_question = line.endswith("?") or line.lower().startswith(("what", "who", "how", "why", "when", "where", "do ", "does", "did", "can ", "is ", "are "))
        # bare negation = rejection of the previous answer, never a fact
        if line.lower().strip(" .!") in ("no", "wrong", "incorrect", "that is wrong", "thats wrong") and last_exchange[0]:
            REJECTED.add((qkey(last_exchange[0]), last_exchange[1].strip()))
            with open(FEEDBACK_LOG, "a") as f:
                f.write("REJ\t" + qkey(last_exchange[0]) + "\t" + last_exchange[1] + "\t(bare no)\n")
            print("UnisonAI: withdrawn. Tell me the right of it, and I will hold it.\n", flush=True)
            continue
        if not is_question:
            fact_raw = line if line[-1:] in ".!" else line + "."
            fact = flip_perspective(fact_raw)   # held from MY side of the boundary
            if not content_words(line):
                print("UnisonAI: okay.\n", flush=True)   # contentless: acknowledged, not held as fact
                continue
            write_orbits(tok(fact + "\n") * 3)
            hold_sentence(fact, "told")
            write_orbits(tok("q: " + line + "\na: " + fact + "\n") * 2)
            # then speak: a dialogue orbit if one binds back, else acknowledge
            candidate = continue_orbit(tok("Q: " + line) + tok("A:"), rng)
            if candidate and not rejected(line, candidate) and (set(content_words(line)) & set(t.lower() for t in tok(candidate))):
                ans, thought = candidate, "telling held (perspective flipped); dialogue orbit bound back"
            else:
                ans = ("Held. " + (answer_fact("what is my name") or answer_fact("where do i live") or fact)) if got_fact else ("Held: " + fact)
                thought = "telling held" + (" as a relation fact" if got_fact else " at the prediction state")
        else:
            ans, thought = reply(line, rng)
        print("  \u2301 " + thought, flush=True)
        print("UnisonAI: " + dedup(ans) + "\n", flush=True)
        # the thought itself is held (self-observation, XIV-7)
        hold_sentence("On \'" + line[:60] + "\' I thought: " + thought, "thought")
        last_exchange[0], last_exchange[1] = line, ans
        if content_words(line):
            LAST_TOPIC[0] = " ".join(content_words(line)[:4])
        # LEARNING, ongoing: your words always held (the prediction state)
        with open(BASE + "/fold_ai/lessons/lessons_live.txt", "a") as f:
            f.write("Q: " + line + "\nA: " + ans + "\n")
        if is_question:
            write_orbits(tok("Q: " + line + "\n"))
        # THE CLOSURE (XIV-7): y/n + why -- optional (enter skips; learning
        # never depends on it). y consolidates (the antipode completes, the
        # exchange joins the held cycle -- including my reply: earned
        # retention). n withholds the antipode: the reply enters the
        # anti-ledger and your reasoning is held as a corrective telling.
        try:
            fb = input("  y/n + why (enter skips): ").strip()
        except (EOFError, KeyboardInterrupt):
            fb = ""
        if fb[:1].lower() == "y":
            write_orbits(tok("Q: " + line + "\nA: " + ans + "\n") * 3)
            hold_sentence(ans, "confirmed")
            reason = fb[1:].strip(" :,-")
            if reason:
                hold_sentence(reason, "told")
                write_orbits(tok(reason + "\n") * 2)
            with open(FEEDBACK_LOG, "a") as f:
                f.write("CONF\t" + qkey(line) + "\t" + ans + "\n")
        elif fb[:1].lower() == "n":
            REJECTED.add((qkey(line), ans.strip()))
            with open(FEEDBACK_LOG, "a") as f:
                f.write("REJ\t" + qkey(line) + "\t" + ans + "\n")
            # WHATEVER YOU TYPE AFTER n IS THE CORRECTED ANSWER -- no syntax.
            corrected = fb[1:].strip(" :,-")
            if not corrected:
                try:
                    corrected = input("UnisonAI: what should I have said? ").strip()
                except (EOFError, KeyboardInterrupt):
                    corrected = ""
            if corrected:
                held = record_correction(line, corrected)
                print("UnisonAI: held, permanently: " + held + " Ask me again.\n", flush=True)
            else:
                print("UnisonAI: withdrawn. I will not repeat it.\n", flush=True)

if __name__ == "__main__":
    main()
