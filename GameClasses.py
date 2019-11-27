import os
import random
path = os.getcwd()

#call images and save in a list OUTSIDE of the game!!

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
        if self.y + self.h < g.g:
           self.vy += 0.5
        elif self.y + self.h >= g.g:
            self.vy = g.g - (self.y + self.h)
            if self.y + self.h > g.g:
                self.vy = g.g - (self.y + self.h)
        if self.y + self.h == g.g:
            return True

    def display(self):
        self.update() 
        
        #displays hitbox (for verification only)
        stroke(255)
        noFill()
        strokeWeight(3)
        rect(self.hitRangex[0],self.hitRangey[0],(self.hitRangex[-1]-self.hitRangex[0]),(self.hitRangey[-1]-self.hitRangey[0]))
        
        if self.dir >= 0:
            image(self.img,self.x,self.y,self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x,self.y,self.w,self.h,928,0,0,640)



class Player(Entity):
    def __init__(self,x,y,vx,vy,w,h,r,f,img,d):
        Entity.__init__(self,x,y,vx,vy,w,h,f,img,d)
        self.direction = {"left":False, "right":False, "up":False}
        self.r = r
        self.health = 100
        self.attack = 50
        self.mp = 10
        self.experience = 0
        self.level = 1
        #when passive or attacking, you still take damage. passive = knockback, attack = only lose health
        self.status = "passive" #"passive", "attacking", "defending"
        self.dir = d
        self.dualwield = False
        self.lastAction = "still"
        self.action = "still"
        self.up = True
        self.hitRangex = range(int((self.x + self.w) - (self.w/8)),(int(self.x + self.w)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h) - ((self.h/2)*0.3125)),int((self.y + self.h) + ((self.h/2)*1.231)))
        self.moveCounter = 0

        
        self.task = "still"   #this is what decides whether Kirito is moving or fighting (can't do both at the same time)


    def update(self):
        self.gravity()
        
        #if the attack is still in animation, the player cannot switch attacks.
        
        
        #selecting path based on swordcount
        if self.dualwield == True:
            self.swordcount = "dualwield/"
        else:
            self.swordcount = "single/"
    
        #standing or crouched; changes directories for images
        if self.up == False:
            self.stand = "up/"
            self.moveDictPath = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockback":"100", "throw":"100"}
            self.moveDictFrames = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6}
        if self.up == True:
            self.stand = "up/"
            self.moveDictPath = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990"}
            self.moveDictFrames = {"still":7, "walk":5, "jump":6, "block":2, "normalATK":3, "knockBack":6, "throw":5}
        
        
        self.imgPath = str(path) + "/images/" + self.swordcount + self.stand + "Krt" + self.moveDictPath[self.action]


    #updates self.dir based on self.direction
        if self.direction["right"] == True:  #right
            self.dir = 1
            if self.status == "passive":
                self.vx = 5
                if self.y + self.h == g.g and self.up == True:
                    self.action = "walk"
        elif self.direction["left"] == True:  #left
            self.dir = -1
            if self.status == "passive":
                self.vx = -5
                if self.y + self.h == g.g and self.up == True and self.status == "passive":
                    self.action = "walk"
        if self.direction["up"] == True and self.y + self.h == g.g and self.status != "defending": #(g.g or g.platform.x)
            self.action = "jump"
            self.vy = -13
        elif self.direction["up"] == False and self.direction["left"] == False and self.direction["right"] == False: 
            self.vx = 0
            if self.action == ("walk" or "jump"):
                self.action = "still"
        if self.up == False:
            self.vx = 0
            
        #player cannot move when defending or attacking (unless the attack specifically make the player move)
        if self.status == ("attacking" or "defending"):
            self.vx = 0
                
    #player moves slower when crouched            
        if self.stand == False:
            if dir > 0:
                self.vx -= 3
            elif dir < 0:
                self.vx += 3
                
    #updates location of object 
        self.x += self.vx
        self.y += self.vy
        
    #updates hitbox
        self.hitRangex = range(int((self.x + self.w/2) - (self.w/8)),(int(self.x + self.w/2)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h/2) - ((self.h/2)*0.3125)),int((self.y + self.h/2) + ((self.h/2)*0.8125)))
        if self.up == False:
            self.hitRangey = range(int(self.y + (self.h/2*1.125)),int((self.y + self.h/2) + ((self.h/2)*0.8125)))
      
      #reach extends when attacking (all g.enemies in range will be hit)
        if self.status == "attacking":
            if self.dir > 0:
                self.hitRangex = range(int((self.x + self.w/2) - (self.w/8)),(int(self.x + self.w/2)+(self.w/3)))
            elif self.dir < 0:
                self.hitRangex = range(int((self.x + self.w/2) - (self.w/3)),(int(self.x + self.w/2)+(self.w/8)))
                
        #if the plate
                
        #resetting the frame when the action changes
        if (self.action != self.lastAction):
            self.f = 0
            
            
        #if the player is attacking or defending, the "hit" status is removed
        
            
        #selecting the image file to display
        if self.action == "still":
            self.f += 0.4
        elif self.action == "walk":
            self.f += 0.3
        elif self.action == "jump":
            self.f += 0.4
        else:
            self.f += 0.2
        
        if self.up == False and (self.action == "still" or self.action == "walk") and self.status == "passive":
            self.f -= 0.35
            
        if self.up:    
            if self.action != "walk" and self.action != "still":
                if self.action == "jump":
                    if self.f > self.moveDictFrames[self.action]:
                        if self.gravity():
                            self.action = "still"
                            self.f = 0
                        count = 1
                        if self.vy > 10:
                            self.f -= 5.5*count
                            count +=1
                        else:
                            self.f -= 0.4
                        
        if self.status == "defending":
            self.f -= 0.2
            
        self.framePoint = int(round((self.f)%(self.moveDictFrames[self.action]),0))
        
        #changing from attacking to passive
        if self.status == "attacking":
                if self.f >= self.moveDictFrames[self.action]:
                    self.status = "passive"
                    self.action = "still"
                    if self.gravity():
                        self.action = "still"
                    else:
                        self.action = "jump"
        
        #adds the preceding value before framePoint for image file
        if self.framePoint > 9:
            self.buffer = "_"
        else:
            self.buffer = "_0"
        
            
        self.imgPath = self.imgPath + self.buffer + str(self.framePoint) + ".png"
        
        self.img = loadImage(self.imgPath)
        self.lastAction = self.action
        #final verifications
        #print(self.framePoint)
        print(self.action)
        print(self.imgPath)
        print(self.status)
        print(self.dir)
        print(self.up)
        #for i in range(2):
            #print(self.hitRangex[i])
            #print(self.hitRangey[i])
            
        
        
    
