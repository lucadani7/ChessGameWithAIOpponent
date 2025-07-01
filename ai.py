from copy import deepcopy

from evaluation import Evaluation
from move_generator import MoveGenerator

PERSONALITIES = ["machine", "positionalist", "gambiteer", "grinder", "romantic"]


def find_best_move(board, color, depth):
    best_move = None
    best_score = float('-inf')
    for move in MoveGenerator().get_legal_moves(board, color):
        r1, c1, r2, c2 = move
        new_board = deepcopy(board)
        new_board[r2][c2] = new_board[r1][c1]
        new_board[r1][c1] = "  "

        score = minimax(new_board, depth - 1, float('-inf'), float('inf'), False, "b" if color == "w" else "w")

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def minimax(board, depth, alpha, beta, maximizing_player, color):
    if depth == 0 or MoveGenerator().is_in_check(board, color):
        return Evaluation().evaluate_board(board, color)

    legal_moves = MoveGenerator().get_legal_moves(board, color)
    if not legal_moves:
        return Evaluation().evaluate_board(board, color)

    best_score = float('-inf') if maximizing_player else float('inf')
    next_color = "b" if color == "w" else "w"

    for move in legal_moves:
        r1, c1, r2, c2 = move
        new_board = deepcopy(board)
        new_board[r2][c2] = new_board[r1][c1]
        new_board[r1][c1] = "  "

        score = minimax(new_board, depth - 1, alpha, beta, not maximizing_player, next_color)

        best_score = max(best_score, score) if maximizing_player else min(best_score, score)
        if maximizing_player:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)

        if beta <= alpha:
            break

    return best_score
