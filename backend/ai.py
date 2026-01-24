
# def best_move(board, history, depth, player):
#     import math

#     normalized_history = []
#     for m in history:
#         if isinstance(m, dict):
#             p = str(m.get("player", "X"))
#             i = int(m.get("index", 0))
#             normalized_history.append({"player": p, "index": i})
#         elif isinstance(m, tuple) or isinstance(m, list):
#             normalized_history.append({"player": str(m[0]), "index": int(m[1])})
#         else:
#             normalized_history.append({"player": "X", "index": 0})
#     history = normalized_history


#     def mark_age(pos, player, history):

#         player_moves = [m for m in history if m["player"] == player]
#         for move in reversed(player_moves):
#             if move["index"] == pos:
#                 return player_moves.index(move) + 1
#         return 0

#     def evaluate_line_with_age(line, board, history, player):
#         score = 0
#         for pos in line:
#             if board[pos] == player:
#                 score += mark_age(pos, player, history)
#         return score

#     def heuristic(board, history):
#         score = 0
#         lines = [
#             [0,1,2],[3,4,5],[6,7,8],
#             [0,3,6],[1,4,7],[2,5,8],
#             [0,4,8],[2,4,6]
#         ]
#         for line in lines:
#             score += evaluate_line_with_age(line, board, history, "X")
#             score -= evaluate_line_with_age(line, board, history, "O")
#         return score

#     def minimax(board, history, depth, alpha, beta, maximizing):
#         if depth == 0:
#             return heuristic(board, history)
#         moves = [i for i, c in enumerate(board) if c == " "]
#         if maximizing:
#             value = -math.inf
#             for m in moves:
#                 new_board = board[:]
#                 new_board[m] = "X"
#                 new_history = history + [{"player": "X", "index": m}]
#                 value = max(value, minimax(new_board, new_history, depth-1, alpha, beta, False))
#                 alpha = max(alpha, value)
#                 if alpha >= beta:
#                     break
#             return value
#         else:
#             value = math.inf
#             for m in moves:
#                 new_board = board[:]
#                 new_board[m] = "O"
#                 new_history = history + [{"player": "O", "index": m}]
#                 value = min(value, minimax(new_board, new_history, depth-1, alpha, beta, True))
#                 beta = min(beta, value)
#                 if alpha >= beta:
#                     break
#             return value


#     best_val = -math.inf
#     best_mv = None
#     for i, cell in enumerate(board):
#         if cell == " ":
#             new_board = board[:]
#             new_board[i] = player
#             new_history = history + [{"player": player, "index": i}]
#             move_val = minimax(new_board, new_history, depth-1, -math.inf, math.inf, False)
#             if move_val > best_val:
#                 best_val = move_val
#                 best_mv = i

#     return best_mv


def best_move(board, history, depth, player):
    import math
    normalized_history = []
    for m in history:
        if isinstance(m, dict):
            p = str(m.get("player", "X"))
            i = int(m.get("index", 0))
            normalized_history.append({"player": p, "index": i})
        elif isinstance(m, tuple) or isinstance(m, list):
            normalized_history.append({"player": str(m[0]), "index": int(m[1])})
        else:
            normalized_history.append({"player": "X", "index": 0})
    history = normalized_history

    opponent = "O" if player == "X" else "X"

    def mark_age(pos, player, history):
        player_moves = [m for m in history if m["player"] == player]
        for idx, move in enumerate(player_moves):
            if move["index"] == pos:
                return len(player_moves) - idx
        return 0

    def evaluate_line_with_age(line, board, history, player):
        score = 0
        for pos in line:
            if board[pos] == player:
                score += mark_age(pos, player, history)
        return score

    def heuristic(board, history):
        score = 0
        lines = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for line in lines:
            score += evaluate_line_with_age(line, board, history, player)
            score -= evaluate_line_with_age(line, board, history, opponent)
        return score

    def winnercheck(board):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for a,b,c in wins:
            if board[a] == board[b] == board[c] != " ":
                return board[a]
        return None
    
    def minimax(board, history, depth, alpha, beta, maximizing):
        winner = winnercheck(board)
        if winner == player:
            return 100
        if winner == opponent:
            return -100
        if depth == 0:
            return heuristic(board, history)

        moves = [i for i, c in enumerate(board) if c == " "]

        if maximizing:
            value = -math.inf
            for m in moves:
                new_board = board[:]
                new_board[m] = player
                new_history = history + [{"player": player, "index": m}]
                value = max(
                    value,
                    minimax(new_board, new_history, depth-1, alpha, beta, False)
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for m in moves:
                new_board = board[:]
                new_board[m] = opponent
                new_history = history + [{"player": opponent, "index": m}]
                value = min(
                    value,
                    minimax(new_board, new_history, depth-1, alpha, beta, True)
                )
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    best_val = -math.inf
    best_mv = None

    for i, cell in enumerate(board):
        if cell == " ":
            new_board = board[:]
            new_board[i] = player
            new_history = history + [{"player": player, "index": i}]
            move_val = minimax(
                new_board,
                new_history,
                depth-1,
                -math.inf,
                math.inf,
                False
            )
            if move_val > best_val:
                best_val = move_val
                best_mv = i

    return best_mv
