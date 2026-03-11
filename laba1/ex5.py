from turtle import *
import math

speed(10)

x = 50  # начальная длина

for i in range(10):  # 10 квадратов
    # Рисуем квадрат
    fd(x)
    lt(90)
    fd(x)
    lt(90)
    fd(x)
    lt(90)
    fd(x)
    lt(90)
    
    # Переход к следующему квадрату (кроме последнего)
    if i < 9:
        pu()
        rt(135)
        fd(10)
        lt(135)
        pd()
        
        # Увеличиваем длину для следующего квадрата
        x = x + 10 * math.sqrt(2)

done()