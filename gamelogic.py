board = [" "]*9

def printb(board):
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])


history=[]
def movepl(board, position, player):
    if board[position] != " ":
        raise ValueError("Position already occupied")
    board[position] = player
    history.append((position, player))

    return board

def vanishpl(board, history, player):
    player_move=[]
    for m in history:
        if m[1] == player:
            player_move.append(m)
    
    if len(player_move)>3:
        oldpos, _ = player_move[0]
        board[oldpos] = " "
        history.remove(player_move[0])
    return board, history

winning_positions =[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def winnercheck(board):
    for a,b,c in winning_positions:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None

current_player = "X"

while True:
    print(f"{current_player}'s turn")
    pos = int(input("Enter position (0-8): "))
    movepl(board, pos, current_player)
    board, history = vanishpl(board, history, current_player)

    print("\n")
    printb(board)
    print("\n")

    winner = winnercheck(board)
    if winner:
        print(winner, "wins!")
        break

    current_player = "O" if current_player == "X" else "X"

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

def heuristic(player):
    score = 0

    # considering positive scores for "X" and negative for "O"
    for i in range(3):
        # row
        score += evaluate_line(board[i],"X")
        score -= evaluate_line(board[i],"O")

        # col
        col = [board[j][i] for j in range(3)]
        score += evaluate_line(col,"X")
        score -= evaluate_line(col,"O")

    # diagnol
    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2-i] for i in range(3)]

    score += evaluate_line(diag1,"X")
    score += evaluate_line(diag2,"X")
    score -= evaluate_line(diag1,"O")
    score -= evaluate_line(diag2,"O")

    return score

# heuristic logic added

