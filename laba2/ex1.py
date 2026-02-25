import pygame
from pygame.draw import *

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("ex1")

# Цвета
GRAY = (211, 211, 211)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GRAY)

    # Лицо
    pygame.draw.circle(screen, YELLOW, (200, 200), 100) # Желтый круг (центр x,y и радиус)
    pygame.draw.circle(screen, BLACK, (200, 200), 100, 1) # Тот же круг, но только черный контур (толщина 1)

    # Красные глаза с черными зрачками
    # Левый
    pygame.draw.circle(screen, RED, (160, 180), 18)
    pygame.draw.circle(screen, BLACK, (160, 180), 6)
    # Правый
    pygame.draw.circle(screen, RED, (240, 180), 18)
    pygame.draw.circle(screen, BLACK, (240, 180), 6)

    # Бровки
    #Линия (line) рисуется от одной точки (x1, y1) до другой (x2, y2). Последнее число 12 - это толщина. 
    #Чтобы брови были злыми, одна точка должна быть выше другой.
    pygame.draw.line(screen, BLACK, (120, 120), (185, 170), 12) # Левая
    pygame.draw.line(screen, BLACK, (280, 140), (215, 175), 12) # Правая

    # Ротик
    # rect: [отступ слева, отступ сверху, ширина, высота]
    #Рисуем обычный прямоугольник (rect). 
    #Координаты (150, 250) - это левый верхний угол, а 100, 20 - его ширина и высота.
    pygame.draw.rect(screen, BLACK, (150, 250, 100, 20))

    # Показывает всё, что мы нарисовали в этом кадре, на экран
    pygame.display.flip()

pygame.quit() # Корректно закрывает окно, когда цикл остановился
