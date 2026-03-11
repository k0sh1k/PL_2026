import turtle

turtle.speed(10)

n = 360
length = 1

for i in range(n):
    turtle.forward(length)
    turtle.left(360 / n)
