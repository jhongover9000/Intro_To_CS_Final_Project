import os
import random
path = os.getcwd()

###################################################################################################################################################################################################
###################################################################################################################################################################################################

#IMAGES: all loaded at the beginning to reduce memory usage

#background images are divided into lists of moving parts and a background, which are used to create the stages
backgrounds = {}
for k in range(4):
    backgroundSets = []
    for file in os.listdir(path + "/images/Background/" + "0" + str(k)):
        backgroundSets.append(loadImage(path + "/images/Background/" + "0" + str(k) + "/" + file))
    backgrounds[k] = backgroundSets
    
#kirito images
kiritoSingle = []
for file in os.listdir(path + "/images/Kirito/single/"):
    kiritoSingle.append(file)
kiritoSingle.sort()
kiritoImagesSingle = {}
for file in kiritoSingle:
        kiritoImagesSingle[file] = loadImage(path + "/images/Kirito/single/" + str(file))
#print(kiritoImagesSingle.keys())

kiritoDual = []
for file in os.listdir(path + "/images/Kirito/dual/"):
  kiritoDual.append(file)
kiritoDual.sort()
kiritoImagesDual = {}
for file in kiritoDual:
        kiritoImagesDual[file] = loadImage(path + "/images/Kirito/dual/" + str(file))
#print(kiritoImagesDual)

#tatsuya images (boss1)
#tatsuya = []
#for file in os.listdir(path + "/images/Tatsuya/"):
#    tatsuya.append(file)
#
#tatsuyaImages = {}
#for file in tatsuya:
#        tatsuyaImages[file] = loadImage(path + "/images/Tatsuya/" + str(file))

#asuna images
asuna = []
for file in os.listdir(path + "/images/Asuna/"):
    asuna.append(file)
asuna.sort()
asunaImages = {}
for file in asuna:
        asunaImages[file] = loadImage(path + "/images/Asuna/" + str(file))

#enemy images


#projectile images
projectileImages = []





