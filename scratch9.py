import sys
sys.path.append("fold_ai")
from unison_chat import *
uc, _ = wake()

question = "What is the capital of the fold?"
answer = "The capital of the fold is the One"
uc.record_correction(question, answer)
cw = content_words(question)
rng = np.random.default_rng(1)

records = [answer]
print("records:", records)
out = babble_closure(records, cw, rng)
print("babble_closure out:", repr(out))
