
import math
from board import movepl, vanishpl, undo_move
from rules import winnercheck

node_count=0

def mark_age(position, player, history):
    player_moves = [m for m in history if m[1] == player]
    for idx, (pos, _) in enumerate(player_moves):
        if pos == position:
            return len(player_moves) - idx - 1
    return None


def age_weight(age):
    if age == 0:
        return 1.0
    elif age == 1:
        return 0.7
    else:
        return 0.3


def evaluate_line_with_age(line_positions, board, history, player):
    opponent = "O" if player == "X" else "X"

    for pos in line_positions:
        if board[pos] == opponent:
            return 0

    score = 0
    for pos in line_positions:
        if board[pos] == player:
            age = mark_age(pos, player, history)
            score += age_weight(age)

    if score >= 2.5:
        return 1000
    if score >= 1.5:
        return 100
    if score > 0:
        return 10 * score

    return 0


def heuristic(board, history):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    score = 0
    for line in lines:
        score += evaluate_line_with_age(line, board, history, "X")
        score -= evaluate_line_with_age(line, board, history, "O")
    return score


def minimax(board, history, depth, alpha, beta, maximizing):
    global node_count
    node_count+=1
    
    winner = winnercheck(board)

    if winner == "X":
        return 1000
    if winner == "O":
        return -1000
    if depth == 0:
        return heuristic(board, history)

    if maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                movepl(board, history, i, "X")
                removed = vanishpl(board, history, "X")

                value = minimax(board, history, depth-1, alpha, beta, False)

                undo_move(board, history, i, removed)
                best = max(best, value)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                movepl(board, history, i, "O")
                removed = vanishpl(board, history, "O")

                value = minimax(board, history, depth-1, alpha, beta, True)

                undo_move(board, history, i, removed)
                best = min(best, value)
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


def best_move(board, depth, player):
    global node_count
    node_count=0
    
    best_score = -float("inf") if player == "X" else float("inf")
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = player
            score = minimax(board, depth - 1, player == "O")
            board[i] = " "

            if player == "X":
                if score > best_score:
                    best_score = score
                    move = i
            else:
                if score < best_score:
                    best_score = score
                    move = i

    return move

