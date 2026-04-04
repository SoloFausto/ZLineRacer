from raylib import *
from enum import Enum
from collections import deque
from settings import *
import math

class Wall:
    
    def __init__(self,position:Vector2,color:Color,color_name=None,heading=0) -> None:
        self.position = position
        self.lifetime = 20
        self.alive = True
        self.color = color
        self.color_name = color_name
        self.heading = heading
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
        wall_key = self.color_name + "_wall" if self.color_name else None
        if wall_key and wall_key in TEXTURES:
            tex = TEXTURES[wall_key]
            cx = position.x + CELL_W / 2
            cy = position.y + CELL_H / 2
            DrawTexturePro(tex, Rectangle(0, 0, tex.width, tex.height),
                           Rectangle(cx, cy, CELL_W, CELL_H),
                           Vector2(CELL_W / 2, CELL_H / 2), self.heading * 90.0, WHITE)
        else:
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