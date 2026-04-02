import enum

from raylib import *
from settings import *

from wall import Wall
from enum import Enum
import math


class Retrocycle:
    base_cells_per_second = 75
    max_speed_multiplier = 2.5
    turn_speed_change = 0.95
    grind_speed_boost = 1.005
    above_interval_recovery_rate = 6.0
    below_interval_recovery_rate = 0.5
    base_move_interval = 1.0 / base_cells_per_second
    min_move_interval = base_move_interval / max_speed_multiplier
    camera_turn_smoothness = 14.0
    max_pillow = 0.10
    pillow_recover_rate = 0.05
    pillow_loss_rate = 0.35
    grind_particle_spawn_rate = 220
    grind_particle_max = 250
    

    def __init__(self, position:Vector2,color:Color,left_key,right_key,view_width,view_height) -> None:
        self.position = position
        self.color = color
        self.body = set()
        self.body.add(Wall(Vector2(position.x,position.y),color))
        self.heading = 2
        self.last_move_vector = map_int_to_heading(self.heading)
        self.left_key = left_key
        self.right_key = right_key
        self.isPlayerDead = False
        self.moveInterval = self.base_move_interval
        self.timer = 0
        self.camera = Camera2D()
        self.camera.offset = Vector2(view_width / 2, view_height / 2)
        self.camera.rotation = 180.0
        self.camera_target_rotation = self.camera.rotation
        self.camera.zoom = 5.0
        self.pillow = self.max_pillow
        self.isrespawning = False
        self.hasCollided = False
        self.isGrinding = False
        self.players = []
        self.particle_emmiter = ParticleEmitter(Vector2(0,0),Vector2(0,0),color,0.1)


        
    def update(self):   
            
        if(is_key_pressed(self.left_key)):
            self.heading = (self.heading - 1) % 4
            self.moveInterval /= self.turn_speed_change
            self.camera_target_rotation = (self.camera_target_rotation + 90) % 360

        if(is_key_pressed(self.right_key)):
            self.heading = (self.heading + 1) % 4
            self.moveInterval /= self.turn_speed_change
            self.camera_target_rotation = (self.camera_target_rotation - 90) % 360
        
        
        
        self.timer += get_frame_time()
                    

        
        if(self.timer >= self.moveInterval):
            self.timer -= self.moveInterval
            desiredPosition = Vector2Add(self.position,map_int_to_heading(self.heading))
            next_wall = Wall(Vector2(desiredPosition.x, desiredPosition.y),self.color)
            has_collision = False
            if (check_vector_OOB(desiredPosition,GRID_AMOUNT_X)):
                has_collision = True
            for _ , player in self.players:
                if(player.isrespawning):
                    continue
                if(next_wall in player.body):
                    has_collision = True
                    break

            if(has_collision):
                self.hasCollided = True
            else:
                self.hasCollided = False
                self.last_move_vector = map_int_to_heading(self.heading)
                self.position = desiredPosition
            
        
        if(self.hasCollided):
            self.pillow -= self.pillow_loss_rate * get_frame_time()
            if(self.pillow <= 0):
                self.isPlayerDead = True
        else:
                self.pillow = min(self.max_pillow, self.pillow + self.pillow_recover_rate * get_frame_time())
        
        
        target_interval = self.base_move_interval
        if(self.moveInterval > self.base_move_interval):
            interval_t = min(1.0, self.above_interval_recovery_rate * get_frame_time())
        else:
            interval_t = min(1.0, self.below_interval_recovery_rate * get_frame_time())

        self.moveInterval = lerp(self.moveInterval, target_interval, interval_t)
        self.moveInterval = max(self.min_move_interval, self.moveInterval)
            
        self.isGrinding = self.should_be_grinding()
        if(self.isGrinding):
            self.moveInterval = max(self.min_move_interval, self.moveInterval / self.grind_speed_boost)
            self.particle_emmiter.add_particles(2)
        #smooth camera rotation
        # https://stackoverflow.com/questions/28036652/finding-the-shortest-distance-between-two-angles
        rotation_delta = ((self.camera_target_rotation - self.camera.rotation + 180.0) % 360.0) - 180.0
        self.camera.rotation += rotation_delta * min(1.0, self.camera_turn_smoothness * get_frame_time())

        
        self.camera.target = vector2_add(translateGridtoXY(self.position),Vector2(CELL_W/2,CELL_H/2))
        self.process_body(get_frame_time())
        self.particle_emmiter.update(Vector2Add(translateGridtoXY(self.position),Vector2(CELL_SIZE//2,CELL_SIZE//2)),get_frame_time())

    

                

    def should_be_grinding(self):
        
        current_vector = self.last_move_vector
        left = Vector2(-current_vector.y, current_vector.x)
        right = Vector2(current_vector.y, -current_vector.x)

        left_pos = Vector2(self.position.x + left.x, self.position.y + left.y)
        right_pos = Vector2(self.position.x + right.x, self.position.y + right.y)
        for _ , player in self.players:
            if(Wall(left_pos,self.color) in player.body or Wall(right_pos,self.color) in player.body):
                return True

        #check if against wall
        if(self.position.x == 0 or
           self.position.y == 0 or
           self.position.x == GRID_AMOUNT_X - 1 or
           self.position.y == GRID_AMOUNT_Y - 1):
            return True
        return False
            
        
    def draw(self):
        for bodyPart in self.body:
                bodyPart.draw()
        
        for _ , player in self.players:
            if (self is not player):
                for bodyPart in player.body:
                    bodyPart.draw()
        
        self.particle_emmiter.draw()
    
    def process_body(self, tick):
        if(Wall(Vector2(self.position.x,self.position.y),self.color) not in self.body and not self.isrespawning):
            self.body.add(Wall(Vector2(self.position.x,self.position.y),self.color))
        for bodyPart in self.body.copy():
            bodyPart.update(tick)
            if(not bodyPart.alive):
                self.body.remove(bodyPart)


    def respawn(self):
        self.position = Vector2(randint(1,GRID_AMOUNT_X - 2),randint(1,GRID_AMOUNT_Y - 2))
        self.moveInterval = self.base_move_interval
        self.timer = 0
        self.heading = 2
        self.last_move_vector = map_int_to_heading(self.heading)
        self.pillow = self.max_pillow
        self.body.clear()
        self.camera.rotation = 90.0 * self.heading
        self.camera_target_rotation = self.camera.rotation
        self.isPlayerDead = False
        self.isrespawning = False
        
        
def check_vector_OOB(vector: Vector2, bound):
    if(vector.x >= 0 and vector.y >= 0 and vector.x < bound and vector.y < bound):
        return False
    return True

    
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

class ParticleEmitter:
    def __init__(self, position:Vector2, velocity:Vector2, color:Color, lifetime:float) -> None:
        self.position = position
        self.velocity = velocity
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.number_of_particles = 5
        self.particles = []
        
    def update(self,position,delta_time):
        self.position = position
        self.age += delta_time
        #update particles
        for particle in self.particles:
            particle['age'] += delta_time
            if particle['age'] < particle['lifetime']:
                particle['position'].x += particle['velocity'].x * delta_time
                particle['position'].y += particle['velocity'].y * delta_time
        
        #remove dead particles - use list comprehension to avoid modifying list during iteration
        self.particles = [particle for particle in self.particles if particle['age'] < particle['lifetime']]
        
        return True
    def add_particles(self, count):
        for _ in range(count):
            angle = random() * 2 * math.pi
            speed = 50 + random() * 100
            velocity = Vector2(cos(angle) * speed, sin(angle) * speed)
            self.particles.append({
                'position': Vector2(self.position.x, self.position.y),
                'velocity': velocity,
                'lifetime': 0.5 + random() * 0.5,
                'age': 0.0
            })
            
    def draw(self):
        for particle in self.particles:
            DrawCircleV(particle['position'], 2, self.color)