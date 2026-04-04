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
  TEXTURES["bg_menu"] = load_texture("assets/bg_menu.png")
  isTitleScreen = True
  isInstructions = False
  isPlayerSelect = False
  game = Game(1)
  game.isGameOver = True
  num_players = 2
  
  while not window_should_close():
    if game.isGameOver:
      if isTitleScreen:
        if IsKeyPressed(KEY_ENTER):
          isTitleScreen = False
          isInstructions = True

      elif isInstructions:
        if IsKeyPressed(KEY_ENTER):
          isInstructions = False
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
        isInstructions = False
        isPlayerSelect = False
    
    begin_drawing()
    clear_background(BLACK)
    
    
    if not game.isGameOver:
      game.draw()
    else:
      bg = TEXTURES["bg_menu"]
      DrawTexturePro(bg, Rectangle(0, 0, bg.width, bg.height),
                     Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
                     Vector2(0, 0), 0.0, WHITE)

    if isTitleScreen and game.isGameOver:
        draw_text("COMET RIDERS", 50, WINDOW_HEIGHT//2 - 20, 200, GREEN)
        draw_text("Press Enter to Start", 60, WINDOW_HEIGHT//2 + 250, 100, WHITE)
    elif isInstructions and game.isGameOver:
        draw_text("HOW TO PLAY", 50, 80, 150, GREEN)
        y = 300
        line_h = 80
        draw_text("- Ride your spaceship and leave a trail behind you.", 80, y, 60, WHITE)
        y += line_h
        draw_text("- Crash into any trail or the arena wall and you die.", 80, y, 60, WHITE)
        y += line_h
        draw_text("- Turning slows you down.", 80, y, 60, WHITE)
        y += line_h
        draw_text("- Grinding (riding alongside a wall or trail) builds even more speed.", 80, y, 60, WHITE)
        y += line_h
        draw_text("- The pillow helps cushion some impacts, use it to your advantage.", 80, y, 60, WHITE)
        y += line_h
        draw_text("- Press return to pause the game and see the scores.", 80, y, 60, WHITE)
        y += line_h
        draw_text("- Out manouver your oponents! Follow the arrows to see where they are.", 80, y, 60, YELLOW)
        y += line_h * 2
        draw_text("Press Enter to Continue", 80, WINDOW_HEIGHT - 130, 70, WHITE)
    elif isPlayerSelect and game.isGameOver:
        draw_text("PLAYER SELECT", 50, 200, 200, GREEN)
        draw_text(f"Number of Players: {num_players}", 60,400, 100, WHITE)
        draw_text("Use Left/Right to Change", 60, 500, 100, WHITE)
        player_x = 60
        player_start_y = 650
        player_row_spacing = 140
        for i in range(num_players):
            ship_key = PLAYER_COLOR_NAMES[i] + "_ship"
            player_y = player_start_y + i * player_row_spacing
            if ship_key in TEXTURES:
                tex = TEXTURES[ship_key]
                DrawTexturePro(tex, Rectangle(0, 0, tex.width, tex.height),
                   Rectangle(player_x, player_y, 80, 80),
                               Vector2(0, 0), 0.0, WHITE)
            else:
              draw_rectangle(player_x, player_y, 80, 80, PLAYER_COLORS[i])
            draw_text(f"Player {i+1} controls are: {PLAYER_CONTROL_NAMES[i]}", player_x + 110, player_y + 25, 40, WHITE)
        draw_text("Press Enter to Start", 60, WINDOW_HEIGHT -150, 100, WHITE)


    end_drawing()

close_window()
  
