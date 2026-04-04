from raylib import *
from settings import * 
from cycle_game import Game


if __name__ == '__main__':  

  init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Game")
  set_target_fps(120)
  for name in PLAYER_COLOR_NAMES:
    TEXTURES[f"{name}_ship"] = load_texture(f"assets/{name}_ship.png")
    TEXTURES[f"{name}_wall"] = load_texture(f"assets/{name}_wall.png")
  TEXTURES["bg"] = load_texture("assets/bg.png")
  isTitleScreen = True
  isPlayerSelect = False
  game = Game(1)
  game.isGameOver = True
  num_players = 2


 

  while not window_should_close():
    if game.isGameOver:
      if isTitleScreen:
        if IsKeyPressed(KEY_ENTER):
          isTitleScreen = False
          isPlayerSelect = True
      
      elif isPlayerSelect:
        if IsKeyPressed(KEY_LEFT):
          num_players = max(1, num_players - 1)
        elif IsKeyPressed(KEY_RIGHT):
          num_players = min(4, num_players + 1)
        elif IsKeyPressed(KEY_ENTER):
          game.reset(num_players)
          game.isGameOver = False
          isPlayerSelect = False
    else:
      game.update()
      if game.isGameOver:
        isTitleScreen = True
    
    begin_drawing()
    clear_background(BLACK)
    
    if not game.isGameOver:
      game.draw()
    elif isTitleScreen:
        draw_text("RETROCYCLE GAME", 50, WINDOW_HEIGHT//2 - 20, 200, GREEN)
        draw_text("Press Enter to Start", 60, WINDOW_HEIGHT//2 + 250, 100, GRAY)
    elif isPlayerSelect:
        draw_text("PLAYER SELECT", 50, WINDOW_HEIGHT//2 - 20, 200, GREEN)
        draw_text(f"Number of Players: {num_players}", 60, WINDOW_HEIGHT//2 + 250, 100, GRAY)
        draw_text("Use Left/Right to Change", 60, WINDOW_HEIGHT//2 + 350, 100, GRAY)
        
        draw_text("Press Enter to Start", 60, WINDOW_HEIGHT//2 + 450, 100, GRAY)
        for i in range(num_players):
            ship_key = PLAYER_COLOR_NAMES[i] + "_ship"
            if ship_key in TEXTURES:
                tex = TEXTURES[ship_key]
                DrawTexturePro(tex, Rectangle(0, 0, tex.width, tex.height),
                               Rectangle(60 + i * 100, WINDOW_HEIGHT//2 + 150, 80, 80),
                               Vector2(0, 0), 0.0, WHITE)
            else:
                draw_rectangle(60 + i * 100, WINDOW_HEIGHT//2 + 150, 80, 80, PLAYER_COLORS[i])
            draw_text (f"Player {i+1} controls are:", 60 + i * 100, WINDOW_HEIGHT//2 + 240, 20, GRAY)
            left_key, right_key = GAME_CONTROLS[i]
            draw_text (f"Left: {glfwGetKeyName(left_key,left_key)}", 60 + i * 100, WINDOW_HEIGHT//2 + 270, 20, GRAY)
            draw_text (f"Right: {glfwGetKeyName(right_key,right_key)}", 60 + i * 100, WINDOW_HEIGHT//2 + 300, 20, GRAY)

    end_drawing()

close_window()
  
