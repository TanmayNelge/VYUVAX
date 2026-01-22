import random
from gamelogic import best_move, movepl, vanishpl, winnercheck

def random_agent(board):
    legal_moves = [i for i, cell in enumerate(board) if cell == " "]
    
    if legal_moves:
        return random.choice(legal_moves)
    return None

def play_tournament(games=10):
    results = {"AI (X)": 0, "Random (O)": 0, "Draw": 0}
    
    for i in range(games):
        current_board = [" "] * 9
        current_history = []
        current_player = "X"
        game_over = False
        
        # Limit turns to 50 to prevent infinite loops
        for turn in range(50):
            if current_player == "X":
                # AI's turn
                move = best_move(current_board, current_history, depth=4,player="X")
            else:
                # Random Agent's turn
                #move = random_agent(current_board)
                move = best_move(current_board,current_history,depth=6,player="O")
            
            if move is None: break
            
            movepl(current_board, current_history, move, current_player)
            vanishpl(current_board, current_history, current_player)
            
            winner = winnercheck(current_board)
            if winner:
                results[f"AI (X)" if winner == "X" else "Random (O)"] += 1
                game_over = True
                break
            
            current_player = "O" if current_player == "X" else "X"
            
        if not game_over:
            results["Draw"] += 1
            
    return results

def random_vs_ai():
    no=int(input("Enter number of games for comparisions: "))
    tournament_results = play_tournament(no)
    print(f"Final Statistics: {tournament_results}")

random_vs_ai()