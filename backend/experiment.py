from ai import best_move
from rules import winnercheck, movepl, vanishpl

def play_tournament(games=10, depth_x=4, depth_o=6):
    results = {"X": 0, "O": 0, "Draw": 0}

    for _ in range(games):
        board = [" "] * 9
        history = []
        current_player = "X"
        game_over = False

        for _ in range(50): 
            if current_player == "X":
                move = best_move(board, history, depth_x, "X")
            else:
                move = best_move(board, history, depth_o, "O")

            if move is None:
                break

            movepl(board, history, move, current_player)
            vanishpl(board, history, current_player)

            winner = winnercheck(board)
            if winner:
                results[winner] += 1
                game_over = True
                break

            current_player = "O" if current_player == "X" else "X"

        if not game_over:
            results["Draw"] += 1

    return results


def run_experiment():
    games = int(input("Enter number of games: "))
    dx = int(input("Depth for X: "))
    do = int(input("Depth for O: "))

    results = play_tournament(games, dx, do)
    print("Final Results:", results)

if __name__ == "__main__":
    run_experiment()
