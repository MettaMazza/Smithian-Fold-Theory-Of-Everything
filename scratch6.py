import sys
sys.path.append("fold_ai")
from unison_chat import *
uc, _ = wake()

q = "What is the capital of the fold?"
a = "The capital of the fold is the One."
print("Before record:")
print("cw:", content_words(q))
print("qkey:", qkey(q))

uc.record_correction(q, a)

print("After record:")
print("cw:", content_words(q))
print("qkey:", qkey(q))
print("In CORRECTIONS?", qkey(q) in uc.CORRECTIONS)
