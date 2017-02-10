import sys, time, random, copy
import pygame as pg
import gamestate_solution
import gamestate_student
from settings import *

class Connect4:
    
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(500, 100)
        self.clock  = pg.time.Clock()
        # set the version of the state you will use here
        # set this to your student version once it is working, use solution to test
        self.initial_state = gamestate_solution.GameState(BOARD_ROWS, BOARD_COLS)
        self.state = copy.deepcopy(self.initial_state)
        self.width  = self.state.cols() * TILESIZE
        self.height = self.state.rows() * TILESIZE + 40
        self.screen = pg.display.set_mode((self.width, self.height))    
        self.font = pg.font.SysFont(FONTNAME, FONTSIZE, bold=FONTBOLD)
        self.winner = PLAYER_NONE
        self.text_position = (10, self.height-35)
        # the players that will play in the game
        # setting a player to None means it is a human GUI player
        self.players = [None, gamestate_solution.Player_AlphaBeta(0, 2000)]

    # game main loop update function
    def update(self):
        self.dt = self.clock.tick(FPS) / 1000
        self.do_turn()
        self.events()
        self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    # draw the grid elements and return the surface
    def draw_board(self):
        # draw the tile rectangles
        self.screen.fill(CBLUE)
        for c in range(self.state.cols()):
            for r in range(self.state.rows()):
                self.draw_piece(self.screen, (r,c), PIECECOLOR[self.state.get(r,c)], 2)

    # draw a tile (r,c) location with given parameters
    def draw_piece(self, surface, tile, color, border):
        row, col = self.state.rows() - 1 - tile[0], tile[1]
        pg.draw.circle(self.screen, color, (col*TILESIZE+TILESIZE//2, row*TILESIZE+TILESIZE//2), TILESIZE//2-PIECEPAD)
        pg.draw.circle(self.screen, BLACK, (col*TILESIZE+TILESIZE//2, row*TILESIZE+TILESIZE//2), TILESIZE//2-PIECEPAD+border, border)
        
    # draw some text with the given arguments
    def draw_text(self, text, pos, color):
        label = self.font.render(text, 1, color)
        self.screen.blit(label, pos)

    # reset the game to a blank board
    def reset(self):
        self.winner = PLAYER_NONE
        self.state = copy.deepcopy(self.initial_state)

    # do the current turn
    def do_turn(self):
        self.winner = self.state.winner()
        if self.winner == PLAYER_NONE:                   # there is no winner yet, so get the next move from the AI
            player = self.state.player_to_move()    # get the next player to move from the state
            if self.players[player] != None:        # if the current player is an AI, get its move
                self.state.do_move(self.players[player].get_move(self.state))
                

    # draw everything to the screen
    def draw(self):
        self.draw_board()
        player = self.state.player_to_move()
        if (self.winner == PLAYER_NONE):
            self.draw_text(PLAYER_NAMES[player] + (": Human" if self.players[player] == None else ": AI Thinking"), self.text_position, PIECECOLOR[player])
        else:    
            self.draw_text(GAME_RESULT_STRING[self.winner], self.text_position, PIECECOLOR[self.winner])
        pg.display.flip()

    # returns the tile (r,c) on the grid underneath a given mouse position in pixels
    def get_tile(self, mpos):
        return (mpos[1] // TILESIZE, mpos[0] // TILESIZE)

    # returns a pixel rectangle, given a tile (r,c) on the grid
    def get_rect(self, tile, pad):
        return (tile[1]*TILESIZE+pad, tile[0]*TILESIZE+pad, TILESIZE-pad, TILESIZE-pad)

    # events and input handling
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: self.quit()
                if event.key == pg.K_r:      self.reset()
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    move = self.get_tile(event.pos)[1]
                    if self.state.is_legal(move) and self.state.winner() == PLAYER_NONE:
                        self.state.do_move(move)


# A sample player that returns a random legal move
class Player_Random:

    def get_move(self, state):
        return random.choice(state.get_legal_moves())

sys.setrecursionlimit(10000)

# create the game object
g = Connect4()

# run the main game loop
while True:
    g.update()