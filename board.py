import sys

from AlphaBetaSearcher import alpha_beta_search
import time


class Board:
    def __init__(self, depth=0, board_state=None, board_size=8):
        if board_state is None:
            self.board_state = [['-' for i in range(board_size)] for j in range(board_size)]
        else:
            self.board_state = board_state
        self.depth = depth
        self.board_size = board_size

        # contains the last move made by the AI
        self.move_made = [0, 0]

    # takes a move for the computer
    def computer_move(self, allowed_time):
        # get start time
        start_time = time.time()
        # max depth = total allowed moves minus moves so far
        max_depth = (self.board_size * self.board_size) - self.depth
        best_move = None
        depth_reached = 1

        # go through every depth
        for depth in range(1, max_depth):
            # if we have gone past our time limit
            if time.time() - start_time > allowed_time:
                # need to return prev best move because if time ran out.
                # most likely we never got through the previous depth and have a bad state to change
                break

            depth_reached = depth

            # default best val to smallest possible number
            max_score = -sys.maxsize

            # make a new board state with every possible next move
            for i in range(self.board_size):
                for j in range(self.board_size):
                    # if that area of the board is not filled
                    if self.board_state[i][j] == "-":
                        self.board_state[i][j] = "X"
                        self.move_made = [i, j]

                        # for every child state get its score
                        local_score = alpha_beta_search(self, depth, start_time, "O", allowed_time, -sys.maxsize, sys.maxsize)
                        # if the score is better, this is our new best state and best score
                        if local_score > max_score:
                            max_score, best_move = local_score, self.move_made

                        self.board_state[i][j] = "-"

        # return the best move
        print("Computer reached a depth of:", depth_reached, "\n")
        return best_move

    # TODO subtract for distance to closest opponent piece
    # evaluates how good the current state is and returns its value
    def evaluate_state(self):
        closest_piece_dist = 5
        score = 0
        # get the current move made
        row = self.move_made[0]
        col = self.move_made[1]
        char_move = self.board_state[row][col]
        negative_char_move = "X" if char_move == "O" else "O"

        good_for_us_score = 0
        hurt_them_score = 0
        # add score for every col good state and blocker
        for i in range(max(0, col - 3), min(5, col + 1)):
            possible_connect = True
            obstructed_path = False
            our_pieces = 0
            enemy_pieces = 0
            for j in range(4):
                if i + j is not col:
                    if self.board_state[row][i + j] == char_move:
                        our_pieces += 1
                        obstructed_path = True
                    if self.board_state[row][i + j] == negative_char_move:
                        enemy_pieces += 1
                        closest_piece_dist = min(closest_piece_dist, abs(col - (i + j)))
                        possible_connect = False

            # if we can connect and we already have a piece there
            if possible_connect and our_pieces > 0:
                good_for_us_score += our_pieces * our_pieces
            # if we are removing a path that is not already obstructed add a point
            if enemy_pieces > 0 and not obstructed_path:
                hurt_them_score += enemy_pieces * enemy_pieces * enemy_pieces
            if our_pieces == 3 and possible_connect:
                score += 300
            # stopping a potential winning move
            if enemy_pieces == 3 and not obstructed_path:
                score += 1000

        # add score for every good row and blocker row
        for i in range(max(0, row - 3), min(5, row + 1)):
            possible_connect = True
            obstructed_path = False
            our_pieces = 0
            enemy_pieces = 0
            for j in range(4):
                if i + j is not row:
                    if self.board_state[i + j][col] == char_move:
                        our_pieces += 1
                        obstructed_path = True
                    if self.board_state[i + j][col] == negative_char_move:
                        enemy_pieces += 1
                        closest_piece_dist = min(closest_piece_dist, abs(row - (i + j)))
                        possible_connect = False

            # if we can connect and we already have a piece there
            if possible_connect and our_pieces > 0:
                good_for_us_score += our_pieces * our_pieces
            # if we are removing a path that is not already obstructed add a point
            if enemy_pieces > 0 and not obstructed_path:
                hurt_them_score += enemy_pieces * enemy_pieces * enemy_pieces
            if our_pieces == 3 and possible_connect:
                score += 300
            # stopping a potential winning move
            if enemy_pieces == 3 and not obstructed_path:
                score += 1000

        available_spots_score = min(row, 3)
        available_spots_score += min(col, 3)
        available_spots_score += min(self.board_size - (row + 1), 3)
        available_spots_score += min(self.board_size - (col + 1), 3)

        score += (good_for_us_score + hurt_them_score) + available_spots_score/13
        return score

    # returns all possible successor states for a given character
    def get_successor_states(self, char_move):
        successor_states = []

        # make a new board state with every possible next move
        for i in range(self.board_size):
            for j in range(self.board_size):
                # if that area of the board is not filled
                if self.board_state[i][j] == "-":
                    new_board = self.get_board_clone()
                    new_board.board_state[i][j] = char_move
                    new_board.move_made = [i, j]
                    successor_states.append(new_board)

        return successor_states

    # determines whether the current board state is solved or not
    def is_solved(self, char):
        row = self.move_made[0]
        col = self.move_made[1]
        # check horz solves
        for i in range(max(0, col - 3), min(5, col + 1)):
            pieces = 0
            for j in range(4):
                if self.board_state[row][i + j] == char:
                    pieces += 1
            if pieces == 4:
                return True

        # check vertical solves
        for i in range(max(0, row - 3), min(5, row + 1)):
            pieces = 0
            for j in range(4):
                if self.board_state[i + j][col] == char:
                    pieces += 1
            if pieces == 4:
                return True

        return False

    # checks if all the spots are taken which would mean cats game if not solved
    def is_full(self):
        for i in range(len(self.board_state)):
            for j in range(len(self.board_state)):
                if self.board_state[i][j] == "-":
                    return False
        return True

    # get board string equivalent
    def __str__(self):
        string = "  1 2 3 4 5 6 7 8\n"
        for i in range(len(self.board_state)):
            string += chr(ord('@')+i + 1)
            for j in range(len(self.board_state)):
                string += " " + self.board_state[i][j]
            string += "\n"
        return string

    def get_board_input_from_user(self):
        board_updated = False
        while not board_updated:
            try:
                move = input("Choose your next move: ")

                if len(move) > 2:
                    print("Not a legal move!")
                    continue

                row = ord(move[0]) - 97
                col = int(move[1]) - 1

                # is the col in range
                if col < 0 or col >= self.board_size:
                    print("Not a legal move!")
                    continue

                # is the row in range
                if row < 0 or row >= self.board_size:
                    print("Not a legal move!")
                    continue

                # if nothing at this state
                if self.board_state[row][col] == "-":
                    self.board_state[row][col] = "O"
                    self.move_made = [row, col]
                    return

                else:
                    print("Move already taken!")
                    continue

            except:
                print("Not a legal move!")

    # gets clone of the board
    def get_board_clone(self):
        return Board(self.depth, [[self.board_state[j][i] for i in range(8)] for j in range(8)])
