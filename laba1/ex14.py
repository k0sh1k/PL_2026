from turtle import *

speed(10)

def star(n, size):
    grad = 180 - (180 / n)  # угол поворота для звезды
    
    for i in range(n):
        fd(size)
        rt(grad)

# Звезда с 5 вершинами
pu()
goto(-150, 0)
pd()
color("blue")
star(5, 100)

# Звезда с 11 вершинами
pu()
goto(150, 0)
pd()
color("red")
star(11, 100)
