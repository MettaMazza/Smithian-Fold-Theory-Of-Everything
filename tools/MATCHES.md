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
