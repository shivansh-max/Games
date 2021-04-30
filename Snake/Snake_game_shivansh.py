# print("Hello World")
#   imports
import turtle
import random
import time

delay = 0.1
# SCORE
score = 0
high_score = 0

# Screen
win = turtle.Screen()
win.title("Snake")
win.bgcolor("black")
win.setup(width=700,height=700)
win.tracer(0)

# border
border= turtle.Turtle()
border.speed(0)
border.color("white")
border.pensize(4)
border.hideturtle()
border.penup()
border.goto(-300,-300)
border.down()

for side in range(4):
    border.fd(600)
    border.left(90)

border.penup()
border.goto(0, 350)
border.write("SNAKE",align="center",font=("Arial",24,"normal"))

# Snake:
# Player:
head=turtle.Turtle()
head.color("red")
head.shape("square")
head.penup()
head.speed(0)
head.setposition(0, 0)
head.direction = "stop"

bob = ["blue","green","yellow","white","orange","red","pink","purple"]
boba = ["blue","green","yellow","white","orange","red","pink","purple"]

# Food:
#Apple :
food=turtle.Turtle()
food.color((random.choice(bob)))
food.shape("circle")
food.penup()
food.speed(0)
food.setposition(0, 100)
food.direction = "stop"
head.destination = (0, 0)



segments = []


# SCORE
pen = turtle.Turtle()
pen.speed(0)
pen.color("yellow")
pen.penup()
pen.hideturtle()
pen.goto(0,310)
pen.pendown()
pen.write("SCORE: 0  HIGH SCORE: 0",align = "center",font= ("Comic Sans MS", 14,"normal"))


# Functions:
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":                                        
        x = head.xcor()
        head.setx(x + 20)

                                                                  
# Keyboard calling
win.listen()
win.onkeypress(go_up,"Up")
win.onkeypress(go_down,"Down")
win.onkeypress(go_right,"Right")
win.onkeypress(go_left,"Left")                                                                       

# The loop                                 
while True:

    win.update()

    # Border checking
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # border checking
        for segment in segments:
            segment.goto(1000, 1000)

        # reseting score:
        score = 0
        pen.clear()
        delay = 0.1
        pen.write("SCORE : {}  HIGH SCORE : {}".format(score, high_score),align="center",font=("Comic Sans MS",14,"normal"))

        segments.clear()
    # collision with the food:
    if head.distance(food) < 20:
        food.color((random.choice(bob)))
        x = random.randrange(-280,280,20)
        y = random.randrange(-280, 280,20)
        food.goto(x, y)

        # Add a segment:
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        bang = random.choice(boba)
        new_segment.color(bang)
        new_segment.penup()
        segments.append(new_segment)


        #Add to the score
        score += 10
        delay -= 0.001
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write("SCORE : {}  HIGH SCORE : {}".format(score, high_score),align="center",font=("Comic Sans MS",14,"normal"))

    for index in range(len(segments) -1 , 0 , -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            # reseting score:
            score = 0
            pen.clear()
            delay = 0.1
            pen.write("SCORE : {}  HIGH SCORE : {}".format(score, high_score),align="center",font=("Comic Sans MS",14,"normal"))
            head.goto(0,0)
            head.direction = "stop"

            for segment in segments:
              segment.goto(1000, 1000)

            segments.clear()


    time.sleep(delay)