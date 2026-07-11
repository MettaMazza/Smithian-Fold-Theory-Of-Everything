from fractions import Fraction
import random
from math import lcm

stores = {1: {("the",): {"one": 3}}, 2: {("is", "the"): {"one": 3}}, 3: {("fold", "is", "the"): {"one": 3}}}

def mixed_dist(ctx):
    agg = {}
    for L in range(min(3, len(ctx)), 0, -1):
        s = stores.get(L, {}).get(tuple(ctx[-L:]))
        if s:
            total = sum(s.values())
            w = Fraction(2 ** L)
            for tkn, n in s.items():
                agg[tkn] = agg.get(tkn, Fraction(0)) + w * Fraction(n, total)
    return agg

def mixed_next(ctx, rng):
    agg = mixed_dist(ctx)
    if not agg: return None
    items = list(agg.items())
    cd = 1
    for _, frac in items: cd = lcm(cd, frac.denominator)
    scaled_probs = [frac.numerator * (cd // frac.denominator) for _, frac in items]
    total_prob = sum(scaled_probs)
    if total_prob <= 0: return None
    _r = random.Random(int(rng.integers(0, 2**31 - 1)))
    pick = _r.randrange(total_prob)
    running = 0
    for i, p in enumerate(scaled_probs):
        running += p
        if pick < running: return items[i][0]
    return items[-1][0]

import numpy as np
rng = np.random.default_rng(0)
ctx = ["fold", "is", "the"]
print("next:", mixed_next(ctx, rng))
