import sys
import time


# alpha beta search func
def alpha_beta_search(board, depth, start_time, char_move, allowed_time, alpha, beta):
    # determines max value of a certain depth
    def max_value(state, alpha, beta, depth):
        val = -sys.maxsize
        # make a new board state with every possible next move
        for i in range(state.board_size):
            for j in range(state.board_size):
                # if that area of the board is not filled
                if state.board_state[i][j] == "-":
                    state.board_state[i][j] = char_move
                    state.move_made = [i, j]
                    new_char_move = ("X" if char_move == "O" else "O")
                    val = max(val, alpha_beta_search(state, depth - 1, start_time, new_char_move, allowed_time, alpha, beta))

                    # undo the move
                    state.board_state[i][j] = "-"
                    # pruning
                    if val > beta:
                        return val
                    alpha = max(alpha, val)
        return val

    # determines min val of certain depth
    def min_value(state, alpha, beta, depth):
        val = sys.maxsize
        # make a new board state with every possible next move
        for i in range(state.board_size):
            for j in range(state.board_size):
                # if that area of the board is not filled
                if state.board_state[i][j] == "-":
                    state.board_state[i][j] = char_move
                    state.move_made = [i, j]
                    new_char_move = ("X" if char_move == "O" else "O")
                    val = min(val, alpha_beta_search(state, depth - 1, start_time, new_char_move, allowed_time, alpha, beta))

                    # undo the move
                    state.board_state[i][j] = "-"
                    # pruning
                    if val < alpha:
                        return val
                    beta = min(beta, val)
        return val

    # if the board is solved lets return the max/min score
    if board.is_solved("X"):
        return sys.maxsize
    if board.is_solved("O"):
        return -sys.maxsize

    # if we are done looking return the value of the state
    if depth <= 0 or time.time() - start_time > allowed_time:
        return board.evaluate_state()

    # returns the best value board
    return max_value(board, alpha, beta, depth) if char_move == "X" else min_value(board, alpha, beta, depth)
