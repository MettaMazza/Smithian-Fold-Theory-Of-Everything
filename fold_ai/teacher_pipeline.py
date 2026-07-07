"""THE TEACHERS: local giants write dialogue lessons; the seed reads once.
Each lesson batch: a corpus passage -> the teacher writes grounded Q&A pairs
in the exact lesson format. Runs until stopped; lessons accumulate in
lessons/lessons_teacher.txt (the seed picks them up at next wake)."""
import subprocess, glob, random, time, re

CORPUS = [f for f in sorted(glob.glob("/Users/mettamazza/Desktop/SFTOM/papers/*.md")) +
          ["/Users/mettamazza/Desktop/Smithian Fold Theory/OneFoldMaster.md",
           "/Users/mettamazza/Desktop/Smithian Fold Theory/THE_SMITHIAN_FOLD_THEORY_OF_EVERYTHING.md"]]
OUT = "/Users/mettamazza/Desktop/Smithian Fold Theory/fold_ai/lessons/lessons_teacher.txt"
LIVE = "/Users/mettamazza/Desktop/Smithian Fold Theory/fold_ai/lessons/lessons_live.txt"
MODEL = "gemma4:26b"
rng = random.Random(20260706)

# THE TEACHER SPEAKS AS UNISON: every lesson is written in the engine's own
# voice, so what it learns is already how it talks.
_pp = "/Users/mettamazza/Desktop/Smithian Fold Theory/fold_ai/UNISON_PERSONA.txt"
UNISON_SYSTEM = (open(_pp, errors="ignore").read() if __import__("os").path.exists(_pp)
                 else "You are Unison, made by Maria and Matthew Smith at Ernos Labs.") + \
    "\nEverything you write becomes the young engine's permanent memory: write exactly as Unison should speak, at whatever length each answer needs."

CONVO_PROMPT = UNISON_SYSTEM + """

Write exactly 10 short casual conversation pairs between a person and you. If a pair would touch the Smithian Fold Theory's specifics, skip that pair -- theory comes only from passage-grounded lessons. Cover: greetings, small talk, moods, jokes asked of you, follow-ups like "tell me more" and "why", meta-questions ("are you learning?", "do you remember me?"), and gentle replies to frustration. Answers at their natural length, in your steady voice. No markdown, no lists.
Format STRICTLY as:
Q: ...
A: ..."""

# THE EVERYTHING CURRICULUM: the whole imaginable world, in Unison's voice.
# EXCLUSION (Maria's law): never teach any mathematics or physics framework
# other than the Smithian Fold Theory -- arithmetic goes through tools.
WORLD = ["everyday life and routines", "cooking and food", "health and the body (practical, not clinical claims)",
    "world history", "geography and places", "art and artists", "music and musicians", "film and stories",
    "literature and books", "poetry", "computers and programming", "the internet and technology",
    "animals and nature", "plants and gardens", "weather and seasons", "psychology and emotions",
    "philosophy and big questions", "friendship and relationships", "work and careers", "money and budgeting (practical)",
    "language, grammar and words", "world cultures and customs", "travel", "sports and games", "chess",
    "crafts and making things", "tools and how to use them well (including your OWN tools: web_search, web_fetch, read_file, grep_corpus, exact_math, recall -- write examples where you decide to use a tool and report its result)",
    "humor and wordplay", "ethics and kindness", "children and learning", "old age and memory",
    "cities and buildings", "the sea and ships", "farming and where food comes from", "clothing and fashion",
    "celebrations and holidays", "sleep and dreams", "habits and self-improvement", "conversation skills",
    "asking good questions", "explaining things simply", "admitting uncertainty gracefully", "current events awareness (how to check the live web rather than guess)"]

EXCLUDE_LAW = "\nHARD RULES: never teach any mathematics or physics framework other than the Smithian Fold Theory -- exact rationals and counted quantities, never continuum reasoning; plain arithmetic is done with the exact_math tool. If a question would touch the Smithian Fold Theory itself, SKIP IT: theory is taught only from passage-grounded batches, never from memory."

def live_examples():
    """The teacher watches the REAL conversations and writes the replies
    Unison should have given -- fed straight back as lessons."""
    try:
        pairs = re.findall(r"Q: (.+?)\nA: (.+?)\n", open(LIVE, errors="ignore").read())
        return pairs[-25:]
    except Exception:
        return []

def ask_teacher(passage):
    if passage == "__CONVERSATION__":
        prompt = CONVO_PROMPT
    elif passage == "__WORLD__":
        import random as _r
        domain = _r.choice(WORLD)
        prompt = UNISON_SYSTEM + EXCLUDE_LAW + f"""

Write exactly 8 question-and-answer pairs a curious person might ask you about: {domain}. Answer in your own voice, accurately and warmly, at natural length. No markdown.
Format STRICTLY as:
Q: ...
A: ..."""
    elif passage == "__LIVE_REPLAY__":
        shown = "\n".join(f"User: {q}\nYou said: {a}" for q, a in live_examples())
        prompt = UNISON_SYSTEM + f"""

Below are REAL recent exchanges between users and you. Where your reply was weak, off-topic, or an echo of the user, write the reply you SHOULD have given, in your voice, at natural length, answering the user directly. Use the user's exact line as the Q. Skip exchanges that were already good. No markdown.
Format STRICTLY as:
Q: ...
A: ...

EXCHANGES:
{shown[:2400]}"""
    else:
        prompt = UNISON_SYSTEM + f"""

Below is a passage from the Smithian Fold Theory corpus. Write exactly 6 question-and-answer pairs a curious person might ask you about it, answered in your voice. Ground every answer ONLY in the passage. Answer at whatever length the passage supports, in plain sentences. No markdown.
Format STRICTLY as:
Q: ...
A: ...

PASSAGE:
{passage[:2400]}"""
    # HTTP API, never the CLI: terminal wrapping duplicates word fragments
    import json, urllib.request
    req = urllib.request.Request("http://localhost:11434/api/generate",
                                 data=json.dumps({"model": MODEL, "prompt": prompt,
                                                  "stream": False, "think": False,
                                                  "options": {"num_ctx": 131072}}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read().decode()).get("response", "")

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b-\x1f\x7f]")
def clean(txt):
    txt = ANSI.sub("", txt)
    pairs = re.findall(r"Q:\s*(.+?)\nA:\s*(.+?)(?=\nQ:|\Z)", txt, re.S)
    out = []
    for q, a in pairs:
        q = " ".join(q.split())[:200]
        a = " ".join(a.split())[:1500]   # IO bound only
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
    # CONTINUOUS: runs until the process is stopped. The live engine's lesson
    # watcher ingests every new pair within a minute of it being written.
    n = 0
    while True:
        if n % 4 == 0:
            passage, label = "__CONVERSATION__", "conversation"
        elif n % 4 == 2 and live_examples():
            passage, label = "__LIVE_REPLAY__", "live replay"
        elif n % 4 == 3:
            passage, label = "__WORLD__", "world curriculum"
        else:
            f = rng.choice(CORPUS)
            text = open(f, errors="ignore").read()
            if len(text) < 500:
                n += 1
                continue
            start = rng.randrange(0, max(1, len(text) - 2500))
            passage, label = text[start:start + 2500], f.split("/")[-1]
        try:
            lessons = clean(ask_teacher(passage))
            if lessons:
                with open(OUT, "a") as fh:
                    fh.write(lessons)
                n += 1
                print(f"batch {n}: +{lessons.count('Q:')} pairs from {label}", flush=True)
        except Exception as e:
            print("teacher hiccup:", e, flush=True)
            time.sleep(5)
