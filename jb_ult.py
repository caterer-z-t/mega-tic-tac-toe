import os
import time

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')

'''
    This implements a game of Ultimate tic-tac-toe
'''
# Create the ultimate tic-tac-toe game
class ultimate:
    # Initialize as an array of smaller tic-tac-toe games, and one board to represent the larger board
    def __init__(self):
        self.ult_board = []
        for i in range(0,9):
            self.ult_board.append(TicTacToe())
        self.current_player = 'X'
        self.eq_board = TicTacToe()
        self.curr_board = None
    
    def print_ult_board(self):
        clear_terminal()
        for row in range(3):
            for j in range(len(self.ult_board[0].board_arr)):
                print(self.ult_board[row*3].board_arr[j], " || ", self.ult_board[row*3+1].board_arr[j], " || " 
                      + self.ult_board[row*3+2].board_arr[j])
            if(row == 0 or row == 1):
                print('===============||=================||===============')
    
    def make_move(self, move):
        # Set the current player for the small board to the same as the current player
        self.ult_board[self.curr_board].current_player = self.current_player
        # try to make the move
        self.ult_board[self.curr_board].make_move(move)
        # The next move will take place in the board according to the current move
        self.curr_board = move
        # Check for a winner
        if self.check_winner():
            print(f"{self.current_player} wins the board!")
            return False
        elif self.ult_board[self.curr_board].winner != None:
            # if the next board was already won, there is no given next board, need to ask player
            self.curr_board = None
        elif self.check_draw():
            print("Its a draw")
            return False
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    
    def check_draw(self):
        for game in self.ult_board:
            if game.winner == None:
                return False
        return True
        
    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        # Check for winning combo
        for combo in winning_combinations:
            if self.ult_board[combo[0]].winner == self.ult_board[combo[1]].winner == \
                    self.ult_board[combo[2]].winner != None:
                self.winner = self.current_player
                return True
        return False
    

# Implements a single tic-tac-toe game
class TicTacToe:
    # initialize the board, starting player is always X for now
    def __init__(self):
        self.winner = None
        self.board = [' ' for _ in range(9)]  # Create an empty board
        self.current_player = 'X'
        self.board_arr = [""]*5
        self.printable_board()

    # Get the board as a printable array
    def printable_board(self):
        for j in range(0,3):
            row = [self.board[i*3:(i+1)*3] for i in range(3)][j]
            self.board_arr[j*2] = str('  ' + ' | '.join(row) + '  ')
            if j >= 0 and j <2:
                self.board_arr[j*2+1] = str(' ---+---+--- ')
                
    # print the board
    def print_board(self):
        for i in range(len(self.board_arr)):
            print(self.board_arr[i])  
              
    # Make a move given the player and position selected
    def make_move(self, position):
        # Make sure empty space
        if self.board[position] == ' ':
            # Make the move
            self.board[position] = self.current_player
            
            # check winner
            if self.check_winner():
                #print(f'Player {self.winner} wins!')
                return True
            # if no winner, and no open space, its a draw
            elif ' ' not in self.board:
                print("It's a draw!")
                self.board_arr = ["             ",
                                  "             ",
                                  "             ",
                                  "             ",
                                  "             "]
                return True
            # otherewise swap players
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.printable_board()
                return False
        else:
            print("Invalid move. Position already taken.")
            return False
    # check for a winner
    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        # Check for winning combo
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.winner = self.current_player
                if self.winner == 'X':
                    self.board_arr=["    \   /    ",
                                    "     \ /     ",
                                    "      X      ",
                                    "     / \     ",
                                    "    /   \    "]
                else:
                    self.board_arr=["      _      ",
                                    "    /   \    ",
                                    "   |     |   ",
                                    "    \ _ /    ",
                                    "             "]
                return True
        return False

def move_helper(game):
    try:
        game.print_ult_board()
        if game.curr_board == None:
            board_x, board_y, pos_x, pos_y = map(int, input(f"Player {game.current_player}, enter your move (format: board_row,board_col row,col): ").split(','))
            game.curr_board = (board_x-1)*3 + board_y-1
        else: 
            pos_x, pos_y = map(int, input(f"Player {game.current_player}, enter your move (format: row,col)\n\tYou are playing in board {int((game.curr_board - (game.curr_board%3)+1)/3 + 1)}, {(game.curr_board%3) + 1}: ").split(','))
        
        move = (pos_x-1)*3 + pos_y-1
        if game.make_move(move):
            game.print_ult_board()
            if game.check_winner():
                return True
            else:
                return False
        else:
            return move_helper(game)
    except ValueError:
        print("Invalid input. Please enter your move as four comma-separated numbers.")
        return move_helper(game)

if __name__ == '__main__':
    game = ultimate()
    winner = False
    game.print_ult_board()
    while winner == False:
        move_helper(game)
        

