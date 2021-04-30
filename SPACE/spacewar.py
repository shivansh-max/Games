# Imports
import winsound
import turtle
import random
import time

# Global variables
width = 700
height = 700

# Screen
win = turtle.Screen()
win.bgcolor('black')
win.tracer(0)
win.setup(width, height)
win.title('SpaceWAR')


# classes
# The class that will generate the sprites
class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # Boundry
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def collision(self, other):
        if (self.xcor() >= (other.xcor() - 10)) and \
                (self.xcor() <= (other.xcor() + 10)) and \
                (self.ycor() >= (other.ycor() - 10)) and \
                (self.ycor() <= (other.ycor() + 10)):
            return True
        else:
            return False


# Player class
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 1
        self.lives = 3

    def turn_left(self):
        self.left(25)

    def turn_right(self):
        self.right(25)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1


# Enemy class
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))


# Enemy class
class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)

        # Boundry
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)


class Partical(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_len=0.1, stretch_wid=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(10)


# Bullet class
class Bullet(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 20
        self.status = 'ready'
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.goto(-1000, -1000)

    def fire(self):
        if self.status == 'ready':
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = 'firing'
            winsound.PlaySound("Laser.wav.wav", winsound.SND_ASYNC)

    def move(self):
        if self.status == 'firing':
            self.fd(self.speed)

        if self.xcor() > 290 or self.xcor() < -290 or self.ycor() > 290 or self.ycor() < -290:
            self.goto(-1000, 1000)
            self.status = 'ready'

        if self.status == 'ready':
            self.goto(-1000, -1000)


# creates the main game
class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = 'playing'
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.forward(600)
            self.pen.right(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_the_stuff(self):
        self.pen.undo()
        msg = 'SCORE: %s' % (self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=('comic sans ms', 16, 'normal'))


# Creating stuff with classes
player = Player('triangle', 'white', 0, 0)
# enemy = Enemy('circle', 'red', -100, 0)
missle = Bullet('triangle', 'yellow', 0, 0)
game = Game()
# ally = Ally('square', 'blue', 100, 0)


amount_of_enemys_and_allys = 6
enemies = []
allies = []
particals = []
for i in range(amount_of_enemys_and_allys):
    enemies.append(Enemy('circle', 'red', -100, 0))
for j in range(amount_of_enemys_and_allys):
    allies.append(Ally('square', 'blue', 100, 0))
for l in range(20):
    particals.append(Partical('circle', 'orange', 0, 0))

# Draw the border
game.draw_border()
game.show_the_stuff()

# Keyboard listening
turtle.onkeypress(player.turn_right, 'Right')
turtle.onkeypress(player.turn_left, 'Left')
turtle.onkeypress(player.accelerate, 'Up')
turtle.onkeypress(player.decelerate, 'Down')
turtle.onkeypress(missle.fire, 'space')
turtle.listen()

while True:
    time.sleep(0.05)
    win.update()

    player.move()
    # enemy.move()
    missle.move()

    for enemy in enemies:
        enemy.move()
        if player.collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            winsound.PlaySound("Boom.wav.wav", winsound.SND_ASYNC)

        if missle.collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missle.status = 'ready'
            game.score += 100
            game.show_the_stuff()
            winsound.PlaySound("Boom.wav.wav", winsound.SND_ASYNC)

    for ally in allies:
        ally.move()

        if missle.collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missle.status = 'ready'
            game.score -= 50
            game.show_the_stuff()
            winsound.PlaySound("Boom.wav.wav", winsound.SND_ASYNC)
