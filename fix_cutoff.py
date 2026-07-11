import sys
with open("fold_ai/unison_chat.py", "r") as f:
    text = f.read()

text = text.replace("TOTAL_TOKS / (GEN_B ** 10)", "TOTAL_TOKS / (GEN_B ** 9)")

with open("fold_ai/unison_chat.py", "w") as f:
    f.write(text)
print("Done")