###################################################################################################################################################################################################
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
        self.dir = d
        
    def gravity(self):
        if self.y + self.h < g.g:
           self.vy += 0.3
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
        print(self.hitRangex[0])
        
        if self.dir > 0:
            image(self.img,self.x-g.middlex, self.y-self.h//2,self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-g.middlex,self.y-self.h//2,self.w,self.h)
            
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

#class Player, derived from class Entity
class Player(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        
        #stats
        self.level = 1
        self.maxHealth = 100
        self.health = self.maxHealth
        self.attack = 50
        self.maxMP = 20
        self.mp = self.maxMP
        self.maxXP = 100
        self.experience = 20
        self.shieldHealth = 100
        
        #image attributes (dictionaries for images and frame count; made to ensure that random commands won't crash game)
        self.kiritoImages = kiritoImagesSingle
        self.actionIndex = "000"
        #single blade
        self.moveDictPathDownSingle = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockBack":"100", "throw":"100", "hit":"507", "die":"600"}
        self.moveDictFramesDownSingle = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6, "knockBack":1, "throw":1, "hit":3, "die":7}
        self.moveDictPathUpSingle = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990", "hit":"508", "die":"600"}
        self.moveDictFramesUpSingle = {"still":7, "walk":5, "jump":6, "block":1, "normalATK":3, "knockBack":6, "throw":5, "hit":3, "die":7}
        #dual blade (damage multiplied by 2)
        self.dualWield = False
        self.moveDictPathDownDual = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockBack":"100", "throw":"100"}
        self.moveDictFramesDownDual = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6}
        self.moveDictPathUpDual = {"still": "090", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990"}
        self.moveDictFramesUpDual = {"still":7, "walk":5, "jump":6, "block":1, "normalATK":3, "knockBack":6, "throw":5}
        
        #setup initial dictionaries
        self.movePath = self.moveDictPathUpSingle
        self.moveFrames = self.moveDictFramesUpSingle        
        #command keys
        self.direction = {"left":False, "right":False, "up":False, "down":False}
        self.dir = d
        
        #hitbox components
        #NOTICE: the y range of the hitbox is based on the location of the ground. If this changes, then CHANGE THE Y VALUES
        self.x1 = (self.x + self.w/2) - (self.w/8)
        self.x2 = (self.x + self.w/2) + (self.w/8)
        
        #action calling for dictionaries, plus status update
        self.lastAction = "still"
        self.action = "still"
        self.lastStatus = "passive"
        self.status = "passive" #divided into "passive", "attacking", "defending". passive = knockBack, attack = only lose health
        self.hitCounter = 0   #makes it so that player is immobilized for a short period of time
        self.shieldCounter = 0   #displays shield health for short period of time
        self.shieldBroken = False
        self.shieldBrokenNotify = False    #triggers display saying "Shield Broken"
        self.shieldBrokenCounter = 0    #displays "Shield Broken!" for certain period of time
        self.mpLackingNotify = False    #triggers display saying "Not enough MP!"
        
    def update(self):
        self.gravity()
        self.shieldBrokenNotify
        
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
                
        #if player is hit, they can't do anything for 20 frames
        if self.action == "hit":
            if self.lastAction == "jump":
                self.vy -= 1
                self.vx -= self.dir*1
            if self.lastAction != "hit":
                self.f = 0
            self.lastAction = "hit"
            self.hitCounter +=1
            if self.hitCounter > 20:
                self.action = "still"
                self.hitCounter = 0
                                
        #if the player presses random buttons while down (the ones that don't have any effects) they stay "passive"
        if (self.direction["down"] == True) and self.action != ("still" or "normalATK" or "block" or "hit"):
            self.status = "passive"
            
        #if attacking, then the entire animation needs to be completed before attempting a new one    
        if self.status == "attacking":
            self.throwObject()
            self.knockBackSlash()
            if self.action != self.lastAction:
                self.f = 0
                self.lastAction = self.action
            elif self.action == self.lastAction:
                if self.f <= self.moveFrames[self.action]:
                    self.lastAction = self.action
                else:
                    self.action = "still"
                        
        #reset frames when actions change
        if self.action != self.lastAction:
            self.f = 0
        
        self.lastAction = self.action
        
        #basically, you can't do anything when hit.    
        if self.action != "hit":
            #changing status from attacking to passive and changing frames
            if self.status == "attacking":
                if self.action != "walk":
                    if self.f >= self.moveFrames[self.action]:
                        self.f = 0
                        self.status = "passive"
                        if self.gravity():
                            self.action = "still"
                        else:
                            self.action = "jump"           
                        
            #to prevent glitch where player keeps attacking when crouching     
            if self.action == "normalATK":
                if self.f >= self.moveFrames[self.action]:
                    self.status = "passive"
                    if self.gravity():
                        self.action = "still"
                    else:
                        self.action = "jump"
                        
            #UPDATE PLAYER ACTION            
            self.lastAction = self.action
            
            #player unblocks after block (animation) - dependent on lastAction                               
            if self.lastAction == "block":
                if self.action == "block":
                    self.status = "defending"
                    self.f = 0
                elif self.action != "block":
                    self.action = "block"
                    self.lastAction = "still"   
                                     
            if self.status != "attacking":                    
                #update directional movement
                if self.direction["left"]:
                    self.dir = -1
                    if self.status == "passive":
                        self.vx = -8
                        if self.y + self.h == g.g:
                            self.action = "walk"
                elif self.direction["right"] == True:  #right
                    self.dir = 1
                    if self.status == "passive":
                        self.vx = 8
                        if self.y + self.h == g.g:
                            self.action = "walk"
                if self.direction["up"] == True and self.y + self.h == g.g and self.status != "defending":
                    self.vy = -13
                    self.action = "jump"
                    
                #move back to "still" if no keys are pressed    
                if (self.direction["up"] == False) and (self.direction["left"] == False) and (self.direction["right"] == False):
                    self.vx = 0
                    if self.lastAction == ("walk" or "jump"):
                        self.action = "still"
            #velocity is 0 when object ducks
            if self.direction["down"]:
                self.vx = 0
            #velocity is 0 when player is attacking or defending    
            if self.status == ("attacking" or "defending"):
                self.vx = 0
                
        #if hit, vx = 0
        if self.action == "hit":
            self.vx = 0
        #keep player from moving off screen   
        if (self.x + self.w/2) <= 0 and self.dir == -1:
            self.vx = 0
        #updates final position of object
        self.x += self.vx
        self.y += self.vy
        
        if g.type == "boss":
            pass
        else:
            #moves game screen along
            if (self.x + self.w/2) > g.w/2:
                g.middlex += self.vx
            elif (self.x + self.w/2) <= g.w/2:
                g.middlex = 0
        
        #hitbox update
        y1 = (self.y + self.h/2) - ((self.h/2)*0.3125)
        y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
        if self.x < 0:
            self.x1 = (self.x + self.w) - self.w/2 - self.w/8
            self.x2 = (self.x + self.w) - self.w/2 + self.w/8
        elif self.x >= 0 and (self.x + self.w/2) <= g.w/2:   #if between starting point and middle
            self.x1 = (self.x + self.w/2) - (self.w/8)
            self.x2 = (self.x + self.w/2) + (self.w/8)
        elif (self.x + self.w/2) > g.w/2:   #if self.x + self.w/2 goes beyond midpoint
            if g.type == "boss":
                self.x1 = (self.x + self.w/2) - self.w/8
                self.x2 = (self.x + self.w/2) + self.w/8
            else:
                self.x1 = (g.w/2) - (self.w/8)
                self.x2 = (g.w/2) + (self.w/8)
        if self.direction["down"]:
            y1 = self.y + (self.h/2*1.125)
            y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)   
        #reach extends when attacking (all g.enemies in range will be hit)
        if self.status == "attacking":
            if self.dir > 0:
                self.x2 += self.w/4
            elif self.dir < 0:
                self.x1 -= self.w/4
        #create hitbox        
        self.hitRangex = range(int(self.x1),int(self.x2))
        self.hitRangey = range(int(y1),int(y2))
        
        
        #choosing the speeds of the animations for each action
        if self.status == "attacking":
            self.f += 0.05*self.moveFrames[self.action]
        else:
            self.f += 0.035*self.moveFrames[self.action]
        
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
        
        #SELECTS IMAGE TO DISPLAY
        self.img = self.kiritoImages["Krt" + self.movePath[self.action] + self.buffer + str(self.framePoint) + ".png"]
        
        #UPDATES LAST STATUS
        self.lastStatus = self.status

        
        #update stats
        self.maxHealth = 100 + 10*(self.level-1)
        self.maxMP = 20 + 10*(self.level-1)
        self.maxXP = 100*1.3**(self.level-1)
    
    #throwing knife        
    def throwObject(self):
        if self.action == "throw" and self.status == "attacking":
            if self.lastAction != "throw":    #(x,y,vx,vy,w,h,f,d,type,dmg)
                if self.x < g.w/2:
                    g.flyingObjects.append(Projectile((self.x + self.w/2),(self.y + self.h/2),g.kirito.dir*6,0,0,0,0,g.kirito.dir,"knockBack",self.attack,"player"))
                elif self.x >= g.w/2:
                    if g.type == "boss":
                        g.flyingObjects.append(Projectile((self.x + self.w/2),(self.y + self.h/2),g.kirito.dir*6,0,0,0,0,g.kirito.dir,"knockBack",self.attack,"player"))
                    else:
                        g.flyingObjects.append(Projectile((g.w/2),(self.y + self.h/2),g.kirito.dir*6,0,0,0,0,g.kirito.dir,"knockBack",self.attack,"player"))
                
    #knockBack slash
    def knockBackSlash(self):
        if self.action == "knockBack" and self.status == "attacking":
            print("knock")
            if self.lastAction != "knockBack":
                if self.x < g.w/2:
                    g.flyingObjects.append(Projectile((self.x + self.w/2),((self.y + self.h/2) + ((self.h/2)*0.8125) ),g.kirito.dir*6,0,0,0,0,g.kirito.dir,"knockBack",self.attack,"player"))
                elif self.x >= g.w/2:
                    if g.type == "boss":
                        g.flyingObjects.append(Projectile((self.x + self.w/2),((self.y + self.h/2) + ((self.h/2)*0.8125) ),g.kirito.dir*6,0,0,0,0,g.kirito.dir,"knockBack",self.attack,"player"))
                    else:
                        g.flyingObjects.append(Projectile((g.w/2),((self.y + self.h/2) +(self.h/4)),g.kirito.dir*6,0,0,0,0,g.kirito.dir,"knockBack",self.attack,"player"))
                
    def takeDamage(self,dmg):
        self.action = "hit"
        self.health -= dmg
    
    #display that shield is out of health. never got to implementing this part, though...        
    def shieldBrokenNotify(self):
        if self.shieldBrokenNotify == True:
            self.shieldBrokenNotifyCounter += 1
            textFont(Silom,18)
            if self.x > g.w/2:
                text("Shield Broken!", g.w/2, self.y + self.h/4)
            elif self.x <= g.w/2:
                text("Shield Broken!", self.x + self.w/2, self.y + self.h/4)
            if self.shieldBrokenNotifyCounter//40 > 1:
                self.shieldBrokenNotify = False
    
    def display(self):
        self.update()
    
        #displays hitbox (for verification only)
        stroke(255)
        noFill()
        strokeWeight(3)
        rect(self.hitRangex[0],self.hitRangey[0],(self.hitRangex[-1]-self.hitRangex[0]),(self.hitRangey[-1]-self.hitRangey[0]))
        #print(self.hitRangey[0])
        #print(self.hitRangey[-1])
        if g.type == "boss":
            if self.dir >= 0:
                image(self.img,self.x,self.y,self.w,self.h)
            elif self.dir < 0:
                image(self.img,self.x,self.y,self.w,self.h,928,0,0,640)
        else:
            if self.dir >= 0:
                image(self.img,self.x-g.middlex,self.y,self.w,self.h)
            elif self.dir < 0:
                image(self.img,self.x-g.middlex,self.y,self.w,self.h,928,0,0,640)
            
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

