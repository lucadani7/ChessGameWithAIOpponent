from copy import deepcopy

from utils import on_board, is_empty, is_enemy


class MoveGenerator:
    def get_all_moves(self, board, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.startswith(color):
                    piece_type = piece[1]
                    pos = (row, col)
                    match piece_type:
                        case "P":
                            moves += self.get_pawn_moves(board, pos, color)
                        case "R":
                            moves += self.get_rook_moves(board, pos, color)
                        case "Q":
                            moves += self.get_queen_moves(board, pos, color)
                        case "K":
                            moves += self.get_king_moves(board, pos, color)
                        case "B":
                            moves += self.get_bishop_moves(board, pos, color)
                        case "N":
                            moves += self.get_knight_moves(board, pos, color)
        return moves

    def get_pawn_moves(self, board, pos, color):
        row, col = pos
        direction = -1 if color == "w" else 1
        start_row = 6 if color == "w" else 1
        moves = []

        # Forward move
        if on_board(row + direction, col) and is_empty(board, row + direction, col):
            moves.append((row, col, row + direction, col))

            # Double move from starting row
            if row == start_row and is_empty(board, row + 2 * direction, col):
                moves.append((row, col, row + 2 * direction, col))

        # Captures
        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if on_board(r, c) and is_enemy(board, r, c, color):
                moves.append((row, col, r, c))

        return moves

    def get_knight_moves(self, board, pos, color):
        row, col = pos
        directions = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        moves = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if on_board(r, c) and (is_empty(board, r, c) or is_enemy(board, r, c, color)):
                moves.append((row, col, r, c))

        return moves

    def get_king_moves(self, board, pos, color):
        row, col = pos
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        moves = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if on_board(r, c) and (is_empty(board, r, c) or is_enemy(board, r, c, color)):
                moves.append((row, col, r, c))

        return moves

    def get_sliding_moves(self, board, pos, color, directions):
        row, col = pos
        moves = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while on_board(r, c):
                if is_empty(board, r, c):
                    moves.append((row, col, r, c))
                elif is_enemy(board, r, c, color):
                    moves.append((row, col, r, c))
                    break
                else:
                    break
                r += dr
                c += dc

        return moves

    def is_in_check(self, board, color):
        enemy_color = "b" if color == "w" else "w"

        # Find king position
        king_pos = None
        for row in range(8):
            for col in range(8):
                if board[row][col] == color + "K":
                    king_pos = (row, col)
                    break

        # Scan enemy moves to see if they attack king
        enemy_moves = self.get_all_moves(board, enemy_color)
        for move in enemy_moves:
            _, _, r, c = move
            if (r, c) == king_pos:
                return True
        return False

    def get_legal_moves(self, board, color):
        candidate_moves = self.get_all_moves(board, color)
        legal_moves = []

        for move in candidate_moves:
            r1, c1, r2, c2 = move
            new_board = deepcopy(board)

            # Make the move
            new_board[r2][c2] = new_board[r1][c1]
            new_board[r1][c1] = "  "

            # Check legality
            if not self.is_in_check(new_board, color):
                legal_moves.append(move)

        return legal_moves

    def get_detailed_moves(self, board, color):
        basic_moves = self.get_legal_moves(board, color)
        detailed = []

        for r1, c1, r2, c2 in basic_moves:
            from_piece = board[r1][c1].strip()
            to_piece = board[r2][c2].strip()

            if not from_piece:
                continue  # defensive coding, just in case

            piece_type = from_piece[1]
            is_capture = bool(to_piece and to_piece[0] != color)

            # Promotion detection
            is_promotion = (
                    piece_type == "P"
                    and ((color == "w" and r2 == 0) or (color == "b" and r2 == 7))
            )

            # Check detection
            new_board = deepcopy(board)
            new_board[r2][c2] = new_board[r1][c1]
            new_board[r1][c1] = "  "
            gives_check = self.is_in_check(new_board, "b" if color == "w" else "w")

            detailed.append(
                (r1, c1, r2, c2, piece_type, is_capture, is_promotion, gives_check)
            )

        return detailed

    def get_rook_moves(self, board, pos, color):
        return self.get_sliding_moves(board, pos, color, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def get_bishop_moves(self, board, pos, color):
        return self.get_sliding_moves(board, pos, color, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def get_queen_moves(self, board, pos, color):
        return self.get_sliding_moves(board, pos, color,
                                      [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])
    

    
