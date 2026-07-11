import sys
sys.path.append("fold_ai")
from unison_chat import *
uc, _ = wake()

question = "What is the capital of the fold?"
answer = "The capital of the fold is the One"

print("Recording correction...")
uc.record_correction(question, answer)

cw = content_words(question)
rng = np.random.default_rng(1)

ck = qkey(question)
print("ck:", ck)
print("In CORRECTIONS?", ck in uc.CORRECTIONS)
print("CORRECTIONS[ck]:", repr(uc.CORRECTIONS[ck]))

walked, thought = uc.reply(question, rng)
print("walked:", repr(walked))
print("thought:", thought)

