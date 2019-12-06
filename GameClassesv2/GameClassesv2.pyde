import os
import random
path = os.getcwd()

###################################################################################################################################################################################################
#IMAGES: all loaded at the beginning to reduce memory usage

#kirito images
kiritoSingle = []
for file in os.listdir(path + "/images/Kirito/single/"):
    kiritoSingle.append(file)
kiritoSingle.sort()
kiritoSingle.remove(kiritoSingle[0])
kiritoImagesSingle = {}
for file in kiritoSingle:
        kiritoImagesSingle[file] = loadImage(path + "/images/Kirito/single/" + str(file))
#print(kiritoImagesSingle)

kiritoDual = []
for file in os.listdir(path + "/images/Kirito/dual/"):
  kiritoDual.append(file)
kiritoDual.sort()
kiritoImagesDual = {}
for file in kiritoDual:
        kiritoImagesDual[file] = loadImage(path + "/images/Kirito/dual/" + str(file))
#print(kiritoImagesDual)

#tatsuya images (boss1)



#asuna images

#enemy images

###################################################################################################################################################################################################
#MOVING OBJECTS

#create class Entity; all moving objects will stem from this
class Entity:
    def __init__(self,x,y,vx,vy,w,h,f,d):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.f = f
        self.d = d
        
    def gravity(self):
        if self.y + self.h < g.g:
           self.vy += 0.4
        elif self.y + self.h >= g.g:
            self.vy = g.g - (self.y + self.h)
            if self.y + self.h > g.g:
                self.vy = g.g - (self.y + self.h)
        if self.y + self.h == g.g:
            return True
        else:
            return False
        
    def update(self):
        self.x += self.vx
        self.y = self.vy
        
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
        
