"""
AI player for Mega Tic-Tac-Toe.

Levels
------
random  – picks a uniformly random valid move
easy    – simple heuristic (win > win-mini-board > block > center)
medium  – minimax, depth 2
hard    – minimax with alpha-beta pruning, depth 4
expert  – minimax with alpha-beta pruning, depth 6
"""

import math
import random

from game.board import DRAW, EMPTY, O, WINNING_COMBOS, X, MegaTicTacToe

_LEVEL_DEPTH = {
    "random": 0,
    "easy": 0,
    "medium": 2,
    "hard": 4,
    "expert": 6,
}


class AIPlayer:
    def __init__(self, level: str = "medium"):
        self.level = level

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_move(self, game: MegaTicTacToe):
        """Return (mini_board, cell) for the best move at the chosen level."""
        moves = game.get_valid_moves()
        if not moves:
            return None
        if self.level == "random":
            return random.choice(moves)
        if self.level == "easy":
            return self._easy_move(game, moves)
        depth = _LEVEL_DEPTH.get(self.level, 2)
        return self._minimax_best(game, depth)

    # ------------------------------------------------------------------
    # Easy heuristic
    # ------------------------------------------------------------------

    def _easy_move(self, game: MegaTicTacToe, moves: list):
        player = game.current_player
        opponent = O if player == X else X

        # 1. Win the overall game immediately
        for mb, c in moves:
            g = game.copy()
            g.make_move(mb, c)
            if g.game_winner == player:
                return (mb, c)

        # 2. Win a mini-board
        win_mini = [
            (mb, c)
            for mb, c in moves
            if self._would_win_mini(game.cells[mb], c, player)
        ]
        if win_mini:
            return random.choice(win_mini)

        # 3. Block opponent from winning a mini-board
        block_mini = [
            (mb, c)
            for mb, c in moves
            if self._would_win_mini(game.cells[mb], c, opponent)
        ]
        if block_mini:
            return random.choice(block_mini)

        # 4. Prefer center cells
        centers = [(mb, c) for mb, c in moves if c == 4]
        if centers:
            return random.choice(centers)

        return random.choice(moves)

    @staticmethod
    def _would_win_mini(cells: list, cell_idx: int, player: int) -> bool:
        test = cells[:]
        test[cell_idx] = player
        for a, b, c in WINNING_COMBOS:
            if test[a] == test[b] == test[c] == player:
                return True
        return False

    # ------------------------------------------------------------------
    # Minimax with alpha-beta pruning
    # ------------------------------------------------------------------

    def _minimax_best(self, game: MegaTicTacToe, depth: int):
        player = game.current_player
        best_score = -math.inf
        best_moves: list = []

        moves = game.get_valid_moves()
        # Order moves: winning moves first, then center cells
        moves = self._order_moves(game, moves, player)

        for mb, c in moves:
            g = game.copy()
            g.make_move(mb, c)
            score = self._minimax(g, depth - 1, -math.inf, math.inf, False, player)
            if score > best_score:
                best_score = score
                best_moves = [(mb, c)]
            elif score == best_score:
                best_moves.append((mb, c))

        return random.choice(best_moves) if best_moves else moves[0]

    def _minimax(
        self,
        game: MegaTicTacToe,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        player: int,
    ) -> float:
        opponent = O if player == X else X

        if game.game_over:
            if game.game_winner == player:
                return 1000 + depth          # win sooner is better
            if game.game_winner == opponent:
                return -1000 - depth         # lose later is better
            return 0                          # draw

        if depth == 0:
            return self._evaluate(game, player)

        moves = game.get_valid_moves()

        if maximizing:
            val = -math.inf
            for mb, c in moves:
                g = game.copy()
                g.make_move(mb, c)
                val = max(val, self._minimax(g, depth - 1, alpha, beta, False, player))
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return val
        else:
            val = math.inf
            for mb, c in moves:
                g = game.copy()
                g.make_move(mb, c)
                val = min(val, self._minimax(g, depth - 1, alpha, beta, True, player))
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return val

    # ------------------------------------------------------------------
    # Heuristic evaluation (non-terminal positions)
    # ------------------------------------------------------------------

    def _evaluate(self, game: MegaTicTacToe, player: int) -> float:
        opponent = O if player == X else X
        score = 0.0

        # Mini-board win/loss
        for w in game.mini_winners:
            if w == player:
                score += 10
            elif w == opponent:
                score -= 10

        # Potential winning lines across the mega-board
        for a, b, c in WINNING_COMBOS:
            vals = [game.mini_winners[i] for i in (a, b, c)]
            p_cnt = sum(1 for v in vals if v == player)
            o_cnt = sum(1 for v in vals if v == opponent)
            if o_cnt == 0 and p_cnt:
                score += p_cnt * 2
            elif p_cnt == 0 and o_cnt:
                score -= o_cnt * 2

        # Center mini-board is strategically valuable
        if game.mini_winners[4] == player:
            score += 4
        elif game.mini_winners[4] == opponent:
            score -= 4

        # Corner mini-boards
        for corner in (0, 2, 6, 8):
            if game.mini_winners[corner] == player:
                score += 2
            elif game.mini_winners[corner] == opponent:
                score -= 2

        return score

    # ------------------------------------------------------------------
    # Move ordering (improves alpha-beta cut efficiency)
    # ------------------------------------------------------------------

    def _order_moves(self, game: MegaTicTacToe, moves: list, player: int) -> list:
        opponent = O if player == X else X

        def priority(move):
            mb, c = move
            # Highest priority: immediately win the game
            g = game.copy()
            g.make_move(mb, c)
            if g.game_winner == player:
                return 0
            # Win a mini-board
            if self._would_win_mini(game.cells[mb], c, player):
                return 1
            # Block opponent mini-board win
            if self._would_win_mini(game.cells[mb], c, opponent):
                return 2
            # Center cell
            if c == 4:
                return 3
            # Corner cell
            if c in (0, 2, 6, 8):
                return 4
            return 5

        random.shuffle(moves)   # break ties randomly
        return sorted(moves, key=priority)
