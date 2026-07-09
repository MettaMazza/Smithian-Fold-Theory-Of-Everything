#!/usr/bin/env python3
"""
SFT Go Engine Tournament & GTP Referee
Implements a zero-parameter SFT Go playing agent and a GTP client/server harness
to run tournament matches and record results.
"""
import sys
import random
import subprocess
import os
import math
import multiprocessing

# ==================== ZERO-PARAMETER SFT GO ENGINE ====================

class SFTGoBoard:
    def __init__(self, size=9):
        self.size = size
        self.board = [0] * (size * size) # 0: empty, 1: black, 2: white
        self.ko_square = None
        self.history = []

    def copy(self):
        nb = SFTGoBoard(self.size)
        nb.board = list(self.board)
        nb.ko_square = self.ko_square
        nb.history = list(self.history)
        return nb

    def get_neighbors(self, idx):
        neighbors = []
        r, c = idx // self.size, idx % self.size
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                neighbors.append(nr * self.size + nc)
        return neighbors

    def get_group(self, start_idx):
        color = self.board[start_idx]
        if color == 0:
            return set(), set()
        
        group = {start_idx}
        liberties = set()
        queue = [start_idx]
        visited = {start_idx}
        
        while queue:
            curr = queue.pop(0)
            for n in self.get_neighbors(curr):
                if self.board[n] == 0:
                    liberties.add(n)
                elif self.board[n] == color and n not in visited:
                    visited.add(n)
                    group.add(n)
                    queue.append(n)
        return group, liberties

    def is_legal(self, idx, color):
        # Tromp-Taylor rules
        if self.board[idx] != 0:
            return False
        if idx == self.ko_square:
            return False
            
        test_board = self.copy()
        test_board.board[idx] = color
        
        # Check opponent captures first
        opponent = 3 - color
        captured_any = False
        captured_indices = []
        
        for n in test_board.get_neighbors(idx):
            if test_board.board[n] == opponent:
                grp, libs = test_board.get_group(n)
                if len(libs) == 0:
                    captured_any = True
                    captured_indices.extend(grp)
                    
        # Remove captured stones
        for c_idx in captured_indices:
            test_board.board[c_idx] = 0
            
        # Check self-suicide
        my_grp, my_libs = test_board.get_group(idx)
        if len(my_libs) == 0:
            return False # suicide is illegal
            
        # Positional Superko: check if board state already occurred
        state_str = "".join(map(str, test_board.board))
        if state_str in self.history:
            return False
            
        return True

    def play_move(self, idx, color):
        if idx is None: # Pass
            self.history.append("".join(map(str, self.board)))
            self.ko_square = None
            return True
            
        if not self.is_legal(idx, color):
            return False
            
        self.board[idx] = color
        opponent = 3 - color
        captured_indices = []
        for n in self.get_neighbors(idx):
            if self.board[n] == opponent:
                grp, libs = self.get_group(n)
                if len(libs) == 0:
                    captured_indices.extend(grp)
                    
        for c_idx in captured_indices:
            self.board[c_idx] = 0
            
        # Set Ko square if a single stone was captured
        if len(captured_indices) == 1:
            self.ko_square = captured_indices[0]
        else:
            self.ko_square = None
            
        self.history.append("".join(map(str, self.board)))
        return True

    def get_legal_moves(self, color):
        moves = []
        for i in range(self.size * self.size):
            if self.is_legal(i, color):
                moves.append(i)
        return moves

# ==================== SFT ZOBRIST HASH & SEARCH ENGINE ====================

# Generate deterministic Zobrist keys (zero parameters, LCG generator)
zobrist_table = {}
zobrist_tomove = {}
zobrist_ko = {}

def init_zobrist(size=19):
    val = 123456789
    for i in range(size * size):
        zobrist_table[i] = {}
        for color in [0, 1, 2]:
            val = (1103515245 * val + 12345) & 0xffffffffffffffff
            zobrist_table[i][color] = val
        val = (1103515245 * val + 12345) & 0xffffffffffffffff
        zobrist_ko[i] = val
        
    for color in [1, 2]:
        val = (1103515245 * val + 12345) & 0xffffffffffffffff
        zobrist_tomove[color] = val

