from retrocycle import Retrocycle
from wall import Wall
from raylib import *
from settings import *

class Game():
    def __init__(self,num_players) -> None:
        self.isGameOver = True
        self.numPlayers = num_players
        self.view_width = WINDOW_WIDTH // self.numPlayers
        self.view_height = WINDOW_HEIGHT
        # Source rectangle for render textures (negative height keeps texture upright).
        self.split_screen_rectangle = Rectangle(0, 0, self.view_width, -self.view_height)
        if(num_players > len(GAME_CONTROLS)):
            print("Too many players! Max is 4")
            exit()
        self.players = []
        self.playersRenderTexture = []
        for i in range(num_players):
            left_key, right_key = GAME_CONTROLS[i]
            curr_player = Retrocycle(Vector2(5, 5), PLAYER_COLORS[i], left_key, right_key, self.view_width, self.view_height)
            player_texture = load_render_texture(self.view_width, self.view_height)
            self.players.append((player_texture, curr_player))
        for _ , player in self.players:
            player.players = self.players
            player.respawn()
        
    def update(self):
        for texture , player in self.players:
            player.update()
            
            if(player.isPlayerDead):
                print("Player died!")
                player.respawn()
    def draw(self):
        
        # https://www.raylib.com/examples/core/loader.html?name=core_2d_camera_split_screen
        for player_texture, player in self.players:
            begin_texture_mode(player_texture)
            clear_background(BLACK)
            begin_mode_2d(player.camera)
            player.draw()

            for i in range(0,GRID_AMOUNT_Y + 1,1):
                x = i * CELL_W
                DrawLine(x, 0, x, WINDOW_HEIGHT, GRAY)

            for i in range(0,GRID_AMOUNT_X + 1,1):
                y = i * CELL_H
                
                DrawLine(0, y, WINDOW_WIDTH, y, GRAY)
            end_mode_2d()
            end_texture_mode()

        for i, (player_texture, _) in enumerate(self.players):
            draw_texture_rec(player_texture.texture, self.split_screen_rectangle, Vector2(i * self.view_width, 0), WHITE)
        
    def decide_player_respawn_location(self, player):
        player.position = Vector2(randint(1,GRID_AMOUNT_X - 2),randint(1,GRID_AMOUNT_Y - 2))

    
