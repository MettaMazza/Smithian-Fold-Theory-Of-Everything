import sys
sys.path.append("fold_ai")
from unison_chat import *
import random

stores = {1: {("the",): {"one": 3}}, 2: {("is", "the"): {"one": 3}}, 3: {("fold", "is", "the"): {"one": 3}}}

def mixed_next_choice(ctx, rng):
    agg = mixed_dist(ctx)
    if not agg: return None
    items = list(agg.items())
    probs = [float(frac) for _, frac in items]
    total_prob = sum(probs)
    if total_prob <= 0: return None
    return rng.choice([t for t, _ in items], p=[p / total_prob for p in probs])

import numpy as np
rng = np.random.default_rng(0)
ctx = ["fold", "is", "the"]
print("choice next:", mixed_next_choice(ctx, rng))
