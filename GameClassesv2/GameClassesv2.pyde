import os
import random
path = os.getcwd()

###################################################################################################################################################################################################
#IMAGES: all loaded at the beginning to reduce memory usage

#kirito images
kiritoImagesSingle = []
for file in os.listdir(path + "/images/Kirito/single"):
	kiritoImagesSingle.append(file)
kiritoImagesSingle.sort()
kiritoImagesSingle.remove('.DS_Store')

kiritoImagesDual = []
for file in os.listdir(path + "/images/Kirito/dual"):
  kiritoImagesDualSingle.append(file)
kiritoImagesDual.sort()
print(kiritoImagesSingle)

#tatsuya images (boss1)

#

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
           self.vy += 0.5
        elif self.y + self.h >= g.g:
            self.vy = g.g - (self.y + self.h)
            if self.y + self.h > g.g:
                self.vy = g.g - (self.y + self.h)
        if self.y + self.h == g.g:
            return True
        
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
        self.imgpath = "Kirito/"
        self.movePath = self.moveDictPathUpSingle
        self.moveFrames = self.moveDictFramesUpSingle
        self.kiritoImages = kiritoImagesSingle
        self.actionIndex = "000"
        #single blade
        self.moveDictPathDownSingle = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockback":"100", "throw":"100"}
        self.moveDictFramesDownSingle = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6}
        self.moveDictPathUpSingle = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990"}
        self.moveDictFramesUpSingle = {"still":7, "walk":5, "jump":6, "block":2, "normalATK":3, "knockBack":6, "throw":5}
        #dual blade (damage multiplied by 2)
        self.dualWield = False
        self.moveDictPathDownDual = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockback":"100", "throw":"100"}
        self.moveDictFramesDownDual = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6}
        self.moveDictPathUpDual = {"still": "090", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990"}
        self.moveDictFramesUpDual = {"still":7, "walk":5, "jump":6, "block":2, "normalATK":3, "knockBack":6, "throw":5}
        
        #command keys
        self.direction = {"left":False, "right":False, "up":False, "down":False}
        
        #hitbox
        self.hitRangex = range(int((self.x + self.w) - (self.w/8)),(int(self.x + self.w)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h) - ((self.h/2)*0.3125)),int((self.y + self.h) + ((self.h/2)*1.231)))

        #action calling for dictionaries, plus status update
        self.lastAction = "still"
        self.action = "still"
        self.status = "passive" #divided into "passive", "attacking", "defending". passive = knockback, attack = only lose health
        
    def update(self):
        self.gravity()
        
        #if attacking, player cannot change attacks; all frames must pass in order for player to change actions (must choose wisely)
        if self.status == "attacking":
            if self.f < self.moveFrames[self.action]:
                self.action = self.lastAction
        
        #update movement dictionaries
        if self.dualWield == False:
            if self.direction["down"] == False:
                self.movePath = self.moveDictPathUpSingle
                self.moveFrames = self.moveDictFramesUpSingle
            else:
                self.movePath = self.moveDictPathDownSingle
                self.moveFrames = self.moveDictFramesDownSingle
        else:
            self.kiritoImages = kiritoImagesDual
            if self.direction["down"] == False:
                self.movePath = self.moveDictPathUpDual
                self.moveFrames = self.moveDictFramesUpDual
            else:
                self.movePath = self.moveDictPathDownDual
                self.moveFrames = self.moveDictFramesDownDual
                
        #update image path using search function for first index, then use the frames to choose up to what extent to display.
        #if the action is still going, then add one frame.
        #if the framecount has reached the max, then start over.
        if self.action != self.lastAction:
              for action in kiritoImages:
                if self.action in kiritoImages[action]:
                    self.actionIndex = action
                    
        else:
            if self.f >= self.moveFrame[self.action]:
                self.f = 0
                
        self.img = path + "/images/" + self.imgpath + kiritoImages[self.actionIndex]
        
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

#g = Game()

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
        
###################################################################################################################################################################################################
#KEYBOARD CONTROL AND RESET


#if g.gameReset == True:
    #g = Game()
