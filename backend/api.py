import sys
import json
from ai import best_move

def main():
    data = json.loads(sys.stdin.read())

    board = data["board"]
    history = data["history"]
    depth = data["depth"]
    player = data["player"]

    move = best_move(board, history, depth, player)

    print(json.dumps({"move": move}))

if __name__ == "__main__":
    main()
