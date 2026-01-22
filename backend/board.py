
board = [" "] * 9
history = []


def printb(board):
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])


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
