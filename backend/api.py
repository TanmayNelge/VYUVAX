import sys
import json
from ai import best_move
from rules import winnercheck

def main():
    data = json.loads(sys.stdin.read())

    board = data["board"]
    history = data["history"]
    depth = data["depth"]
    player = data["player"]

    move = best_move(board, history, depth, player)
    winner = winnercheck(board)

    print(json.dumps({"move": move, "winner" : winner}))

if __name__ == "__main__":
    main()
