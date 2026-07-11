import re
def dedup(s):
    out = []
    for t in s.split():
        if not out or out[-1].lower() != t.lower():
            out.append(t)
    s = re.sub(r"\s+([.,!?;:])", r"\1", " ".join(out))
    return re.sub(r"(\w)\s*'\s*(s|t|re|ve|ll|d|m)\b", r"\1'\2", s)

def _skey(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

walk = "The capital of the fold is the One .".split()
out = dedup(" ".join(walk))
out = " ".join(re.split(r"(?<=[.!?])\s+", out.strip())[:1])
print("out:", repr(out))
print("skey out:", repr(_skey(out)))

rec = "The capital of the fold is the One."
print("skey rec:", repr(_skey(rec)))
print("Match?", _skey(out) == _skey(rec))
