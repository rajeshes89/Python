from turtle import *
from random import randint

bgcolor('white')
x = 1
speed(10)
while x < 100:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    print(r,g,b)
    colormode(255)
    pencolor(167,159,87)
    fd(50+x)
    rt(90.991)
    x = x + 1

exitonclick()