# Imports
import pygame
import time
import random
from tkinter import *
from tkinter import messagebox

# Init
pygame.init()

# Global Vars
Width = 500
Height = 700
size = (Width, Height)
bird_size = 50
gravity = 3

# Rgb
light_blue = (3, 252, 227)
green = (3, 135, 45)
yellow = (255, 247, 0)
black = (0, 0, 0)
white = (255,255,255)

# Win
win = pygame.display.set_mode(size , pygame.RESIZABLE)
pygame.display.set_caption('Flapy Bird')
pygame.display.set_icon(pygame.image.load('Bird.png'))

# sound
music = pygame.mixer.music.load('bensound-summer.wav')
# Bg
BG = pygame.image.load('BG.png')

# Functions
def jump(y):
    y -= 100
    return y


def msgbox(score):
    
    root = Tk().wm_withdraw()
    MsgBox = messagebox.askquestion(title='GAMEOVER',
                                    message='The bird has died his score was : ' + str(
                                        score) + '\nWould you like to play again ? ',
                                    icon='question')
    if MsgBox == 'yes':
        time.sleep(0.75)
        main()
    else:
        sys.exit()
    
    # loss_window = pygame.display.set_mode((200,200))

def wirte_text_screen(msg, color, x, y, size):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, color)
    win.blit(text, [x,y])

# draw the shop button
def draw_shop_button_and_operate_shop(x,y,radius, color, sx ,sy):
    pygame.draw.circle(win, color, (x,y), radius)

# Main loop in  main functions
def main():
    pygame.mixer.music.play(-1)

    i = 50
    color = yellow

    changeColor = (random.randint(0,255),random.randint(0,255), random.randint(0,255))
    # died = False
    # currency = 0
    x = 30
    y = (Height // 2)

    rect_x = random.randint(75, 500)

    rect_height = random.randint(0, 350)
    rect_y = 0

    rect_bottom_height = 100
    rect_y_bottom = 600

    score = 0

    ball_radius = 15

    while True:

        rect_x -= 5

        time.sleep(0.03)

        # Event catcher
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    y = jump(y)


            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                y = jump(y)


        delay_for_jump = 0.7
        if y > 700:
            time.sleep(delay_for_jump)
            msgbox(score)

        if y < 0:
            time.sleep(delay_for_jump)
            y = -100000
            msgbox(score)

        if rect_x < -0:
            score += 10
            rect_height = random.randint(350, 500)
            rect_x = 500

        y += gravity

        win.blit(BG, (0,0))

        # print_the_bird(x, y)

        green_bottom = pygame.Rect(rect_x, rect_y_bottom, 75, rect_bottom_height)
        green_top = pygame.Rect(rect_x, rect_y, 75, rect_height)

        green_bottom_border = pygame.Rect(rect_x - 0, rect_y_bottom - 5, 75, rect_bottom_height + 5)
        green_top_border = pygame.Rect(rect_x - 0, rect_y - 10, 75, rect_height + 5)

        pygame.draw.rect(win, green, green_top)
        pygame.draw.rect(win, green, green_bottom)

        pygame.draw.rect(win, black, green_top_border, 10)
        pygame.draw.rect(win, black, green_bottom_border, 10)

        # pygame.draw.line(win, black, rect_x, (rect_x + 75 ), 1)

        if score > i:
            color = (random.randint(0,255),random.randint(0,255), random.randint(0,255))
            bird = pygame.draw.circle(win, color, (x, y), ball_radius)
            i += 50
        else:
            bird = pygame.draw.circle(win, color, (x, y), ball_radius)

        wirte_text_screen(f'SCORE : {score}', black, 190, 0, 50)

        pygame.display.update()

        # draw_shop_button_and_operate_shop()

        if green_top.colliderect(bird) or green_bottom.colliderect(bird): msgbox(score)


# if __name__ == '__main__':
main()