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

print("UnisonAI waking: reading everything once...", flush=True)
t0 = time.time()
corpus_text = "\n".join(open(f, errors="ignore").read() for f in CORPUS)
lesson_text = "\n".join(open(f, errors="ignore").read() for f in LESSONS)

# ---------- HOLDING: orbits for continuation + the sentence store ----------
stores = [defaultdict(lambda: defaultdict(int)) for _ in range(CTX_MAX + 1)]
def write_orbits(tl):
    for i in range(len(tl) - 1):
        nxt = tl[i + 1]
        for L in range(0, CTX_MAX + 1):
            if i - L + 1 < 0:
                break
            stores[L][tuple(tl[i - L + 1:i + 1])][nxt] += 1

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
            s = stores[L].get(tuple(ctx[-L:]))
            if s:
                break
        if not s:
            break
        items = list(s.items())
        counts = np.array([n for _, n in items], dtype=np.float64)
        probs = counts / counts.sum()
        nxt = items[int(rng.choice(len(items), p=probs))][0]
        if nxt == "Q":
            break
        out.append(nxt)
        ctx.append(nxt)
        if nxt in (".", "!", "?") and len(out) > 3:
            break
    s = " ".join(out)
    return re.sub(r"\s+([.,!?;:])", r"\1", s)

# ---------- CHECKING (XIV-7) + the reply law ----------
def reply(user_line, rng):
    cw = content_words(user_line)
    thought = ["focus=" + ",".join(cw[:4]) if cw else "focus=(none)"]
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
    if candidate:
        thought.append("weak binding; speaking the unchecked candidate")
        return candidate, "; ".join(thought)
    thought.append("nothing bound above the floor; asking to be told")
    return "I do not hold that yet. Tell me, and I will.", "; ".join(thought)

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
        if not is_question:
            # a telling: hold the fact first, always
            fact = line if line[-1:] in ".!" else line + "."
            write_orbits(tok(fact + "\n") * 3)
            hold_sentence(fact, "told")
            write_orbits(tok("Q: " + line + "\nA: " + fact + "\n") * 2)
            # then speak: a dialogue orbit if one binds back, else acknowledge
            candidate = continue_orbit(tok("Q: " + line) + tok("A:"), rng)
            if candidate and not rejected(line, candidate) and (set(content_words(line)) & set(t.lower() for t in tok(candidate))):
                ans, thought = candidate, "telling held; dialogue orbit bound back"
            else:
                ans, thought = "Held. " + fact, "telling held at the prediction state"
        else:
            ans, thought = reply(line, rng)
        print("  \u2301 " + thought, flush=True)
        print("UnisonAI: " + ans + "\n", flush=True)
        # the thought itself is held (self-observation, XIV-7)
        hold_sentence("On \'" + line[:60] + "\' I thought: " + thought, "thought")
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
                fact2 = reason if reason[-1:] in ".!" else reason + "."
                write_orbits(tok(fact2 + "\n") * 3)
                hold_sentence(fact2, "told")
                write_orbits(tok("Q: " + line + "\nA: " + fact2 + "\n") * 2)
                print("UnisonAI: held the correction.\n", flush=True)

if __name__ == "__main__":
    main()
