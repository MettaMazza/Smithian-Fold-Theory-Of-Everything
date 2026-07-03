"""Match harness: the fold chess bot vs an opponent, refereed by python-chess.

python-chess is the INDEPENDENT rules oracle: every move the fold bot emits is
checked against board.legal_moves before being accepted; one illegal move fails
the run. Games are adjudicated by full chess rules (mate, stalemate, insufficient
material, 75-move, fivefold). The bot binary is stateless per call: it receives
the depth, the move list so far, then the sentinel 8888, and prints its move.
"""
import subprocess, sys, random
import chess

BOT = "/Users/mettamazza/Desktop/Smithian Fold Theory/tests/fold_bot_cli"
PROMO_CODE = {chess.QUEEN: 5, chess.ROOK: 4, chess.BISHOP: 3, chess.KNIGHT: 2}
CODE_PROMO = {v: k for k, v in PROMO_CODE.items()}

def encode(move: chess.Move) -> int:
    promo = PROMO_CODE[move.promotion] if move.promotion else 0
    return promo * 4096 + move.from_square * 64 + move.to_square

def decode(value: int, board: chess.Board) -> chess.Move:
    promo = value // 4096
    rest = value % 4096
    mv = chess.Move(rest // 64, rest % 64,
                    promotion=CODE_PROMO[promo] if promo else None)
    # bare king-two-files / plain encodings are already python-chess UCI shapes
    return mv

def bot_move(depth: int, history: list[int]) -> int:
    feed = "\n".join([str(depth)] + [str(m) for m in history] + ["8888"]) + "\n"
    out = subprocess.run([BOT], input=feed, capture_output=True, text=True, timeout=300)
    return int(out.stdout.strip().splitlines()[-1])

def play_game(depth: int, bot_is_white: bool, seed: int, max_plies=240):
    rng = random.Random(seed)
    board = chess.Board()
    history = []
    illegal = 0
    while not board.is_game_over(claim_draw=True) and len(history) < max_plies:
        if board.turn == chess.WHITE and bot_is_white or board.turn == chess.BLACK and not bot_is_white:
            value = bot_move(depth, history)
            mv = decode(value, board)
            if mv not in board.legal_moves:
                illegal += 1
                print(f"  ILLEGAL from bot: {mv.uci()} in {board.fen()}")
                return "illegal", illegal
            board.push(mv)
            history.append(value)
        else:
            mv = rng.choice(list(board.legal_moves))
            board.push(mv)
            history.append(encode(mv))
    outcome = board.outcome(claim_draw=True)
    if outcome is None:
        return "draw(cap)", illegal
    if outcome.winner is None:
        return "draw", illegal
    bot_won = (outcome.winner == chess.WHITE) == bot_is_white
    return ("win" if bot_won else "loss"), illegal

def main():
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    games = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    results = {"win": 0, "loss": 0, "draw": 0, "draw(cap)": 0, "illegal": 0}
    total_illegal = 0
    for g in range(games):
        res, ill = play_game(depth, bot_is_white=(g % 2 == 0), seed=1000 + g)
        results[res] += 1
        total_illegal += ill
        print(f"game {g+1:2d} (bot as {'White' if g%2==0 else 'Black'}): {res}")
    print(f"\nRESULT vs random mover, depth {depth}: "
          f"{results['win']}W {results['loss']}L {results['draw']+results['draw(cap)']}D "
          f"(caps: {results['draw(cap)']}) | illegal bot moves: {total_illegal}")

if __name__ == "__main__":
    main()
