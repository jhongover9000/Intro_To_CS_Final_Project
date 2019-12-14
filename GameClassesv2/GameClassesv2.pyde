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
kiritoImagesSingle = {}
for file in kiritoSingle:
        kiritoImagesSingle[file] = loadImage(path + "/images/Kirito/single/" + str(file))
print(kiritoImagesSingle.keys())

kiritoDual = []
for file in os.listdir(path + "/images/Kirito/dual/"):
  kiritoDual.append(file)
kiritoDual.sort()
kiritoImagesDual = {}
for file in kiritoDual:
        kiritoImagesDual[file] = loadImage(path + "/images/Kirito/dual/" + str(file))

#melee enemy images ############################################################################
enemySingle = []
for file in os.listdir(path + "/images/Melee/"):
    enemySingle.append(file)
enemySingle.sort()
enemyImagesSingle = {}
for file in enemySingle:
        enemyImagesSingle[file] = loadImage(path + "/images/Melee/" + str(file))
print(enemyImagesSingle.keys())
#################################################################################################

#background images are divided into lists of moving parts and a background, which are used to create the stages
backgrounds = {}
for k in range(4):
    backgroundSets = []
    for file in os.listdir(path + "/images/Background/" + "0" + str(k)):
        backgroundSets.append(loadImage(path + "/images/Background/" + "0" + str(k) + "/" + file))
    backgrounds[k] = backgroundSets


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
        
        if self.dir > 0:
            image(self.img,self.x-g.middlex, self.y-self.h//2,self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-g.middlex,self.y-self.h//2,self.w,self.h)

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
        
#create class Player, derived from class Entity
class Player(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        
        #stats
        self.level = 1
        self.maxHealth = 100
        self.health = self.maxHealth
        self.attack = 25
        self.maxMP = 20
        self.mp = self.maxMP
        self.maxXP = 100
        self.a = 0
        self.shieldHealth = 100
        self.experience = 0
        
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
        self.timer = 0
        self.lastLevel = 1
        
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
            self.throwObject()
            if self.lastAction != self.action:
                self.f = 0
            if self.f >= self.moveFrames[self.action]:
                
                #Dealing Damage!
                for e in g.enemies:
                    if self.action == "throw":
                        e.health -= self.attack
                    if abs((e.x + e.w/1.9 - g.middlex) - (self.x - g.middlex + 250)) < e.w//4:
                        if self.action == "knockBack":
                            e.health -= self.attack * 2
                        else:
                            e.health -= self.attack
                            if self.mp != self.maxMP:
                                self.mp += 5
                    
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
            if self.lastAction == ("walk" or "jump"):
                self.action = "still"
        #velocity is 0 when object ducks
        if self.direction["down"]:
            self.vx = 0
        #velocity is 0 when player is attacking or defending    
        if self.status == ("attacking" or "defending"):
            self.vx = 0
         
        #keep player from moving off screen   
        if self.x + self.w/2 <= 0 and self.dir == -1:
            self.vx = 0
            
        #updates final position of object
        self.x += self.vx
        self.y += self.vy
        
        #moves game screen along
        if (self.x + self.w/2) >= g.w // 2:
            g.middlex += self.vx
        
        #hitbox components
        x1 = (self.x + self.w/2) - (self.w/8)
        x2 = (self.x%g.w + self.w/2)+(self.w/8)
        y1 = (self.y + self.h/2) - ((self.h/2)*0.3125) #3125 brings hitbox down to Kirito's head
        y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
        
        if self.x >= 0 and (self.x + self.w/2) < g.w/2:   #if between starting point and middle
            x1 = (self.x + self.w/2) - (self.w/8)
            x2 = (self.x%g.w + self.w/2) + (self.w/8)
            y1 = (self.y + self.h/2) - ((self.h/2)*0.3125)
            y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
        elif (self.x + self.w/2) >= g.w/2:     #if self.x + self.w/2 goes beyond midpoint
            x1 = (g.w/2) - (self.w/8)
            x2 = (g.w/2) + (self.w/8)
            y1 = (self.y + self.h/2) - ((self.h/2)*0.3125)
            y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
        if self.direction["down"]:
            y1 = self.y + (self.h/2*1.125)
            y2 = (self.y + self.h/2) + ((self.h/2)*0.8125)
            
        #reach extends when attacking (all g.enemies in range will be hit)
        if self.status == "attacking":
            if self.dir > 0:
                x2 += self.w/4
            elif self.dir < 0:
                x1 -= self.w/4
                
        self.hitRangex = range(int(x1),int(x2))
        self.hitRangey = range(int(y1),int(y2))
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
        
        #update stats
        self.maxHealth = 100 + 20*(self.level-1)
        self.maxMP = 20 + 10*(self.level-1)
        self.maxXP = 100
        self.attack = 25 + 10*(self.level-1)
        
        if self.level != self.lastLevel:
            self.timer += 1
            fill(0,255,0)
            textSize(40)
            text("Level Up!", g.w/2.5, 300)
            if self.timer//60 > 2:
                self.lastLevel = self.level
                self.timer = 0
        
        #All Checks!
        #print(self.f)
        #print(self.framePoint)
        #print(self.status)
        ##print(self.action)
        #print(self.lastAction)
        #print(self.vy)
        #print(self.dir)
        #for i in range(2):
            #print(self.hitRangex[i])
            #print(self.hitRangey[i])
            
    def display(self):
        self.update()
    
        #displays hitbox (for verification only)
        stroke(255)
        noFill()
        strokeWeight(3)
        #rect(self.hitRangex[0],self.hitRangey[0],(self.hitRangex[-1]-self.hitRangex[0]),(self.hitRangey[-1]-self.hitRangey[0])) #x,y,w,h (HITBOX DISPLAY)
    
        if self.dir >= 0:
            image(self.img,self.x-g.middlex,self.y,self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-g.middlex,self.y,self.w,self.h,928,0,0,640)
            
    #throwing weapon, if spell is used     
    def throwObject(self):
        if self.action == "throw" and self.status == "attacking":
            if self.lastAction != "throw":    #(x,y,vx,vy,w,h,f,d,type,dmg)
                g.flyingObjects.append(Projectile((self.x + self.w/2),(self.y + self.h/2),self.dir*6,0,0,0,0,self.dir,"knockBack",self.attack, "player"))

#create class Enemy, derived from class Entity
class Enemy(Entity):
    def __init__(self,x,y,vx,vy,w,h,f,d,health,a,type,index):
        Entity.__init__(self,x,y,vx,vy,w,h,f,d)
        #type of enemy; "melee" and "ranged"
        self.type = type
        
        #stats (stages will have multipliers on these stats)
        self.health = health   #defined later in stages as 100*g.difficulty*stagenumber.multiplier + stage.levelAddition
        self.maxhealth = health
        self.attack = a   #defined later in stages as 50*g.difficulty*stagenumber.multiplier + stage.levelAddition
        self.index = index #This tells us what index the enemy is in the "enemies" List
        
        #image attributes (dictionaries for images and frame count; made to ensure that random commands won't crash game)
        self.enemyImages = enemyImagesSingle
        self.actionIndex = "000"
        #single blade
        self.movePath = {"still": "000", "walk":"400", "attack":"320", "hit":"508", "dead":"600"}
        self.moveFrames = {"still":7, "walk":5, "attack":9, "hit":3, "dead":7}

        self.dir = d
        self.buffer = "_0"
        
        #action calling for dictionaries, plus status update
        self.lastAction = "still"
        self.action = "still"
        self.status = "passive" #divided into "passive", "attacking", "defending". passive = knockback, attack = only lose health, or "dead" if dead
        self.deathcount = 0 #for displaying a single sequence of death frames
    ###################################################################################################################################################################

    def display(self):
        self.update()
        
     #DISPLAY HITBOX######################
        #displays hitbox (for verification only)
        stroke(255, 0, 0)
        noFill()
        strokeWeight(3)
        #rect(self.x + self.w/2.4 - g.middlex, self.y + self.h/7, (self.hitRangex[-1]-self.hitRangex[0]), (self.hitRangey[-1]-self.hitRangey[0])) #x,y,w,h
        #Hitbox attributes
        #X -- self.x + self.w/2.4 - g.middlex
        #Y -- self.y + self.h/7                      #Positioned to match the feet of enemy
        #Width -- (self.hitRangex[-1]-self.hitRangex[0])
        #Height -- (self.hitRangey[-1]-self.hitRangey[0])
    ##############################################################################################################################   

        if self.dir >= 0:
            image(self.img,self.x-g.middlex,self.y,self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-g.middlex,self.y,self.w,self.h,928,0,0,640) #img,x,y,w,h,x1,y1,x2,y2
        
        #Enemy health bar
        noStroke()
        if self.health > (self.maxhealth//2): #50% health or more
            fill(0, 255, 0)
        elif self.health < (self.maxhealth//4): #25% Health or less
            fill(255, 0, 0)
        else:
            fill(255, 200, 0) #25% - 50% health
        self.newHealth = (float(self.health) / self.maxhealth) * (self.hitRangex[-1]-self.hitRangex[0]) #Percentage of max health, * width
        
        #Health Bar Display
        rect(self.x + self.w/2.4 - g.middlex, self.y + self.h/7 - 10, self.newHealth, 5) #Displays above enemy postion
        stroke(192)
        noFill()
        rect(self.x + self.w/2.4 - g.middlex, self.y + self.h/7 - 10, (self.hitRangex[-1]-self.hitRangex[0]), 5) #x,y,w,h, subtract middle x to keep above when enemy in middle!
            
    def update(self):
        self.gravity()
        
        #Changing direction
        #rect(self.x + self.w/1.9 - g.middlex, self.y, 2, 100) #Markers for verification
        #rect(g.kirito.x - g.middlex + 250, g.kirito.y, 2, 100)
        
        if self.x + self.w/1.9 - g.middlex > g.kirito.x - g.middlex + 250:
            self.dir = -1
            
        elif self.x + self.w/1.9 - g.middlex < g.kirito.x - g.middlex + 250:
            self.dir = 1
        
        #Speed
        if self.dir == -1:
            self.vx = -2
        elif self.dir == 1:
            self.vx = 2
                
    #reset frames when actions change
        if self.action != self.lastAction:
            self.f = 0
            
        #Attacking Player
        self.attackPlayer() #Outside of if statement!
            
    #Adding walking based on direction
        if self.dir == -1:
            if self.status == "passive":
                self.vx = -2
                if self.y + self.h == g.g:
                    self.action = "walk"
                    
        elif self.dir == 1:
            if self.status == "passive":
                self.vx = 2
                if self.y + self.h == g.g:
                    self.action = "walk"
        
        #Movement
        self.x += self.vx
        self.y += self.vy
                    
        #changing status from attacking to passive and changing frames
        
        if self.status == "attacking":
            print("ATTACKING", self.lastAction, self.action)
            if self.lastAction != self.action:
                self.f = 0
            if self.f >= self.moveFrames[self.action]:
                g.kirito.health -= self.attack
                print("RESET ACTION")
                
                self.status = "passive"
                if self.gravity():
                    self.action = "still"
    #Checking if enemy is dead
        if self.health <= 0:
            self.action = "dead"
            self.healthChance = random.randint(1,2) #Randomly gain health when killing an enemy
            if self.healthChance == 1:
                if g.kirito.health != g.kirito.maxHealth:
                    g.kirito.health += 20 
            g.kirito.experience += 25 #Adding experience for killing an enemy
            if g.kirito.experience == 100:
                g.kirito.level += 1
           
            self.vx = 0

        self.hitRangex = range(int((self.x + self.w) - (self.w/8)),(int(self.x + self.w)+(self.w/8)))
        self.hitRangey = range(int((self.y + self.h) - ((self.h/2)*0.3125)),int((self.y + self.h) + ((self.h/2)*1.231)))
        #print(self.hitRangex, self.hitRangey)
        print("STATUS", self.status, self.action, self.lastAction)
        
    #choosing the speeds of the animations for each action        
        self.f += 0.028*self.moveFrames[self.action]
        
    #creating an attribute to get the framepoint for the image to be displayed                                        
        self.framePoint = int(round((self.f)%(self.moveFrames[self.action]),0))   

        self.buffer = "_0"
        
        #Different display if the enemy is dead
        if self.action != "dead":
            #print(self.action)
            self.img = self.enemyImages["Hiw" + self.movePath[self.action] + self.buffer + str(self.framePoint) + ".png"]
        else: #Enemy is dead
            if self.deathcount < 8:
                self.img = self.enemyImages["Hiw" + self.movePath[self.action] + self.buffer + str(self.framePoint) + ".png"]
                self.deathcount += 1
                self.status = "dead"
        
        #final tweaks
        self.lastAction = self.action

    ##ATTACK############
    def attackPlayer(self):
        if self.type == "melee":
            if self.action != "dead": #Makes sure Enemy can't attack while dead
                #Check if kirito is near enemy
                if abs((self.x + self.w/1.9 - g.middlex) - (g.kirito.x - g.middlex + 250)) < self.w//4: #self.w//4 determines how close the enemy comes to kirito!
                    print("LEFT TRUE", self.action, self.lastAction)
                    self.vx = 0
                    self.action = "attack"
                    self.status = "attacking"
                else:
                    self.status = "passive" #Means that enemy will keep walking if not within range

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
        self.backgr = backgrounds[1]
        self.kirito = Player(0,0,0,0,500,345,0,1) #x,y,vx,vy,w,h,f,d
        self.kirito.y = self.g - (self.kirito.h) + 100
        self.projectileTimer = 0
        self.flyingObjects = []      #keep track of airborne objects (knives, bullets, knockBack, etc.)
        self.enemies = []
        self.stageCount = 1
        
        #Changed to Main Menu on default
        self.state = "mainmenu"
  
    def makeStage(self, d, stage = 1):
        self.difficulty = d
        self.stageCount = stage
        #Difficulty
        if self.difficulty == "normal":
            self.attack = 5
        elif self.difficulty == "hard":
            self.attack = 10
        elif self.difficulty == "nightmare":
            self.attack = 20
            
        #Adding STAGE 1#############################
        if self.stageCount == 1:
            for i in range(3): #0, 1, 2
                self.enemy = Enemy(900 + (200*i),self.g,0,0,400,320,30,-1,100,self.attack,"melee", i) #x,y,vx,vy,w,h,f,d,health,a,type, adds enemies 100 apart
                self.enemy.y = self.g - (self.enemy.h) #Keeps enemy above ground, same height as kirito
                self.enemies.append(self.enemy)
      
        #Adding STAGE 2##################################
        if self.stageCount == 2:
            g.kirito.x = 0
            self.backgr = backgrounds[2]
            for i in range(5): #0, 1, 2, 3, 4
                self.enemy = Enemy(900 + (200*i),self.g,0,0,400,320,30,-1,100,self.attack * 2,"melee", i) #x,y,vx,vy,w,h,f,d,health,a,type, adds enemies 100 apart
                self.enemy.y = self.g - (self.enemy.h) #Keeps enemy above ground, same height as kirito
                self.enemies.append(self.enemy)
          
        #Adding STAGE 3################################### 
        if self.stageCount == 3:
            g.kirito.x = 0
            self.backgr = backgrounds[3]
            for i in range(7): #0, 1, 2, 3, 4
                self.enemy = Enemy(900 + (200*i),self.g,0,0,400,320,30,-1,100,self.attack * 3,"melee", i) #x,y,vx,vy,w,h,f,d,health,a,type, adds enemies 100 apart
                self.enemy.y = self.g - (self.enemy.h) #Keeps enemy above ground, same height as kirito
                self.enemies.append(self.enemy)
            
    def display(self):
        for i in range(4):
            img = self.backgr[i]
            image(img, 0, 0, self.w, self.h)
        self.frames +=1
        cnt = 4
        
   #Changing the backgrounds
        for img in self.backgr:
            x = (self.middlex//cnt) % self.w #always 0, self.x is 0 until mario reaches the middle of screen
            image (img,0,0,self.w-x+1,self.h,x-1,0,self.w,self.h) #displayed first, loads right half of mario image, shorter width    
            #UL: (0,0), LR: (x, self.h)
            image (img,self.w-x,0,x,self.h,0,0,x,self.h) #loads the left half of mario image, shorter width
            cnt -= 1
        
    #Displaying Enemies########################################################
        for e in self.enemies:
            e.display()
        self.kirito.display()
        
        #a flying object is removed and deals damage if it hits a moving object (player or enemy)
        for fly in self.flyingObjects:
            for i in self.enemies:
                if fly.origin != "enemy":
                    if fly.x in i.hitRangex:
                        if fly.y in i.hitRangey:
                            i.health -= fly.damage
        
        #Dead enemy check
        for e in self.enemies:
            if e.status == "dead":
                self.enemies.remove(e)
                print("REMOVED")
        
        #Increasing the stage if all enemies are dead
        if len(self.enemies) == 0:
            if self.stageCount != 4:
                self.stageCount += 1
                self.makeStage(self.difficulty, self.stageCount)
            if self.stageCount == 4:
                fill(0, 255, 0)
                textSize(80)
                text("YOU WIN", 330, 150)
                self.backgr = backgrounds[0]
            
    ################################################################################
        
        #Displaying Player Stats
        #Stats Titles
        #Experience
        fill(173,216,255)
        textSize(20)
        text("XP", 15, 40)
        #Health
        fill(0, 255, 0)
        textSize(20)
        text("HP", 15, 60)
        #Mana
        fill(0, 0, 255)
        textSize(20)
        text("MP", 15, 85)
        
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
        #XP Bar Outline
        rect(50, 30, self.newXP, 10, 3)
        stroke(192)
        noFill()
        rect(50, 30, 300, 10, 3) #x,y,w,h
        
        #Stage Count
        fill(255,255,255)
        textSize(30)
        text("Stage Count: " + str(self.stageCount), 600, 50)
        
        #Levels
        fill(255,255,255)
        textSize(30)
        text("Level: " + str(self.kirito.level), 900, 50)
        
        #Bottom Buffer
        fill(0,0,0)
        rect(0, 630, 1080, 500)
        fill(255,255,255)
        textSize(30)
        text("( J )-Strong atk, 5MP               (K)-Spell, 10MP              (L)-Attack, 0MP", 10, 660)
        
        #Game over
        self.gameOverCheck()

    def gameOverCheck(self):
        if self.kirito.health <= 0:
            self.state = "gameover"
            
    def reset(self):
        self.kirito.health = 100
        g.state = "game"

###################################################################################################################################################################################################
#SETUP AND DRAW
g = Game(1080,720,640)


def setup():
    size(g.w,g.h)
    background(0)
        
def draw():
    background(0)
    
    #MAIN MENU ##############################################
    if g.state == "mainmenu":
        #Title
        fill(255, 255, 255)
        textSize(80)
        text("THE GAME", 330, 150)
        textSize(35)
        
        #New Game
        if 100 < mouseX < 350 and 320 < mouseY < 360:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Start New Game", 100, 350)
        
        #Instructions
        if 100 < mouseX < 300 and 370 < mouseY < 410:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Instructions", 100, 400)
        
        #Quit
        if 100 < mouseX < 180 and 420 < mouseY < 460:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Quit", 100, 450)
    ###########################################################
     
     #Difficulty selection screen
    elif g.state == "difficulty":
        #Title
        fill(255, 255, 255)
        textSize(40)
        text("Difficulty Selection", 330, 150)
        textSize(35)
        #Normal
        if 100 < mouseX < 350 and 320 < mouseY < 360:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Normal", 100, 350)
        
        #Hard
        if 100 < mouseX < 300 and 370 < mouseY < 410:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Hard", 100, 400)
        
        #Nightmare
        if 100 < mouseX < 250 and 420 < mouseY < 460:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Nightmare", 100, 450)
        
    elif g.state == "instructions":
        fill(255, 255, 255)
        textSize(15)
        text("This is a simple hack-and-slash game. You can move around using the WASD keys", 100, 200)
        text("and attack using the JKL keys.\nEnemies can randomly drop health, and also give you experience, which increases your stats.", 100, 300)
        text("Rank up as much as you can, and get through the stages of increasing difficulties!", 100, 400)
        text("Click to go back...", 200, 600)
        
    #Game state to run the game
    elif g.state == "game":
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
        text("Respawn?", 460, 450)
        
        if 460 < mouseX < 610 and 470 < mouseY < 510:
            fill(255,0,0)
        else:
            fill(255, 255, 255)
        text("Quit?", 460, 500)
        
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
            if g.kirito.mp > 0:
                g.kirito.status = "attacking"
                g.kirito.action = "knockBack"
                g.kirito.mp -= 5
        
    elif keyCode == 75:    #(K) Mana attack
        if g.kirito.status != "defending" and g.kirito.direction["down"] == False:
            if g.kirito.mp > 0:
                g.kirito.status = "attacking"
                g.kirito.action = "throw"
                g.kirito.mp -= 10
        
    elif keyCode == 32: #spacebar
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
    
    elif keyCode == 32: #spacebar
        g.kirito.action = "still"
        g.kirito.status = "passive"

#######################################
def mouseClicked():
    if mouseButton == LEFT:
        
        #Main Menu
        if g.state == "mainmenu":
            #New Game
            if 100 < mouseX < 350 and 320 < mouseY < 360:
                g.state = "difficulty"
                
            #Instructions
            if 100 < mouseX < 300 and 370 < mouseY < 410:
                g.state = "instructions" 
                
            #Quit
            if 100 < mouseX < 180 and 420 < mouseY < 460:
                exit()
        
        #Difficulty Selection
        elif g.state == "difficulty":
            print("STATE DIFFICULTY")
            #Normal
            if 100 < mouseX < 350 and 320 < mouseY < 360:
                g.state = "game"
                g.makeStage("normal", g.stageCount)
                
            #Hard
            if 100 < mouseX < 300 and 370 < mouseY < 410:
                g.state = "game"
                g.makeStage("hard")
                
            #Nightmare
            if 100 < mouseX < 250 and 420 < mouseY < 460:
                g.state = "game"
                g.makeStage("nightmare")
        
        elif g.state == "instructions":
            g.state = "mainmenu"
        
        #TESTING ON CLICKS
        elif g.state == "game":
            for e in g.enemies:
                if e.health != 0:
                    e.health -= 10
                
        #Game Over
        elif g.state == "gameover":
            if 460 < mouseX < 610 and 420 < mouseY < 460:
                g.reset()
            if 460 < mouseX < 610 and 470 < mouseY < 510:
                exit()
###########################################
