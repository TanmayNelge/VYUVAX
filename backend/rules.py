from board import printb
from ai import best_move
from board import movepl, vanishpl, undo_move

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

def play():
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
