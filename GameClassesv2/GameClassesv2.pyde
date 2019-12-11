import os
import random
path = os.getcwd()

###################################################################################################################################################################################################
###################################################################################################################################################################################################

#IMAGES: all loaded at the beginning to reduce memory usage

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



#asuna images

#enemy images


#projectile images
projectileImages = []


#background images are divided into lists of moving parts and a background, which are used to create the stages
backgroundSets = []
for i in range(5):
    pass

#


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
        self.d = d
        
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
        self.x1 = (self.x + self.w/2) - (self.w/8)
        self.x2 = (self.x + self.w/2) + (self.w/8)
        self.y1 = (self.y + self.h/2) - ((self.h/2)*0.3125)
        self.y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
        
        #action calling for dictionaries, plus status update
        self.lastAction = "still"
        self.action = "still"
        self.lastStatus = "passive"
        self.status = "passive" #divided into "passive", "attacking", "defending". passive = knockBack, attack = only lose health
        self.hitCounter = 0
        
    def update(self):
        self.gravity()
        self.throwObject()
        self.knockBackSlash()
        
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
            if self.lastAction != "hit":
                self.f = 0
            self.lastAction = "hit"
            self.hitCounter +=1
            if self.hitCounter > 20:
                self.action = "still"
                self.hitCounter = 0
                                
        #if the player presses random buttons while down (the ones that don't have any effects) they stay "passive"
        if (self.action != ("still" or "normalATK" or "block" or "hit")) and self.direction["down"]:
            self.status = "passive"
        #if attacking, then the entire animation needs to be completed before attempting a new one    
        if self.status == "attacking":
            if self.lastAction != "still":
                if self.framePoint < self.moveFrames[self.action]:
                    self.action = self.lastAction
                               
        #reset frames when actions change
        if self.action != self.lastAction:
            self.f = 0
            
        #basically, you can't do anything when hit.    
        if self.action != "hit":
            #changing status from attacking to passive and changing frames
            if self.status == "attacking":
                if self.lastAction != self.action:
                    self.f = 0
                elif self.f >= self.moveFrames[self.action]:
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
            #player unblocks after block (animation)                                
            if self.lastAction == "block":
                if self.action == "block":
                    self.status = "defending"
                    self.f = 0
                elif self.action != "block":
                    self.action = "block"
                    self.lastAction = "still"                    
                                
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
        
        #moves game screen along
        if (self.x + self.w/2) > g.w//2:
            g.middlex += self.vx
        elif (self.x + self.w/2) == g.w//2:
            g.middlex = 0
        

        if self.x < 0:
            self.x1 = (self.x + self.w) - self.w/2 - self.w/8
            self.x2 = (self.x + self.w) - self.w/2 + self.w/8
        elif self.x >= 0 and (self.x + self.w/2) <= g.w/2:   #if between starting point and middle
            self.x1 = (self.x + self.w/2) - (self.w/8)
            self.x2 = (self.x%g.w + self.w/2) + (self.w/8)
        elif (self.x + self.w/2) > g.w/2:     #if self.x + self.w/2 goes beyond midpoint
            self.x1 = (g.w/2) - (self.w/8)
            self.x2 = (g.w/2) + (self.w/8)
        if self.direction["down"]:
            self.y1 = self.y + (self.h/2*1.125)
            self.y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)   
        #reach extends when attacking (all g.enemies in range will be hit)
        if self.status == "attacking":
            if self.dir > 0:
                self.x2 += self.w/4
            elif self.dir < 0:
                self.x1 -= self.w/4
        #create hitbox        
        self.hitRangex = range(int(self.x1),int(self.x2))
        self.hitRangey = range(int(self.y1),int(self.y2))
        #choosing the speeds of the animations for each action
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
        

        self.img = self.kiritoImages["Krt" + self.movePath[self.action] + self.buffer + str(self.framePoint) + ".png"]
        #final tweaks
        self.lastAction = self.action

        
        #update stats
        self.maxHealth = 100 + 10*(self.level-1)
        self.maxMP = 20 + 10*(self.level-1)
        self.maxXP = 100*1.3**(self.level-1)
        
        #print(self.f)
        #print(self.framePoint)
        #print(self.moveFrames)
        #print(self.status)
        print(self.action)
        #print(self.lastAction)
        #print(self.vy)
        #print(self.gravity())
        #print(self.dir)
        #for i in range(2):
            #print(self.hitRangex[i])
            #print(self.hitRangey[i])
    
    #throwing knife        
    def throwObject(self):
        if self.action == "throw":
            if self.lastAction != "throw":    #(x,y,vx,vy,w,h,f,d,type,dmg)
                g.flyingObjects.append(Projectile((g.kirito.x + g.kirito.w/2),(g.kirito.y + g.kirito.h/2 - 10),g.kirito.dir*6,0,0,0,0,g.kirito.d,"knife",self.attack))
    #knockBack slash
    def knockBackSlash(self):
        if self.action == "knockBack":
            print("knock")
            if self.lastAction != "knockBack":
                g.flyingObjects.append(Projectile((g.kirito.x + g.kirito.w/2),(g.kirito.y + g.kirito.h/2 - 10),g.kirito.dir*6,0,0,0,0,g.kirito.d,"knockBack",self.attack))
                
    def takeDamage(self,dmg):
        self.action = "hit"
        self.health -= dmg
    
    def display(self):
        self.update()
    
        #displays hitbox (for verification only)
        stroke(255)
        noFill()
        strokeWeight(3)
        rect(self.hitRangex[0],self.hitRangey[0],(self.hitRangex[-1]-self.hitRangex[0]),(self.hitRangey[-1]-self.hitRangey[0]))
        print(self.hitRangex[0])

        if self.dir >= 0:
            image(self.img,self.x-g.middlex,self.y,self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-g.middlex,self.y,self.w,self.h,928,0,0,640)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

