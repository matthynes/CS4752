import sys, time, random
from settings import *

class GameState:
    # Initializer for the Connect4 GameState
    # Board is initialized to size width*height

    def __init__(self, rows, cols):
        self.__rows  = rows         # number of rows in the board
        self.__cols = cols          # number of columns in the board
        self.__pieces = [0]*cols    # __pieces[c] = number of pieces in a column c
        self.__player = 0           # the current player to move, 0 = Player One, 1 = Player Two
        self.__board   = [[PLAYER_NONE]*cols for r in range(rows)]

    # performs the given move, putting the piece into the appropriate column and swapping the player
    def do_move(self, move):
        if not self.is_legal(move): 
            print("DOING ILLEGAL MOVE")
            sys.exit()
        self.__board[self.pieces(move)][move] = self.player_to_move()
        self.__pieces[move] += 1
        self.__player = (self.__player + 1) % 2
    
    def get(self, r, c):        return self.__board[r][c]   # piece type located at (r,c)
    def cols(self):             return self.__cols          # number of columns in board
    def rows(self):             return self.__rows          # number of rows in board
    def pieces(self, col):      return self.__pieces[col]   # number of pieces in a given column
    def total_pieces(self):     return sum(self.__pieces)   # total pieces on the board
    def player_to_move(self):   return self.__player        # the player to move next

    # a move (placing a piece into a given column) is legal if the column isn't full
    def is_legal(self, move):   return move >= 0 and move < self.cols() and self.__pieces[move] < self.rows()
    # returns a list of legal moves at this state (which columns aren't full yet)
    def get_legal_moves(self):  return [i for i in range(self.cols()) if self.is_legal(i)]

    # Student TODO: Implement
    #   Calculates a heuristic evaluation for the current GameState from the P.O.V. of the player to move
    #
    #   Returns:
    #     
    #     value (int) - A heuristic evaluation of the current GameState
    #
    #     Suggested return values:
    #     Large positive value  = Player is winning the game (infinity if player has won)
    #     Larger negative value = Opponent is winning the game (-infinity if player has lost)
    #                             Infinity = Some large integer > non-win evaluations 
    def eval(self):
        return 0

    # Student TODO: Implement
    #   Calculates whether or not there is a winner on the current board and returns one of the following values
    #
    #   Return PLAYER_ONE  (0) - Player One has won the game 
    #   Return PLAYER_TWO  (1) - Player Two has won the game
    #   Return PLAYER_NONE (2) - There is no winner yet and the board isn't full
    #   Return DRAW        (3) - There is no winner and the board is full
    #
    #   A Player has won a connect 4 game if they have 4 pieces placed in a straight line or on a diagonal
    #   REMEMBER: The board rows and columns can be any size, make sure your checks acccount for this 
    #   TIP: Create 4 seprate loops to check win formations: horizontal, vertical, diagonal up, diagonal down 
    #        Be sure to test this function extensively, if you don't detect wins correctly it will be bad
    def winner(self):
        return PLAYER_NONE

# Student TODO: Implement this class
class Player_AlphaBeta:

    # Constructor for the Player_AlphaBeta class
    #
    # Ideally, this object should be constructed once per player, and then the get_move function will be
    # called once per turn to get the move the AI should do for a given state
    #
    # Args:
    #
    #  depth      (int) - Max depth for the AB search. If 0, no limit is used for depth
    #  time_limit (int) - Time limit (in ms) for the AB search. If 0, no limit is used for time
    #
    #  NOTE: One or both of depth or time_limit must be set to a value > 0
    def __init__(self, max_depth, time_limit):
        self.max_depth = max_depth      # set the max depth of search
        self.time_limit = time_limit    # set the time limit (in milliseconds)
        self.best_move = -1             # record the best move found so far
        # Add more class variables here as necessary (you will probably need more)

    # Student TODO: Implement this function
    #
    # This function calculates the move to be perfomed by the AI at a given state
    # This function will (ideally) call your alpha_beta recursive function from the the root node
    #
    # Args:
    #
    #   state (GameState) - The current state of the Connect4 game, with the AI next to move
    #
    # Returns:
    #
    #   move (int)        - The move the AI should do at this state. The move integer corresponds to
    #                       which column to place the next piece into (0 is the left-most column)
    #
    # NOTE: Make sure to remember the current player to move, as this is the player you are calculating
    # a move for, and will act as the maximizing player throughout your AB recusive calls
    def get_move(self, state):

        # store the time that we started calculating this move, so we can tell how much time has passed
        self.time_start = time.clock()

        # store the player that we're deciding a move for and set it as a class variable
        self.player = state.player_to_move()

        # do your alpha beta (or ID-AB) search here
        ab_value = self.alpha_beta(state, 0, -1000000, 1000000, True)

        # return the best move computer by alpha_beta
        return self.best_move

    # Student TODO: You might have a function like this... wink wink
    def alpha_beta(self, state, depth, alpha, beta, max_player):

        # Student TODO: Amazing recursive things that plays good
        #               See Lecture 12 notes on the course website

        # this line will determine how long has passed (in milliseconds) since you started the timer
        self.time_elapsed_ms = (time.clock() - self.time_start)*1000

        # but for now just have a placeholder that computes a random move
        self.best_move = random.choice(state.get_legal_moves())