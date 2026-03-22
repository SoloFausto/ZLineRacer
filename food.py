from raylib import *
from enum import Enum
from collections import deque
from settings import *
import math

class Food:
    
    def __init__(self,color):
        self.position = Vector2(0,0)
        self.color = color
    
    def roll_random_position(self,snake_body,bound):
        rolled_pos = Vector2(GetRandomValue(0,bound),GetRandomValue(0,bound))
        while self.check_if_pos_in_snake(rolled_pos,snake_body):
            rolled_pos = Vector2(GetRandomValue(0,bound),GetRandomValue(0,bound))
        print(rolled_pos.x,rolled_pos.y)
        self.position = rolled_pos
    
    def draw(self):
        position = translateGridtoXY(self.position)    
        DrawRectangleV(position,(CELL_W,CELL_H),self.color)

    def check_if_pos_in_snake(self,pos,snake):
        for i in range(0,len(snake)):
            if Vector2Equals(snake[i],pos):
                return True
        return False