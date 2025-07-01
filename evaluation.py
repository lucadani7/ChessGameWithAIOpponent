from move_generator import MoveGenerator


class Evaluation:
    def __init__(self):
        self.piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
        self.pawn_table = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 5, 5, -5, -5, 5, 5, 5],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
            [0.5, 1, 1, -2, -2, 1, 1, 0.5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.knight_table = [
            [-5, -4, -3, -3, -3, -3, -4, -5],
            [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
            [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
            [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
            [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
            [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
            [-4, -2, 0, 0, 0, 0, -2, -4],
            [-5, -4, -3, -3, -3, -3, -4, -5]
        ]

    def calculate_percentage(self, part, total, round_to=2):
        return 0 if min(part, total) == 0 else round((part / total) * 100, round_to)

    def reverse_table(self, table):
        return table[::-1]

    def mobility_score(self, board, color):
        return 0.1 * len(MoveGenerator().get_legal_moves(board, color))

    def center_control_score(self, board, color, enemy):
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        score = 0

        # Create attack maps
        my_moves = MoveGenerator().get_detailed_moves(board, color)  # [(r1, c1, r2, c2, piece_type), ...]
        enemy_moves = MoveGenerator().get_detailed_moves(board, enemy)

        for square in center_squares:
            attackers = {"P": 0, "N": 0, "B": 0, "R": 0, "Q": 0, "K": 0}
            defenders = {"P": 0, "N": 0, "B": 0, "R": 0, "Q": 0, "K": 0}

            # Count friendly attackers
            for r1, c1, r2, c2, ptype in my_moves:
                if (r2, c2) == square:
                    attackers[ptype] += 1

            # Count enemy attackers (aka defenders)
            for r1, c1, r2, c2, ptype in enemy_moves:
                if (r2, c2) == square:
                    defenders[ptype] += 1

            # Piece-weighted influence
            piece_weights = {
                "P": 1, "N": 3, "B": 3.3, "R": 5, "Q": 9, "K": 0
            }

            atk_score = sum(attackers[p] * piece_weights[p] for p in attackers)
            def_score = sum(defenders[p] * piece_weights[p] for p in defenders)

            total_pressure = atk_score + def_score
            if total_pressure > 0:
                percent = (atk_score / total_pressure) * 100
                score += (percent - 50) * 0.05  # scale effect so ±50% → ±2.5 pts

            # Bonus for full control (no defenders)
            if def_score == 0 and atk_score > 0:
                score += 0.3
            elif atk_score == 0 and def_score > 0:
                score -= 0.3

        return round(score, 2)

    def pawn_structure_score(self, board, color):
        score = 0
        files = {i: [] for i in range(8)}
        enemy_color = "b" if color == "w" else "w"

        for row in range(8):
            for col in range(8):
                if board[row][col] == color + "P":
                    files[col].append(row)

        for col in range(8):
            pawns = files[col]
            if not pawns:
                continue

            if len(pawns) > 1:
                score -= 0.5 * (len(pawns) - 1)

            for row in pawns:
                # Isolated check
                is_isolated = True
                for adj in [col - 1, col + 1]:
                    if 0 <= adj < 8 and files[adj]:
                        is_isolated = False
                if is_isolated:
                    score -= 0.3

                # Passed pawn check
                blocked = False
                for r in range(row - 1, -1, -1) if color == "w" else range(row + 1, 8):
                    for dc in [col - 1, col, col + 1]:
                        if 0 <= dc < 8 and board[r][dc] == enemy_color + "P":
                            blocked = True
                if not blocked:
                    score += 0.5

        return score

    def evaluate_board(self, board, color, personality="machine", verbose=False):
        enemy = "b" if color == "w" else "w"
        score, positional_bonus, material = 0, 0, 0

        for row in range(8):
            for col in range(8):
                square = board[row][col]
                if square.strip():
                    pc_color = square[0]
                    pc_type = square[1]
                    val = self.piece_values.get(pc_type, 0)

                    # Positional table bonuses
                    bonus = 0
                    match pc_type:
                        case "P":
                            table = self.pawn_table if pc_color == "w" else self.reverse_table(self.pawn_table)
                            bonus = table[row][col]
                        case "N":
                            table = self.knight_table if pc_color == "w" else self.reverse_table(self.knight_table)
                            bonus = table[row][col]

                    total_piece_score = val + bonus
                    material += val if pc_color == color else -val
                    positional_bonus += bonus if pc_color == color else -bonus
                    score += total_piece_score if pc_color == color else -total_piece_score

            # — Modular Heuristic Weights Based on Personality —
            structure = self.pawn_structure_score(board, color)
            mobility = self.mobility_score(board, color)
            center = self.center_control_score(board, color, enemy)
            match personality:
                case "positionalist":
                    score += 0.6 * structure + 0.3 * mobility + 0.4 * center
                case "gambiteer":
                    score += 0.2 * structure + 0.7 * mobility - 0.1 * abs(structure) + 0.1 * center
                case "grinder":
                    score += 0.7 * structure + 0.4 * mobility + 0.3 * center
                case "romantic":
                    score += 0.1 * structure + 0.8 * mobility + 0.2 * center
                case _:
                    score += 0.4 * structure + 0.5 * mobility + 0.25 * center

            if verbose:
                base_total = abs(material) + abs(positional_bonus) + abs(structure) + abs(mobility) + abs(center)
                print(f"\n🧠 Evaluation Breakdown [{personality.upper()}]:")
                print(f"  Material:   {self.calculate_percentage(abs(material), base_total)}%")
                print(f"  Positional: {self.calculate_percentage(abs(positional_bonus), base_total)}%")
                print(f"  Structure:  {self.calculate_percentage(abs(structure), base_total)}%")
                print(f"  Mobility:   {self.calculate_percentage(abs(mobility), base_total)}%")
                print(f"  Center Ctrl: {self.calculate_percentage(abs(center), base_total)}%")
                print(f"  Total Evaluation: {round(score, 2)}")

        return round(score, 2)
