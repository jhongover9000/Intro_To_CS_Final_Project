import os
import random
path = os.getcwd()

class Entity:
    def __init__(self,x,y,vx,vy,w,h,f,img,d):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.f = f
        self.health = 100
        self.attack = 5    
        self.dir = d



def gravity(self):
    if self.y + self.r >= self.g:
        self.vy = 0
    else:
        self.vy += 0.3
        if self.y + self.r + self.vy > self.g:
            self.vy = self.g - (self.y+self.r)



class Player(Entity):
    def __init__(self,x,y,vx,vy,w,h,r,f,img,d):
        Entity.__init__(self,x,y,vx,vy,w,h,f,img,d)
        self.direction = {"left":False, "right":False, "up":False}
        self.health = 100
        self.attack = 50
        self.mp = 10
        self.experience = 0
        self.level = 1
        self.status = "OK"    #split into "OK"(not hit) and "HIT" (moves to damage animation, player can't move for 0.5 seconds)
        self.dir = d
        self.dualwield = False
        self.move = "still"
        self.action = "still"
        
        self.task = "still"   #this is what decides whether Kirito is moving or fighting (can't do both at the same time)


    def update(self):
        
        #selecting path based on swordcount
        if self.dualwield == True:
            self.swordcount = "dualwield/"
        else:
            self.swordcount = "single/"
    
        #standing or crouched
        self.up = True
        if self.up == False:
            self.stand = "down/"
        else:
            self.stand = "up/"
        

