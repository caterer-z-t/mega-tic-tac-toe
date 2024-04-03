def print_tic_tac_toe_board(board):
    print("-------------")
    for row in range(3):
        print("|", end="")
        for col in range(3):
            location = row * 3 + col + 1
            print(f" {board.get(location, ' ')} ", end="|")
        print("\n-------------")

printable_board = {1: 'X', 2: 'O', 3: 'X', 4: 'O', 5: 'X', 6: 'O', 7: 'X', 8: 'O', 9: 'X'}


# Adjusting the existing nested_tic_tac_toe_board function to work with the new key format
def nested_tic_tac_toe_board(boards):
    # Define the top rule based on the size of a board (3x3 in this case)
    top_rule = "---------------"
    midrule = '============='
    # Print the top rule three times with space as a separator
    print((midrule + "==") * 3)
    # Iterate over each row in the 3x3 mega board
    for row in range(1, 4):
        # For each of the three rows in a single mega tic-tac-toe board cell
        for sub_row in range(1, 4):
            # Print a row for each of the three mega cells horizontally
            for col in range(1, 4):
                # Access the board using the new list keys for row and column
                board_key = (row, col)
                # Print the inner cells with values
                if col == 3:
                    print(f"  {boards[board_key][(sub_row, 1)]} | {boards[board_key][(sub_row, 2)]} | {boards[board_key][(sub_row, 3)]}  ", end=" ")
                else:
                    print(f"  {boards[board_key][(sub_row, 1)]} | {boards[board_key][(sub_row, 2)]} | {boards[board_key][(sub_row, 3)]}  ", end=" ||")
            print('\n', top_rule * 3)
        # Print the bottom rule of each cell row
        print((midrule + "===") * 3)

# Sample board with the new key format
sample_nested_board = {
    (1, 1): {(1, 1): 'X', (1, 2): 'O', (1, 3): ' ', (2, 1): 'X', (2, 2): ' ', (2, 3): 'O', (3, 1): ' ', (3, 2): 'X', (3, 3): 'O'},
    (1, 2): {(1, 1): 'O', (1, 2): 'X', (1, 3): 'O', (2, 1): ' ', (2, 2): 'X', (2, 3): ' ', (3, 1): 'O', (3, 2): ' ', (3, 3): 'X'},
    (1, 3): {(1, 1): ' ', (1, 2): ' ', (1, 3): 'X', (2, 1): 'O', (2, 2): 'X', (2, 3): 'O', (3, 1): 'X', (3, 2): ' ', (3, 3): ' '},
    (2, 1): {(1, 1): 'X', (1, 2): ' ', (1, 3): 'O', (2, 1): 'X', (2, 2): 'O', (2, 3): ' ', (3, 1): 'X', (3, 2): 'O', (3, 3): ' '},
    (2, 2): {(1, 1): 'O', (1, 2): 'O', (1, 3): 'X', (2, 1): ' ', (2, 2): ' ', (2, 3): ' ', (3, 1): 'X', (3, 2): 'X', (3, 3): 'O'},
    (2, 3): {(1, 1): 'X', (1, 2): 'X', (1, 3): 'O', (2, 1): 'O', (2, 2): ' ', (2, 3): 'X', (3, 1): ' ', (3, 2): ' ', (3, 3): 'O'},
    (3, 1): {(1, 1): 'O', (1, 2): 'X', (1, 3): ' ', (2, 1): ' ', (2, 2): 'O', (2, 3): 'X', (3, 1): ' ', (3, 2): 'X', (3, 3): 'O'},
    (3, 2): {(1, 1): ' ', (1, 2): 'O', (1, 3): 'X', (2, 1): 'X', (2, 2): ' ', (2, 3): 'O', (3, 1): 'X', (3, 2): ' ', (3, 3): ' '},
    (3, 3): {(1, 1): 'X', (1, 2): ' ', (1, 3): 'O', (2, 1): ' ', (2, 2): 'X', (2, 3): 'O', (3, 1): 'O', (3, 2): 'X', (3, 3): ' '}
}


# Print the sample nested tic-tac-toe board
nested_tic_tac_toe_board(sample_nested_board)

# modified_nested_tic_tac_toe_board(sample_nested_board)
