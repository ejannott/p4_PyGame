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
from pygame.sprite import *
import random
import time

pygame.init()
pygame.mixer.init()

#Define Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (50,205,50)
BLUE = (0,0,255)
LIGHTBLUE = (30,144,255)


# --- Classes

class Player(pygame.sprite.Sprite):
	### Class that represents the player ###
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('spriteImages/rocket.png').convert()
		self.image = pygame.transform.scale(self.image, (60,60))
		self.image = pygame.transform.rotate(self.image, 270)
		self.transColor = self.image.get_at((0,0))
		self.image.set_colorkey(self.transColor)
		self.rect = self.image.get_rect()

		# IDK what this line does
		screen = pygame.display.get_surface()

		self.area = screen.get_rect()
		self.speed = 10
		self.state = 'still'
		self.reinit()

	def reinit(self):
		### Updates the player's location ###
		self.state = 'still'
		self.movepos = [0,0]

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	def moveup(self):
		self.movepos[1] = self.movepos[1] - (self.speed)
		self.state = 'moveup'

	def movedown(self):
		self.movepos[1] = self.movepos[1] + (self.speed)
		self.state = 'movedown'

	def moveleft(self):
		self.movepos[0] = self.movepos[0] - (self.speed)
		self.state = 'moveleft'

	def moveright(self):
		self.movepos[0] = self.movepos[0] + (self.speed)
		self.state = 'movedown'

class Laser(pygame.sprite.Sprite):
	### This class represents the laser shots ###
	def __init__(self):
		# call the parent class (sprite) constructor
		super().__init__()

		self.image = pygame.image.load('spriteImages/bullet.bmp').convert()
		self.image = pygame.transform.scale(self.image, (40,10))
		self.transColor = self.image.get_at((0,0))
		self.image.set_colorkey(self.transColor)
		self.rect = self.image.get_rect()

	def update(self):
		### Move the laser ###
		self.rect.x += 15

# class Enemy(pygame.sprite.Sprite):
# 	### This class represents the enemys that come on screen ###

# 	def __init__ (self):
# 		### Constructor, creates the image of the enemy ###
# 		super


screenWidth = 1100
screenHeight = 572

#Set up the game screen
screen = pygame.display.set_mode((screenWidth,screenHeight))  #(double parentheses to let py know we are passing a tuple as a parameter)
pygame.display.set_caption('Defend the city!') #here is the TITLE of the window/game title
clock = pygame.time.Clock() #this is the 'gameclock' - this is imposed on everything in the game

backGround1 = pygame.image.load('skylineBG.bmp')
backGround2 = pygame.image.load('skylineBG.bmp')
backGround1_x = 0
backGround2_x = backGround1.get_width()

laserSound = pygame.mixer.Sound("sounds/laserSound.wav")

player1 = Player()

#List of all the Sprites
all_sprites = pygame.sprite.Group(player1)

#List of all of the Enemies
enemy_list = pygame.sprite.Group()

#List of all of the laser shots
laser_list = pygame.sprite.Group()

score = 0



# - - - - - - - Main Program - - - - - - - #

running = True #when you start the game, you havent crashed yet
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			running = False

		if event.type == pygame.KEYDOWN:
			### Player Movement
			if event.key == pygame.K_UP:
				player1.moveup()
			if event.key == pygame.K_DOWN:
				player1.movedown()
			if event.key == pygame.K_LEFT:
				player1.moveleft()
			if event.key == pygame.K_RIGHT:
				player1.moveright()
			### Player Shoots
			if event.key == pygame.K_SPACE:
				laser = Laser()
				laser.rect.x = player1.rect.x
				laser.rect.y = player1.rect.y + 25
				#Add the laser to the lists
				all_sprites.add(laser)
				laserSound.play()
				laser_list.add(laser)


		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				player1.movepos[1] = 0
				player1.state = 'still'
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				player1.movepos[0] = 0
				player1.state = 'still'

	for laser in laser_list:
		#check to see if it's hit an enemy
		enemy_hit_list = pygame.sprite.spritecollide(laser, enemy_list, True)

		#For each hit, remove the enemy and add to the score
		for enemy in enemy_hit_list:
			laser_list.remove(laser)
			all_sprites.remove(laser)
			score += 1
			print(score)

		#Remove laser is if flies off the screen
		if laser.rect.y < -10:
			laser_list.remove(laser)
			all_sprites.remove(laser)


	#Have the background repeat itself 
	screen.fill(BLACK)
	screen.blit(backGround1, (backGround1_x,40))
	screen.blit(backGround2, (backGround2_x,40))

	if backGround2_x <= -backGround2.get_width() + 7:
		backGround2_x = backGround2.get_width()
	if backGround1_x <= -backGround1.get_width() + 7:
		backGround1_x = backGround1.get_width()
	backGround1_x -= 10
	backGround2_x -= 10

	all_sprites.update()
	all_sprites.draw(screen)

	pygame.display.update()

	#define frames per second
	clock.tick(60) #the number is the frames per second - RUNS THROUGH THE LOOP THIS QUICKLY

#uninitiate pygame
pygame.display.quit()
pygame.quit()
quit()
