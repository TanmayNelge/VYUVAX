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

# import sys
# import json
# from ai import best_move
# from rules import winnercheck, vanishpl

# def main():
#     try:
#         data = json.loads(sys.stdin.read())
#         ai_move = None
#         board = data.get("board", [" "] * 9)
#         history = data.get("history", [])
#         depth = data.get("depth", 4)
#         player = data.get("player", "X")
#         move_index = data.get("move_index") 
#         mode = data.get("mode", "single") 

#         if move_index is not None:
#             board[move_index] = player
#             history.append({"player": player, "index": move_index})
#             vanishpl(board, history, player)

#         winner = winnercheck(board)
#         if winner:
#             print(json.dumps({
#                 "board": board,
#                 "history": history,
#                 "winner": winner
#             }))
#             return
#         if mode == "single":
#             ai_player = "O" if player == "X" else "X"
#             ai_move = best_move(board, history, depth, ai_player)
            
#         if ai_move is not None:
#             board[ai_move] = ai_player
#             history.append({"player": ai_player, "index": ai_move})
#             vanishpl(board, history, ai_player)

#         winner = winnercheck(board)

#         print(json.dumps({
#             "board": board,
#             "history": history,
#             "winner": winner,
#             "ai_move": ai_move
#         }))

#     except Exception as e:
#         print(json.dumps({ "error": str(e) }))

# if __name__ == "__main__":
#     main()




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys

from ai import best_move
from rules import winnercheck, vanishpl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameState(BaseModel):
    board: List[str]
    history: List[Dict[str, Any]]
    depth: int = 4
    player: str = "X"
    move_index: Optional[int] = None
    mode: str = "single"

@app.post("/move")
def make_move(state: GameState):
    try:
        board = state.board.copy()
        history = state.history.copy()
        player = state.player
        ai_move = None

        if state.move_index is not None:
            board[state.move_index] = player
            history.append({"player": player, "index": state.move_index})
            vanishpl(board, history, player)

        winner = winnercheck(board)
        if winner:
            return {"board": board, "history": history, "winner": winner}
            
        if state.mode == "single":
            ai_player = "O" if player == "X" else "X"
            ai_move = best_move(board, history, state.depth, ai_player)
            
            if ai_move is not None:
                board[ai_move] = ai_player
                history.append({"player": ai_player, "index": ai_move})
                vanishpl(board, history, ai_player)

        winner = winnercheck(board)

        return {
            "board": board,
            "history": history,
            "winner": winner,
            "ai_move": ai_move
        }

    except Exception as e:
        return {"error": str(e)}