#class Boss, derived from class Player
class Boss(Player):
    def __init__(self,x,y,vx,vy,w,h,f,d,character,fileName,level):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        
        #stats
        self.level = level
        self.maxHealth = self.level*700
        self.health = self.maxHealth
        self.attack = self.level*20
        self.maxMP = self.level*40
        self.mp = self.maxMP
        
        self.Images = asunaImages
        self.imagePath = "Asu"
        self.moveDictPathUp = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990", "hit":"508", "die":"600", "ability":"201"}
        self.moveDictFramesUp = {"still":7, "walk":5, "jump":6, "block":1, "normalATK":3, "knockBack":6, "throw":5, "hit":3, "die":7, "ability":15}
        self.moveDictPathDown = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockBack":"100", "throw":"100", "hit":"507", "die":"600", "ability":"201"}
        self.moveDictFramesDown = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6, "knockBack":1, "throw":1, "hit":3, "die":7, "ability":1}
        
        #image attributes (dictionaries for images and frame count; made to ensure that random commands won't crash game)
        self.character = character    #this will choose between either Asuna or Tatsuya
        self.fileName = fileName      #this is to add the extension name at the start of the string (for calling images)
        self.actionIndex = "000"
        
        #movement dictionaries based on character
        if self.character == "tatsuya":
            self.Images = tatsuyaImages
            self.imagePath = "Oni"
            self.moveDictPathUp = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990", "hit":"508", "die":"600"}
            self.moveDictFramesUp = {"still":7, "walk":5, "jump":6, "block":1, "normalATK":3, "knockBack":6, "throw":5, "hit":3, "die":7}
            self.moveDictPathDown = {"still": "100", "walk":"100", "jump":"110", "block":"501", "normalATK":"103", "knockBack":"100", "throw":"100", "hit":"507", "die":"600"}
            self.moveDictFramesDown = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6, "knockBack":1, "throw":1, "hit":3, "die":7}
        
        elif self.character == "asuna":
            self.Images = asunaImages
            self.imagePath = "Asu"
            self.moveDictPathUp = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990", "hit":"508", "die":"600", "ability":"201"}
            self.moveDictFramesUp = {"still":7, "walk":5, "jump":6, "block":1, "normalATK":3, "knockBack":6, "throw":5, "hit":3, "die":7, "ability":15}
            self.moveDictPathDown = {"still": "100", "walk":"100", "jump":"100", "block":"501", "normalATK":"101", "knockBack":"100", "throw":"100", "hit":"507", "die":"600", "ability":"201"}
            self.moveDictFramesDown = {"still":1, "walk":1, "jump":1, "block":2, "normalATK":6, "knockBack":1, "throw":1, "hit":3, "die":7, "ability":1}
        
        #setup initial dictionaries
        self.movePath = self.moveDictPathUp
        self.moveFrames = self.moveDictFramesUp        
        
        #direction and distances (between player)
        self.dir = d
        self.distance = 800
        
        #hitbox components
        #NOTICE: the y range of the hitbox is based on the location of the ground, so it's referenced later.
        self.x1 = (self.x + self.w/2) - (self.w/8)
        self.x2 = (self.x + self.w/2) + (self.w/8)
        
        #action calling for dictionaries, plus status update
        self.lastAction = "still"
        self.action = "still"
        self.lastStatus = "passive"
        self.status = "passive" #divided into "passive", "attacking", "defending", "retreat"
        self.hitCounter = 0   #makes it so that boss is immobilized for a short period of time
        self.attackCounter = 0    #to keep track of the boss attacks (when it moves away to perform ranged attacks)
        self.moveCounter = 0    #to keep track of movements
        self.walkCounter = 0
        self.actionEnd = True  #keeps track of whether an action has been completed
        self.count = 0
        self.ultraAttackCounter = 0   #each successful hit adds 1 to the counter, and the boss does an ultra attack at 15 hits
        
        #hitbox components
        #NOTICE: the y range of the hitbox is based on the location of the ground. If this changes, then CHANGE THE Y VALUES
        self.x1 = (self.x + self.w/2) - (self.w/8)
        self.x2 = (self.x + self.w/2) + (self.w/8)
        y1 = (self.y + self.h/2) - ((self.h/2)*0.3125)
        y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
        #create hitbox        
        self.hitRangex = range(int(self.x1),int(self.x2))
        self.hitRangey = range(int(y1),int(y2))
        
    def update(self):
        self.distance = abs((self.x + self.w/2) - (g.kirito.x + g.kirito.w/2))
        self.gravity()
        
        self.movePath = self.moveDictPathUp
        self.moveFrames = self.moveDictFramesUp
        
        #if boss dies, then status is updated
        if self.action == "die":
            if self.lastAction != "die":
                self.f = 0
                self.lastAction = self.action
            elif self.action == self.lastAction:
                if self.f <= self.moveFrames[self.action]:
                    self.lastAction = self.action
                else:
                    self.status = "dead"
            
        #if boss is hit, they can't do anything for 1 count (20 co
        if self.action == "hit":
            if self.lastAction != "hit":
                self.f = 0
            self.lastAction = "hit"
            self.hitCounter +=1
            if self.hitCounter > 20:
                self.action = "still"
                self.hitCounter = 0
        else:
            #if attacking, then the entire animation needs to be completed before attempting a new one    
            if self.status == "attacking":
                if self.action != self.lastAction:
                    self.f = 0
                    self.lastAction = self.action
                elif self.action == self.lastAction:
                    if self.f <= self.moveFrames[self.action]:
                        self.lastAction = self.action
                    else:
                        self.action = "still"
                        self.status = "passive"
                        
            #if jumping, the boss goes through the entire frame set            
            if self.action == "jump":
                if self.action != self.lastAction:
                    self.f = 0
                    self.lastAction = self.action
                elif self.action == self.lastAction:
                    if self.gravity() != True:
                        self.lastAction = self.action
                    else:
                        self.action = "still"
                        self.status = "passive"
                    
            #to prevent glitch where boss keeps attacking     
            if self.action == "normalATK":
                if self.f > self.moveFrames[self.action]:
                    self.status = "passive"
                    if self.gravity():
                        self.action = "still"
                    else:
                        self.action = "jump"
               
            #the moves of the boss are decided with an action and a count
            #the boss will perform the action until the counter reaches the designated count
            if self.status != "attacking":
                if self.distance < self.w/3:
                    self.actionEnd = True
                elif self.action != self.lastAction:
                    self.f = 0
                    self.lastAction = self.action
                if self.action == self.lastAction:
                    self.moveCounter += 1
                    self.lastAction = self.action
                    if self.moveCounter//20 > self.count:
                        self.actionEnd = True
                        self.status = "passive"
                        self.action = "still"
            if self.actionEnd:
                self.action = "still"
                
            #based on distances, only activated when boss completes a moveset
            if self.action == "still" or (self.status == "passive" and self.actionEnd):
                
                if self.distance < self.w/3:  #if in hitting distance
                    self.attackCounter += 1
                    if self.attackCounter//20 > 3:
                        n = random.randint(0,1)
                        print(n)
                        if n == 0:   #back away from player
                            self.action = "walk"
                            self.count = 1
                            self.dir = (self.x - g.kirito.x)/abs(self.x - g.kirito.x)
                            if self.moveCounter == 0:
                                self.attackPlayer("melee")
                        elif n == 1:  #attack player
                            self.attackPlayer("melee")
                        
                elif self.distance < self.w/2:   #if further than hitting distance
                    self.attackCounter += 1
                    if self.attackCounter//20 > 3:
                        n = random.randint(0,1)
                        if n == 0:   #walk towards player
                            self.action = "walk"
                            self.dir = -(self.x - g.kirito.x)/abs(self.x - g.kirito.x)
                            self.count = 2
                        elif n == 1:  #attack player
                            self.attackPlayer("mranged")
                        
                else:   #if beyond this distance
                    self.attackCounter += 1
                    if self.attackCounter//20 > 3:
                        n = random.randint(0,1)
                        if n == 0:   #walk towards player
                            self.action = "walk"
                            self.dir = -(self.x - g.kirito.x)
                            self.count = 2
                            if self.x + self.w/2 <= g.kirito.x:
                                self.dir = 1
                            else:
                                self.dir = -1
                        elif n == 1:  #attack player
                            self.attackPlayer("ranged")
        
            #IF WALKING
            if self.action == "walk":
                self.vx = 3*self.dir
                if self.distance > g.w:
                    if self.actionEnd:
                        self.action == "still"
                else:
                    self.actionEnd = True
                        
            self.actionEnd = False
                        
            if self.status == "passive" and self.vx == 0 and self.gravity():
                self.action = "still"
                        
            #fixing directions       
            if (self.x + self.w/2 <= 0 and self.dir == -1):
                self.dir = 1
                self.action = "walk"
                self.count = 5
            elif self.x + self.w/2 > g.w:
                self.dir *= -1
                self.vx = 0
                    
            #stops moving when attacking
            if self.status == ("attacking" or "defending"):
                self.vx = 0
    
            #updates final position of object
            self.x += self.vx
            self.y += self.vy  
            
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
                            
            #reset frames when actions change
            if self.action != self.lastAction:
                self.f = 0
                self.moveCounter = 0
            
        #hitbox update
        y1 = (self.y + self.h/2) - ((self.h/2)*0.3125)
        y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
        if self.x < 0:
            self.x1 = (self.x + self.w) - self.w/2 - self.w/8
            self.x2 = (self.x + self.w) - self.w/2 + self.w/8
        elif self.x >= 0 and (self.x + self.w/2) <= g.w/2:   #if between starting point and middle
            self.x1 = (self.x + self.w/2) - (self.w/8)
            self.x2 = (self.x + self.w/2) + (self.w/8)
        elif self.x + self.w/2 > g.w/2:
            self.x1 = (self.x + self.w/2) - (self.w/8)
            self.x2 = (self.x + self.w/2) + (self.w/8)
        #reach extends when attacking (all g.enemies in range will be hit)
        if self.status == "attacking":
            if self.dir > 0:
                self.x2 += self.w/4
            elif self.dir < 0:
                self.x1 -= self.w/4
        #create hitbox        
        self.hitRangex = range(int(self.x1),int(self.x2))
        self.hitRangey = range(int(y1),int(y2))
        
        #animating boss before hitting the ground  
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
    
        #choosing the speeds of the animations for each action
        if self.status == "attacking":
            self.f += 0.05*self.moveFrames[self.action]
        else:
            self.f += 0.035*self.moveFrames[self.action]
            
        if self.action == "ability":
            self.f -= 0.02*self.moveFrames[self.action]

        #creating an attribute to get the framepoint for the image to be displayed                                        
        self.framePoint = int(round((self.f)%(self.moveFrames[self.action]),0))   
                
        #adds the buffer to get the image name
        if self.framePoint > 9:
            self.buffer = "_"
        else:
            self.buffer = "_0"
        
        #SELECTS IMAGE TO DISPLAY
        self.img = self.Images[self.imagePath + self.movePath[self.action] + self.buffer + str(self.framePoint) + ".png"]
        
        #UPDATES LAST STATUS
        self.lastStatus = self.status
        
        #print(self.f)
        #print(self.framePoint)
        #print(self.moveFrames)
        #print(self.status)
        #print(self.health)
        #print(self.lastStatus)
        #print(self.action)
        #print(self.distance)
        #print(self.lastAction)
        #print(self.vy)
        #print(self.gravity())
        #print(self.dir)
        #for i in range(2):
         #   print(self.hitRangex[i])
         #   print(self.hitRangey[i])

    def attackPlayer(self,type):
        self.dir = -(self.x - g.kirito.x)/abs(self.x - g.kirito.x)
        if type == "melee":
            if self.ultraAttackCounter > 15:
                self.status = "attacking"
                self.action = "ability"
            else:
                n = random.randint(0,4)
                print(n)
                if n == (0 or 1):
                    self.status = "attacking"
                    self.action = "normalATK"
                    print(self.action)
                elif n == (4):
                    self.status = "defending"
                    self.action = "block"
                    self.count = 1
        elif type == "mranged":
            n = random.randint(0,4)
            if n == (0 or 2):
                self.status = "attacking"
                self.action = "throw"
                self.throwObject()
            elif n == 4:
                self.status = "attacking"
                self.action = "knockBack"
                self.knockBackSlash()
            elif n == (1 or 3):
                self.status = "defending"
                self.action = "block"
                self.count = 1
                    
        elif type == "ranged":
            n = random.randint(0,4)
            if n == (0 or 2):
                self.status = "attacking"
                self.action = "throw"
                self.throwObject()
            elif n == (3 or 4):
                self.status = "attacking"
                self.action = "knockBack"
                self.knockBackSlash()
            elif n == (1):
                self.status = "defending"
                self.action = "block"
                self.count = 1
                        
    #throwing weapon        
    def throwObject(self):
        if self.action == "throw" and self.status == "attacking":
            if self.lastAction != "throw":    #(x,y,vx,vy,w,h,f,d,type,dmg)
                g.flyingObjects.append(Projectile((self.x + self.w/2),(self.y + self.h/2),self.dir*6,0,0,0,0,self.dir,"knockBack",self.attack, "enemy"))
                    
    #knockBack slash
    def knockBackSlash(self):
        if self.action == "knockBack" and self.status == "attacking":
            if self.lastAction != "knockBack":
                g.flyingObjects.append(Projectile((self.x + self.w/2),(self.y + self.h/2 + self.h/4),self.dir,0,0,0,0,self.dir,"knockBack",self.attack, "enemy"))

                
    def takeDamage(self,dmg):
        self.action = "hit"
        self.health -= dmg
        

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

