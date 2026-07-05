"""Loss autopsy: play games vs SF at a capped Elo, then have FULL-STRENGTH
Stockfish evaluate every position and name the bot's biggest blunders --
move number, game phase, SAN, and the eval swing. Usage:
    python3 autopsy.py [elo] [games]     (default 1900, 6 games)
"""
import subprocess, sys, chess, chess.engine
from concurrent.futures import ProcessPoolExecutor

import shutil, tempfile, os, atexit
_pin = tempfile.NamedTemporaryFile(delete=False, suffix="_fold_bot")
_pin.close()
shutil.copy2("/Users/mettamazza/Desktop/Smithian Fold Theory/tests/fold_bot_cli", _pin.name)
os.chmod(_pin.name, 0o755)
atexit.register(lambda: os.unlink(_pin.name))
BOT = _pin.name
SF = "/opt/homebrew/bin/stockfish"
ELO = int(sys.argv[1]) if len(sys.argv) > 1 else 1900
GAMES = int(sys.argv[2]) if len(sys.argv) > 2 else 6
PROMO = {chess.QUEEN: 5, chess.ROOK: 4, chess.BISHOP: 3, chess.KNIGHT: 2}
CP = {v: k for k, v in PROMO.items()}


def enc(m):
    return (PROMO[m.promotion] if m.promotion else 0) * 4096 + m.from_square * 64 + m.to_square


def dec(v):
    p, r = v // 4096, v % 4096
    return chess.Move(r // 64, r % 64, promotion=CP[p] if p else None)


def bot_move(hist):
    feed = "\n".join(["12"] + [str(m) for m in hist] + ["8888"]) + "\n"
    return int(subprocess.run([BOT], input=feed, capture_output=True, text=True,
                              timeout=900).stdout.strip().splitlines()[-1])


def phase(board):
    n = len(board.piece_map())
    if board.fullmove_number <= 12:
        return "opening"
    return "endgame" if n <= 10 else "middlegame"


def autopsy_one(g):
    bot_white = g % 2 == 0
    opp = chess.engine.SimpleEngine.popen_uci(SF)
    opp.configure({"UCI_LimitStrength": True, "UCI_Elo": ELO})
    board = chess.Board()
    hist, record = [], []  # record: (ply, bot_moved, san, phase)
    while not board.is_game_over(claim_draw=True) and len(hist) < 240:
        bot_turn = (board.turn == chess.WHITE) == bot_white
        if bot_turn:
            mv = dec(bot_move(hist))
            if mv not in board.legal_moves:
                opp.quit(); return (g, "ILLEGAL", [])
        else:
            mv = opp.play(board, chess.engine.Limit(time=0.05)).move
        record.append((len(hist), bot_turn, board.san(mv), phase(board)))
        board.push(mv); hist.append(enc(mv))
    opp.quit()
    o = board.outcome(claim_draw=True)
    res = "draw(cap)" if o is None else ("draw" if o.winner is None
          else ("win" if (o.winner == chess.WHITE) == bot_white else "loss"))

    # Full-strength evaluation sweep (no Elo cap), bot's perspective.
    judge = chess.engine.SimpleEngine.popen_uci(SF)
    board = chess.Board()
    evals = [0]
    replay = chess.Board()
    moves = []
    b2 = chess.Board()
    for (ply, bot_moved, san, ph) in record:
        moves.append(b2.parse_san(san)); b2.push(moves[-1])
    for mv in moves:
        board.push(mv)
        info = judge.analyse(board, chess.engine.Limit(time=0.25))
        sc = info["score"].pov(chess.WHITE if bot_white else chess.BLACK)
        evals.append(sc.score(mate_score=10000))
    judge.quit()

    # The bot's blunders: eval drop across the bot's own moves.
    drops = []
    for i, (ply, bot_moved, san, ph) in enumerate(record):
        if bot_moved:
            drop = evals[i] - evals[i + 1]
            drops.append((drop, ply, san, ph, evals[i], evals[i + 1]))
    drops.sort(reverse=True)
    # The slide: eval every 10 plies, and the first bot ply after which the
    # position stays below -150 for good (the losing moment).
    curve = [(i, evals[i]) for i in range(0, len(evals), 10)]
    losing_ply = -1
    for i in range(1, len(evals)):
        if evals[i] < -150 and all(e < -150 for e in evals[i:]):
            losing_ply = i
            break
    return (g, res, drops[:3], curve, losing_ply)


if __name__ == "__main__":
    phase_tally = {}
    with ProcessPoolExecutor(max_workers=GAMES) as pool:
        for g, res, top, curve, losing_ply in pool.map(autopsy_one, range(GAMES)):
            print(f"game {g+1} ({'White' if g % 2 == 0 else 'Black'}): {res}", flush=True)
            print("    curve: " + " ".join(f"{p}:{e:+d}" for p, e in curve), flush=True)
            print(f"    goes permanently bad at ply {losing_ply} (move {losing_ply//2+1})" if losing_ply >= 0
                  else "    never permanently bad", flush=True)
            for (drop, ply, san, ph, before, after) in top:
                print(f"    blunder: move {ply//2+1} {san:8s} [{ph:10s}] "
                      f"eval {before:+5d} -> {after:+5d}  (drop {drop})", flush=True)
                if drop >= 150:
                    phase_tally[ph] = phase_tally.get(ph, 0) + 1
    print("BLUNDER PHASES (drops >= 150cp):", phase_tally)
