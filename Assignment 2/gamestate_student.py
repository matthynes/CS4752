import sys, time, random, copy

import math
from settings import *

# Infinity constant used for AB & evaluation function
INF = math.inf


class GameState:
    # Initializer for the Connect4 GameState
    # Board is initialized to size width*height
    def __init__(self, rows, cols):
        self.__rows = rows  # number of rows in the board
        self.__cols = cols  # number of columns in the board
        self.__pieces = [0] * cols  # __pieces[c] = number of pieces in a column c
        self.__player = 0  # the current player to move, 0 = Player One, 1 = Player Two
        self.__board = [[PLAYER_NONE] * cols for r in range(rows)]

    # performs the given move, putting the piece into the appropriate column and swapping the
    # player
    def do_move(self, move):
        if not self.is_legal(move):
            print("ILLEGAL MOVE. STOP RIGHT THERE, CRIMINAL SCUM!")
            sys.exit()
        self.__board[self.pieces(move)][move] = self.player_to_move()
        self.__pieces[move] += 1
        self.__player = (self.__player + 1) % 2

    # some getter functions that you probably won't need to modify
    def get(self, r, c):
        return self.__board[r][c]  # piece type located at (r,c)

    def cols(self):
        return self.__cols  # number of columns in board

    def rows(self):
        return self.__rows  # number of rows in board

    def pieces(self, col):
        return self.__pieces[col]  # number of pieces in a given column

    def total_pieces(self):
        return sum(self.__pieces)  # total pieces on the board

    def player_to_move(self):
        return self.__player  # the player to move next

    # a move (placing a piece into a given column) is legal if the column isn't full
    def is_legal(self, move):
        return move >= 0 and move < self.cols() and self.__pieces[move] < self.rows()

    # returns a list of legal moves at this state (which columns aren't full yet)
    def get_legal_moves(self):
        return [i for i in range(self.cols()) if self.is_legal(i)]

    # Calculates a heuristic evaluation for the current GameState from the P.O.V. of the
    # player to move
    #
    #   Args:
    #
    #     player (int) - The player whose POV the evaluation is from. 
    #
    #   Returns:
    #     
    #     value  (int) - A heuristic evaluation of the current GameState. Positive value should
    # indicate
    #                    that the input player is winning, negative value that they are losing.
    #
    #     Suggested return values:
    #     Large positive value  = Player is winning the game (infinity if player has won)
    #     Larger negative value = Opponent is winning the game (-infinity if player has lost)
    #                             Infinity = Some large integer > non-win evaluations 
    #
    # This heuristic evaluation determines the "goodness" of a move by determining how many potential
    # four-in-a-rows each player can still make.
    def eval(self, player):
        # if the player is about to win/lose then the evaluation is infinity and -infinity, respectively
        if self.winner() == player:
            return INF
        elif self.winner() == self.get_opponent(player):
            return -INF
        else:
            # calculates the number of potential wins for the player then subtracts the opponent's potential wins
            h = 0
            for r in range(self.rows()):
                for c in range(self.cols()):
                    h += self.num_in_a_row(r, c, player)
                    h -= self.num_in_a_row(r, c, self.get_opponent(player))
            return h

    def winner(self):
        # check for horizontal wins
        for r in range(self.rows()):
            for c in range(self.cols() - 3):
                if self.get(r, c) == self.get(r, c + 1) == self.get(r, c + 2) == self.get(r, c + 3):
                    tile = self.get(r, c)
                    if tile != PLAYER_NONE:
                        return tile

        # check for vertical wins
        for r in range(self.rows() - 3):
            for c in range(self.cols()):
                if self.get(r, c) == self.get(r + 1, c) == self.get(r + 2, c) == self.get(r + 3, c):
                    tile = self.get(r, c)
                    if tile != PLAYER_NONE:
                        return tile

        # check for descending (left to right) diagonal wins
        for r in range(self.rows() - 3):
            for c in range(self.cols() - 3):
                if self.get(r, c) == self.get(r + 1, c + 1) == self.get(r + 2, c + 2) == self.get(r + 3, c + 3):
                    tile = self.get(r, c)
                    if tile != PLAYER_NONE:
                        return tile

        # check for ascending (left to right) diagonal wins
        for r in range(3, self.rows()):
            for c in range(self.cols() - 3):
                if self.get(r, c) == self.get(r - 1, c + 1) == self.get(r - 2, c + 2) == self.get(r - 3, c + 3):
                    tile = self.get(r, c)
                    if tile != PLAYER_NONE:
                        return tile

        # board is full
        if self.total_pieces() == (self.rows() * self.cols()):
            return DRAW

        return PLAYER_NONE

    def is_terminal(self):
        return self.winner() != PLAYER_NONE

    # calculates the number of potential wins a player can still obtain
    def num_in_a_row(self, r, c, player):

        # all the potential moves given the current (r,c)
        moves = [[(r, c), (r + 1, c), (r + 2, c), (r + 3, c)],
                 [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)],
                 [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)],
                 [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]]

        # used in the following lambda function to make sure a move is not out-of-bounds
        def check_move(r, c):
            if (0 <= r < self.rows()) and (0 <= c < self.cols()):
                return self.get(r, c)
            return None

        # creates a list of piece types located at each of the potential moves
        moves = map(lambda x: map(lambda y: check_move(y[0], y[1]), x), moves)

        count = 0

        # checks the number of potential pieces in a row for the player.
        # if the player's piece is already in a spot or the spot is empty then the loop continues.
        # if the inner loop finishes (ie; it has explored those 4 moves) and the opponent's piece hasn't blocked
        # it (ie; the same flag is True) then that's a potential four-in-a-row and the count is incremented.
        for m in moves:
            same = False
            for p in m:
                if p == player or p == PLAYER_NONE:
                    same = True
                    continue
                else:
                    same = False
                    break

            if same:
                count += 1

        return count

    def get_opponent(self, player):
        if player == PLAYER_ONE:
            return PLAYER_TWO

        return PLAYER_ONE


