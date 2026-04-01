from pyray import *
from raylib import *
from random import random
from math import cos, sin

from random import randint, uniform
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 2880, 1800

GRID_AMOUNT_X = 350
GRID_AMOUNT_Y = 350 
GAME_CONTROLS = [(KEY_Z,KEY_X),(KEY_N,KEY_M),(KEY_O,KEY_P),(KEY_Q,KEY_W)]
PLAYER_COLORS = [RED, GREEN, YELLOW, BLUE]


CELL_SIZE = min(WINDOW_WIDTH // GRID_AMOUNT_X, WINDOW_HEIGHT // GRID_AMOUNT_Y)
CELL_W = CELL_SIZE
CELL_H = CELL_SIZE
#AI helped me with centering the playfield
PLAYFIELD_WIDTH = CELL_W * GRID_AMOUNT_X
PLAYFIELD_HEIGHT = CELL_H * GRID_AMOUNT_Y
PLAYFIELD_OFFSET_X = (WINDOW_WIDTH - PLAYFIELD_WIDTH) // 2
PLAYFIELD_OFFSET_Y = (WINDOW_HEIGHT - PLAYFIELD_HEIGHT) // 2
NUM_PLAYERS = 1



def translateGridtoXY(gridcoord):
    top_x = PLAYFIELD_OFFSET_X + (CELL_W * gridcoord.x)
    top_y = PLAYFIELD_OFFSET_Y + (CELL_H * gridcoord.y)
    return Vector2(top_x,top_y)