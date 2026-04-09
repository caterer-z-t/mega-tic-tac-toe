EMPTY = 0
X = 1
O = -1
DRAW = 2

WINNING_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),              # diagonals
]


class MegaTicTacToe:
    """
    Ultimate (Mega) Tic-Tac-Toe.

    The board is a 3×3 grid of mini 3×3 boards (9 boards × 9 cells = 81 cells).
    After each move in cell `c` of a mini-board, the opponent must play in
    mini-board `c`.  If that board is already won or full, the opponent may
    play in any available board.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        # cells[mini_board_idx][cell_idx]  →  EMPTY | X | O
        self.cells = [[EMPTY] * 9 for _ in range(9)]
        # EMPTY = still in play, X/O = that player won, DRAW = full with no winner
        self.mini_winners = [EMPTY] * 9
        self.current_player = X
        # -1 means the player can choose any available mini-board
        self.active_board = -1
        self.game_winner = EMPTY   # EMPTY | X | O | DRAW
        self.game_over = False
        self.move_history = []     # list of (mini_board, cell, player)

    # ------------------------------------------------------------------
    # Move logic
    # ------------------------------------------------------------------

    def _board_available(self, idx: int) -> bool:
        return (
            self.mini_winners[idx] == EMPTY
            and any(c == EMPTY for c in self.cells[idx])
        )

    def get_valid_moves(self) -> list:
        if self.game_over:
            return []
        boards = (
            [i for i in range(9) if self._board_available(i)]
            if self.active_board == -1
            else [self.active_board]
        )
        return [
            (b, c)
            for b in boards
            for c in range(9)
            if self.cells[b][c] == EMPTY
        ]

    def make_move(self, mini_board: int, cell: int) -> bool:
        if (mini_board, cell) not in self.get_valid_moves():
            return False

        self.cells[mini_board][cell] = self.current_player
        self.move_history.append((mini_board, cell, self.current_player))

        self.mini_winners[mini_board] = self._check_mini_winner(mini_board)
        self.game_winner = self._check_game_winner()

        # Next active board is determined by the cell just played
        self.active_board = cell if self._board_available(cell) else -1

        self.current_player = O if self.current_player == X else X

        if self.game_winner != EMPTY:
            self.game_over = True
        elif not self.get_valid_moves():
            self.game_over = True
            self.game_winner = DRAW

        return True

    # ------------------------------------------------------------------
    # Win detection
    # ------------------------------------------------------------------

    def _check_mini_winner(self, board_idx: int) -> int:
        cells = self.cells[board_idx]
        for a, b, c in WINNING_COMBOS:
            if cells[a] != EMPTY and cells[a] == cells[b] == cells[c]:
                return cells[a]
        if all(c != EMPTY for c in cells):
            return DRAW
        return EMPTY

    def _check_game_winner(self) -> int:
        w = self.mini_winners
        for a, b, c in WINNING_COMBOS:
            if w[a] not in (EMPTY, DRAW) and w[a] == w[b] == w[c]:
                return w[a]
        return EMPTY

    # ------------------------------------------------------------------
    # Serialisation (used by Dash dcc.Store)
    # ------------------------------------------------------------------

    def copy(self) -> "MegaTicTacToe":
        g = MegaTicTacToe.__new__(MegaTicTacToe)
        g.cells = [row[:] for row in self.cells]
        g.mini_winners = self.mini_winners[:]
        g.current_player = self.current_player
        g.active_board = self.active_board
        g.game_winner = self.game_winner
        g.game_over = self.game_over
        g.move_history = self.move_history[:]
        return g

    def to_dict(self) -> dict:
        return {
            "cells": self.cells,
            "mini_winners": self.mini_winners,
            "current_player": self.current_player,
            "active_board": self.active_board,
            "game_winner": self.game_winner,
            "game_over": self.game_over,
            "move_history": self.move_history,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "MegaTicTacToe":
        g = cls.__new__(cls)
        g.cells = d["cells"]
        g.mini_winners = d["mini_winners"]
        g.current_player = d["current_player"]
        g.active_board = d["active_board"]
        g.game_winner = d["game_winner"]
        g.game_over = d["game_over"]
        g.move_history = d["move_history"]
        return g
