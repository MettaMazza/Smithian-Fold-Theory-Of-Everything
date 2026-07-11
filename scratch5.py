import sys
sys.path.append("fold_ai")
from unison_chat import *
uc, _ = wake()
rng = np.random.default_rng(0)

q = "Why is the Smithian Fold Theory considered a unified framework?"
cw = content_words(q)
_icw = {w for w in cw if uc.TOK_FREQ.get(w, 0) <= uc.TOTAL_TOKS / (uc.GEN_B ** 9)}
_has_focus = len(_icw) >= uc.GEN_B

hits = uc.bind(q, top=1)
if hits:
    hit = hits[0]
    hw = {t.lower() for t in tok(hit[0])}
    strong = _has_focus and len(hw & _icw) * uc.GEN_B >= len(_icw)
    print("strong:", strong)
    print("cw:", cw)
    print("_icw:", _icw)
    print("hw:", hw)
    print("overlap:", hw & _icw)
else:
    print("No hits")

