from fractions import Fraction

TOK_FREQ = {"what": 1000, "the": 10000, "capital": 3, "fold": 5000, "one": 3}
TOTAL_TOKS = 21950931
CTX_MAX = 6

def tok(s):
    import re
    return [t for t in re.split(r"([.,!?:;\"'()\[\]{}\s])", s) if t.strip()]

def informativeness_old(w):
    f = TOK_FREQ.get(w.lower(), 0)
    return 0.0 if f == 0 else TOTAL_TOKS / f

def content_words_old(s):
    ws = [t.lower() for t in tok(s) if len(t) > 2]
    scored = [(informativeness_old(w), w) for w in ws]
    scored = [x for x in scored if x[0] > 0]
    scored.sort(reverse=True)
    return [w for _, w in scored[:CTX_MAX]]

def informativeness_new(w):
    f = TOK_FREQ.get(w.lower(), 0)
    return Fraction(0) if f == 0 else Fraction(TOTAL_TOKS, f)

def content_words_new(s):
    ws = [t.lower() for t in tok(s) if len(t) > 2]
    scored = [(informativeness_new(w), w) for w in ws]
    scored = [x for x in scored if x[0] > 0]
    scored.sort(reverse=True)
    return [w for _, w in scored[:CTX_MAX]]

q = "What is the capital of the fold?"
print("old:", content_words_old(q))
print("new:", content_words_new(q))
