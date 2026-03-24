import enum

from raylib import *
from settings import *

from wall import Wall
from enum import Enum


class Retrocycle:
    speed_divider = 0.001
    base_accel_speed = 30
    min_accel_speed = base_accel_speed * 1.5
    turn_accel_multiplier = 0.98
    accel_speed_below = base_accel_speed / 10
    accel_speed_above = base_accel_speed / 50
    camera_turn_smoothness = 14.0
    max_pillow = 0.10
    pillow_recover_rate = 0.05
    

    def __init__(self, position:Vector2,color:Color,left_key,right_key,view_width,view_height) -> None:
        self.position = position
        self.color = color
        self.body = set()
        self.body.add(Wall(Vector2(position.x,position.y)))
        self.heading = 2
        self.left_key = left_key
        self.right_key = right_key
        self.isPlayerDead = False
        self.moveInterval = 0.020
        self.timer = 0
        self.camera = Camera2D()
        self.camera.offset = Vector2(view_width / 2, view_height / 2)
        self.camera.rotation = 180.0
        self.camera_target_rotation = self.camera.rotation
        self.camera.zoom = 2.0
        self.pillow = self.max_pillow
        self.isrespawning = False
        self.players = []


        
    def update(self):   
            
        if(is_key_pressed(self.left_key)):
            self.heading = (self.heading - 1) % 4
            self.moveInterval /= self.turn_accel_multiplier
            self.camera_target_rotation = (self.camera_target_rotation + 90) % 360

        if(is_key_pressed(self.right_key)):
            self.heading = (self.heading + 1) % 4
            self.moveInterval /= self.turn_accel_multiplier
            self.camera_target_rotation = (self.camera_target_rotation - 90) % 360
        
                
        
        self.timer += get_frame_time()
        
        
        if(self.timer >= self.moveInterval):
            desiredPosition = Vector2Add(self.position,map_int_to_heading(self.heading))

            if (check_vector_OOB(desiredPosition,GRID_AMOUNT_X)):
                next_wall = Wall(Vector2(desiredPosition.x, desiredPosition.y))
                has_collision = False

                for _ , player in self.players:
                    if(player.isrespawning):
                        continue
                    if(next_wall in player.body):
                        has_collision = True
                        break

                if(has_collision):
                    self.pillow -= 1 * get_frame_time()
                    if(self.pillow <= 0):
                        self.isPlayerDead = True
                else:
                    self.position = desiredPosition
                    self.pillow = lerp(self.pillow, self.max_pillow, self.pillow_recover_rate)

            else:
                if(not self.isrespawning):
                    self.pillow -= 1 * get_frame_time()
                    if(self.pillow <= 0):
                        self.isPlayerDead = True
            
            self.timer -= self.moveInterval
        
        
        target_interval = self.base_accel_speed * self.speed_divider
        if(self.moveInterval > self.base_accel_speed * self.speed_divider):
            recover_rate = self.accel_speed_below * self.speed_divider
        else:
            recover_rate = self.accel_speed_above * self.speed_divider
        step = recover_rate * get_frame_time()

        interval_diff = abs(target_interval - self.moveInterval)
        interval_t = 1.0 if interval_diff == 0 else min(1.0, step / interval_diff)
        self.moveInterval = lerp(self.moveInterval, target_interval, interval_t)
        
        if(self.moveInterval > self.min_accel_speed * self.speed_divider):
            self.moveInterval = self.min_accel_speed * self.speed_divider
            

        #smooth camera rotation
        # https://stackoverflow.com/questions/28036652/finding-the-shortest-distance-between-two-angles
        rotation_delta = ((self.camera_target_rotation - self.camera.rotation + 180.0) % 360.0) - 180.0
        self.camera.rotation += rotation_delta * min(1.0, self.camera_turn_smoothness * get_frame_time())
            
        if(self.should_be_grinding()):
            self.moveInterval /= 1.005
        
        self.camera.target = vector2_add(translateGridtoXY(self.position),Vector2(CELL_W/2,CELL_H/2))
        self.process_body(get_frame_time())

    

                

    def should_be_grinding(self):
        
        current_vector = map_int_to_heading(self.heading)
        left = Vector2(-current_vector.y, current_vector.x)
        right = Vector2(current_vector.y, -current_vector.x)

        left_pos = Vector2(self.position.x + left.x, self.position.y + left.y)
        right_pos = Vector2(self.position.x + right.x, self.position.y + right.y)
        for texture , player in self.players:
            if(Wall(left_pos) in player.body or Wall(right_pos) in player.body):
                return True

        #check if against wall
        if(self.position.x == 0 or
           self.position.y == 0 or
           self.position.x == GRID_AMOUNT_X - 1 or
           self.position.y == GRID_AMOUNT_Y - 1):
            return True
        return False
            
        
    def draw(self):
        for _ , player in self.players:
            for bodyPart in player.body:
                sx = bodyPart.position.x
                sy = bodyPart.position.y
                sv = Vector2(sx,sy)
                square_coords = translateGridtoXY(sv)
                DrawRectangleV(square_coords,(CELL_W,CELL_H),player.color)
    
    def process_body(self, tick):
        if(Wall(Vector2(self.position.x,self.position.y)) not in self.body and not self.isrespawning):
            self.body.add(Wall(Vector2(self.position.x,self.position.y)))
        for bodyPart in self.body.copy():
            bodyPart.update(tick)
            if(not bodyPart.alive):
                self.body.remove(bodyPart)

                
            
    def respawn(self):
        self.position = Vector2(randint(1,GRID_AMOUNT_X - 2),randint(1,GRID_AMOUNT_Y - 2))
        self.moveInterval = self.base_accel_speed * self.speed_divider
        self.heading = randint(0,3)
        self.pillow = self.max_pillow
        self.body.clear()
        self.camera.rotation = 90.0 * self.heading
        self.camera_target_rotation = self.camera.rotation
        # self.body.add(Wall(Vector2(self.position.x, self.position.y)))
        self.isPlayerDead = False
        self.isrespawning = False
        
        
def check_vector_OOB(vector: Vector2, bound):
    if(vector.x >= 0 and vector.y >= 0 and vector.x < bound and vector.y < bound):
        return True
    return False

    
def map_int_to_heading(num):
    match num:
        case 0:
            return Vector2(0, -1)  # up_heading
        case 1:
            return Vector2(1, 0)   # right_heading
        case 2:
            return Vector2(0, 1)   # down_heading
        case 3:
            return Vector2(-1, 0)  # left_heading
        case _:
            return Vector2(0, 0)
