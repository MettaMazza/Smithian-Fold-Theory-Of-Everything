import sys
sys.path.append("fold_ai")
from unison_chat import *
# skip the slow graph_genesis and wake
# just test babble_closure
record_correction("What is the capital of the fold?", "The capital of the fold is the One")
rng = np.random.default_rng(0)
cw = content_words("What is the capital of the fold?")
ans = babble_closure(["The capital of the fold is the One"], cw, rng)
print("E4 Output:", ans)
