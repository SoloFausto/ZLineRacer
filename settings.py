from pyray import *
from raylib import *


from random import randint, uniform
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1800, 1800

GRID_AMOUNT_X = 100
GRID_AMOUNT_Y = 100 
GAME_CONTROLS = [(KEY_Z,KEY_X),(KEY_N,KEY_M),(KEY_O,KEY_P),(KEY_Q,KEY_W)]
PLAYER_COLORS = [RED, GREEN, YELLOW, BLUE]


CELL_W = WINDOW_WIDTH // GRID_AMOUNT_X
CELL_H = WINDOW_HEIGHT // GRID_AMOUNT_Y
WIN_SCORE = 5



def translateGridtoXY(gridcoord):
    top_x= (WINDOW_WIDTH // GRID_AMOUNT_X) * gridcoord.x
    top_y = (WINDOW_HEIGHT // GRID_AMOUNT_Y) * gridcoord.y
    return Vector2(top_x,top_y)