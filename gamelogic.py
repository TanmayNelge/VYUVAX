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

# current_player = "X"

# while True:
#     print(f"{current_player}'s turn")
#     pos = int(input("Enter position (0-8): "))
#     movepl(board, pos, current_player)
#     board, history = vanishpl(board, history, current_player)

#     print("\n")
#     printb(board)
#     print("\n")

#     winner = winnercheck(board)
#     if winner:
#         print(winner, "wins!")
#         break

#     current_player = "O" if current_player == "X" else "X"

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



    