#class Boss, derived from class Player

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

#class Enemy, derived from class Entity
class Enemy(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d,health,a,type):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        
        #type of enemy; "melee" and "ranged"
        self.type = type
        
        #movement dictionaries for enemies
        
        self.moveDictPathMelee = {"still": "000", "walk":"400", "attack":"001", "hit":"508"}
        self.moveDictFramesMelee = {"still":7, "walk":5, "attack":3, "hit":3}
        #uses Quen images
        self.moveDictPathRanged = {"still": "000", "attack":"301", "hit":"508"}
        self.moveDictFramesRanged = {"still":1, "attack":3, "hit":3}
        
        #stats (stages will have multipliers on these stats)
        self.health = health   #defined later in stages as 100*g.difficulty*stagenumber.multiplier + stage.levelAddition
        self.attack = a   #defined later in stages as 10*g.difficulty*stagenumber.multiplier + stage.levelAddition
        
        #hitbox
        if self.x <= 720:
            self.hitRangex = range(int((self.x + self.w) - (self.w/8)),(int(self.x + self.w)+(self.w/8)))
            self.hitRangey = range(int((self.y + self.h) - ((self.h/2)*0.3125)),int((self.y + self.h) + ((self.h/2)*1.231)))
        
        
    def attackPlayer(self):
        if self.type == "melee":
            if (self.x > g.kirito.x) and (self.x - g.kirito.x < self.w//3):
                self.action = "attack"
            
    def update(self):
        if self.x > g.kirito.x:
            self.dir = -1
            self.vx = -3
        elif self.x < g.kirito.x:
            self.dir = 1
            self.vx = 3
        elif self.x == g.kirito.x:
            self.attackPlayer()
            
        #if hit, the enemies can't do anything, either    
        if self.action != "hit":    
            self.attackPlayer()
                
            if self.vx != 0:
                self.action = "walk"
        
            
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-        

#class Projectile, derived from class Entity; this is the projectile throw by player
#2 types: "knife", "knockBack", and "bullet", which are used to differentiate images and projectile speeds
#format: Projectile((g.kirito.x + g.kirito.w/2),(g.kirito.y + g.kirito.h//2),g.kirito.dir*8,0,0,g.kirito.d,"knife",g.kirito.attack)
class Projectile(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d,type,dmg):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        self.type = type
        self.count = 1
        self.damage = dmg
        
    def update(self):
        #accelerates with time
        self.count +=1
        self.x += self.vx + 1.5*self.count
        
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

#create class Stage; all stages will stem from this (uses player (will need to be constant throughout game; g.kirito),enemies,etc)

#create class StageOne(Stage)

#create class StageTwo(Stage)

#create class StageThree(Stage)

###################################################################################################################################################################################################
###################################################################################################################################################################################################

#GAME

#create class Game (self,g,h,w,kirito = Player(arg))
class Game:
    def __init__(self,w,h,g):
        self.w = w
        self.h = h
        self.g = g
        self.middlex = 0
        self.frames = 0
        self.backgr = ["","",""]
        self.projectileTimer = 0
        self.kirito = Player(0,0,0,0,500,345,0,1) #x,y,vx,vy,w,h,f,d
        self.kirito.y = self.g - (self.kirito.h)
        self.enemies = []    #keep track of enemies
        self.flyingObjects = []      #keep track of airborne objects
        self.state = "game"
        
        #Loading Background Images from /images/background
        for i in (range(3)): #[0, 1, 2]
            self.backgr[i] = loadImage(path + "/images/Background/0" + str(i) + ".png")
            
            
    def update(self):
        #if kirito attacks, if his last action is different, then he deals damage (prevents him from putting out 4k+ damage with one swing)
        #this also applies to the enemies vs Kirito
        for i in self.enemies:
            for num in i.hitRangex:
                if num in self.kirito.hitRangex:
                    for i in i.hitRangey:
                        if num in self.kirito.hitRangex:
                            if i.lastAction != "attack":
                                g.kirito.takeDamage(i.attack)
        
        #a flying object is removed and deals damage if it hits a moving object (player or enemy)
        for fly in self.flyingObjects:
            for i in self.enemies:
                if fly.x in i.hitRangex:
                    if self.y in i.hitRangey:
                        i.takeDamage(fly.damage)
            if fly.x in g.kirito.hitRangex:
                if fly in g.kirito.hitRangey:
                    g.kirito.takeDamage(fly.damage)
                                                        
        #every 5-10 counts, a flyingObject is removed from the map
        if len(self.flyingObjects) > 0:
            self.projectileTimer += 1
            if self.projectileTimer//20 >= 5:
                del self.flyingObjects[0]
                self.projectileTimer = 0
        
    
    def display(self):
        self.update()
        
        for img in self.backgr:
            image(img, 0, 0, self.w, self.h)
        self.frames +=1
        cnt = 3
        
        #display background
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
        self.gameOverCheck()

    def gameOverCheck(self):
        if self.kirito.health == 0:
            self.state = "gameover"
            
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

#def gameComplete(self):
    #

###################################################################################################################################################################################################
###################################################################################################################################################################################################

#SETUP AND DRAW
g = Game(1080,720,640)


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
        textSize(80)
        text("YOU DIED", 350, 350)
        textSize(30)
        
        if 460 < mouseX < 610 and 420 < mouseY < 460:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Continue?", 460, 450)
        
###################################################################################################################################################################################################
###################################################################################################################################################################################################

#KEYBOARD CONTROL AND RESET

def keyPressed():
    if keyCode == 83:     #down(S)
        if g.kirito.y + g.kirito.h == g.g and g.kirito.status != "defending":
            g.kirito.direction["down"] = True
            
    elif keyCode == 32:
        g.kirito.vx = 0
        g.kirito.status = "defending"
        g.kirito.action = "block"
        
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

def mouseClicked():
    g.kirito.takeDamage(10)

#if g.gameReset == True:
    #g = Game()
