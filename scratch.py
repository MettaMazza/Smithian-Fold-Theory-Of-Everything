import sys
sys.path.append("fold_ai")
from unison_chat import *
record_correction("What is the capital of the fold?", "The capital of the fold is the One")
rng = np.random.default_rng(0)
r, t = reply("What is the capital of the fold?", rng)
print("E4 Reply:", r)