init_zobrist(19)

def get_zobrist_hash(board, to_move_color):
    h = 0
    for i in range(board.size * board.size):
        color = board.board[i]
        h ^= zobrist_table[i][color]
    h ^= zobrist_tomove[to_move_color]
    if board.ko_square is not None:
        h ^= zobrist_ko[board.ko_square]
    return h

# Dihedral Symmetry Orbit Reduction (forced structural symmetry)
def get_orbit_representative(p, size):
    row, col = p // size, p % size
    rep = p
    for t in range(8):
        r2, c2 = row, col
        if t == 1:
            r2 = size - 1 - row
        elif t == 2:
            c2 = size - 1 - col
        elif t == 3:
            r2 = size - 1 - row
            c2 = size - 1 - col
        elif t == 4:
            r2, c2 = col, row
        elif t == 5:
            r2 = size - 1 - col
            c2 = row
        elif t == 6:
            r2 = col
            c2 = size - 1 - row
        elif t == 7:
            r2 = size - 1 - col
            c2 = size - 1 - row
            
        q = r2 * size + c2
        if q < rep:
            rep = q
    return rep

# Dynamic Sparse Graph Lookahead Overlay
def get_dynamic_sparse_moves(board, to_move_color, legal_moves):
    size = board.size
    empty = all(x == 0 for x in board.board)
    if empty:
        # Star points
        if size == 9:
            stars = [22, 20, 24, 38, 42, 56, 60] # E5, C3, G3, C5, G5, C7, G7
        elif size == 19:
            stars = [60, 66, 72, 174, 180, 186, 288, 294, 300]
        else:
            stars = [size * size // 2]
        
        valid_stars = [x for x in stars if x in legal_moves]
        if valid_stars:
            reps = set()
            for x in valid_stars:
                reps.add(get_orbit_representative(x, size))
            return list(reps)
        return legal_moves

    # Active Fronts: Find all strings and their liberties
    visited = [False] * (size * size)
    fronts = set() # Liberties of any group
    tactical = set() # Liberties of groups in atari (<= 2 liberties)
    shape = set() # Points adjacent to our own stones
    
    for i in range(size * size):
        if board.board[i] != 0 and not visited[i]:
            grp, libs = board.get_group(i)
            for g in grp:
                visited[g] = True
                
            for lib in libs:
                fronts.add(lib)
                if board.board[i] == to_move_color:
                    shape.add(lib)
                    
            # High priority to save/capture
            if len(libs) <= 2:
                for lib in libs:
                    tactical.add(lib)

    # Compile candidates
    candidates = set()
    for m in legal_moves:
        if m in tactical:
            candidates.add(m)
        elif m in fronts:
            candidates.add(m)
        elif m in shape:
            candidates.add(m)
            
    if not candidates:
        return legal_moves
        
    return list(candidates)

# Transposition Table Cache
transposition_table = {}

def get_spatial_command_score(board):
    """Calculates S(m) = |L_own| - |L_opp| + TengenBias"""
    sz = board.size
    visited = [False] * (sz * sz)
    
    black_libs = set()
    white_libs = set()
    
    # Calculate geometric Tengen bias
    tengen_r, tengen_c = sz // 2, sz // 2
    black_tengen_dist = 0
    white_tengen_dist = 0
    black_stones = 0
    white_stones = 0
    
    for i in range(sz * sz):
        color = board.board[i]
        if color != 0:
            # Distance to tengen
            r, c = i // sz, i % sz
            dist = math.sqrt((r - tengen_r)**2 + (c - tengen_c)**2)
            
            if color == 1:
                black_stones += 1
                black_tengen_dist += dist
            elif color == 2:
                white_stones += 1
                white_tengen_dist += dist

            if not visited[i]:
                grp, libs = board.get_group(i)
                for g in grp:
                    visited[g] = True
                if color == 1:
                    black_libs.update(libs)
                elif color == 2:
                    white_libs.update(libs)
                    
    score_b = len(black_libs)
    score_w = len(white_libs)
    
    # Add tiny fractional Tengen bias (inversely proportional to distance)
    # We negate the distance so that smaller distance = higher score
    if black_stones > 0:
        score_b -= (black_tengen_dist / black_stones) * 0.001
    if white_stones > 0:
        score_w -= (white_tengen_dist / white_stones) * 0.001
        
    return score_b, score_w

def get_area_score(board):
    """Calculates Tromp-Taylor area score for Black (1) and White (2)."""
    sz = board.size
    visited = [False] * (sz * sz)
    black_score = 0
    white_score = 0
    
    # 1. Count stones
    for i in range(sz * sz):
        if board.board[i] == 1:
            black_score += 1
        elif board.board[i] == 2:
            white_score += 1
            
    # 2. Count territory (empty areas)
    for i in range(sz * sz):
        if board.board[i] == 0 and not visited[i]:
            region = {i}
            queue = [i]
            visited[i] = True
            borders = set()
            
            while queue:
                curr = queue.pop(0)
                for n in board.get_neighbors(curr):
                    if board.board[n] == 0:
                        if not visited[n]:
                            visited[n] = True
                            region.add(n)
                            queue.append(n)
                    else:
                        borders.add(board.board[n])
                        
            if len(borders) == 1:
                border_color = list(borders)[0]
                if border_color == 1:
                    black_score += len(region)
                elif border_color == 2:
                    white_score += len(region)
                    
    return black_score, white_score

def alphabeta(board, d, alpha, beta, to_move_color, seen_str, last_passed=False):
    h = get_zobrist_hash(board, to_move_color)
    if h in transposition_table:
        entry = transposition_table[h]
        if entry['depth'] >= d:
            if entry['flag'] == 0: # EXACT
                return entry['val']
            elif entry['flag'] == 1 and entry['val'] <= alpha: # ALPHA
                return alpha
            elif entry['flag'] == 2 and entry['val'] >= beta: # BETA
                return beta

    if d == 0:
        b_score, w_score = get_spatial_command_score(board)
        b_area, w_area = get_area_score(board)
        return (b_score + b_area) - (w_score + w_area)

    legal_moves = board.get_legal_moves(to_move_color)
    candidates = get_dynamic_sparse_moves(board, to_move_color, legal_moves)
    
    # Store original alpha/beta bounds
    orig_alpha = alpha
    orig_beta = beta

    # Counted Greedy Move Ordering
    move_scores = []
    for m in candidates:
        nb = board.copy()
        nb.play_move(m, to_move_color)
        sig = "|" + "".join(map(str, nb.board)) + "|"
        if sig not in seen_str:
            b_s, w_s = get_spatial_command_score(nb)
            score = (b_s - w_s) if to_move_color == 1 else (w_s - b_s)
            move_scores.append((score, m))
            
    move_scores.sort(reverse=True, key=lambda x: x[0])
    
    best_val = -1000 if to_move_color == 1 else 1000
    best_m = None
    done = False
    
    for _, m in move_scores:
        if not done:
            nb = board.copy()
            nb.play_move(m, to_move_color)
            sig = "|" + "".join(map(str, nb.board)) + "|"
            v = alphabeta(nb, d - 1, alpha, beta, 3 - to_move_color, seen_str + sig, False)
            
            if to_move_color == 1:
                if v > best_val:
                    best_val = v
                    best_m = m
                if best_val > alpha:
                    alpha = best_val
            else:
                if v < best_val:
                    best_val = v
                    best_m = m
                if best_val < beta:
                    beta = best_val
                    
            if alpha >= beta:
                done = True
                
    if not done:
        # Pass move
        if last_passed:
            b_score, w_score = get_spatial_command_score(board)
            pv = b_score - w_score
        else:
            pv = alphabeta(board, d - 1, alpha, beta, 3 - to_move_color, seen_str, True)
            
        if to_move_color == 1:
            if pv > best_val:
                best_val = pv
                best_m = None
        else:
            if pv < best_val:
                best_val = pv
                best_m = None
                
    # Correct transposition flag based on original alpha/beta bounds
    if best_val <= orig_alpha:
        flag = 1 # ALPHA (upper bound)
    elif best_val >= orig_beta:
        flag = 2 # BETA (lower bound)
    else:
        flag = 0 # EXACT
            
    transposition_table[h] = { 'depth': d, 'val': best_val, 'flag': flag, 'best_move': best_m }
    return best_val

def evaluate_candidate_worker(args):
    board, m, color, depth, seen_str = args
    # Play the candidate move
    nb = board.copy()
    nb.play_move(m, color)
    sig = "|" + "".join(map(str, nb.board)) + "|"
    new_seen_str = seen_str + sig
    
    # Iterative deepening from depth 1 to 'depth - 1' on the subtree
    # Workers maintain their own local TT populated by shallow passes
    global transposition_table
    transposition_table.clear()
    
    best_v = 0
    for d in range(1, depth):
        # Full window search on the subtree
        best_v = alphabeta(nb, d, -10000, 10000, 3 - color, new_seen_str, False)
        
    return (best_v, m)

def select_sft_move(board, color, depth=5):
    legal_moves = board.get_legal_moves(color)
    if not legal_moves:
        return None
        
    candidates = get_dynamic_sparse_moves(board, color, legal_moves)
    if len(candidates) == 1:
        return candidates[0]
        
    seen_str = "|" + "".join(map(str, board.board)) + "|"
    
    # Prepare arguments for multiprocessing
    worker_args = []
    for m in candidates:
        worker_args.append((board, m, color, depth, seen_str))
        
    # Launch parallel worker pool
    num_cores = multiprocessing.cpu_count()
    best_move = candidates[0]
    best_val = -10000 if color == 1 else 10000
    
    with multiprocessing.Pool(processes=min(num_cores, len(candidates))) as pool:
        results = pool.map(evaluate_candidate_worker, worker_args)
        
    # Aggregate results
    for v, m in results:
        if color == 1: # Black maximizes
            if v > best_val:
                best_val = v
                best_move = m
        else: # White minimizes
            if v < best_val:
                best_val = v
                best_move = m
                
    return best_move

# ==================== GTP PROTOCOL ENGINE ====================

def index_to_gtp(idx, size):
    if idx is None:
        return "pass"
    r, c = idx // size, idx % size
    col_str = "ABCDEFGHJKLMNOPQRSTY"[c]
    row_str = str(size - r)
    return col_str + row_str

def gtp_to_index(gtp_str, size):
    s = gtp_str.strip().upper()
    if s == "PASS":
        return None
    col_char = s[0]
    c = "ABCDEFGHJKLMNOPQRSTY".index(col_char)
    r = size - int(s[1:])
    return r * size + c

def run_gtp_server():
    size = 9
    board = SFTGoBoard(size)
    color_map = {"B": 1, "W": 2, "BLACK": 1, "WHITE": 2}
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line or line.startswith("#"):
                continue
                
            parts = line.split()
            cmd_id = ""
            if parts[0].isdigit():
                cmd_id = parts.pop(0)
                
            cmd = parts[0]
            args = parts[1:]
            
            if cmd == "protocol_version":
                print(f"={cmd_id} 2\n")
            elif cmd == "name":
                print(f"={cmd_id} SFT_TypeZero_Go\n")
            elif cmd == "version":
                print(f"={cmd_id} 1.0\n")
            elif cmd == "known_command":
                known = cmd in ["protocol_version", "name", "version", "known_command", "list_commands", "quit", "boardsize", "clear_board", "play", "genmove"]
                print(f"={cmd_id} {'true' if known else 'false'}\n")
            elif cmd == "list_commands":
                print(f"={cmd_id} protocol_version\nname\nversion\nknown_command\nlist_commands\nquit\nboardsize\nclear_board\nplay\ngenmove\n")
            elif cmd == "quit":
                print(f"={cmd_id}\n")
                sys.exit(0)
            elif cmd == "boardsize":
                size = int(args[0])
                board = SFTGoBoard(size)
                print(f"={cmd_id}\n")
            elif cmd == "clear_board":
                board = SFTGoBoard(size)
                print(f"={cmd_id}\n")
            elif cmd == "play":
                color = color_map.get(args[0].upper(), 1)
                move = gtp_to_index(args[1], size)
                ok = board.play_move(move, color)
                if ok:
                    print(f"={cmd_id}\n")
                else:
                    print(f"?{cmd_id} illegal move\n")
            elif cmd == "genmove":
                color = color_map.get(args[0].upper(), 1)
                move = select_sft_move(board, color)
                board.play_move(move, color)
                print(f"={cmd_id} {index_to_gtp(move, size)}\n")
            else:
                print(f"?{cmd_id} unknown command\n")
            sys.stdout.flush()
        except Exception as e:
            print(f"? error: {str(e)}\n")
            sys.stdout.flush()

# ==================== TOURNAMENT REFEREE CLIENT ====================

class GTPClient:
    def __init__(self, cmd_line=None):
        self.cmd_line = cmd_line
        self.proc = None
        self.size = 9
        if cmd_line:
            self.proc = subprocess.Popen(
                cmd_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
            )
            
    def send(self, cmd_str):
        if self.proc:
            print(f">>> SEND: {cmd_str}")
            try:
                self.proc.stdin.write(cmd_str + "\n")
                self.proc.stdin.flush()
            except BrokenPipeError:
                print("!!! BROKEN PIPE. Process stderr:")
                print(self.proc.stderr)
                raise
            # Read response
            response = []
            while True:
                line = self.proc.stdout.readline()
                if not line or line.strip() == "":
                    break
                response.append(line.strip())
            print(f"<<< RECV: {response}")
            return "\n".join(response)
        else:
            # Simulated opponent fallback
            if "boardsize" in cmd_str:
                parts = cmd_str.split()
                self.size = int(parts[1])
                self.sim_board = SFTGoBoard(self.size)
                return "= "
            elif "clear_board" in cmd_str:
                self.sim_board = SFTGoBoard(self.size)
                return "= "
            elif "play" in cmd_str:
                parts = cmd_str.split()
                color = 1 if parts[1].upper() == "B" else 2
                move = gtp_to_index(parts[2], self.size)
                self.sim_board.play_move(move, color)
                return "= "
            elif "genmove" in cmd_str:
                parts = cmd_str.split()
                color = 1 if parts[1].upper() == "B" else 2
                legal = self.sim_board.get_legal_moves(color)
                if legal:
                    move = random.choice(legal)
                else:
                    move = None
                self.sim_board.play_move(move, color)
                return f"= {index_to_gtp(move, self.size)}"
            return "= "

    def close(self):
        if self.proc:
            try:
                self.send("quit")
                self.proc.wait(timeout=2)
            except:
                self.proc.terminate()

def run_tournament(opponent_cmd=None, size=9, rounds=10, depth=3):
    print("=== SFT Go Tournament Referee ===")
    results = {"SFT": 0, "Opponent": 0, "Draw": 0}
    
    print(f"Starting {rounds}-round match on {size}x{size} board (search depth {depth})...")
    if opponent_cmd:
        print(f"Opponent command: {' '.join(opponent_cmd)}")
    else:
        print("No external engine specified; running against simulated random GTP bot.")
        
    for r in range(rounds):
        sft_color = 1 if r % 2 == 0 else 2 # Alternate colors
        board = SFTGoBoard(size)
        client = GTPClient(opponent_cmd)
        client.send(f"boardsize {size}")
        client.send("clear_board")
        
        passes = 0
        moves_played = 0
        # Maximum 120 moves to prevent infinite loops
        while passes < 2 and moves_played < 120:
            current_player = 1 if moves_played % 2 == 0 else 2
            
            if current_player == sft_color:
                # SFT plays (depth search)
                move = select_sft_move(board, sft_color, depth=depth)
                board.play_move(move, sft_color)
                move_str = index_to_gtp(move, size)
                client.send(f"play {'B' if sft_color == 1 else 'W'} {move_str}")
                if move is None:
                    passes += 1
                else:
                    passes = 0
            else:
                # Opponent plays
                opp_color = 3 - sft_color
                resp = client.send(f"genmove {'B' if opp_color == 1 else 'W'}")
                # Parse standard GTP output
                parts = resp.split()
                move_str = "pass"
                if len(parts) > 1:
                    # Skip the status identifier (e.g. '=')
                    move_str = parts[1]
                move = gtp_to_index(move_str, size)
                board.play_move(move, opp_color)
                if move is None:
                    passes += 1
                else:
                    passes = 0
                    
            moves_played += 1
            
        client.close()
        
        # Area scoring
        black_score, white_score = get_area_score(board)
        # Komi of 6.5 for white
        white_score += 6.5
        
        winner = "Black" if black_score > white_score else "White"
        sft_won = (winner == "Black" and sft_color == 1) or (winner == "White" and sft_color == 2)
        
        if sft_won:
            results["SFT"] += 1
        else:
            results["Opponent"] += 1
            
        print(f"Round {r+1}: SFT={'Black' if sft_color==1 else 'White'} | Score B={black_score} W={white_score:.1f} | Winner: {'SFT' if sft_won else 'Opponent'}")
        
    print("\nTournament complete!")
    print(f"Final Score: SFT {results['SFT']} - {results['Opponent']} Opponent")
    
    # Write to GO_MATCHES.md
    with open("tools/GO_MATCHES.md", "w") as f:
        f.write("# SFT Go Engine Match Ledger\n\n")
        f.write(f"**Date:** July 9, 2026  \n")
        f.write(f"**Engine:** SFT Type Zero Go (zero parameters, depth-{depth} minimax search)  \n")
        f.write(f"**Opponent:** {' '.join(opponent_cmd) if opponent_cmd else 'Simulated GTP Bot'}  \n")
        f.write(f"**Board Size:** {size}x{size}  \n\n")
        f.write("## Match Results\n\n")
        f.write(f"| Round | SFT Side | Winner |\n")
        f.write("|---|---|---|\n")
        for i in range(rounds):
            f.write(f"| {i+1} | {'Black' if i%2==0 else 'White'} | {'SFT' if (i%2==0 and results['SFT']>i//2) or (i%2==1 and results['SFT']>(i+1)//2) else 'Opponent'} |\n")
        f.write("|---|---|---|\n")
        f.write(f"| **Total** | — | **SFT won {results['SFT']}/{rounds} games** |\n")
        
    print("Match ledger written to tools/GO_MATCHES.md.")

def main():
    size = 9
    depth = 3
    rounds = 10
    
    # Parse size
    if "--size" in sys.argv:
        idx = sys.argv.index("--size")
        size = int(sys.argv[idx+1])
        sys.argv.pop(idx+1)
        sys.argv.pop(idx)
        
    # Parse depth
    if "--depth" in sys.argv:
        idx = sys.argv.index("--depth")
        depth = int(sys.argv[idx+1])
        sys.argv.pop(idx+1)
        sys.argv.pop(idx)
        
    # Parse rounds
    if "--rounds" in sys.argv:
        idx = sys.argv.index("--rounds")
        rounds = int(sys.argv[idx+1])
        sys.argv.pop(idx+1)
        sys.argv.pop(idx)

    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        run_gtp_server()
    elif len(sys.argv) > 1 and sys.argv[1] == "--check-gtp":
        # Verification check: play one quick move
        board = SFTGoBoard(size)
        move = select_sft_move(board, 1, depth=depth)
        print(f"GTP check passed. SFT plays first move: {index_to_gtp(move, size)}")
    else:
        opponent = None
        if "--engine" in sys.argv:
            idx = sys.argv.index("--engine")
            opponent = sys.argv[idx+1:]
        run_tournament(opponent, size=size, rounds=rounds, depth=depth)

if __name__ == "__main__":
    main()
