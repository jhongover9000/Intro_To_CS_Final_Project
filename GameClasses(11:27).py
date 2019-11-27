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
        if self.y + self.h < g.g:
           self.vy += 0.5
        elif self.y + self.h >= g.g:
            self.vy = g.g - (self.y + self.h)
            if self.y + self.h > g.g:
                self.vy = g.g - (self.y + self.h)
        if self.y + self.h == g.g:
            return True

        



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
        self.status = "OK"    #split into "OK"(not hit) and "HIT" (moves to damage animation, player can't move for 0.5 seconds)
        self.dir = d
        self.dualwield = False
        self.move = "still"
        self.action = "still"
        self.up = True
        self.hitRangex = range((self.x + self.w) - (self.w/8),(self.x + self.w)+(self.w/8))
        self.hitRangey = range((self.y + self.h) - ((self.h/2)*0.3125),(self.y + self.h) + ((self.h/2)*1.231))

        
        self.task = "still"   #this is what decides whether Kirito is moving or fighting (can't do both at the same time)


    def update(self):
        self.gravity()
        #selecting path based on swordcount
        if self.dualwield == True:
            self.swordcount = "dualwield/"
        else:
            self.swordcount = "single/"
    
        #standing or crouched; changes directories for images
        if self.up == False:
            self.stand = "down/"
            self.moveDictPath = {"still": "100", "walk":"100", "normalATK":"103"}
            self.moveDictFrames = {"still":1, "walk":1, "downStrike":6}
        else:
            self.stand = "up/"
            self.moveDictPath = {"still": "000", "walk":"400", "jump":"200", "downStrike":"001", "knockBack":"003", "throw":"990"}
            self.moveDictFrames = {"still":7, "walk":5, "jump":6, "normalATK":3, "knockBack":6}
        
        
        self.imgPath = str(path) + "/images/" + self.swordcount + self.stand + "Krt" + self.moveDictPath[self.action]


    #updates self.dir based on self.direction
        if self.direction["right"] == True:  #right
            self.dir = 1
            self.vx = 5
            if self.y + self.h == g.g and self.up == True:
                self.action = "walk"
        elif self.direction["left"] == True:  #left
            self.dir = -1
            self.vx = -5
            if self.y + self.h == g.g and self.up == True:
                self.action = "walk"
        if self.direction["up"] == True and self.y + self.h == g.g: #(g.g or g.platform.x):
            self.action = "jump"
            self.vy = -13
        elif self.direction["up"] == False and self.direction["left"] == False and self.direction["right"] == False: 
            self.vx = 0
            if self.action == ("walk" or "jump"):
                self.action = "still"
        if self.up == False:
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
        
        #resetting the frame when the action changes
        if self.action != self.move:
            self.f = 0
            self.move = self.action
            
        #selecting the image file to display
        if self.action == "still":
            self.f += 0.4
        elif self.action == "walk":
            self.f += 0.2
        elif self.action == "jump":
            self.f += 0.4
        
        if self.up == False:
            self.f -= 0.3
            
        if self.action != "walk" and self.action != "still":
            if self.f > self.moveDictFrames[self.action]:
                if self.gravity():
                    self.action = "still"
                    self.f = 0
                else:
                    self.f -= 0.4
        self.framePoint = int(round((self.f)%(self.moveDictFrames[self.action]),0))
            
            
        
        #adds the preceding value before framePoint for image file
        if self.framePoint > 9:
            self.buffer = "_"
        else:
            self.buffer = "_0"
        
            
        self.imgPath = self.imgPath + self.buffer + str(self.framePoint) + ".png"
        
        self.img = loadImage(self.imgPath)
        
        #final verifications
        #print(self.framePoint)
        print(self.imgPath)
        print(self.action)
        print(self.hitRangex)
        print(self.hitRangey)
        
    def display(self):
        self.update() 
        if self.dir >= 0:
            image(self.img,self.x,self.y,self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x,self.y,self.w,self.h,928,0,0,640)


class Game:
    def __init__(self,w,h,g):
        self.w = w
        self.h = h
        self.g = g
        self.frames = 0


        self.kirito = Player(0,0,0,0,500,345,0,60,"Krt",0)
        self.kirito.y = self.g - (self.kirito.h + self.kirito.h)

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
        if g.kirito.y + g.kirito.h == g.g:
            g.kirito.up = False
            print("kepresseD")
        
    elif keyCode == 87:
        g.kirito.direction["up"] = True
        
    elif keyCode == 65:
        g.kirito.direction["left"] = True
    
    elif keyCode == 68:
        g.kirito.direction["right"] = True
    

def keyReleased():
    if keyCode == 83:
        g.kirito.up = True
        
    elif keyCode == 87:    #up(w)
        g.kirito.direction["up"] = False
    
    elif keyCode == 65:    #left(a)
        g.kirito.direction["left"] = False
    
    elif keyCode == 68:     #right(d)
        g.kirito.direction["right"] = False