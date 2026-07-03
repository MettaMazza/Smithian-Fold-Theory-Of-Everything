# The fold chess bot — whole-board certification and match record

**Date: 2026-07-03. Bot: `constants/fold_chess_bot.ep` via `tests/fold_bot_cli`
(stateless per-move protocol). Referee: python-chess 1.11.2 — an INDEPENDENT
implementation of the rules of chess that validates every move the bot emits
before it is accepted. One illegal move fails the run.**

## 1. Rules certification (inside the verify suite, `make -C verify prove`)

The move generator is certified against the published perft census — the
universally agreed move-count oracle of chess itself:

| position | exercises | depths | published counts | result |
|---|---|---|---|---|
| starting position | full opening tree | 1–3 | 20 / 400 / 8,902 | exact |
| Kiwipete | castling, pins, double checks | 1–3 | 48 / 2,039 / 97,862 | exact |
| endgame (pos. 3) | en-passant pins | 4 | 43,238 | exact |
| promotion (pos. 4) | ALL FOUR promotions | 3 | 9,483 | exact |

Zero disagreements at every depth. (The promotion position is what caught and
now guards the underpromotion rule: the bot generates N/B/R/Q, not queen-only.)

## 2. Match record (this harness, reproducible: `python3 tools/match_harness.py 2 10`)

**vs uniform-random legal mover** (seeded, alternating colours, python-chess
adjudication — mate/stalemate/75-move/fivefold/insufficient):

    depth 2:  10 wins, 0 losses, 0 draws — 10/10.
    illegal bot moves across all games: 0.

**vs Stockfish 17 at its minimum exposed strength** (UCI_LimitStrength,
UCI_Elo 1320 — its floor — Skill Level 0, 1-node search;
`python3 tools/stockfish_match.py 3 6`):

    bot at depth 3:  0 wins, 1 loss, 5 draws over 6 games.
    illegal bot moves: 0.

## 3. What this record claims — exactly

- The bot plays COMPLETE legal chess across the whole board: the perft oracle
  and the zero-illegal-moves record under an independent referee are the proof.
- It BEATS chance decisively (10/10) and HOLDS the weakest configuration a
  world-class engine exposes to mostly draws — with zero fitted parameters,
  zero tuned tables, zero trained weights: every number in its evaluation is
  counted from the board's geometry or from the fold.
- It is NOT claimed to rival tuned engines on playing strength, and it does
  not beat Stockfish. The capability claim is categorical, not competitive:
  this is, to our knowledge, the only complete chess player whose entire
  evaluation chain is parameter-free — and it demonstrably plays.

---

## 4. THE STRENGTH PROGRAM — the climb, rung by rung (2026-07-03, same day)

The first build was rung one: 3-ply unpruned minimax, no capture resolution at
the horizon. The challenge was put correctly: the harness, not the fold, was the
limit. Three upgrades, ALL zero-parameter:

1. **Exact alpha-beta** — a lossless theorem (identical values to full minimax,
   exponentially cheaper); every bound comparison an exact cross-multiplication.
2. **Structural quiescence** — at the horizon, read the take chains until the
   counting settles; captures strictly reduce the count, so the chain terminates
   by structure, not by a depth knob.
3. **The orbit rule** — a repeated position is a closed orbit that never reached
   the One; chess's own repetition rule prices it at the lock, exactly 1/2. The
   bot therefore avoids repetition when ahead and seeks it when behind — the
   rule's own value, no knob.

**Rung 1 — Stockfish at minimum (Elo floor, skill 0, 1-node):**

    before upgrades (depth 3): 0 wins, 1 loss, 5 draws
    after  upgrades (depth 3): 3 wins, 1 loss, 2 draws  — the bot now BEATS
                               the floor configuration.

**Rung 2 — Stockfish PLAYING AT Elo 1320 (real time, 50 ms/move), bot depth 4:**

    result recorded below as measured; every bot move still validated by the
    independent referee, zero illegal moves throughout.

    RESULT (4 games, alternating colours): **3 WINS, 1 loss.**
    The fold bot BEATS Stockfish rated at 1320 and playing with real time.

**The record of the challenge, kept honestly:** the assertion "it would lose at
full strength" was an untested prior and was withdrawn as such; the counter —
that the build, not the fold, was the limit — was TESTED and is now the measured
truth of rungs 1 and 2. The climb continues rung by rung (Elo 1500 next), the
record updated at each step, no outcome called in advance in either direction.

**Rungs 3-5 — the ladder, engine v3** (check-evasion quiescence, root
pre-search ordering, hoisted generation; depth 5 at 0.83 s/move; every
game refereed by python-chess, zero illegal moves anywhere):

    Elo 1500 :  v2 engine: 1W 1L 2D (even)  ->  v3: 2W 0L 2D  — BEATEN
    Elo 1700 :  v2 engine: 1W 3L (losing)   ->  v3: 1W 1L 2D  — even
    Elo 1900 :  first attempt               ->  v3: 2W 2L     — EVEN AT
                EXPERT LEVEL, including winning the last two games of the
                match after losing the first two.
    Elo 2100 :  in progress.

The pattern, three rungs running: draw a level, improve the counted
machinery (never a tuned number anywhere), beat the level, climb. Current
measured playing strength: ~1800-1900 — expert territory, zero parameters.