#create class Player, derived from class Entity
class Player(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        
        #stats
        self.health = 100
        self.attack = 50
        self.mp = 20
        self.experience = 0
        self.level = 1
        
        #image attributes (dictionaries for images and frame count; made to ensure that random commands won't crash game)
        self.kiritoImages = kiritoImagesSingle
        self.actionIndex = "000"
        #single blade
        self.moveDictPathDownSingle = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockback":"100", "throw":"100", "hit":"507"}
        self.moveDictFramesDownSingle = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6, "knockback":1, "throw":1, "hit":3}
        self.moveDictPathUpSingle = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990", "hit":"508"}
        self.moveDictFramesUpSingle = {"still":7, "walk":5, "jump":6, "block":2, "normalATK":3, "knockBack":6, "throw":5, "hit":3}
        #dual blade (damage multiplied by 2)
        self.dualWield = False
        self.moveDictPathDownDual = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockback":"100", "throw":"100"}
        self.moveDictFramesDownDual = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6}
        self.moveDictPathUpDual = {"still": "090", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990"}
        self.moveDictFramesUpDual = {"still":7, "walk":5, "jump":6, "block":2, "normalATK":3, "knockBack":6, "throw":5}
        
        #setup initial dictionaries
        self.movePath = self.moveDictPathUpSingle
        self.moveFrames = self.moveDictFramesUpSingle        
        #command keys
        self.direction = {"left":False, "right":False, "up":False, "down":False}
        self.dir = d
        
        #hitbox
        self.hitRangex = range(int((self.x + self.w) - (self.w/8)),(int(self.x + self.w)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h) - ((self.h/2)*0.3125)),int((self.y + self.h) + ((self.h/2)*1.231)))

        #action calling for dictionaries, plus status update
        self.lastAction = "still"
        self.action = "still"
        self.status = "passive" #divided into "passive", "attacking", "defending". passive = knockback, attack = only lose health
        
    def update(self):
        self.gravity()
        
        #update movement dictionaries
        if self.dualWield == False:
            if (self.gravity() == False) or (self.direction["down"] == False):
                self.movePath = self.moveDictPathUpSingle
                self.moveFrames = self.moveDictFramesUpSingle
            else:
                self.movePath = self.moveDictPathDownSingle
                self.moveFrames = self.moveDictFramesDownSingle
        else:
            self.kiritoImages = kiritoImagesDual
            if (self.gravity() == False) or (self.direction["down"] == False):
                self.movePath = self.moveDictPathUpDual
                self.moveFrames = self.moveDictFramesUpDual
            else:
                self.movePath = self.moveDictPathDownDual
                self.moveFrames = self.moveDictFramesDownDual
        
                                
        #if the player presses random buttons while down (the ones that don't have any effects) they stay "passive"
        if self.direction["down"] == True and self.action != ("still" or "normalATK" or "block" or "hit"):
            self.status = "passive"
            
        #if attacking, then the entire animation needs to be completed before attempting a new one    
        if self.status == "attacking":
            if self.lastAction != "still":
                if self.framePoint < self.moveFrames[self.action]:
                    self.action = self.lastAction
                
                               
        #reset frames when actions change
        if self.action != self.lastAction:
            self.f = 0
            
        #changing status from attacking to passive and changing frames
        if self.status == "attacking":
            if self.lastAction != self.action:
                self.f = 0
            if self.f >= self.moveFrames[self.action]:
                self.status = "passive"
                if self.gravity():
                    self.action = "still"
                else:
                    self.action = "jump"
                            
        #update directional movement
        if self.direction["left"]:
            self.dir = -1
            if self.status == "passive":
                self.vx = -5
                if self.y + self.h == g.g:
                    self.action = "walk"
        elif self.direction["right"] == True:  #right
            self.dir = 1
            if self.status == "passive":
                self.vx = 5
                if self.y + self.h == g.g:
                    self.action = "walk"
        if self.direction["up"] == True and self.y + self.h == g.g and self.status != "defending":
            self.vy = -13
            self.action = "jump"
            
        #move back to "still" if no keys are pressed    
        if (self.direction["up"] == False) and (self.direction["left"] == False) and (self.direction["right"] == False):
            self.vx = 0
            if self.action == ("walk" or "jump"):
                self.action = "still"
        #velocity is 0 when object ducks
        if self.direction["down"]:
            self.vx = 0
        #velocity is 0 when player is attacking or defending    
        if self.status == ("attacking" or "defending"):
            self.vx = 0
            
        #updates final position of object
        self.x += self.vx
        self.y += self.vy
        
        #updates hitbox
        self.hitRangex = range(int((self.x + self.w/2) - (self.w/8)),(int(self.x + self.w/2)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h/2) - ((self.h/2)*0.3125)),int((self.y + self.h/2) + ((self.h/2)*0.8125)))
        if self.direction["down"]:
            self.hitRangey = range(int(self.y + (self.h/2*1.125)),int((self.y + self.h/2) + ((self.h/2)*0.8125)))
            
        #reach extends when attacking (all g.enemies in range will be hit)
        if self.status == "attacking":
            if self.dir > 0:
                self.hitRangex = range(int((self.x + self.w/2) - (self.w/8)),(int(self.x + self.w/2)+(self.w/3)))
            elif self.dir < 0:
                self.hitRangex = range(int((self.x + self.w/2) - (self.w/3)),(int(self.x + self.w/2)+(self.w/8)))

        #choosing the speeds of the animations for each action
        self.f += 0.028*self.moveFrames[self.action]
        
        #animating player before hitting the ground  
        if self.action != ("walk" and "still" and "hit"):
            if self.action == "jump":
                if self.f > self.moveFrames[self.action]:
                    if self.gravity():
                        self.action = "still"
                        self.f = 0
                    count = 1
                    if self.vy > 5:
                        self.f -= 4.8*count
                        count +=1
                    else:
                        self.f -= 0.4

        #creating an attribute to get the framepoint for the image to be displayed                                        
        self.framePoint = int(round((self.f)%(self.moveFrames[self.action]),0))   
                
        #adds the buffer to get the image name
        if self.framePoint > 9:
            self.buffer = "_"
        else:
            self.buffer = "_0"
        

        self.img = self.kiritoImages["Krt" + self.movePath[self.action] + self.buffer + str(self.framePoint) + ".png"]
        #final tweaks
        self.lastAction = self.action
        
        #print(self.f)
        #print(self.framePoint)
        print(self.status)
        #print(self.action)
        print(self.lastAction)
        print(self.vy)
        #print(self.dir)
        #for i in range(2):
            #print(self.hitRangex[i])
            #print(self.hitRangey[i])
