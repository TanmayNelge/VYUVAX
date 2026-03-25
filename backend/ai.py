
# # def best_move(board, history, depth, player):
# #     import math

# #     normalized_history = []
# #     for m in history:
# #         if isinstance(m, dict):
# #             p = str(m.get("player", "X"))
# #             i = int(m.get("index", 0))
# #             normalized_history.append({"player": p, "index": i})
# #         elif isinstance(m, tuple) or isinstance(m, list):
# #             normalized_history.append({"player": str(m[0]), "index": int(m[1])})
# #         else:
# #             normalized_history.append({"player": "X", "index": 0})
# #     history = normalized_history


# #     def mark_age(pos, player, history):

# #         player_moves = [m for m in history if m["player"] == player]
# #         for move in reversed(player_moves):
# #             if move["index"] == pos:
# #                 return player_moves.index(move) + 1
# #         return 0

# #     def evaluate_line_with_age(line, board, history, player):
# #         score = 0
# #         for pos in line:
# #             if board[pos] == player:
# #                 score += mark_age(pos, player, history)
# #         return score

# #     def heuristic(board, history):
# #         score = 0
# #         lines = [
# #             [0,1,2],[3,4,5],[6,7,8],
# #             [0,3,6],[1,4,7],[2,5,8],
# #             [0,4,8],[2,4,6]
# #         ]
# #         for line in lines:
# #             score += evaluate_line_with_age(line, board, history, "X")
# #             score -= evaluate_line_with_age(line, board, history, "O")
# #         return score

# #     def minimax(board, history, depth, alpha, beta, maximizing):
# #         if depth == 0:
# #             return heuristic(board, history)
# #         moves = [i for i, c in enumerate(board) if c == " "]
# #         if maximizing:
# #             value = -math.inf
# #             for m in moves:
# #                 new_board = board[:]
# #                 new_board[m] = "X"
# #                 new_history = history + [{"player": "X", "index": m}]
# #                 value = max(value, minimax(new_board, new_history, depth-1, alpha, beta, False))
# #                 alpha = max(alpha, value)
# #                 if alpha >= beta:
# #                     break
# #             return value
# #         else:
# #             value = math.inf
# #             for m in moves:
# #                 new_board = board[:]
# #                 new_board[m] = "O"
# #                 new_history = history + [{"player": "O", "index": m}]
# #                 value = min(value, minimax(new_board, new_history, depth-1, alpha, beta, True))
# #                 beta = min(beta, value)
# #                 if alpha >= beta:
# #                     break
# #             return value


# #     best_val = -math.inf
# #     best_mv = None
# #     for i, cell in enumerate(board):
# #         if cell == " ":
# #             new_board = board[:]
# #             new_board[i] = player
# #             new_history = history + [{"player": player, "index": i}]
# #             move_val = minimax(new_board, new_history, depth-1, -math.inf, math.inf, False)
# #             if move_val > best_val:
# #                 best_val = move_val
# #                 best_mv = i

# #     return best_mv


# # def best_move(board, history, depth, player):
# #     import math, sys
# #     from rules import movepl, vanishpl, undo_move

# #     normalized_history = []
# #     for m in history:
# #         if isinstance(m, dict):
# #             p = str(m.get("player", "X"))
# #             i = int(m.get("index", 0))
# #             normalized_history.append({"player": p, "index": i})
# #         elif isinstance(m, tuple) or isinstance(m, list):
# #             normalized_history.append({"player": str(m[1]), "index": int(m[0])})
# #         else:
# #             normalized_history.append({"player": "X", "index": 0})
# #     history = normalized_history

# #     opponent = "O" if player == "X" else "X"

# #     def mark_age(pos, player, history):
# #         player_moves = [m for m in history if m["player"] == player]
# #         for idx, move in enumerate(player_moves):
# #             if move["index"] == pos:
# #                 return len(player_moves) - idx - 1
# #         return 0

# #     def age_weight(age):
# #         if age == 0:
# #             return 1.0
# #         elif age == 1:
# #             return 0.7
# #         else:
# #             return 0.3

# #     def evaluate_line_with_age(line, board, history, player):
# #         blocker = "O" if player == "X" else "X"
# #         score = 0
# #         for pos in line:
# #             if board[pos] == blocker:
# #                 return 0

