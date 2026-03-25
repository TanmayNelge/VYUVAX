import math
import sys
from rules import movepl, vanishpl, undo_move, winnercheck

def mark_age(pos, p_mark, history):
    player_moves = [m for m in history if m["player"] == p_mark]
    for idx, move in enumerate(player_moves):
        if move["index"] == pos:
            return len(player_moves) - idx - 1
    return 0

def age_weight(age):
    if age == 0: return 1.0
    elif age == 1: return 0.7
    else: return 0.3

def evaluate_line_with_age(line, board, history, p_mark):
    blocker = "O" if p_mark == "X" else "X"
    score = 0
    
    # If the opponent is in this line, it's blocked. No points.
    for pos in line:
        if board[pos] == blocker:
            return 0

    # Calculate score based on how "fresh" the pieces are
    for pos in line:
        if board[pos] == p_mark:
            age = mark_age(pos, p_mark, history)
            score += age_weight(age)

    # Score thresholds
    if score >= 2.5: return 1000
    if score >= 1.5: return 100
    if score > 0: return 10 * score
    return 0

def heuristic(board, history):
    score = 0
    lines = [
        [0,1,2],[3,4,5],[6,7,8], # Rows
        [0,3,6],[1,4,7],[2,5,8], # Cols
        [0,4,8],[2,4,6]          # Diagonals
    ]
    # X always adds to the score (+), O always subtracts (-)
    for line in lines:
        score += evaluate_line_with_age(line, board, history, "X")
        score -= evaluate_line_with_age(line, board, history, "O")
    return score

# The Minimax Algorithm

def minimax(board, history, depth, alpha, beta, maximizing):
    winner = winnercheck(board)

    # Base cases: X wins, O wins, or we hit our depth limit
    if winner == "X": return 1000000 + depth
    if winner == "O": return -1000000 - depth
    if depth == 0: return heuristic(board, history)

    if maximizing: # X's Turn (Trying to get the highest positive score)
        best = -math.inf
        for i in range(len(board)):
            if board[i] == " ":
                movepl(board, history, i, "X")
                removed_info = vanishpl(board, history, "X")
                
                value = minimax(board, history, depth-1, alpha, beta, False)
                
                undo_move(board, history, i, removed_info)
                best = max(best, value)
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
        
    else: # O's Turn (Trying to get the lowest negative score)
        best = math.inf
        for i in range(len(board)):
            if board[i] == " ":
                movepl(board, history, i, "O")
                removed_info = vanishpl(board, history, "O")
                
                value = minimax(board, history, depth-1, alpha, beta, True)
                
                undo_move(board, history, i, removed_info)
                best = min(best, value)
                beta = min(beta, best)
                if beta <= alpha: break
        return best

# Data Normalization

def normalize_history(raw_history):
    # Ensures the history array always looks exactly how Python expects it
    normalized = []
    for m in raw_history:
        if isinstance(m, dict):
            p = str(m.get("player", "X"))
            i = int(m.get("index", 0))
            normalized.append({"player": p, "index": i})
        elif isinstance(m, tuple) or isinstance(m, list):
            normalized.append({"player": str(m[1]), "index": int(m[0])})
        else:
            normalized.append({"player": "X", "index": 0})
    return normalized


# Main AI Entry Point

def best_move(board, raw_history, depth, player):
    history = normalize_history(raw_history)

    if player == "X":
        best_val = -math.inf
        best_mv = None
        for i in range(len(board)):
            if board[i] == " ":
                movepl(board, history, i, "X")
                removed_info = vanishpl(board, history, "X")
                
                # Next turn is O's (False = Minimizing)
                move_val = minimax(board, history, depth - 1, -math.inf, math.inf, False)
                undo_move(board, history, i, removed_info)

                if move_val > best_val:
                    best_val = move_val
                    best_mv = i
        return best_mv
        
    else: # player == "O"
        best_val = math.inf
        best_mv = None
        for i in range(len(board)):
            if board[i] == " ":
                movepl(board, history, i, "O")
                removed_info = vanishpl(board, history, "O")
                
                # Next turn is X's (True = Maximizing)
                move_val = minimax(board, history, depth - 1, -math.inf, math.inf, True)
                undo_move(board, history, i, removed_info)

                if move_val < best_val:
                    best_val = move_val
                    best_mv = i
        return best_mv  