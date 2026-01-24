# # import sys
# # import json
# # from ai import best_move
# # from rules import winnercheck

# # def main():
# #     data = json.loads(sys.stdin.read())

# #     board = data["board"]
# #     history = data["history"]
# #     depth = data["depth"]
# #     player = data["player"]

# #     print("Received data from React:", data)
# #     print("Board:", board)
# #     print("History:", history)

# #     move = best_move(board, history, depth, player)
# #     winner = winnercheck(board)

# #     print(json.dumps({"move": move, "winner" : winner}))

# # if __name__ == "__main__":
# #     main()


# import sys
# import json
# from ai import best_move
# from rules import winnercheck

# def main():
#     try:
#         data = json.loads(sys.stdin.read())

#         board = data["board"]
#         history = data.get("history", [])
#         depth = data.get("depth", 4)
#         player = data.get("player", "X")

#         move = best_move(board, history, depth, player)

#         if move is not None:
#             board[move] = player
#             history.append({"player": player, "index": move})

#         winner = winnercheck(board)

#         print(json.dumps({
#             "move": move,
#             "board": board,
#             "history": history,
#             "winner": winner
#         }))

#     except Exception as e:
#         # Always return JSON, even on error
#         print(json.dumps({
#             "error": str(e)
#         }))

# if __name__ == "__main__":
#     main()

import sys
import json
from ai import best_move
from rules import winnercheck

def main():
    raw = sys.stdin.read()
    data = json.loads(raw)

    board = data["board"]
    history = data["history"]
    depth = data["depth"]
    player = data["player"]

    move = best_move(board, history, depth, player)
    winner = None
    if move is not None:
        board_after = board[:]
        board_after[move] = player
        winner = winnercheck(board_after)
    else:
        winner = winnercheck(board)

    sys.stdout.write(json.dumps({
        "move": move,
        "winner": winner
    }))

if __name__ == "__main__":
    main()


