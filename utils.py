def on_board(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def is_enemy(board, row, col, color):
    piece = board[row][col]
    return piece != "  " and not piece.startswith(color)


def is_empty(board, row, col):
    return board[row][col] == "  "