# #         for pos in line:
# #             if board[pos] == player:
# #                 age = mark_age(pos, player, history)
# #                 score += age_weight(age)

# #         if score >= 2.5:
# #             return 1000
# #         if score >= 1.5:
# #             return 100
# #         if score > 0:
# #             return 10 * score

# #         return 0

# #     def heuristic(board, history):
# #         score = 0
# #         lines = [
# #             [0,1,2],[3,4,5],[6,7,8],
# #             [0,3,6],[1,4,7],[2,5,8],
# #             [0,4,8],[2,4,6]
# #         ]
# #         for line in lines:
# #             score += evaluate_line_with_age(line, board, history, "X")
# #             score -= evaluate_line_with_age(line, board, history, "O")
# #         return score

# #     def winnercheck(board):
# #         wins = [
# #             [0,1,2],[3,4,5],[6,7,8],
# #             [0,3,6],[1,4,7],[2,5,8],
# #             [0,4,8],[2,4,6]
# #         ]
# #         for a,b,c in wins:
# #             if board[a] == board[b] == board[c] != " ":
# #                 return board[a]
# #         return None

# #     def minimax(board, history, depth, alpha, beta, maximizing):
# #         winner = winnercheck(board)

# #         if winner == "X":
# #             return 1000000 + depth
# #         if winner == "O":
# #             return -1000000 - depth
# #         if depth == 0:
# #             return heuristic(board, history)

# #         if maximizing:
# #             best = -math.inf
# #             for i in range(len(board)):
# #                 if board[i] == " ":
# #                     movepl(board, history, i, player)
# #                     removed_info = vanishpl(board, history, player)

# #                     value = minimax(board, history, depth-1, alpha, beta, False)

# #                     undo_move(board, history, i, removed_info)

# #                     best = max(best, value)
# #                     alpha = max(alpha, best)
# #                     if beta <= alpha:
# #                         break
# #             return best
# #         else:
# #             best = math.inf
# #             for i in range(len(board)):
# #                 if board[i] == " ":
# #                     movepl(board, history, i, opponent)
# #                     removed_info = vanishpl(board, history, opponent)

# #                     value = minimax(board, history, depth-1, alpha, beta, True)

# #                     undo_move(board, history, i, removed_info)

# #                     best = min(best, value)
# #                     beta = min(beta, best)
# #                     if beta <= alpha:
# #                         break
# #             return best

# #     if player == "X":
# #         best_val = -math.inf
# #         best_mv = None

# #         for i in range(len(board)):
# #             if board[i] == " ":
# #                 movepl(board, history, i, player)
# #                 removed_info = vanishpl(board, history, player)

# #                 move_val = minimax(
# #                     board,
# #                     history,
# #                     depth - 1,
# #                     -math.inf,
# #                     math.inf,
# #                     False
# #                 )

# #                 undo_move(board, history, i, removed_info)

# #                 sys.stderr.write(f"Move {i}: {move_val}\n")

# #                 if move_val > best_val:
# #                     best_val = move_val
# #                     best_mv = i

# #         sys.stderr.write(f"Best Move: {best_mv} with Score {best_val}\n")
# #         return best_mv

# #     else:
# #         best_val = math.inf
# #         best_mv = None

# #         for i in range(len(board)):
# #             if board[i] == " ":
# #                 movepl(board, history, i, player)
# #                 removed_info = vanishpl(board, history, player)

# #                 move_val = minimax(
# #                     board,
# #                     history,
# #                     depth - 1,
# #                     -math.inf,
# #                     math.inf,
# #                     True
# #                 )

# #                 undo_move(board, history, i, removed_info)

# #                 if move_val < best_val:
# #                     best_val = move_val
# #                     best_mv = i

# #         return best_mv


# def best_move(board, history, depth, player):
#     import math
#     import sys
#     from rules import movepl, vanishpl, undo_move

#     normalized_history = []
#     for m in history:
#         if isinstance(m, dict):
#             p = str(m.get("player", "X"))
#             i = int(m.get("index", 0))
#             normalized_history.append({"player": p, "index": i})
#         elif isinstance(m, tuple) or isinstance(m, list):
#             normalized_history.append({"player": str(m[1]), "index": int(m[0])})
#         else:
#             normalized_history.append({"player": "X", "index": 0})
#     history = normalized_history

