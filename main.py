import sys

from Helpers import *


def main():
    # make a board
    game_board = Board()
    game_over = False

    # allowed time in seconds
    allowed_time_for_computer_move = 5

    # ask who goes first
    first_string = get_string_input("Would you like to go first? (y/n): ", ["y", "n"])

    # print original board
    print(game_board)

    # if comp goes first run a move here otherwise go into the loop
    if first_string == "n":
        best_next_state = game_board.computer_move(allowed_time_for_computer_move)
        game_board.move_made = [best_next_state[0], best_next_state[1]]
        game_board.board_state[best_next_state[0]][best_next_state[1]] = "X"
        game_board.depth += 1
        print(game_board)

    while not game_over:
        # user takes a turn
        game_board.get_board_input_from_user()
        game_board.depth += 1

        # print board and check if game over or board full
        print(game_board)
        if game_board.is_solved("O"):
            print("You Win!")
            game_over = True
            break
        if game_board.is_full():
            print("Board is completely full, no winner")
            game_over = True
            break

        # comp takes a turn
        best_next_state = game_board.computer_move(allowed_time_for_computer_move)
        game_board.move_made = [best_next_state[0], best_next_state[1]]
        game_board.board_state[best_next_state[0]][best_next_state[1]] = "X"
        game_board.depth += 1

        # print board and check if game over or board full
        print(game_board)
        if game_board.is_solved("X"):
            print("Computer Wins :(")
            game_over = True
        if game_board.is_full():
            print("Board is completely full, draw")
            game_over = True

    print("Game Over")
    print("\nClose Window")


if __name__ == '__main__':
    main()
