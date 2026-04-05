from retrocycle import Retrocycle
from wall import Wall
from raylib import *
from settings import *

class Game():
    def __init__(self,num_players, win_score=WIN_SCORE) -> None:
        self.isGameOver = True
        self.ispaused = False
        self.winner = None
        self.win_score = win_score
        self.numPlayers = num_players
        self.view_width = WINDOW_WIDTH // self.numPlayers
        self.view_height = WINDOW_HEIGHT
        self.split_screen_rectangle = Rectangle(0, 0, self.view_width, -self.view_height)
        if(num_players > len(GAME_CONTROLS)):
            print("Too many players! Max is 4")
            exit()
        self.players = []
        self.playersRenderTexture = []
        for i in range(num_players):
            left_key, right_key = GAME_CONTROLS[i]
            curr_player = Retrocycle(Vector2(0, 0), PLAYER_COLORS[i], PLAYER_COLOR_NAMES[i], left_key, right_key, self.view_width, self.view_height)
            player_texture = load_render_texture(self.view_width, self.view_height)
            self.players.append((player_texture, curr_player))
        for _ , player in self.players:
            player.players = self.players
            player.respawn()
        
    def update(self):
        if(is_key_pressed(PAUSE_KEY)):
            self.ispaused = not self.ispaused
        
        if(is_key_pressed(KEY_H) and self.ispaused):
            self.isGameOver = True
            self.ispaused = False
        if(self.ispaused):
            return
        for _ , player in self.players:
            player.update()
            
            if(player.isPlayerDead):
                if player.collided_with is player:
                    player.score = max(0, player.score - 1)
                elif player.collided_with is not None:
                    player.collided_with.score += 1
                    if player.collided_with.score >= self.win_score:
                        self.winner = player.collided_with
                        self.isGameOver = True
                        return
                player.respawn()

        any_grinding = any(p.isGrinding for _, p in self.players)
        if "grind" in SOUNDS:
            if any_grinding and not is_sound_playing(SOUNDS["grind"]):
                play_sound(SOUNDS["grind"])
            elif not any_grinding and is_sound_playing(SOUNDS["grind"]):
                stop_sound(SOUNDS["grind"])

    def reset(self, num_players, win_score=WIN_SCORE):
        self.__init__(num_players, win_score)
    def draw(self):
        
        # https://www.raylib.com/examples/core/loader.html?name=core_2d_camera_split_screen
        for player_texture, player in self.players:
            begin_texture_mode(player_texture)
            clear_background(BLACK)
            begin_mode_2d(player.camera)

            background = TEXTURES["bg"]
            DrawTexturePro(background, Rectangle(0, 0, background.width, background.height),
                            Rectangle(PLAYFIELD_OFFSET_X, PLAYFIELD_OFFSET_Y, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT),
                            Vector2(0, 0), 0.0, WHITE)
            player.draw()

            for i in range(0, GRID_AMOUNT_X + 1, 1):
                x = PLAYFIELD_OFFSET_X + (i * CELL_W)
                
                DrawLine(x, PLAYFIELD_OFFSET_Y, x, PLAYFIELD_OFFSET_Y + PLAYFIELD_HEIGHT, GRAY)

            for i in range(0, GRID_AMOUNT_Y + 1, 1):
                y = PLAYFIELD_OFFSET_Y + (i * CELL_H)
                
                DrawLine(PLAYFIELD_OFFSET_X, y, PLAYFIELD_OFFSET_X + PLAYFIELD_WIDTH, y, GRAY)
            
            self.draw_player_arrow(player)

            end_mode_2d()
            end_texture_mode()

        for i, (texture, player) in enumerate(self.players):
            draw_texture_rec(texture.texture, self.split_screen_rectangle, Vector2(i * self.view_width, 0), WHITE)
            self.draw_player_UI(player, i * self.view_width)
        
        if(self.ispaused):
            root_x = WINDOW_WIDTH // 2 - FONT_SIZE * 5
            root_y = WINDOW_HEIGHT // 4 + FONT_SIZE * 3

            draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Color(0, 0, 0, 150))
            draw_text("PAUSED", root_x, WINDOW_HEIGHT // 4, FONT_SIZE * 2, WHITE)

            draw_text("SCOREBOARD", root_x, root_y, FONT_SIZE, WHITE)
            root_y += FONT_SIZE + 10
            for i, (_, player) in enumerate(self.players):
                draw_text(f"Player {i + 1}:  {player.score}", root_x, root_y, FONT_SIZE, player.color)
                root_y += FONT_SIZE + 5

            draw_text("Press Return to Resume", root_x, WINDOW_HEIGHT * 3 // 4, FONT_SIZE, WHITE)
            draw_text("Press H to return to the main menu", root_x, WINDOW_HEIGHT * 3 // 4 + FONT_SIZE + 10, FONT_SIZE, WHITE)

        
    def draw_player_UI(self, player,view_root):
        show_velocity = round(1.0 / player.moveInterval, 2)
        shown_pillow = round(player.pillow * 100, 2)
        draw_text(f"Score: {player.score}", view_root + 10, 10, FONT_SIZE, player.color)
        draw_text(f"Velocity: {show_velocity}", view_root + 10, 10 + FONT_SIZE + 5, FONT_SIZE, WHITE)
        draw_text(f"Pillow: {shown_pillow}", view_root + 10, 10 + (FONT_SIZE + 5) * 2, FONT_SIZE, WHITE)
        
                        
    def draw_player_arrow(self,target_player):
        # Copilot helped with some of the vector math
        arrow_head_length = 3
        arrow_head_half_width = 2.5
        arrow_length = 2.5
        target_player_pos = Vector2Add(translateGridtoXY(target_player.position), Vector2(CELL_SIZE / 2, CELL_SIZE / 2))
        for _ , player in self.players:
            
            if (target_player is not player):
                to_other_player = Vector2Subtract(translateGridtoXY(player.position), target_player_pos)
                if(Vector2Length(to_other_player) > 0):
                    to_other_player = Vector2Normalize(to_other_player)
                    line_start = Vector2Add(target_player_pos,Vector2Scale(to_other_player, CELL_SIZE * 1))
                    line_end = Vector2Add(target_player_pos,Vector2Scale(to_other_player, CELL_SIZE * arrow_length))

                    arrow_tip = Vector2Add(line_end, Vector2Scale(to_other_player, arrow_head_length))
                    perpendicular = Vector2(-to_other_player.y, to_other_player.x)
                    triangle_point1 = Vector2Add(line_end, Vector2Scale(perpendicular, arrow_head_half_width))
                    triangle_point2 = Vector2Add(line_end, Vector2Scale(perpendicular, -arrow_head_half_width))
                    DrawTriangle(arrow_tip, triangle_point1, triangle_point2, player.color)
                    DrawTriangle(arrow_tip, triangle_point2, triangle_point1, player.color)
                    DrawLineEx(line_start, line_end, 2.0, player.color)
        
    def decide_player_respawn_location(self, player):
        player.position = Vector2(randint(1,GRID_AMOUNT_X - 2),randint(1,GRID_AMOUNT_Y - 2))


