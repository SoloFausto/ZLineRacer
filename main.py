from raylib import *
from settings import * 
from cycle_game import Game


if __name__ == '__main__':  

  set_config_flags(FLAG_WINDOW_RESIZABLE | FLAG_WINDOW_HIGHDPI)
  init_window(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, "Comet Riders")
  toggle_borderless_windowed()
  init_audio_device()
  set_target_fps(120)
  SOUNDS["crash"] = load_sound("assets/crash.mp3")
  set_sound_volume(SOUNDS["crash"], 0.25)
  SOUNDS["grind"] = load_sound("assets/grind.mp3")
  
  hum = load_music_stream("assets/hum.mp3")
  music = load_music_stream("assets/music.mp3")
  play_music_stream(hum)
  play_music_stream(music)
  set_music_volume(music, 0.15)
  set_music_volume(hum, 0.15)

  for name in PLAYER_COLOR_NAMES:
    TEXTURES[f"{name}_ship"] = load_texture(f"assets/{name}_ship.png")
    TEXTURES[f"{name}_wall"] = load_texture(f"assets/{name}_wall.png")
  TEXTURES["bg"] = load_texture("assets/bg.png")
  TEXTURES["bg_menu"] = load_texture("assets/bg_menu.png")
  game_screen = load_render_texture(WINDOW_WIDTH, WINDOW_HEIGHT)
  instruction_lines = [
      ("- Ride your spaceship and leave a trail behind you.", WHITE),
      ("- Crash into any trail or the arena wall and you die.", WHITE),
      ("- Turning slows you down.", WHITE),
      ("- Grinding (riding alongside a wall or trail) builds even more speed.", WHITE),
      ("- The pillow helps cushion some impacts, use it to your advantage.", WHITE),
      ("- Press return to pause the game and see the scores.", WHITE),
      ("- Out manouver your oponents! Follow the arrows to see where they are.", YELLOW),
  ]
  instruction_font_size = 60
  while any(measure_text(text, instruction_font_size) > WINDOW_WIDTH - 160 for text, _ in instruction_lines):
    instruction_font_size -= 1
  instruction_line_height = instruction_font_size + 20
  isTitleScreen = True
  isInstructions = False
  isPlayerSelect = False
  isWinScreen = False
  game = Game(1)
  game.isGameOver = True
  num_players = 2
  win_score = WIN_SCORE

  while not window_should_close():
    update_music_stream(music)
    if game.isGameOver:
      if isWinScreen:
        if IsKeyPressed(KEY_ENTER):
          isWinScreen = False
          isTitleScreen = True
      elif isTitleScreen:
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
        elif IsKeyPressed(KEY_UP):
          win_score = min(99, win_score + 1)
        elif IsKeyPressed(KEY_DOWN):
          win_score = max(1, win_score - 1)
        elif IsKeyPressed(KEY_ENTER):
          game.reset(num_players, win_score)
          game.isGameOver = False
          isPlayerSelect = False
    else:
      game.update()
      update_music_stream(hum)

      if game.isGameOver:
        if game.winner is not None:
          isWinScreen = True
        else:
          isTitleScreen = True
        isInstructions = False
        isPlayerSelect = False
    
    if not game.isGameOver:
      game.render_player_views()

    begin_texture_mode(game_screen)
    clear_background(BLACK)
    
    
    if not game.isGameOver:
      game.draw()
    else:
      bg = TEXTURES["bg_menu"]
      DrawTexturePro(bg, Rectangle(0, 0, bg.width, bg.height),
                     Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
                     Vector2(0, 0), 0.0, WHITE)

    if isWinScreen and game.isGameOver:
        winner = game.winner
        winner_index = next(i for i, (_, p) in enumerate(game.players) if p is winner)
        draw_text(f"PLAYER {winner_index + 1} WINS!", 50, WINDOW_HEIGHT // 2 - 100, 200, winner.color)
        draw_text(f"Score: {winner.score}", 50, WINDOW_HEIGHT // 2 + 130, 100, winner.color)
        draw_text("Press Enter to continue", 50, WINDOW_HEIGHT // 2 + 280, 80, WHITE)
    elif isTitleScreen and game.isGameOver:
        draw_text("COMET RIDERS", 50, 300 , 200, GREEN)
        draw_text("Press Enter to Start", 60, WINDOW_HEIGHT//2 + 150, 100, WHITE)
    elif isInstructions and game.isGameOver:
        draw_text("HOW TO PLAY", 50, 80, 150, GREEN)
        y = 300
        for instruction, color in instruction_lines:
            draw_text(instruction, 80, y, instruction_font_size, color)
            y += instruction_line_height
        draw_text("Press Enter to Continue", 80, WINDOW_HEIGHT - 130, 70, WHITE)
    elif isPlayerSelect and game.isGameOver:
        draw_text("PLAYER SELECT", 50, 200, 200, GREEN)
        draw_text(f"Number of Players: {num_players}", 60, 400, 100, WHITE)
        draw_text("Use Left/Right to Change", 60, 500, 100, WHITE)
        draw_text(f"Win Score: {win_score}", 60, 620, 100, WHITE)
        draw_text("Use Up/Down to Change", 60, 720, 100, WHITE)
        player_x = 60
        player_start_y = 880
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
    end_texture_mode()

    begin_drawing()
    clear_background(BLACK)
    screen_width = get_screen_width()
    screen_height = get_screen_height()
    screen_scale = min(screen_width / WINDOW_WIDTH, screen_height / WINDOW_HEIGHT)
    rendered_width = WINDOW_WIDTH * screen_scale
    rendered_height = WINDOW_HEIGHT * screen_scale
    screen_x = (screen_width - rendered_width) / 2
    screen_y = (screen_height - rendered_height) / 2
    draw_texture_pro(
        game_screen.texture,
        Rectangle(0, 0, WINDOW_WIDTH, -WINDOW_HEIGHT),
        Rectangle(screen_x, screen_y, rendered_width, rendered_height),
        Vector2(0, 0),
        0.0,
        WHITE,
    )


    end_drawing()

close_audio_device()
close_window()
  