#class Enemy, derived from class Entity
class Enemy(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d,health,a,type):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        #type of enemy; "melee" and "ranged"
        self.type = type
        
        #movement dictionaries for enemies
        
        self.moveDictPathMelee = {"still": "000", "walk":"400", "jump":"200", "block":"500", "normalATK":"001", "knockBack":"003", "throw":"990", "hit":"508"}
        self.moveDictFramesMelee = {"still":7, "walk":5, "normalATK":3, "hit":3}
        #uses Quen images
        self.moveDictPathRanged = {"still": "000", "attack":"301", "hit":"508"}
        self.moveDictFramesRanged = {"still":1, "attack":3, "hit":3}
        
        #stats (stages will have multipliers on these stats)
        self.health = health   #defined later in stages as 100*g.difficulty*stagenumber.multiplier + stage.levelAddition
        self.maxhealth = health
        self.attack = a   #defined later in stages as 50*g.difficulty*stagenumber.multiplier + stage.levelAddition
        
        #Enemy hitbox
        self.hitRangex = range(int((self.x + self.w) - (self.w/8)),(int(self.x + self.w)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h) - ((self.h/2)*0.3125)),int((self.y + self.h) + ((self.h/2)*1.231)))

    def display(self):
        self.update()
        #Diplaying the enemy
        rect(self.x - g.middlex, self.y, self.w, self.h) #x,y,w,h
        
        #Enemy health bar
        noStroke()
        if self.health > (self.maxhealth//2): #50% health or more
            fill(0, 255, 0)
        elif self.health < (self.maxhealth//4): #25% Health or less
            fill(255, 0, 0)
        else:
            fill(255, 200, 0) #25% - 50% health
        self.newHealth = (float(self.health) / self.maxhealth) * self.w #Percentage of max health
        
        #Health Bar Display
        rect(self.x - g.middlex, self.y - 10, self.newHealth, 5) #Displays above enemy postion
        print(g.kirito.x + 200, self.x, self.y - 10)
        stroke(192)
        noFill()
        rect(self.x - g.middlex, self.y - 10, self.w, 5) #x,y,w,h, subtract middle x to keep above when Kirito in middle!

    def attackPlayer(self):
        if self.type == "melee":
            print(self.x, g.kirito.x, self.x - g.kirito.x, self.w//3)
            if (self.x > g.kirito.x) and (self.x - (g.kirito.x + 200) < self.w//3):
                print("TRUE")
                self.action = "attack"
                if self.lastAction != "attack":
                    g.kirito.takeDamage(self.attack)
            
    def update(self):
        self.gravity()
        if self.x > g.kirito.x + 200:
            self.dir = -1
            
        elif self.x < g.kirito.x + 200:
            self.dir = 1
        self.attackPlayer()
        
        #Speed
        if self.dir == -1:
            self.vx = -2
        elif self.dir == 1:
            self.vx = 2
            
        if g.kirito.x > g.middlex:
            self.x1 -= g.kirito.vx
            self.x2 -= g.kirito.vx
        
        #update position                
        self.x += self.vx
        self.y += self.vy
            
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-        

#class Projectile, derived from class Entity; this is the projectile throw by player
#2 types: "knife", "knockBack", and "bullet", which are used to differentiate images and projectile speeds
#format: Projectile((g.kirito.x + g.kirito.w/2),(g.kirito.y + g.kirito.h//2),g.kirito.dir*8,0,0,g.kirito.d,"knife",g.kirito.attack)
class Projectile(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d,type,dmg,character):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        self.dir = d
        self.type = type
        self.count = 1
        self.damage = dmg
        self.origin = character
        
    def update(self):
        #accelerates with time
        self.count +=1
        self.x += (self.vx + 1.5*self.count)*self.dir
        
        if g.kirito.x > g.middlex:
            self.x -= g.kirito.vx
        
    def display(self):
        self.update()
        stroke(255)
        fill(255,0,0)
        rect(self.x,self.y,10,10)
            

#create class KnockBackBlast, derived from class Entity; this is knockBack effect for both player and boss

#

###################################################################################################################################################################################################
###################################################################################################################################################################################################
#STAGES
'''
#create class Stage; all stages will stem from this (uses player (will need to be constant throughout game; g.kirito),enemies,etc)
class Stage:
    def __init__(self,w,h,g,level,middlex):
        self.w = w
        self.h = h
        self.g = g
        self.middlex = 0
        self.frames = 0
        self.backgr = []
        
        self.projectileTimer = 0
        self.flyingObjects = []
        
        self.level = level
        self.healthDrop = 10*(self.level/2)
        self.enemies = []
        
    def update():
        pass
        
        
        
class BossRoom(Stage):
    def __init__ (self,w,h,g,level,middlex):
        Stage.__init__(self,w,h,g,level,middlex)
        self.middlex = middlex
        self.frames = 0
        self.backgr = []
        
        self.projectileTimer = 0
        self.flyingObjects = []
        
        self.enemies = [Boss(500,0,0,0,432,345,0,-1,"asuna","Asu",2)]
        
    def update(self):
        #if kirito attacks, if his last action is different, then he deals damage (prevents him from putting out 4k+ damage with one swing)
        #this also applies to the enemies vs Kirito
        for i in self.enemies:
            for num in i.hitRangex:
                if num in self.kirito.hitRangex:
                    if self.kirito.y - i.y <= 0:
                        if i.status == "attacking" and i.lastStatus != "attacking":
                            self.kirito.takeDamage(i.attack)
                        elif self.kirito.status == "attacking" and self.kirito.lastStatus != "attacking":
                            i.takeDamage(self.kirito.attack)
        
        #a flying object is removed and deals damage if it hits a moving object (player or enemy)
        for fly in self.flyingObjects:
            for i in self.enemies:
                if fly.origin != "enemy":
                    if fly.x in i.hitRangex:
                        if fly.y in i.hitRangey:
                            i.takeDamage(fly.damage)
            if fly.origin != "player":                
                if fly.x in self.kirito.hitRangex:
                    if fly.y in self.kirito.hitRangey:
                        self.kirito.takeDamage(fly.damage)
                    
        #every 3 counts, a flyingObject is removed from the map
        if len(self.flyingObjects) > 0:
            self.projectileTimer += 1
            #print(self.projectileTimer)
            if self.projectileTimer//20 >= 3:
                del self.flyingObjects[0]
                self.projectileTimer = 0
    
'''
    

#create class StageTwo(Stage)

#create class StageThree(Stage)

###################################################################################################################################################################################################
###################################################################################################################################################################################################

#GAME

#create class Game (self,g,h,w,kirito = Player(arg))
class Game:
    def __init__(self,w,h,g,type):
        self.w = w
        self.h = h
        self.g = g
        self.middlex = 0
        self.frames = 0
        self.backgr = backgrounds[1]
        self.projectileTimer = 0
        self.kirito = Player(0,0,0,0,500,345,0,1) #x,y,vx,vy,w,h,f,d
        self.kirito.y = self.g - (self.kirito.h)
        self.flyingObjects = []      #keep track of airborne objects (knives, bullets, knockBack, etc.)
        self.state = "game"
        self.level = 1
        self.type = "boss"
        
        self.enemies = [Boss(500,0,0,0,432,345,0,-1,"asuna","Asu",2)]   #x,y,vx,vy,w,h,f,d,character,fileName,level
        self.enemies[0].y = self.g - (self.enemies[0].h)
            
            
    def update(self):
        self.gameOverCheck()
        print(self.state)
            
        if self.kirito.x + self.kirito.w/2 > self.w:
            self.kirito.vx = 0
            self.action = "still"
            
        if self.enemies[0].x + self.enemies[0].w/2 > self.w:
            self.enemies[0].vx = 0
            self.action = "still"
            
        
        #if kirito attacks, if his last action is different, then he deals damage (prevents him from putting out 4k+ damage with one swing)
        #this also applies to the enemies vs Kirito
        for i in self.enemies:
            if abs(i.x-self.kirito.x) < i.w/2:
                if i.action == "normalATK" and i.lastAction != "normalATK":
                    print("worked but nothing else")
                    if (i.x < self.kirito.x and i.dir > 0) or (i.x > self.kirito.x and i.dir < 0):
                        self.kirito.takeDamage(i.attack/10)
                elif self.kirito.action == "normalATK" and self.kirito.lastAction != "normalATK":
                    if (self.kirito.x < i.x and self.kirito.dir > 0) or (self.kirito.x > i.x and self.kirito.dir < 0):
                        i.takeDamage(self.kirito.attack*10)
        
        
#a flying object is removed and deals damage if it hits a moving object (player or enemy)
        for fly in self.flyingObjects:
            for i in self.enemies:
                if fly.origin != "enemy":
                    if fly.x in i.hitRangex:
                        if fly.y in i.hitRangey:
                            i.takeDamage(fly.damage/20)
            if fly.origin != "player":                
                if fly.x in self.kirito.hitRangex:
                    if fly.y in self.kirito.hitRangey:
                        self.kirito.takeDamage(fly.damage/20)
                        
        for i in self.enemies:
            if i.health <= 0:
                i.action = "die"
                if i.status == "dead":
                    self.enemies.remove(i)
                    
        if len(self.enemies) == 0:
            self.state = "complete"
            
                                                        
        #every 3 counts, a flyingObject is removed from the map
        if len(self.flyingObjects) > 0:
            self.projectileTimer += 1
            #print(self.projectileTimer)
            if self.projectileTimer//20 >= 3:
                del self.flyingObjects[0]
                self.projectileTimer = 0
        
    
    def display(self):
        self.update()
        count = 0
        for i in range(4):
            img = self.backgr[i]
            image(img, 0, 0, self.w, self.h)
        self.frames +=1
        cnt = 4
        
        for img in self.backgr:
            #print(self.middlex, cnt, self.w)
            x = (self.middlex//cnt) % self.w #always 0, self.x is 0 until mario reaches the middle of screen
            #Remainder always resets x after it passes the 'width' --> 1280%1280 = 0, 1281%1280 = 1 ...
            #img5 has the highest x! -> 
            
            #print(self.middlex, x, self.w-x+1, self.w-x)
            #image(img, x, y, width, height, x1, y1, x2, y2) //// (x1, y1) -> upper left, (x2, y2) -> lower right
            image (img,0,0,self.w-x+1,self.h,x-1,0,self.w,self.h)
            image (img,self.w-x,0,x,self.h,0,0,x,self.h)
            cnt -= 1
           
        #display flyingObjects     
        for fly in self.flyingObjects:
            fly.display()  
        
        #display enemies
        for i in self.enemies:
            i.display()
        
        #display player    
        self.kirito.display()
        
        #Displaying Player Stats
        #Health bar
        noStroke()
        if self.kirito.health > 50:
            fill(0, 255, 0)
        elif self.kirito.health < 25:
            fill(255, 0, 0)
        else:
            fill(255, 200, 0)
        self.newHealth = (float(self.kirito.health) / self.kirito.maxHealth) * 200 #Percentage of max health
        #Health Bar Outline
        rect(50, 50, self.newHealth, 15)
        stroke(192)
        noFill()
        rect(50, 50, 200, 15) #x,y,w,h
        
        noStroke()
        fill(0,0,255)
        self.newMP = (float(self.kirito.mp) / self.kirito.maxMP) * 200 #Percentage of max health
        #MP Bar Outline
        rect(50, 75, self.newMP, 15)
        stroke(192)
        noFill()
        rect(50, 75, 200, 15) #x,y,w,h
        
        noStroke()
        fill(173,216,255)
        self.newXP = (float(self.kirito.experience)%self.kirito.maxXP / self.kirito.maxXP) * 300 #Percentage of max health
        #MP Bar Outline
        rect(50, 30, self.newXP, 10, 3)
        stroke(192)
        noFill()
        rect(50, 30, 300, 10, 3) #x,y,w,h
        
        
        #Game over
        

    def gameOverCheck(self):
        if self.kirito.health <= 0:
            self.state = "gameover"
        elif len(self.enemies) == 0:
            self.state = "complete"
        
            
    def reset(self):
        self.kirito.health = 100



#def update(self):
    #this whole area will take care of all stages and levels in them. self.stageCount will determine the stage (background and enemies)
    #and self.levelCount will determine the level (level 3, enter boss room)
    
    #if player's health reaches 0, self.playerDeath == True
    
#def gameOver(self):
    #display "You Died" in red. display restart menu
    #if restart is clicked:
        #g.gameReset == True

###################################################################################################################################################################################################
###################################################################################################################################################################################################

#SETUP AND DRAW
g = Game(1080,720,640,"boss")


def setup():
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
    #Game state to run the game
    if g.state == "game":
        g.display()
    #Gameover state to check for gameover
    elif g.state == "gameover":
        fill(255, 0, 0)
        textSize(60)
        textAlign(CENTER, TOP)
        text("YOU DIED", g.w/2, 350)
        textSize(30)
        
        if 460 < mouseX < 610 and 420 < mouseY < 460:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Continue?", g.w/2, 450)
    elif g.state == "complete":
        fill(255, 0, 0)
        textSize(60)
        textAlign(CENTER, TOP)
        text("You Win!", g.w/2, 350)
        textSize(30)
        
        if 460 < mouseX < 610 and 420 < mouseY < 460:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Restart?", g.w/2, 450)
        
        
###################################################################################################################################################################################################
###################################################################################################################################################################################################

#KEYBOARD CONTROL AND RESET

def keyPressed():
    if keyCode == 83:     #down(S)
        if g.kirito.y + g.kirito.h == g.g and g.kirito.status != "defending":
            g.kirito.direction["down"] = True
            
    elif keyCode == 32:
        if g.kirito.shieldBroken == False:
            g.kirito.vx = 0
            g.kirito.status = "defending"
            g.kirito.action = "block"
        else:
            g.kirito.shieldBrokenNotify = True
                        
    elif keyCode == 76:    # (L)
        if g.kirito.status != "defending":
            g.kirito.status = "attacking"
            g.kirito.action = "normalATK"
            
    elif keyCode == 74:    # (J)
        #this skill takes 10 mp. If the player doesn't have enough, the game notifies the player saying that there's "No MP!"
        if g.kirito.status != "defending" and g.kirito.direction["down"] == False:
            if g.kirito.mp - 10 > 0:
                g.kirito.status = "attacking"
                g.kirito.action = "knockBack"
                g.kirito.mp -= 10
            else:
                g.kirito.mpLackingNotify = True
                        
    elif keyCode == 75:    #(K)
        #this skill takes 5 mp. If the player doesn't have enough, the game notifies the player saying that there's "No MP!"
        if g.kirito.status != "defending" and g.kirito.direction["down"] == False:
            if g.kirito.mp - 5 > 0:
                g.kirito.status = "attacking"
                g.kirito.action = "throw"
                g.kirito.mp -=5
            else:
                g.kirito.mpLackingNotify = True
        
    elif keyCode == 87:    #up(W)
        if (not g.kirito.direction["down"]) and g.kirito.status != "defending":
            g.kirito.direction["up"] = True
        
    elif keyCode == 65:    #left(A)
        if g.kirito.status != "defending":
            g.kirito.direction["left"] = True
    
    elif keyCode == 68:     #right(D)
        if g.kirito.status != "defending":
            g.kirito.direction["right"] = True

        
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
        if g.kirito.shieldBroken == False:
            g.kirito.action = "still"
            g.kirito.status = "passive"

def mouseClicked():
    g.kirito.takeDamage(10)
    g.enemies[0].takeDamage(10)
