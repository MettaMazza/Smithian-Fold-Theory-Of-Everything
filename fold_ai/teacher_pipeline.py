"""THE TEACHERS: local giants write dialogue lessons; the seed reads once.
Each lesson batch: a corpus passage -> the teacher writes grounded Q&A pairs
in the exact lesson format. Runs until stopped; lessons accumulate in
lessons/lessons_teacher.txt (the seed picks them up at next wake)."""
import subprocess, glob, random, time, re

CORPUS = [f for f in sorted(glob.glob("/Users/mettamazza/Desktop/SFTOM/papers/*.md")) +
          ["/Users/mettamazza/Desktop/Smithian Fold Theory/OneFoldMaster.md",
           "/Users/mettamazza/Desktop/Smithian Fold Theory/THE_SMITHIAN_FOLD_THEORY_OF_EVERYTHING.md"]]
OUT = "/Users/mettamazza/Desktop/Smithian Fold Theory/fold_ai/lessons/lessons_teacher.txt"
MODEL = "gemma4:26b"
rng = random.Random(20260706)

def ask_teacher(passage):
    prompt = f"""Below is a passage from the Smithian Fold Theory corpus. Write exactly 6 question-and-answer pairs a curious person might ask about it. Ground every answer ONLY in the passage. Keep answers to 1-2 plain sentences. Also include 2 general conversational pairs (greetings, how are you, what can you do) answered in the voice of UnisonAI, a fold-native engine whose knowledge is written as exact orbits.
Format STRICTLY as:
Q: ...
A: ...

PASSAGE:
{passage[:2400]}"""
    r = subprocess.run(["ollama", "run", MODEL], input=prompt,
                       capture_output=True, text=True, timeout=600)
    return r.stdout

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b-\x1f\x7f]")
def clean(txt):
    txt = ANSI.sub("", txt)
    pairs = re.findall(r"Q:\s*(.+?)\nA:\s*(.+?)(?=\nQ:|\Z)", txt, re.S)
    out = []
    for q, a in pairs:
        q = " ".join(q.split())[:200]
        a = " ".join(a.split())[:350]
        # strict validation: single clean pair, sentence-like, no leaked markup
        if not (10 < len(q) and 10 < len(a)):
            continue
        if any(bad in q + a for bad in ("Q:", "A:", "```", "PASSAGE", "* ", "..", "\x1b")):
            continue
        if not q.rstrip().endswith("?") and not q[:1].isupper():
            continue
        out.append(f"Q: {q}\nA: {a}\n")
    return "".join(out)

if __name__ == "__main__":
    n = 0
    while n < 200:
        f = rng.choice(CORPUS)
        text = open(f, errors="ignore").read()
        if len(text) < 500:
            continue
        start = rng.randrange(0, max(1, len(text) - 2500))
        passage = text[start:start + 2500]
        try:
            lessons = clean(ask_teacher(passage))
            if lessons:
                with open(OUT, "a") as fh:
                    fh.write(lessons)
                n += 1
                print(f"batch {n}: +{lessons.count('Q:')} pairs from {f.split('/')[-1]}", flush=True)
        except Exception as e:
            print("teacher hiccup:", e, flush=True)
            time.sleep(5)
    print("TEACHING SESSION COMPLETE", flush=True)
