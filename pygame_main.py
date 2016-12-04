#Ethan Jannott
#ejannott
#22235024
#
#
# . . . S T I L L
#                A 
#                  W O R K
#                         I N
#                            P R O G R E S S . . .

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


fontName = pygame.font.match_font('arial')
def draw_text(surface, text, size, x, y):
	font = pygame.font.Font(fontName, size)
	text_surface = font.render(text, True, GREEN) #True means that the font is aliased
	text_rect = text_surface.get_rect()
	text_rect = righttop = (x,y)
	surface.blit(text_surface, text_rect)

def draw_health_bar(surface, x, y, percent):
	if percent < 0:
		percent = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	fill = (percent/100) * BAR_LENGTH
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill_rect)
	pygame.draw.rect(surface, WHITE, outline_rect, 2)


# --- Classes

class Player(pygame.sprite.Sprite):
	### Class that represents the player ###
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('spriteImages/playerShip.bmp').convert()
		self.image = pygame.transform.scale(self.image, (80,80))
		self.image = pygame.transform.rotate(self.image, 270)
		self.transColor = self.image.get_at((0,0))
		self.image.set_colorkey(self.transColor)
		self.rect = self.image.get_rect()
		self.radius = 33

		self.health = 100

		# IDK what this line does
		screen = pygame.display.get_surface()

		self.area = screen.get_rect()
		self.speed = 12
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
		self.rect.x += 25



class Enemy(pygame.sprite.Sprite):
	### This class represents the enemys that come on screen ###
	def __init__ (self):
		### Constructor, creates the image of the enemy ###
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('spriteImages/blueAlien.png').convert()
		self.image = pygame.transform.scale(self.image, (55,65))
		self.transColor = self.image.get_at((0,0))
		self.image.set_colorkey(self.transColor)
		self.rect = self.image.get_rect()
		self.radius = 23

		self.rect.y = random.randrange(0, screenHeight - self.rect.height)
		self.rect.x = random.randrange(1140,1200)
		self.speedx = random.randrange(5,15)

	def update(self):
		self.rect.x -= self.speedx
		if self.rect.right < 0:
			self.rect.y = random.randrange(0, screenWidth - self.rect.height)
			self.rect.x = random.randrange(1100,1140)
			self.speedx = random.randrange(5,15)



class Explosion(pygame.sprite.Sprite):
	def __init__ (self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_animation[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_animation[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_animation[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


screenWidth = 1100
screenHeight = 550

#Set up the game screen
screen = pygame.display.set_mode((screenWidth,screenHeight))  #(double parentheses to let py know we are passing a tuple as a parameter)
pygame.display.set_caption('Defend the city!') #here is the TITLE of the window/game title
clock = pygame.time.Clock() #this is the 'gameclock' - this is imposed on everything in the game

backGround1 = pygame.image.load('skylineBG.bmp')
backGround2 = pygame.image.load('skylineBG.bmp')
backDrop1 = pygame.image.load('starsky.bmp')
backDrop2 = pygame.image.load('starsky.bmp')

backGround1_x = 0
backGround2_x = backGround1.get_width()
backDrop1_x = 0
backDrop2_x = backDrop1.get_width()

pygame.mixer.music.load("sounds/battleMusic.wav")
pygame.mixer.music.play(-1,0.0)
laserSound = pygame.mixer.Sound("sounds/laserSound.wav")
explosionSound = pygame.mixer.Sound("sounds/explosion.wav")


player = Player()

explosion_animation = {}
explosion_animation['large'] = []
explosion_animation['small'] = [] #dictionary - name instead of a number
for i in range(9):
	filename = 'spriteImages/regularExplosion0{}.png'.format(i)
	img = pygame.image.load(filename).convert()
	img.set_colorkey(BLACK)#####
	img_large = pygame.transform.scale(img,(75,75))
	explosion_animation['large'].append(img_large)




#List of all the Sprites
all_sprites = pygame.sprite.Group(player)
#List of all of the Enemies
enemy_list = pygame.sprite.Group()
#List of all of the laser shots
laser_list = pygame.sprite.Group()

for i in range(10):
	enemy = Enemy()
	all_sprites.add(enemy)
	enemy_list.add(enemy)

score = 0



# - - - - - - - Main Program - - - - - - - #

running = True #when you start the game, you havent crashed yet
while running:

	playerhealth = 100


	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			running = False

		if event.type == pygame.KEYDOWN:
			### Player Movement
			if event.key == pygame.K_UP:
				player.moveup()
			if event.key == pygame.K_DOWN:
				player.movedown()
			if event.key == pygame.K_LEFT:
				player.moveleft()
			if event.key == pygame.K_RIGHT:
				player.moveright()
			### Player Shoots
			if event.key == pygame.K_SPACE:
				laser = Laser()
				laser.rect.x = player.rect.x
				laser.rect.y = player.rect.y + 35
				#Add the laser to the lists
				all_sprites.add(laser)
				laserSound.play()
				laser_list.add(laser)


		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				player.movepos[1] = 0
				player.state = 'still'
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				player.movepos[0] = 0
				player.state = 'still'

	for laser in laser_list:
		#check to see if it's hit an enemy
		enemy_hit_list = pygame.sprite.spritecollide(laser, enemy_list, True)

		#For each hit, remove the enemy and add to the score
		for enemy in enemy_hit_list:
			laser_list.remove(laser)
			all_sprites.remove(laser)
			score += 1
			explosionSound.play()
			expl = Explosion(enemy.rect.center, 'large')
			all_sprites.add(expl)

			newEnemy = Enemy()
			levelupEnemy = Enemy()
			all_sprites.add(newEnemy)
			enemy_list.add(newEnemy)
			if score % 7 == 0:
				all_sprites.add(levelupEnemy)
				enemy_list.add(levelupEnemy)

		#Remove laser is if flies off the screen
		if laser.rect.x > screenWidth + 40:
			laser_list.remove(laser)
			all_sprites.remove(laser)
			all_sprites.update()

	
	#Have the background repeat itself 
	screen.fill(BLACK)
	screen.blit(backDrop1, (backDrop1_x,0))
	screen.blit(backDrop2, (backDrop2_x,0))
	screen.blit(backGround1, (backGround1_x,60))
	screen.blit(backGround2, (backGround2_x,60))

	if backDrop2_x <= -backDrop2.get_width():
		backDrop2_x = backDrop2.get_width()
	if backDrop1_x <= -backDrop1.get_width():
		backDrop1_x = backDrop1.get_width()
	backDrop1_x -= 5
	backDrop2_x -= 5

	if backGround2_x <= -backGround2.get_width() + 7:
		backGround2_x = backGround2.get_width()
	if backGround1_x <= -backGround1.get_width() + 7:
		backGround1_x = backGround1.get_width()
	backGround1_x -= 10
	backGround2_x -= 10

	all_sprites.update()
	playerHits = pygame.sprite.spritecollide(player, enemy_list, True, pygame.sprite.collide_circle)
	for hit in playerHits:
		player.health -= 25
		explosionSound.play()
		expl = Explosion(hit.rect.center, 'large')
		all_sprites.add(expl)
		newEnemy = Enemy()
		all_sprites.add(newEnemy)
		enemy_list.add(newEnemy)

		if player.health <= 0:
			running = False

	draw_text(screen, str(score), 24, 10, 20)
	draw_health_bar(screen, 40, 20, player.health)

	all_sprites.draw(screen)

	pygame.display.update()

	#define frames per second
	clock.tick(60) #the number is the frames per second - RUNS THROUGH THE LOOP THIS QUICKLY

#uninitiate pygame
pygame.display.quit()
pygame.quit()
quit()
