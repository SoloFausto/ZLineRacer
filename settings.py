from pyray import *

from random import randint, uniform
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1800, 1800

GRID_AMMOUNT_X = 100
GRID_AMMOUNT_Y = 100 

CELL_W = WINDOW_WIDTH // GRID_AMMOUNT_X
CELL_H = WINDOW_HEIGHT // GRID_AMMOUNT_Y

WIN_SCORE = 5



def translateGridtoXY(gridcoord):
    top_x= (WINDOW_WIDTH // GRID_AMMOUNT_X) * gridcoord.x
    top_y = (WINDOW_HEIGHT // GRID_AMMOUNT_Y) * gridcoord.y
    return Vector2(top_x,top_y)