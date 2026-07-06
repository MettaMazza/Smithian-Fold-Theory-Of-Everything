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
import numpy as np, glob, re, sys, time
from collections import defaultdict, Counter

CTX_MAX = 6
BASE = "/Users/mettamazza/Desktop/Smithian Fold Theory"
LESSONS = sorted(glob.glob(BASE + "/fold_ai/lessons/*.txt"))
CORPUS = [f for f in sorted(glob.glob(BASE + "/**/*.md", recursive=True)) +
          sorted(glob.glob("/Users/mettamazza/Desktop/SFTOM/**/*.md", recursive=True))
          if "/language/" not in f and "/.git/" not in f]

def tok(s):
    return re.findall(r"\w+|[^\w\s]", s)

def tok_display(s):
    return tok(s)

print("UnisonAI waking: reading everything once...", flush=True)
t0 = time.time()
corpus_text = "\n".join(open(f, errors="ignore").read() for f in CORPUS)
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

full = corpus_text + ("\n" + lesson_text) * 3
words = tok(full)
write_orbits(words)

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
for s in re.split(r"(?<=[.!?])\s+", corpus_text):
    if "|" not in s and "#" not in s and "`" not in s and s.count("=") < 2:
        hold_sentence(s, "corpus")

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
    for w in cw:
        for sid in INDEX.get(w, ()):
            votes[sid] += informativeness(w)
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
        FACTS[(_norm_subject(m.group(1)), "name")] = m.group(2).strip().title()
        return True
    # "my/your favourite X is Y"
    m = re.match(r"(?i)(my|your)\s+favou?rite\s+(\w+)\s+is\s+(.+)", t)
    if m:
        FACTS[(_norm_subject(m.group(1)), "favourite " + m.group(2).lower())] = m.group(3).strip()
        return True
    # "I live in X" / "I am from X" / "my home is X"
    m = re.match(r"(?i)(?:i\s+live\s+in|i\s+am\s+from|i'?m\s+from|my\s+home\s+is)\s+(.+)", t)
    if m:
        FACTS[("you", "location")] = m.group(1).strip().title()
        return True
    m = re.match(r"(?i)(?:you\s+live\s+in|your\s+home\s+is)\s+(.+)", t)
    if m:
        FACTS[("self", "location")] = m.group(1).strip().title()
        return True
    # "I am X" / "you are X"  (identity)
    m = re.match(r"(?i)(i\s+am|i'?m|you\s+are|you'?re)\s+(.+)", t)
    if m:
        subj = "you" if m.group(1).lower().startswith("i") else "self"
        FACTS[(subj, "identity")] = m.group(2).strip()
        return True
    return False

def answer_fact(text):
    t = text.strip().rstrip("?.!")
    m = re.search(r"(?i)what\s+is\s+(my|your)\s+name", t)
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

# ---------- CHECKING (XIV-7) + the reply law ----------
def follow_command(line):
    m = re.match(r"(?i)\s*(?:say|repeat after me[:,]?|respond with|reply with)\s*[:,]?\s*['\"]?(.+?)['\"]?\s*$", line)
    if m and len(m.group(1)) < 120:
        w = m.group(1).strip()
        return w if w[-1:] in ".!?" else w + "."
    return None

def reply(user_line, rng):
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
    hit, share = bind(user_line)
    if hit and rejected(user_line, hit[0]):
        thought.append("bound fact previously rejected; withheld")
        hit = None
    if hit and share >= 0.34:
        thought.append(f"bound {hit[1]} at share {share:.2f}; selected at the lock")
        return hit[0], "; ".join(thought)
    thought.append("nothing passed the self-check; asking rather than guessing")
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
        print("UnisonAI: " + ans + "\n", flush=True)
        # the thought itself is held (self-observation, XIV-7)
        hold_sentence("On \'" + line[:60] + "\' I thought: " + thought, "thought")
        last_exchange[0], last_exchange[1] = line, ans
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
            reason = fb[1:].strip(" :,-")
            with open(FEEDBACK_LOG, "a") as f:
                f.write("REJ\t" + qkey(line) + "\t" + ans + "\t" + reason + "\n")
            if reason:
                m = re.search(r"(?:say|reply(?:\s+with)?|respond(?:\s+with)?|answer(?:\s+with)?)\s*[:,]?\s*['\"]([^'\"]+)['\"]", reason, re.I)
                if m:
                    corrected = m.group(1).strip()
                    corrected = corrected if corrected[-1:] in ".!?" else corrected + "."
                    write_orbits(tok("Q: " + line + "\nA: " + corrected + "\n") * 3)
                    hold_sentence(corrected, "told")
                    print("UnisonAI: held. Next time: " + corrected + "\n", flush=True)
                else:
                    fact2 = reason if reason[-1:] in ".!" else reason + "."
                    write_orbits(tok(fact2 + "\n") * 2)
                    hold_sentence("Guidance: " + fact2, "told")
                    print("UnisonAI: held the correction.\n", flush=True)

if __name__ == "__main__":
    main()
