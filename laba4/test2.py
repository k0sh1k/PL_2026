import pygame
from pygame.draw import *
from random import randint

pygame.init()
FPS = 2
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Поймай тарелку")

# Цвета
SKY = (15, 15, 30)
METAL = (170, 170, 180)
GLASS = (100, 200, 255)
BLACK = (0, 0, 0)

# Список вариантов металлических оттенков (для разнообразия)
METAL_COLORS = [
    (170, 170, 180),
    (150, 150, 160),
    (190, 190, 200),
    (130, 130, 140)
]
GLASS_COLORS = [
    (100, 200, 255),
    (120, 220, 255),
    (80, 180, 235),
    (150, 210, 250)
]

def new_plate():
    '''рисует новую тарелку и сохраняет её координаты и размеры'''
    global x, y, w, h, metal_color, glass_color
    # Центр тарелки (верхний левый угол прямоугольника, в который вписывается тарелка)
    x = randint(100, 1100)   # центр по x (для простоты используем центр корпуса)
    y = randint(100, 800)    # центр по y
    w = randint(120, 250)    # ширина корпуса
    h = randint(40, 80)      # высота корпуса
    metal_color = METAL_COLORS[randint(0, len(METAL_COLORS)-1)]
    glass_color = GLASS_COLORS[randint(0, len(GLASS_COLORS)-1)]

    # Рисуем корпус (эллипс)
    ellipse(screen, metal_color, (x - w//2, y - h//2, w, h))
    # Рисуем купол (эллипс поменьше, смещённый вверх)
    cupola_w = w // 2
    cupola_h = h // 2
    ellipse(screen, glass_color, (x - cupola_w//2, y - h//2 - cupola_h//2, cupola_w, cupola_h))

def click(event):
    '''проверяет, попал ли клик в тарелку'''
    # Получаем координаты клика
    mx, my = event.pos
    # Проверяем попадание в прямоугольник корпуса
    left = x - w//2
    right = x + w//2
    top = y - h//2 - (h//2)//2  # верхняя граница купола (приблизительно)
    bottom = y + h//2
    if left <= mx <= right and top <= my <= bottom:
        print("Попал в тарелку!")
    else:
        print("Мимо")

# Основной цикл
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)   # вызываем проверку попадания
            print('Click!')
    new_plate()            # рисуем новую тарелку
    pygame.display.update()
    screen.fill(BLACK)     # очищаем экран

pygame.quit()