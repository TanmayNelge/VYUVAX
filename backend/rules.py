# from board import printb

# winning_positions = [
#     (0,1,2),(3,4,5),(6,7,8),
#     (0,3,6),(1,4,7),(2,5,8),
#     (0,4,8),(2,4,6) 
# ]

# def winnercheck(board):
#     for a, b, c in winning_positions:
#         if board[a] == board[b] == board[c] != " ":
#             return board[a]
#     return None

# def movepl(board, history, position, player):
#     if board[position] != " ":
#         return False
#     board[position] = player
#     history.append((position, player))
#     return True


# def vanishpl(board, history, player):
#     history = [
#     {"player": m["player"], "index": m["index"]} if isinstance(m, dict) else {"player": m[0], "index": m[1]}
#     for m in history
#     ]
#     new_history = []
#     for m in history:
#         if isinstance(m, tuple):
#             new_history.append({"player": m[0], "index": m[1]})
#         else:
#             new_history.append(m)
#     history = new_history    
#     print("Vanishpl received history:", history)
#     print("Element types:", [type(m) for m in history])

#     print("history type:", type(history))
#     if len(history) > 0:
#         print("First element type:", type(history[0]), "value:", history[0])

#     player_moves = [m for m in history if m["player"] == player]

#     removed = None
#     if len(player_moves) > 3:
#         removed = player_moves[0]
#         board[removed[0]] = " "
#         history.remove(removed)

#     return removed


# def undo_move(board, history, position, removed):
#     board[position] = " "
#     history.pop()

#     if removed:
#         pos, player = removed
#         board[pos] = player
#         history.insert(0, removed)


# def play():
#     from ai import best_move  

#     board = [" "] * 9
#     history = []
#     depth = 6
#     current_player = "O"

#     print("Choose mode:")
#     print("1. Single Player (vs AI)")
#     print("2. Two Player")
#     choice = int(input("Enter choice: "))

#     print("\nVanishing Tic Tac Toe\n")

#     if choice == 1:
#         print("You are O | AI is X\n")

#         while True:
#             printb(board)
#             print()

#             winner = winnercheck(board)
#             if winner:
#                 print(winner, "wins!")
#                 break

#             if current_player == "O":
#                 pos = int(input("Enter position (0-8): "))
#                 if not movepl(board, history, pos, "O"):
#                     print("Invalid move")
#                     continue
#                 vanishpl(board, history, "O")
#                 current_player = "X"

#             else:
#                 pos = best_move(board, history, depth, "X")
#                 movepl(board, history, pos, "X")
#                 vanishpl(board, history, "X")
#                 current_player = "O"

#     else:
#         current_player = "X"

#         while True:
#             printb(board)
#             print()
#             print(f"{current_player}'s turn")

#             pos = int(input("Enter position (0-8): "))
#             if not movepl(board, history, pos, current_player):
#                 print("Invalid move")
#                 continue

#             vanishpl(board, history, current_player)

#             winner = winnercheck(board)
#             if winner:
#                 printb(board)
#                 print(winner, "wins!")
#                 break

#             current_player = "O" if current_player == "X" else "X"

winning_positions = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def winnercheck(board):
    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None


def movepl(board, history, position, player):
    if board[position] != " ":
        return False

    board[position] = player
    history.append({"player": player, "index": position})
    return True


def vanishpl(board, history, player):
    """
    Removes the oldest move of `player` if they have more than 3 moves
    """
    player_moves = [m for m in history if m["player"] == player]

    removed = None
    if len(player_moves) > 3:
        removed = player_moves[0]          
        board[removed["index"]] = " "
        history.remove(removed)

    return removed


def undo_move(board, history, position, removed):
    board[position] = " "
    history.pop()

    if removed:
        board[removed["index"]] = removed["player"]
        history.insert(0, removed)

def play():
    from ai import best_move
    from board import printb

    board = [" "] * 9
    history = []
    depth = 6
    current_player = "O"

    print("Choose mode:")
    print("1. Single Player (vs AI)")
    print("2. Two Player")
    choice = int(input("Enter choice: "))

    print("\nVanishing Tic Tac Toe\n")

    if choice == 1:
        print("You are O | AI is X\n")

        while True:
            printb(board)
            print()

            winner = winnercheck(board)
            if winner:
                print(winner, "wins!")
                break

            if current_player == "O":
                pos = int(input("Enter position (0-8): "))
                if not movepl(board, history, pos, "O"):
                    print("Invalid move")
                    continue
                vanishpl(board, history, "O")
                current_player = "X"

            else:
                pos = best_move(board, history, depth, "X")
                movepl(board, history, pos, "X")
                vanishpl(board, history, "X")
                current_player = "O"

    else:
        current_player = "X"

        while True:
            printb(board)
            print()
            print(f"{current_player}'s turn")

            pos = int(input("Enter position (0-8): "))
            if not movepl(board, history, pos, current_player):
                print("Invalid move")
                continue

            vanishpl(board, history, current_player)

            winner = winnercheck(board)
            if winner:
                printb(board)
                print(winner, "wins!")
                break

            current_player = "O" if current_player == "X" else "X"

