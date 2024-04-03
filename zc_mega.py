##############################################################################
###
###                             Imports
###
##############################################################################

from helper_funs.helper_fn import nested_tic_tac_toe_board
import os

##############################################################################
###
###                             Main Code for MINI Game
###
##############################################################################

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')

class UltimateTicTacToe:
    def __init__(self):
        # Initialize a 3x3 grid of empty Tic Tac Toe boards
        self.boards = {(x, y): {(i, j): ' ' for i in range(1, 4) for j in range(1, 4)} for x in range(1, 4) for y in range(1, 4)}
        self.current_player = 'X'
        self.current_board = None  # To control which board the next move should be made on
        self.board_status = {(x, y): ' ' for x in range(1, 4) for y in range(1, 4)}  # To track which mini-boards have been won or tied

    def print_board(self):
        clear_terminal()
        nested_tic_tac_toe_board(self.boards)

    def make_move(self, board_position, position):
        if self.current_board and board_position != self.current_board:
            print(f"You must play in the {self.current_board} board.")
            return False
        board = self.boards[board_position]
        if board[position] != ' ':
            print("This square is already taken.")
            return False
        board[position] = self.current_player
        if self.check_winner(board_position):
            print(f"{self.current_player} wins the board {board_position}!")
            self.board_status[board_position] = self.current_player
        elif all(space != ' ' for space in board.values()):
            print(f"The board {board_position} is a draw.")
            self.board_status[board_position] = 'D'  # D for Draw
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.current_board = position  # Set the next mini-board to play in based on the last move
        return True

    def check_winner(self, board_key):
        board = self.boards[board_key]
        # Define winning combinations for a mini-board
        winning_combinations = [
            ((1, 1), (1, 2), (1, 3)), ((2, 1), (2, 2), (2, 3)), ((3, 1), (3, 2), (3, 3)),  # Rows
            ((1, 1), (2, 1), (3, 1)), ((1, 2), (2, 2), (3, 2)), ((1, 3), (2, 3), (3, 3)),  # Columns
            ((1, 1), (2, 2), (3, 3)), ((1, 3), (2, 2), (3, 1))  # Diagonals
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
                return True
        return False

    def check_global_winner(self):
        # Convert board status to a linear sequence to use the existing logic
        linear_board_status = [
            self.board_status[(x, y)] for x in range(1, 4) for y in range(1, 4)
        ]
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for combo in winning_combinations:
            if linear_board_status[combo[0]] == linear_board_status[combo[1]] == linear_board_status[combo[2]] != ' ':
                print(f"Player {linear_board_status[combo[0]]} wins the game!")
                return True
        return False
    
# Example usage:
game = UltimateTicTacToe()
game.print_board()

while True:
    try:
        board_x, board_y, pos_x, pos_y = map(int, input(f"Player {game.current_player}, enter your move (format: board_row,board_col row,col): ").split(','))
        board_position = (board_x, board_y)
        position = (pos_x, pos_y)
        if game.make_move(board_position, position):
            game.print_board()
            if game.check_global_winner():
                break
            # Check if the move sends the next player to a completed board
            if game.board_status[game.current_board] != ' ':
                print("This board is already completed, you may choose any other board.")
                game.current_board = None
    except ValueError:
        print("Invalid input. Please enter your move as four comma-separated numbers.")

