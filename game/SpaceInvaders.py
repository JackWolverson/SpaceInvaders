import sys
import pygame
import Invader
import Missile
from pygame.locals import *

class SpaceInvaders:

    # Constructor of the basic game class.
    # This constructor calls initialize and main_loop method.
    def __init__(self):
        self.initialize()
        self.main_loop()

    # Initialization method. Allows the game to initialize different
    # parameters and load assets before the game runs
    def initialize(self):
        pygame.init()
        pygame.key.set_repeat(1, 1)

        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.caption = "Space Invader!!"
        pygame.display.set_caption(self.caption)
                
        self.framerate = 30

        self.clock = pygame.time.Clock()
                
        self.gameState = 1

        self.font = pygame.font.Font('space_invaders.ttf',40)# loads the font that all text will be in 

##        self.score = 0 #this is where the score was originally 

        self.initializeGameVariables()
        
    def initializeGameVariables(self): #load all the images for the sprites of the game and sets values for the initial loading of the game
        self.starfieldImg = pygame.image.load('Starfield1024x768.png')# loads the images 
        self.invaderImg = pygame.image.load('inv1.png')
        self.altInvaderImg = pygame.image.load('inv12.png')
        self.rocketLauncherImg = pygame.image.load('LaserBase.png')        
        self.missileImg = pygame.image.load('bullet.png')

        self.rocketXPos = 512 # sets the initial rocket x position

        self.alienDirection = -1      # initial alien direction      
        self.alienSpeed = 16  # aline speed

        self.ticks = 0

        self.score = 0 # this is where the score was moved to 

        self.invaders = [] #makes the invader list
        yPos = 50
        for h in range(5):
            xPos = 400
            self.invaders.append([]) 
            for i in range(11):
                invader = Invader.Invader()
                invader.setPosX(xPos) # sets the x position of all 55 invaders 
                invader.setPosY(yPos) # sets the y position 
                self.invaders[h].append(invader)            
                xPos += 40
            yPos  += 40

        self.missileFired = None

        
    # main loop method keeps the game running. This method continuously
    # calls the update and draw methods to keep the game alive.
    def main_loop(self):
        self.clock = pygame.time.Clock()
        while True:
            gametime = self.clock.get_time()
            self.update(gametime)
            self.draw(gametime)
            self.clock.tick(self.framerate)
            

    def updateStarted(self, gametime): # update the start screen 
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: # looks for the input of th 's' key
                    self.gameState = 2      # then moves the game to the next game state 
                    break 


    def updatePlaying(self, gametime): # update the playing screen (while the game is running) 
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT: # quits the game if the event told to
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # looks for the arrow key inputs then moves thee player in the direction respectively
                if event.key == pygame.K_RIGHT:
                    self.rocketXPos = self.rocketXPos + 4
                elif event.key == pygame.K_LEFT:
                    self.rocketXPos = self.rocketXPos - 4
                elif event.key == pygame.K_SPACE: #looks for the space key to be pressed then fires the missile if so 