#     def mark_age(pos, p_mark, history):
#         player_moves = [m for m in history if m["player"] == p_mark]
#         for idx, move in enumerate(player_moves):
#             if move["index"] == pos:
#                 return len(player_moves) - idx - 1
#         return 0

#     def age_weight(age):
#         if age == 0: return 1.0
#         elif age == 1: return 0.7
#         else: return 0.3

#     def evaluate_line_with_age(line, board, history, p_mark):
#         blocker = "O" if p_mark == "X" else "X"
#         score = 0
#         for pos in line:
#             if board[pos] == blocker:
#                 return 0

#         for pos in line:
#             if board[pos] == p_mark:
#                 age = mark_age(pos, p_mark, history)
#                 score += age_weight(age)

#         if score >= 2.5: return 1000
#         if score >= 1.5: return 100
#         if score > 0: return 10 * score
#         return 0

#     def heuristic(board, history):
#         score = 0
#         lines = [
#             [0,1,2],[3,4,5],[6,7,8],
#             [0,3,6],[1,4,7],[2,5,8],
#             [0,4,8],[2,4,6]
#         ]
#         # X always adds to the score, O always subtracts
#         for line in lines:
#             score += evaluate_line_with_age(line, board, history, "X")
#             score -= evaluate_line_with_age(line, board, history, "O")
#         return score

#     def winnercheck(board):
#         wins = [
#             [0,1,2],[3,4,5],[6,7,8],
#             [0,3,6],[1,4,7],[2,5,8],
#             [0,4,8],[2,4,6]
#         ]
#         for a,b,c in wins:
#             if board[a] == board[b] == board[c] != " ":
#                 return board[a]
#         return None

#     def minimax(board, history, depth, alpha, beta, maximizing):
#         winner = winnercheck(board)

#         # X is the Maximizer (+), O is the Minimizer (-)
#         if winner == "X": return 1000000 + depth
#         if winner == "O": return -1000000 - depth
#         if depth == 0: return heuristic(board, history)

#         if maximizing: # X's Turn
#             best = -math.inf
#             for i in range(len(board)):
#                 if board[i] == " ":
#                     movepl(board, history, i, "X")
#                     removed_info = vanishpl(board, history, "X")
                    
#                     value = minimax(board, history, depth-1, alpha, beta, False)
                    
#                     undo_move(board, history, i, removed_info)
#                     best = max(best, value)
#                     alpha = max(alpha, best)
#                     if beta <= alpha: break
#             return best
#         else: # O's Turn
#             best = math.inf
#             for i in range(len(board)):
#                 if board[i] == " ":
#                     movepl(board, history, i, "O")
#                     removed_info = vanishpl(board, history, "O")
                    
#                     value = minimax(board, history, depth-1, alpha, beta, True)
                    
#                     undo_move(board, history, i, removed_info)
#                     best = min(best, value)
#                     beta = min(beta, best)
#                     if beta <= alpha: break
#             return best

#     # --- ROOT LEVEL (The AI picking its actual move) ---
#     if player == "X":
#         best_val = -math.inf
#         best_mv = None
#         for i in range(len(board)):
#             if board[i] == " ":
#                 movepl(board, history, i, "X")
#                 removed_info = vanishpl(board, history, "X")
                
#                 # Next turn is O's (False = Minimizing)
#                 move_val = minimax(board, history, depth - 1, -math.inf, math.inf, False)
#                 undo_move(board, history, i, removed_info)

#                 if move_val > best_val:
#                     best_val = move_val
#                     best_mv = i
#         return best_mv
        
#     else: # player == "O"
#         best_val = math.inf
#         best_mv = None
#         for i in range(len(board)):
#             if board[i] == " ":
#                 movepl(board, history, i, "O")
#                 removed_info = vanishpl(board, history, "O")
                
#                 # Next turn is X's (True = Maximizing)
#                 move_val = minimax(board, history, depth - 1, -math.inf, math.inf, True)
#                 undo_move(board, history, i, removed_info)

#                 if move_val < best_val:
#                     best_val = move_val
#                     best_mv = i
#         return best_mv


import math
import sys
from rules import movepl, vanishpl, undo_move, winnercheck

# ---------------------------------------------------------
# Helper Functions for Board Evaluation
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# The Minimax Algorithm
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# Data Normalization
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# Main AI Entry Point
# ---------------------------------------------------------

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