from raylib import *
from enum import Enum
from collections import deque
from settings import *
import math

class Wall:
    
    def __init__(self,position:Vector2):
        self.position = position
        self.lifetime = 20
        self.alive = True

    def _grid_key(self):
        return self.position.x, self.position.y

    def __eq__(self, other):
        if not isinstance(other, Wall):
            return NotImplemented
        return self._grid_key() == other._grid_key()

    def __hash__(self):
        return hash(self._grid_key())
    
    def draw(self):
        position = translateGridtoXY(self.position)    
        DrawRectangleV(position,(CELL_W,CELL_H),self.color)

    def update(self,tick):
        self.lifetime -= tick
        if(self.lifetime <= 0):
            self.alive = False
    def check_if_pos_in_snake(self,pos,snake):
        if pos in snake:
            return True
        return False