# custom time limit exception
class TimeLimitException(Exception):
    pass


class Player_AlphaBeta:
    # Constructor for the Player_AlphaBeta class
    #
    # Ideally, this object should be constructed once per player, and then the get_move function
    #  will be
    # called once per turn to get the move the AI should do for a given state
    #
    # Args:
    #
    #  depth      (int) - Max depth for the AB search. If 0, no limit is used for depth
    #  time_limit (int) - Time limit (in ms) for the AB search. If 0, no limit is used for time
    #
    #  NOTE: One or both of depth or time_limit must be set to a value > 0
    #        If both are > 0, then whichever happens first will terminate the AB search
    #
    def __init__(self, max_depth, time_limit):
        self.max_depth = max_depth  # set the max depth of search
        self.time_limit = time_limit  # set the time limit (in milliseconds)
        self.best_move = -1  # record the best move found so far
        # Add more class variables here as necessary (you will probably need more)

    # This function calculates the move to be performed by the AI at a given state
    # This function will (ideally) call your alpha_beta recursive function from the the root node
    #
    # Args:
    #
    #   state (GameState) - The current state of the Connect4 game, with the AI next to move
    #
    # Returns:
    #
    #   move (int)        - The move the AI should do at this state. The move integer
    # corresponds to
    #                       which column to place the next piece into (0 is the left-most column)
    #
    # NOTE: Make sure to remember the current player to move, as this is the player you are
    # calculating
    # a move for, and will act as the maximizing player throughout your AB recusive calls
    #
    def get_move(self, state):
        # store the time that we started calculating this move, so we can tell how much time has
        #  passed
        self.time_start = time.clock()

        # store the player that we're deciding a move for and set it as a class variable
        self.player = state.player_to_move()

        # do your alpha beta (or ID-AB) search here
        # the return value isn't actually used since the best_move is set during the execution of alpha-beta
        ab_value = self.alpha_beta(state, 0, -INF, INF, True)

        legal_moves = state.get_legal_moves()

        # return the best move computed by alpha_beta.
        # very occasionally it will (somehow) return an illegal move so an extra validity check is needed.
        # this typically only occurs once in 15 matches so one random move shouldn't affect results too heavily
        return self.best_move if self.best_move in legal_moves else random.choice(legal_moves)

    def alpha_beta(self, state, depth, alpha, beta, max_player):
        self.time_elapsed_ms = (time.clock() - self.time_start) * 1000

        if self.time_limit and self.time_elapsed_ms > self.time_limit:
            raise TimeLimitException('Time limit exceeded.')

        if (depth > self.max_depth > 0) or state.is_terminal():
            return state.eval(self.player)

        try:
            if max_player:
                val = -INF
                for m in state.get_legal_moves():
                    child = copy.deepcopy(state)
                    child.do_move(m)
                    val = max(val, self.alpha_beta(child, depth + 1, alpha, beta, False))
                    if depth == 0 and val > alpha:
                        self.best_move = m
                    alpha = max(alpha, val)
                    if alpha >= beta:
                        break
                return val
            else:
                val = INF
                for m in state.get_legal_moves():
                    child = copy.deepcopy(state)
                    child.do_move(m)
                    val = min(val, self.alpha_beta(child, depth + 1, alpha, beta, True))
                    beta = min(val, beta)

                    if beta <= alpha:
                        break

                return val
        # time limit reached, return whatever state we have calculated so far
        except TimeLimitException:
            return state.eval(self.player)
