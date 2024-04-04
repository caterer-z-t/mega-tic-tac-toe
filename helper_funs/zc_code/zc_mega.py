##############################################################################
###
###                             Imports
###
##############################################################################

from helper_funs.helper_fn import winning_combinations, mega_x, mega_o, midrule, empty_board, TicTacToe, move_helper, ultimate
import os

##############################################################################
###
###                             Main Code for MINI Game
###
##############################################################################

'''
    This implements a game of Ultimate tic-tac-toe
    ==============================================
    Copied from joe code earlier  -- want to 
    change some elements but not mess with 
    the original code
    ==============================================
'''

if __name__ == '__main__':
    game = ultimate()
    winner = False
    game.print_ult_board()
    while winner == False:
        move_helper(game)
        

