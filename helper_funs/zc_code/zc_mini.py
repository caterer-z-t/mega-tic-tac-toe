##############################################################################
###
###                             Imports
###
##############################################################################

from helper_funs.helper_fn import nested_tic_tac_toe_board

##############################################################################
###
###                             Main Code for MINI Game
###
##############################################################################

"""
Copied from joe code earlier -- want to keep for implementing mega game
"""
# Implements a single tic-tac-toe game
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Create an empty board
        self.current_player = 'X'

    def print_board(self):
        for j in range(0,3):
            row = [self.board[i*3:(i+1)*3] for i in range(3)][j]
            print('  ' + ' | '.join(row) + '  ')
            if j >= 0 and j <2:
                print(' ---+---+---')


    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            if self.check_winner():
                print(f'Player {self.current_player} wins!')
                return True
            elif ' ' not in self.board:
                print("It's a draw!")
                return True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                return False
        else:
            print("Invalid move. Position already taken.")
            return False

    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True
        return False

# Example usage:
game = TicTacToe()
game.print_board()

while True:
    x, y = map(int, input(f"Player {game.current_player}, enter your move (format: row,col): ").split(','))
    position = int(3*(x-1) + (y-1))
    if game.make_move(position):
        game.print_board()
        break
    game.print_board()
