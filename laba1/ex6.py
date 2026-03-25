from turtle import *
import math

speed(10)

n = 12  # количество лап
length = 100  # длина лапы

# Рисуем лапы
for i in range(n):
    pu()
    goto(0, 0)  # центр тела
    pd()
    
    angle = i * (360 / n)  # равномерно распределяем лапы по кругу
    setheading(angle)
    
    fd(length)  # рисуем лапу
    stamp()
    # Возвращаемся назад для следующей лапе
    pu()
    goto(0, 0)

done()