class Enemy(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,img,d):
        Entity.__init__(self,x,y,vx,vy,w,h,f,img,d)
        self.hitRangex = range(int((self.x + self.w) - (self.w/8)),(int(self.x + self.w)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h) - ((self.h/2)*0.3125)),int((self.y + self.h) + ((self.h/2)*1.231))) 




#class stage
        
#stage 1

#stage 2

#stage 3

class Game:
    def __init__(self,w,h,g):
        self.w = w
        self.h = h
        self.g = g
        self.frames = 0


        self.kirito = Player(0,0,0,0,500,345,0,60,"Krt",1)
        self.kirito.y = self.g - (self.kirito.h)

    def display(self):
        self.frames +=1
        self.kirito.display()


g = Game(1080,720,640)


def setup():
    loadImage(path+"/images/single")
    size(g.w,g.h)
    background(0)

def draw():
    background(0)
    g.display()

def keyPressed():
    if keyCode == 83:
        if g.kirito.y + g.kirito.h == g.g and g.kirito.status != "defending":
            g.kirito.up = False
        
    elif keyCode == 87:
        if g.kirito.status != "defending":
            g.kirito.direction["up"] = True
        
    elif keyCode == 65:
        if g.kirito.status != "defending":
            g.kirito.direction["left"] = True
    
    elif keyCode == 68:
        if g.kirito.status != "defending":
            g.kirito.direction["right"] = True
    
    elif keyCode == 76:
        if g.kirito.status != "defending":
            g.kirito.status = "attacking"
            g.kirito.action = "normalATK"
            
    elif keyCode == 74:
        if g.kirito.status != "defending" and g.kirito.up == True:
            g.kirito.status = "attacking"
            g.kirito.action = "knockBack"
        
    elif keyCode == 75:
        if g.kirito.status != "defending" and g.kirito.up == True:
            g.kirito.status = "attacking"
            g.kirito.action = "throw"
        
    elif keyCode == 32:
        g.kirito.vx = 0
        g.kirito.status = "defending"
        g.kirito.action = "block"

def keyReleased():
    if keyCode == 83:
        g.kirito.up = True
        
    elif keyCode == 87:    #up(w)
        g.kirito.direction["up"] = False
    
    elif keyCode == 65:    #left(a)
        g.kirito.direction["left"] = False
    
    elif keyCode == 68:     #right(d)
        g.kirito.direction["right"] = False
    
    elif keyCode == 32:
        g.kirito.action = "still"
        g.kirito.status = "passive"
        
