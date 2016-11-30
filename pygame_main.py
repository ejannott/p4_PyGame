#Ethan Jannott
#ejannott
#22235024
#
#PERSONAL TO-DO:
#	- Get rid of explanation comments - save my final version as a different copy without those.
#
#
##References:
## 
## 
## 
## 

import pygame

pygame.init()
#Set up the game screen
gameDisplay = pygame.display.set_mode((800,600))  #(double parentheses to let py know we are passing a tuple as a parameter)
pygame.display.set_caption('Dodging') #here is the TITLE of the window/game title
clock = pygame.time.Clock() #this is the 'gameclock' - this is imposed on everything in the game

collision = False #when you start the game, you havent crashed yet

#where the game is actaully running - in this loop:
while not collision:
