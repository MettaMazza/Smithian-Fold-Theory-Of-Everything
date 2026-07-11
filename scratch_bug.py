import fold_ai.unison_chat as U
import numpy as np

U.write_orbits("Q: very good\nA: Thank you.\n", repeat=U.GEN_B)

rng = np.random.default_rng()
line = "very good"
candidate = U.continue_orbit(U.tok("Q: " + line + "\nA: "), rng)
print("Candidate:", candidate)

_sh = {w for w in set(U.content_words(line)) & set(t.lower() for t in U.tok(candidate or ""))
       if len(U.tok(line)) < 6 or U.TOK_FREQ.get(w, 0) <= U.TOTAL_TOKS / (U.GEN_B ** 9)}
print("_sh:", _sh)

ctx = U.tok("Q: " + line + "\nA: ")
L = min(U.CTX_MAX, len(ctx))
k = U._key(ctx[-L:])
is_reflex = bool(U.stores[L][k])
print("is_reflex:", is_reflex)
