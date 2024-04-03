def print_tic_tac_toe_board(board):
    print("-------------")
    for row in range(3):
        print("|", end="")
        for col in range(3):
            location = row * 3 + col + 1
            print(f" {board.get(location, ' ')} ", end="|")
        print("\n-------------")

printable_board = {1: 'X', 2: 'O', 3: 'X', 4: 'O', 5: 'X', 6: 'O', 7: 'X', 8: 'O', 9: 'X'}


# Define a function to print a nested tic-tac-toe board given a dictionary of dictionaries
def nested_tic_tac_toe_board(boards):
    # Define the top rule based on the size of a board (3x3 in this case)
    top_rule = "-------------"
    # Print the top rule three times with space as a separator
    print((top_rule + "  ") * 3)
    # Iterate over each row in the 3x3 mega board
    for row in range(1, 10, 3):
        # For each of the three rows in a single mega tic-tac-toe board cell
        for sub_row in range(1, 10, 3):
            # Print a row for each of the three mega cells horizontally
            for col in range(row, row + 3):
                # Print the inner cells with values
                print(f"| {boards[col][sub_row]} | {boards[col][sub_row + 1]} | {boards[col][sub_row + 2]} |", end="  ")
            print()
        # Print the bottom rule of each cell row
        print((top_rule + "  ") * 3)

sample_nested_board = {
    1: {1: 'X', 2: 'O', 3: ' ', 4: 'X', 5: ' ', 6: 'O', 7: ' ', 8: 'X', 9: 'O'},
    2: {1: 'O', 2: 'X', 3: 'O', 4: ' ', 5: 'X', 6: ' ', 7: 'O', 8: ' ', 9: 'X'},
    3: {1: ' ', 2: ' ', 3: 'X', 4: 'O', 5: 'X', 6: 'O', 7: 'X', 8: ' ', 9: ' '},
    4: {1: 'X', 2: ' ', 3: 'O', 4: 'X', 5: 'O', 6: ' ', 7: 'X', 8: 'O', 9: ' '},
    5: {1: 'O', 2: 'O', 3: 'X', 4: ' ', 5: ' ', 6: ' ', 7: 'X', 8: 'X', 9: 'O'},
    6: {1: 'X', 2: 'X', 3: 'O', 4: 'O', 5: ' ', 6: 'X', 7: ' ', 8: ' ', 9: 'O'},
    7: {1: 'O', 2: 'X', 3: ' ', 4: ' ', 5: 'O', 6: 'X', 7: ' ', 8: 'X', 9: 'O'},
    8: {1: ' ', 2: 'O', 3: 'X', 4: 'X', 5: ' ', 6: 'O', 7: 'X', 8: ' ', 9: ' '},
    9: {1: 'X', 2: ' ', 3: 'O', 4: ' ', 5: 'X', 6: 'O', 7: ' ', 8: 'O', 9: 'X'},
}

# Print the sample nested tic-tac-toe board
nested_tic_tac_toe_board(sample_nested_board)

