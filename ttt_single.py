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
        for row in range(3):
            for j in range(len(self.ult_board[0].board_arr)):
                print(self.ult_board[row*3].board_arr[j], " || ", self.ult_board[row*3+1].board_arr[j], " || " 
                      + self.ult_board[row*3+2].board_arr[j])
            if(row == 0 or row == 1):
                print('===============||=================||===============')
    
    def make_move(self, move):
        # TODO:
        return None
    
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
        self.winner = 'X'
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
                return True
            # otherewise swap players
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
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
                    self.board_arr=["   \     /   ",
                                    "    \   /    ",
                                    "      X      ",
                                    "    /   \    ",
                                    "   /     \   "]
                else:
                    self.board_arr=["      _      ",
                                    "    /   \    ",
                                    "   |     |   ",
                                    "    \ _ /    ",
                                    "             "]
                return True
        return False

# Example usage:

game = ultimate()
game.print_ult_board()

