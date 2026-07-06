import numpy as np, glob
from collections import defaultdict
CTX_MAX = 12
paths = sorted(glob.glob("/Users/mettamazza/Desktop/Smithian Fold Theory/papers/*.md")) + \
        sorted(glob.glob("/Users/mettamazza/Desktop/Smithian Fold Theory/*.md"))
text = "".join(open(p, errors="ignore").read() for p in paths)
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
data = [stoi[c] for c in text[:int(0.9 * len(text))]]
stores = [defaultdict(lambda: defaultdict(int)) for _ in range(CTX_MAX + 1)]
tup = tuple(data)
for i in range(len(tup) - 1):
    nxt = tup[i + 1]
    for L in range(0, CTX_MAX + 1):
        if i - L + 1 < 0: break
        stores[L][tup[i - L + 1:i + 1]][nxt] += 1
V = len(chars)
def predict(ctx):
    for L in range(min(CTX_MAX, len(ctx)), -1, -1):
        s = stores[L].get(tuple(ctx[-L:]) if L else ())
        if s:
            total = sum(s.values())
            p = np.full(V, (1.0 / V) / (total + 1.0))
            for c, n in s.items(): p[c] += n / (total + 1.0)
            return p
    return np.full(V, 1.0 / V)
rng = np.random.default_rng(1)
prompt = "The fold "
ctx = [stoi[c] for c in prompt]
out = list(prompt)
for _ in range(400):
    p = predict(ctx)
    c = int(rng.choice(V, p=p / p.sum()))
    out.append(itos[c]); ctx.append(c)
print("".join(out))
