from retrocycle import Retrocycle
from wall import Wall
from raylib import *
from settings import *

class TitleScreen():
    def __init__(self, game_ref) -> None:
        self.game_ref = game_ref

    def update(self):
        if(IsKeyPressed(KEY_ENTER)):
            self.game_ref.isGameOver = False
            # self.game_ref.player.reset()
    def draw(self):
        draw_text("RETROCYCLE GAME", 50, WINDOW_HEIGHT//2 - 20, 200, GREEN)
        draw_text("Press Enter to Start", 60 , WINDOW_HEIGHT//2 + 250, 100, GRAY)
    
