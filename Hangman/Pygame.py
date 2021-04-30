# Imports
import pygame
import sys
import math
from Words import words_list
import random
from tkinter import *
from tkinter import messagebox

# init
pygame.init()

# Global Vars
WIDTH,HEIGHT = 800,500
FPS = 60
clock = pygame.time.Clock()
game_over = False
White = (255,255,255)
Black = (0, 0, 0)

# Screen
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")
# size = pygame.display.get_window_size()

# WIDTH = size[0]
# HEIGHT = size[1]


# Image loading
images = []
for i in range(7):
	image = pygame.image.load("hangman" + str(i) + ".png")  
	images.append(image)

# game vars
hangman_status = 0

# Button Vars
RADIUS = 20
GAP = 15
startx = round((WIDTH - (RADIUS*2 + GAP) * 13)/2)
starty = 400
letters = []
A =65
for i in range(26):
	x = startx + GAP * 2  + ((RADIUS*2+GAP) * (i % 13))
	y = starty + ((i // 13) * (GAP + RADIUS * 2))
	letters.append([x, y, chr(A + i), True])

# Fonts
letter_font = pygame.font.SysFont('comicsans', 40)
word_font = pygame.font.SysFont('comicsans', 60)
title_font = pygame.font.SysFont('comicsans', 75)

# Word
word = random.choice((words_list)).upper()
# print(word)
guessed = []


# function
def draw():
	win.fill(White)

	text = title_font.render('Hangman' , 1, Black)
	win.blit(text, (WIDTH/2 - text.get_width()/2 ,20))

	# draw word
	display_word = ""
	for letter in word:
		if letter in guessed:
			display_word += letter + " "
		else:
			display_word += "_ "
	text = word_font.render(display_word, 1, Black)
	win.blit(text, (400,200))

	# drawing the buttons
	for letter in letters:
		x,y,ltr, vis = letter
		if vis:
			pygame.draw.circle(win, Black, (x, y), RADIUS, 3)
			text = letter_font.render(ltr, 1, Black)
			win.blit(text, 	(x-(text.get_width()/2),y-(text.get_height()/2)))

	win.blit(images[hangman_status] ,(150,100))
	pygame.display.update()

# Mainloop in main function

while not(game_over):
	clock.tick(FPS)


	draw()

	# Event Catcher
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			m_x, m_y = pygame.mouse.get_pos()
			for letter in letters:
				x,y,ltr,vis = letter
				if vis:
					dis = math.sqrt((x- m_x)**2 + (y-m_y) ** 2)
					if dis < RADIUS:
						letter[3] = False
						guessed.append(ltr)
						# print(ltr)
						if ltr not in word:
							hangman_status += 1
	won = True
	for letter in word:
		if letter not in guessed:
			won = False
			break
	# print(word)
	if won :
		win.fill(White)
		text = word_font.render("You Won !", 1, Black)
		win.blit(text, (WIDTH/2 - text.get_width()/2 , HEIGHT/2 - text.get_height()/2))
		pygame.display.update()
		pygame.time.delay(5000)
		break

	if hangman_status == 6:
		pygame.time.delay(1000)
		win.fill(White)
		text = word_font.render("You Lost! The word was : " + word, 1, Black)
		win.blit(text, (WIDTH/2 - text.get_width()/2 , HEIGHT/2 - text.get_height()/2))
		pygame.display.update()
		pygame.time.delay(5000)
		break