##                    self.missileFired = Missile.Missile(self.rocketXPos, 650) #old line where the missile shot from the left of the rocket
                    self.missileFired = Missile.Missile((self.rocketXPos + (self.rocketLauncherImg.get_width()//2)), 650)# so the missile shoots more central
                

        isInvaderRemaining = False
        for h in range(5):
            for i in range(11):
                if self.invaders[h][i] != None:
                    isInvaderRemaining = True
                    break
                
        if isInvaderRemaining == False: # moves the game to the end screen if all invaders are gone 
            self.gameState = 3
            return
        
        if self.missileFired != None: # moves the missile vertically if it has been fired 
            self.missileFired.move()
        
        if self.rocketXPos < 100:
            self.rocketXPos = 100

        if self.rocketXPos > 924:
            self.rocketXPos = 924

        self.ticks = self.ticks + gametime

        if self.ticks > 500:
            for h in range(5):
                for i in range(11):
                    if self.invaders[h][i] != None:
                        self.invaders[h][i].moveHorizontal(self.alienSpeed * self.alienDirection) # moves the alien by the amount of pixels equal to
                                                                                                  # the product of the direction and the speed of the 
            leftMostInvader = None                                                                # invader
            rightMostInvader = None

            for h in range(5):
                for i in range(11):
                    if self.invaders[h][i] != None:
                        leftMostInvader = self.invaders[h][i]
                        break
                
            for h in range(5):
                for i in range(10, -1, -1):
                    if self.invaders[h][i] != None:
                        rightMostInvader = self.invaders[h][i]
                        break

            if leftMostInvader.getPosX() < 96: # if the psiton of the left most invader is less than 96 switch directon
                self.alienDirection = +1

                for h in range(5):
                    xPos = 96
                    for i in range(11):
                        if self.invaders[h][i] != None: #sets the invaders to move down the screen when it hits the side
                            self.invaders[h][i].moveVertical(8)
##                            self.invaders[h][i].setPosX(xPos)
                            if self.invaders[h][i].getPosY() >= 650:#ends the game when the alien is at the same level as the player 
                                self.gameState = 3
                        xPos = xPos + self.invaderImg.get_width()
                        xPos = xPos + 30
                        
            if rightMostInvader.getPosX() > 924 :
                self.alienDirection = -1

                for h in range(5):
                    xPos = 924 - self.invaderImg.get_width() * 10 
                    for i in range(11):
                        if self.invaders[h][i] != None: #sets the invaders to move down the screen when it hits the other side
                            self.invaders[h][i].moveVertical(8)
##                            self.invaders[h][i].setPosX(xPos)
                            if self.invaders[h][i].getPosY() >= 650:#ends the game when the alien is at the same level as the player
                                self.gameState = 3
                        xPos = xPos + self.invaderImg.get_width()
                        xPos = xPos + 30
            self.ticks = 0
        
        for h in range(5):                  #goes through all the invaders creating a rectangle around them also creates a rectangle around the rocket 
                for i in range(11):         # then sees if the two collide if yes then ends the game 
                    if self.invaders[h][i] != None:
                        rectInvader = pygame.Rect(self.invaders[h][i].getPosX(), self.invaders[h][i].getPosY(), self.invaderImg.get_width(), self.invaderImg.get_height())
                        rectRocket = pygame.Rect(self.rocketXPos, 650, self.rocketLauncherImg.get_width(), self.rocketLauncherImg.get_height())
                        if rectInvader.colliderect(rectRocket):
                            self.gameState = 3


                    
        if self.missileFired != None: # creates the rectangle around the missile
            rectMissile = pygame.Rect(self.missileFired.getPosX(), self.missileFired.getPosY(), self.missileImg.get_width(), self.missileImg.get_height())
            for h in range(5):
                for i in range(11):
                    if self.invaders[h][i] != None: # creates the rectangle around the invader 
                        rectInvader = pygame.Rect(self.invaders[h][i].getPosX(), self.invaders[h][i].getPosY(), self.invaderImg.get_width(), self.invaderImg.get_height())
                        if rectMissile.colliderect(rectInvader): # do the two rectangle share a co ordinate
                            self.missileFired = None             # if yes then delete the missile 
                            self.invaders[h][i] = None
                            self.score += 100 
                            break

    def updateEnded(self, gametime): #update the end screen
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_x:  #if the x key is pressed quti the game 
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r: # if r is pressed then restart
                    self.initializeGameVariables()
                    self.gameState = 1 
        
        
    # Update method contains game update logic, such as updating the game
    # variables, checking for collisions, gathering input, and
    # playing audio.
    def update(self, gametime):        
        if self.gameState == 1:
            self.updateStarted(gametime)
        elif self.gameState == 2:
            self.updatePlaying(gametime)
        elif self.gameState == 3:
            self.updateEnded(gametime)


    def drawStarted(self, gametime):# draws the start screen with the text on 
        self.screen.blit(self.starfieldImg, (0,0))
        width, height = self.font.size("S P A C E I N V A D E R S!")
        text = self.font.render("S P A C E I N V A D E R S!", True, (255, 0,0))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 200))
        width, height = self.font.size("P R E S S 'S' T O S T A R T")
        text = self.font.render("P R E S S 'S' T O S T A R T", True,(255, 0, 0))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 400))

        pygame.display.flip()


    def drawPlaying(self, gametime):# draws the game 
        self.screen.blit(self.starfieldImg, (0,0)) # draws the background 
        self.screen.blit(self.rocketLauncherImg, (self.rocketXPos, 650)) # draws the players rocket
        text = self.font.render("Score: %d" %(self.score), True, (102, 255, 0))# draws the score text
        xPos = 0
        yPos = 0
        self.screen.blit(text, (xPos, yPos)) # places the score text at the pre determined x and y postition
        if self.missileFired != None:
            self.screen.blit(self.missileImg, (self.missileFired.getPosX(), self.missileFired.getPosY() - self.missileImg.get_height()))# draws the missile
        for h in range(5):
            for i in range(11):
                if self.invaders[h][i] != None:
                    self.screen.blit(self.invaderImg, self.invaders[h][i].getPosition())# draws the invaders 
        pygame.display.flip()    
        
    # Draw method, draws the current state of the game on the screen                        
    def draw(self, gametime):              
        if self.gameState == 1:
            self.drawStarted(gametime)
        elif self.gameState == 2:
            self.drawPlaying(gametime)
        elif self.gameState == 3:
            self.drawEnded(gametime)        

    def drawEnded(self, gametime): #draws the end screen 
        self.screen.blit(self.starfieldImg, (0,0))
        width, height = self.font.size("P R E S S 'R' T O R E S T A R T G A M E")
        text = self.font.render("P R E S S 'R' T O R E S T A R T G A M E", True, (255, 0, 0))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 200))

        width, height = self.font.size("P R E S S 'X' T O E X I T G A M E")
        text = self.font.render("P R E S S 'X' T O E X I T G A M E", True, (255, 0, 0))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 300))
        pygame.display.flip()


if __name__ == "__main__":
    game = SpaceInvaders()
