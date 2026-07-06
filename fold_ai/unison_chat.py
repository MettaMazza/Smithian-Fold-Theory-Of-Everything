"""UNISON CHAT — the fold-native seed, talkable. Knowledge = every context
read ONCE as exact held orbits (Maria's corpus + lesson files); reply =
unit-capacity selection over the orbit hierarchy, exact rational shares,
No-Zero floor. LIVE LEARNING IS AUTOMATIC (no command): every exchange --
your words AND its own reply -- is written as orbits and persisted the
moment it happens (the 2-to-1 self-observation closure, Claim XIV-7:
the engine holds orbits of its own holding). Usage: python3 unison_chat.py"""
import numpy as np, glob, re, sys, time
from collections import defaultdict

CTX_MAX = 6
LESSONS = sorted(glob.glob("/Users/mettamazza/Desktop/Smithian Fold Theory/fold_ai/lessons/*.txt"))
CORPUS = [f for f in sorted(glob.glob("/Users/mettamazza/Desktop/Smithian Fold Theory/**/*.md", recursive=True)) +
          sorted(glob.glob("/Users/mettamazza/Desktop/SFTOM/**/*.md", recursive=True))
          if "/language/" not in f and "/.git/" not in f]

def tok(s):
    return re.findall(r"\w+|[^\w\s]", s)

print("UnisonAI seed waking: reading everything once...", flush=True)
t0 = time.time()
text = "\n".join(open(f, errors="ignore").read() for f in CORPUS)
lesson_text = "\n".join(open(f, errors="ignore").read() for f in LESSONS)
# lessons are read THREE times -- three written orbits of the dialogue shape
# (writing twice more is writing, not training)
full = text + ("\n" + lesson_text) * 3
words = tok(full)
stores = [defaultdict(lambda: defaultdict(int)) for _ in range(CTX_MAX + 1)]

def write_orbits(token_list):
    for i in range(len(token_list) - 1):
        nxt = token_list[i + 1]
        for L in range(0, CTX_MAX + 1):
            if i - L + 1 < 0:
                break
            stores[L][tuple(token_list[i - L + 1:i + 1])][nxt] += 1

write_orbits(words)
vocab = set()
for s in stores[0].values():
    vocab.update(s.keys())
vocab.update(words[:1])
V = len(vocab) + 1
print(f"awake: {sum(len(s) for s in stores)} orbits from {len(words)} tokens in {time.time()-t0:.0f}s", flush=True)

def predict(ctx):
    for L in range(min(CTX_MAX, len(ctx)), 0, -1):
        s = stores[L].get(tuple(ctx[-L:]))
        if s:
            return s, L
    return stores[1].get((ctx[-1],), {}), 1 if ctx else 0

def reply(history_tokens, rng, max_tokens=70):
    ctx = list(history_tokens)
    out = []
    for _ in range(max_tokens):
        s, L = predict(ctx)
        if not s:
            break
        items = list(s.items())
        counts = np.array([n for _, n in items], dtype=np.float64)
        total = counts.sum()
        probs = counts / (total + 1.0)
        floor = (1.0 / (total + 1.0))
        probs = probs + floor / len(items)
        probs = probs / probs.sum()
        nxt = items[int(rng.choice(len(items), p=probs))][0]
        if nxt == "Q":
            break
        out.append(nxt)
        ctx.append(nxt)
        if nxt in (".", "!", "?") and len(out) > 4:
            break
    s = " ".join(out)
    s = re.sub(r"\s+([.,!?;:])", r"\1", s)
    return s

def main():
    rng = np.random.default_rng()
    print("\nUnisonAI: Hello. I am the seed of UnisonAI. Ask me about the fold, or /teach me something new. (/quit to end)\n", flush=True)
    history = []
    while True:
        try:
            line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line == "/quit":
            break
        if line.startswith("/teach "):
            line = line[7:].strip()  # kept as a courtesy alias; learning is automatic
        q_tokens = tok("Q : " + line + " A :".replace(" : ", ": "))
        q_tokens = tok("Q: " + line) + tok("A:")
        ans = reply(q_tokens, rng)
        if not ans:
            ans = "I have no orbit for that yet. Tell me, and I will hold it."
        print("UnisonAI: " + ans + "\n", flush=True)
        # LIVE LEARNING (automatic, XIV-7 closure): the whole exchange --
        # the user's words and the engine's own reply -- becomes held orbits
        # and persists to the lesson ledger immediately.
        exchange = "Q: " + line + "\nA: " + ans + "\n"
        write_orbits(tok(exchange) * 3)
        with open("/Users/mettamazza/Desktop/Smithian Fold Theory/fold_ai/lessons/lessons_live.txt", "a") as f:
            f.write(exchange)

if __name__ == "__main__":
    main()
