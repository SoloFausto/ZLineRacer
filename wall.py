from raylib import *
from enum import Enum
from collections import deque
from settings import *
import math

class Wall:
    
    def __init__(self,position:Vector2,color:Color) -> None:
        self.position = position
        self.lifetime = 20
        self.alive = True
        self.color = color
        self.darker_color = ColorBrightness(self.color, -0.25)
        self.border_width = 1
        self.lines_spacing = 4

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
           
        DrawRectangleV(position,(CELL_W,CELL_H),self.darker_color)
        DrawRectangleLinesEx((position.x,position.y,CELL_W,CELL_H),self.border_width,self.color)
        DrawLineEx((position.x+1,position.y+1),(position.x + CELL_W-1,position.y + CELL_H-1),self.border_width,self.color)

        

    def update(self,tick):
        self.lifetime -= tick
        if(self.lifetime <= 0):
            self.alive = False
    def check_if_pos_in_snake(self,pos,snake):
        if pos in snake:
            return True
        return False