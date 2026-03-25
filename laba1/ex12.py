from turtle import *

speed(0)

def dug(r, i):
     if i % 2 == 0:
         for i in range(180):
             fd(r)
             lt(1)
    
lt(90)
for x in range(20):
     dug(1, 2)   #Черепаха повернется полукругом и пройдет путь = длина полуокружности.
     dug(0.1, 2) #маленький полукруг