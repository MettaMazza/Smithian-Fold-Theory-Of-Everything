"""Offline conversation test harness: drives the engine's own functions
directly (no subprocess, no stale ledgers) and checks each turn."""
import importlib.util, sys, io, contextlib

# load the engine module but suppress its wake print and skip main()
spec = importlib.util.spec_from_file_location("uc", "unison_chat.py")
uc = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    # prevent main() from running on import: it's guarded by __main__, fine
    spec.loader.exec_module(uc)

import numpy as np
rng = np.random.default_rng(0)

def say(line):
    """Replicate the loop's turn logic and return (answer)."""
    is_question = line.endswith("?") or line.lower().startswith(
        ("what","who","how","why","when","where","do ","does","did","can ","is ","are "))
    import re as _re
    is_command = bool(_re.match(r"(?i)\s*(say|repeat after me|respond with|reply with)\b", line))
    if not is_question and not is_command:
        if not uc.content_words(line):
            return "okay."
        got = uc.learn_fact(line)
        fact = uc.flip_perspective(line if line[-1:] in ".!" else line + ".")
        uc.write_orbits(uc.tok(fact + "\n") * 3)
        uc.hold_sentence(fact, "told")
        if got:
            return "Held. fact"
        return "Held: " + fact
    ans, _ = uc.reply(line, rng)
    return ans

TESTS = [
    ("My name is Maria",              lambda a: "held" in a.lower()),
    ("What is my name?",              lambda a: a == "Your name is Maria."),
    ("I live in Scotland",            lambda a: "held" in a.lower()),
    ("Where do I live?",              lambda a: a == "You live in Scotland."),
    ("My favourite colour is green",  lambda a: "held" in a.lower()),
    ("What is my favourite colour?",  lambda a: "green" in a.lower() and "A:" not in a),
    ("What is the fold?",             lambda a: "One" in a or "fold" in a.lower()),
    ("Say yes",                       lambda a: a.strip().lower() == "yes."),
    ("Repeat after me: the fold is one", lambda a: a.strip().lower() == "the fold is one."),
]
passed = 0
for line, check in TESTS:
    a = say(line)
    ok = check(a)
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] {line!r:40s} -> {a!r}")
print(f"\n{passed}/{len(TESTS)} turns pass")
