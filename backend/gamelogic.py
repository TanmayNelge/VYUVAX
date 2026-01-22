import math
# import random.py

board = [" "]*9

def printb(board):
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])


history=[]
def movepl(board, history, position, player):
    if board[position] != " ":
        return False
    
    board[position] = player
    history.append((position, player))

    return True

def vanishpl(board, history, player):
    player_moves = [m for m in history if m[1] == player]

    removed = None
    if len(player_moves) > 3:
        removed = player_moves[0]
        board[removed[0]] = " "
        history.remove(removed)

    return removed

def undo_move(board, history, position, removed):
    board[position] = " "
    history.pop()

    if removed:
        pos, player = removed
        board[pos] = player
        history.insert(0, removed)


winning_positions =[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def winnercheck(board):
    for a,b,c in winning_positions:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None

# adding heuristic logic

def evaluate_line(line,player):
    opponent = "O" if player=="X" else "X"

    if opponent in line:
        return 0
    
    count = line.count(player)

    if(count==3):
        return 1000
    if(count==2):
        return 100
    if(count==1):
        return 1
    
    return 0

def heuristic(board):
    score = 0

    # considering positive scores for "X" and negative for "O"
    rows = [board[0:3], board[3:6], board[6:9]]
    cols = [
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]]
    ]
    diags = [
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]]
    ]

    for line in rows + cols + diags:
        score += evaluate_line(line, "X")
        score -= evaluate_line(line, "O")

    return score

# heuristic logic added
# Minimax algorithm with heuristic and alpha beta prunning


def minimax(board,history,depth,alpha,beta,maximizing):
    winner = winnercheck(board)

    if winner == "X":
        return 1000
    if winner == "O":
        return -1000
    if depth == 0:
        return heuristic(board)
    
    if maximizing:
        best = -math.inf
        for i in range(9):
            if board[i]==" ":
                movepl(board,history,i,"X")
                removed = vanishpl(board,history,"X")

                value = minimax(board,history,depth-1,alpha,beta,False)

                undo_move(board,history,i,removed)

                best = max(best,value)
                alpha = max(alpha,best)
                if beta<=alpha:
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i]==" ":
                movepl(board,history,i,"O")
                removed = vanishpl(board,history,"O")

                value = minimax(board,history,depth-1,alpha,beta,True)

                undo_move(board,history,i,removed)

                best = min(best,value)
                beta = min(best,beta)
                if beta<=alpha:
                    break
    return best
    
def best_move(board,history,depth):
    # assuming ai is X 
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == " ":
            movepl(board,history,i,"X")
            removed = vanishpl(board,history,"X")

            score = minimax(board,history,depth-1,-math.inf,math.inf,False)

            undo_move(board,history,i,removed)

            if score > best_score:
                best_score = score
                move = i
                
    return move

def play():

    print("Choose mode to play:\n")
    choice = int(input("1.AI\n2.Friend:\n" ))
    depth = 10
    current_player = "O"
    print("Vanishing Tic-Tac-Toe")
    print()
    if(choice == 1):
        print("You are O | AI is X")
        print()

        while True:
            printb(board)
            print()
            winner = winnercheck(board)
            if winner:
                print(winner, "Wins!")
                break

            if current_player == "O":
                pos = int(input("Enter position (0-8): "))
                if not movepl(board, history, pos, "O"):
                    print("Invalid move")
                    continue
                vanishpl(board, history, "O")
                current_player = "X"
            else:
                pos = best_move(board, history, depth)
                movepl(board, history, pos, "X")
                vanishpl(board, history, "X")
                current_player = "O"
    
    else:
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

play()


