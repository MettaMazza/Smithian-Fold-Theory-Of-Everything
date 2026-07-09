"""Engine gate: current bot vs a prior version, 12 parallel refereed games.
Usage: python3 h2h_gate.py <path_to_old_cli> <output>"""
import subprocess, chess, sys
from concurrent.futures import ProcessPoolExecutor
NEW = "/Users/mettamazza/Desktop/Smithian Fold Theory/tests/fold_bot_cli"
OLD = sys.argv[1]
PROMO = {chess.QUEEN:5, chess.ROOK:4, chess.BISHOP:3, chess.KNIGHT:2}
CP = {v:k for k,v in PROMO.items()}
def enc(m): return (PROMO[m.promotion] if m.promotion else 0)*4096 + m.from_square*64 + m.to_square
def dec(v):
    p,r = v//4096, v%4096
    return chess.Move(r//64, r%64, promotion=CP[p] if p else None)
def bot_move(binary, hist):
    feed = "\n".join(["12"]+[str(m) for m in hist]+["8888"])+"\n"
    return int(subprocess.run([binary], input=feed, capture_output=True, text=True, timeout=1800).stdout.strip().splitlines()[-1])
OPENINGS = ["e2e4 e7e5 g1f3 b8c6", "d2d4 d7d5 c2c4 e7e6", "e2e4 c7c5",
            "d2d4 g8f6 c2c4 g7g6", "e2e4 e7e6 d2d4 d7d5", "c2c4 e7e5"]
def play_one(g):
    new_white = g % 2 == 0
    board = chess.Board(); hist = []
    for uci in OPENINGS[g // 2].split():
        mv = chess.Move.from_uci(uci)
        board.push(mv); hist.append(enc(mv))
    while not board.is_game_over(claim_draw=True) and len(hist) < 240:
        new_turn = (board.turn == chess.WHITE) == new_white
        mv = dec(bot_move(NEW if new_turn else OLD, hist))
        if mv not in board.legal_moves: return (g, "ILLEGAL:"+("new" if new_turn else "old"))
        board.push(mv); hist.append(enc(mv))
    o = board.outcome(claim_draw=True)
    if o is None or o.winner is None: return (g, "draw")
    return (g, "new" if (o.winner == chess.WHITE) == new_white else "old")
if __name__ == "__main__":
    tally = {}
    # PARALLEL GAMES (M3 ULTRA 32-CORE): the v19 bot spawns 8 root workers per move.
    # We run 3 games concurrently (max_workers=3), which spawns at most 24 worker
    # processes + 3 baseline threads = 27 active threads. This fits comfortably
    # within the 32 physical cores of the M3 Ultra, preventing CPU starvation
    # while completing the 12-game tournament 3x faster.
    with ProcessPoolExecutor(max_workers=3) as pool:
        for g, r in pool.map(play_one, range(12)):
            tally[r] = tally.get(r, 0) + 1
            print(f"game {g+1}: {r}", flush=True)
    print("GATE RESULT (new vs old):", tally)
