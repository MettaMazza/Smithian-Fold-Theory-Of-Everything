import sys
sys.path.append("fold_ai")
from unison_chat import *
uc, _ = wake()
rng = np.random.default_rng(0)

print("Before:")
print("qkey:", qkey("What is the capital of the fold?"))
print("content_words:", content_words("What is the capital of the fold?"))

uc.record_correction("What is the capital of the fold?", "The capital of the fold is the One")

print("After:")
print("qkey:", qkey("What is the capital of the fold?"))
print("content_words:", content_words("What is the capital of the fold?"))
