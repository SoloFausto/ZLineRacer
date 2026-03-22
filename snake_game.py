from snake import Snake
from food import Food
from raylib import *
from settings import *

class Game():
    def __init__(self) -> None:
        self.playerPos = Vector2()
        self.playerPos.x = 5
        self.playerPos. y = 5
        self.food = Food(ORANGE)
        self.player = Snake(self.playerPos,1,BLUE)
        self.food.roll_random_position(self.player.body,GRID_AMMOUNT_X)
        self.isGameOver = False

    def update(self):
        self.player.update()
        if(Vector2Equals(self.player.position,self.food.position)):
            self.food.roll_random_position (self.player.body,GRID_AMMOUNT_X-1)
            self.player.size += 1
        if(self.player.isPlayerDead):
            self.isGameOver = True
    def draw(self):
        
        
        begin_mode_2d(self.player.camera)
        self.player.draw()
        self.food.draw()

        for i in range(0,GRID_AMMOUNT_Y + 1,1):
            x = i * CELL_W
            DrawLine(x, 0, x, WINDOW_HEIGHT, GRAY)

        for i in range(0,GRID_AMMOUNT_X + 1,1):
            y = i * CELL_H
            
            DrawLine(0, y, WINDOW_WIDTH, y, GRAY)
        end_mode_2d()

    
