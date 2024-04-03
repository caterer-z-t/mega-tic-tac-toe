def print_tic_tac_toe_board(board):
    print("-------------")
    for row in range(3):
        print("|", end="")
        for col in range(3):
            location = row * 3 + col + 1
            print(f" {board.get(location, ' ')} ", end="|")
        print("\n-------------")

printable_board = {1: 'X', 2: 'O', 3: 'X', 4: 'O', 5: 'X', 6: 'O', 7: 'X', 8: 'O', 9: 'X'}
print_tic_tac_toe_board(printable_board)