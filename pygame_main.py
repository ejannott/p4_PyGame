#Ethan Jannott
#ejannott
#22235024
#
#PERSONAL TO-DO:
#	- Get rid of explanation comments - save my final version as a different copy without those.
#	- FIGURE OUT SCROLLING WALLPAPER - the repeat
#	- 
#
##References:
## 
## 
## 
## 

import sys
import pygame
import pygame.mixer
from pygame.locals import *
pygame.init()
pygame.mixer.init()

#set up Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (50,205,50)
BLUE = (0,0,255)
LIGHTBLUE = (30,144,255)

screenWidth = 1100
screenHeight = 572

#Set up the game screen
screen = pygame.display.set_mode((screenWidth,screenHeight))  #(double parentheses to let py know we are passing a tuple as a parameter)
pygame.display.set_caption('Dogfight') #here is the TITLE of the window/game title
clock = pygame.time.Clock() #this is the 'gameclock' - this is imposed on everything in the game


backGround1 = pygame.image.load('skylineBG.bmp')
backGround2 = pygame.image.load('skylineBG.bmp')
backGround1_x = 0
backGround2_x = backGround1.get_width()

initialSound = pygame.mixer.Sound("sounds/bubbles.wav")
initialSound.play()


#set up the player
playerImg = pygame.image.load('spriteImages/playerShip.bmp')
playerImg = pygame.transform.scale(playerImg, (75,75))
playerImg = pygame.transform.rotate(playerImg, 270)

def player(x,y):
	screen.blit(playerImg,(x,y))

player_x = 50
player_y = (screenHeight * 0.5)
player_x_change = 0
player_y_change = 0


running = True #when you start the game, you havent crashed yet

#where the game is actaully running - in this loop:
while running:
	for event in pygame.event.get():  #pygame.event.get() tracks any event that happens - clicks, keys pressed, etc. per frame per second
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player_x_change = -10
			elif event.key == pygame.K_RIGHT:
				player_x_change = 10
			elif event.key == pygame.K_UP:
				player_y_change = -10
			elif event.key == pygame.K_DOWN:
				player_y_change = 10
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				player_x_change = 0
			elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				player_y_change = 0
	player_x += player_x_change
	player_y += player_y_change


	#Have the background repeat itself 
	screen.fill(BLACK)
	screen.blit(backGround1, (backGround1_x,40))
	screen.blit(backGround2, (backGround2_x,40))
	if backGround2_x <= 10:
		backGround1_x = int(backGround1.get_width())
	elif backGround1_x <= -backGround1.get_width():
		backGround1_x = backGround1.get_width()
	backGround1_x -= 10
	backGround2_x -= 10


	player(player_x,player_y)

	pygame.display.update()

	#define frames per second
	clock.tick(60) #the number is the frames per second - RUNS THROUGH THE LOOP THIS QUICKLY

#uninitiate pygame
pygame.display.quit()
pygame.quit()
quit()