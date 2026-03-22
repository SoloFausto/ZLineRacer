from snake import Snake
from food import Food
from raylib import *
from settings import *

class TitleScreen():
    def __init__(self, game_ref) -> None:
        self.game_ref = game_ref

    def update(self):
        if(IsKeyPressed(KEY_ENTER)):
            self.game_ref.isGameOver = False
            self.game_ref.player.reset()
            self.game_ref.food.roll_random_position(self.game_ref.player.body,GRID_AMMOUNT_X-1)
    def draw(self):
        draw_text("SNAKE GAME", 50, WINDOW_HEIGHT//2 - 20, 200, GREEN)
        draw_text("Press Enter to Start", 60 , WINDOW_HEIGHT//2 + 250, 100, GRAY)
    