#create class Boss, derived from class Player


#create class Enemy, derived from class Entity

#create class Projectile, derived from class Entity; this is the projectile throw by player

#create class KnockBackBlast, derived from class Entity; this is knockback effect for both player and boss

#

###################################################################################################################################################################################################
#STAGES

#create class Stage; all stages will stem from this (uses player (will need to be constant throughout game; g.kirito),enemies,etc)

#create class StageOne

#create class StageTwo

#create class StageThree

###################################################################################################################################################################################################
#GAME

#create class Game (self,g,h,w,kirito = Player(arg))
class Game:
    def __init__(self,w,h,g):
        self.w = w
        self.h = h
        self.g = g
        self.frames = 0


        self.kirito = Player(0,0,0,0,500,345,0,1)
        self.kirito.y = self.g - (self.kirito.h)

    def display(self):
        self.frames +=1
        self.kirito.display()



#def update(self):
    #this whole area will take care of all stages and levels in them. self.stageCount will determine the stage (background and enemies)
    #and self.levelCount will determine the level (level 3, enter boss room)
    
    #if player's health reaches 0, self.playerDeath == True
    
#def gameOver(self):
    #display "You Died" in red. display restart menu
    #if restart is clicked:
        #g.gameReset == True

#def gameComplete(self):
    #

###################################################################################################################################################################################################
#SETUP AND DRAW
g = Game(1080,720,640)


def setup():
    loadImage(path+"/images/single")
    size(g.w,g.h)
    background(0)

#def setup():
    #code for main menu and UI
    #start game
    #if g.gameEnd == False:
        #g.update()
        #g.display()
    #if playerDeath == True:
        #g.gameOver()
    #if g.gameEnd == True:
        #g.gameComplete()
        
def draw():
    background(0)
    g.display()
        
###################################################################################################################################################################################################
#KEYBOARD CONTROL AND RESET

def keyPressed():
    if keyCode == 83:     #down(S)
        if g.kirito.y + g.kirito.h == g.g and g.kirito.status != "defending":
            g.kirito.direction["down"] = True
        
    elif keyCode == 87:    #up(W)
        if (not g.kirito.direction["down"]) and g.kirito.status != "defending":
            g.kirito.direction["up"] = True
        
    elif keyCode == 65:    #left(A)
        if g.kirito.status != "defending":
            g.kirito.direction["left"] = True
    
    elif keyCode == 68:     #right(D)
        if g.kirito.status != "defending":
            g.kirito.direction["right"] = True
    
    elif keyCode == 76:    # (L)
        if g.kirito.status != "defending":
            g.kirito.status = "attacking"
            g.kirito.action = "normalATK"
            
    elif keyCode == 74:    # (J)
        if g.kirito.status != "defending" and g.kirito.direction["down"] == False:
            g.kirito.status = "attacking"
            g.kirito.action = "knockBack"
        
    elif keyCode == 75:    #(K)
        if g.kirito.status != "defending" and g.kirito.direction["down"] == False:
            g.kirito.status = "attacking"
            g.kirito.action = "throw"
        
    elif keyCode == 32:
        g.kirito.vx = 0
        g.kirito.status = "defending"
        g.kirito.action = "block"
        
def keyReleased():
    if keyCode == 83:     #down(s)
        g.kirito.direction["down"] = False
        
    elif keyCode == 87:    #up(w)
        g.kirito.direction["up"] = False
    
    elif keyCode == 65:    #left(a)
        g.kirito.direction["left"] = False
    
    elif keyCode == 68:     #right(d)
        g.kirito.direction["right"] = False
    
    elif keyCode == 32:
        g.kirito.action = "still"
        g.kirito.status = "passive"

#if g.gameReset == True:
    #g = Game()
