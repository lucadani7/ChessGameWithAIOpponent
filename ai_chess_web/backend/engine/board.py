class Board:

    def initialize_board(self):
        return [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], ["bP"] * 8, ["  "] * 8, ["  "] * 8, ["  "] * 8,
                ["  "] * 8, ["wP"] * 8,
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

    def print_board(self, board):
        print("  a  b  c  d  e  f  g  h")
        for i, row in enumerate(board):
            print(8 - i, end=" ")
            for square in row:
                print(square if square.strip() else "..", end=" ")
            print()

    def coord_to_index(self, pos):
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        return row, col

    def get_piece(self, board, pos):
        row, col = self.coord_to_index(pos)
        return board[row][col]

    def move_piece(self, board, start, end):
        start_row, start_col = self.coord_to_index(start)
        end_row, end_col = self.coord_to_index(end)
        piece = board[start_row][start_col]
        board[start_row][start_col] = "  "
        board[end_row][end_col] = piece
