from raylib import *
from settings import * 
from cycle_game import Game
from main_title import TitleScreen

if __name__ == '__main__':  

  init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Game")
  set_target_fps(120)
  
  game = Game(1)
  game.isGameOver = True
  title_screen = TitleScreen(game)
  

 

  while not window_should_close():

    if(not game.isGameOver):
      game.update()
    else:
      title_screen.update()
    
    
    begin_drawing()
    clear_background(BLACK)
    
    if(not game.isGameOver):
      game.draw()
    else:
      title_screen.draw()      

    end_drawing()

close_window()
  
