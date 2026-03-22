from raylib import *
from enum import Enum
from collections import deque
from settings import *
import math

class Snake:
        
    def __init__(self, position:Vector2,speed,color:Color):
        self.position = position
        self.speed = speed
        self.color = color
        self.size = 50
        self.body = deque()
        self.body.append(Vector2(position.x,position.y)) 
        self.heading = Vector2(0,self.speed)
        self.isPlayerDead = False
        self.shouldmove = 0 
        self.moveInterval = 0.05
        self.timer = 0
        self.camera = Camera2D()
        self.camera.offset = Vector2(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        self.camera.rotation = 0.0
        self.camera.zoom = 2.0
        self.left_heading = Vector2(-1*self.speed,0)
        self.right_heading = Vector2(self.speed,0)
        self.up_heading = Vector2(0,-1 * self.speed)
        self.down_heading = Vector2(0,self.speed)

        
    def update(self):   
             
        if(IsKeyPressed(KEY_LEFT)):
            if(self.heading != self.right_heading):
                self.heading = self.left_heading
        elif(IsKeyPressed(KEY_UP)):
            if(self.heading != self.down_heading):
                self.heading = self.up_heading
        elif(IsKeyPressed(KEY_RIGHT)):
            if(self.heading != self.left_heading):
                self.heading = self.right_heading
        elif(IsKeyPressed(KEY_DOWN)):
            if(self.heading != self.up_heading):
                self.heading = self.down_heading
            
                
        
        self.timer += get_frame_time()
        
        
        if(self.timer >= self.moveInterval):
            desiredPosition = Vector2Add(self.position,self.heading)
            
            if (check_vector_OOB(desiredPosition,GRID_AMMOUNT_X)):
                self.position = desiredPosition
            else:
                self.isPlayerDead = True
            self.timer -= self.moveInterval
        
        self.process_body()
        self.camera.target = vector2_add(translateGridtoXY(self.position),Vector2(CELL_W/2,CELL_H/2))

                
        while self.size > len(self.body):
            self.body.append(Vector2(self.body[-1].x,self.body[-1].y))
        
                    
        for i in range(1,len(self.body)-1):
            if(Vector2Equals(self.body[i], self.body[0])):
                self.isPlayerDead = True
                

            
            
        
    def draw(self):
        for bodyPart in self.body:
            sx = bodyPart.x
            sy = bodyPart.y
            sv = Vector2(sx,sy)
            # print(sx,sy)
            square_coords = translateGridtoXY(sv)
            DrawRectangleV(square_coords,(CELL_W,CELL_H),self.color)
    
    def process_body(self):
        if(not Vector2Equals(self.body[0], self.position)):
            for i in range(len(self.body)-1,0,-1):
                self.body[i].x = self.body[i-1].x
                self.body[i].y = self.body[i-1].y
            self.body[0].x = self.position.x
            self.body[0].y = self.position.y
            return True
        return False
    
    def reset(self):
        self.position.x = 5
        self.position.y = 5
        self.heading = Vector2(0,self.speed)
        self.size = 2
        self.body.clear()
        self.body.append(Vector2(self.position.x,self.position.y)) 
        self.isPlayerDead = False
        
def check_vector_OOB(vector: Vector2, bound):
    if(vector.x >= 0 and vector.y >= 0 and vector.x < bound and vector.y < bound):
        return True
    return False