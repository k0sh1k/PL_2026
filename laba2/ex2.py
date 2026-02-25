import pygame
from pygame.draw import *

import math

# Настройки окна и цветов
WIDTH, HEIGHT = 800, 600
SKY_BLUE = (220, 230, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Инициализация Pygam
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ex2")

def draw_igloo(surface, x, y):
    #Рисует иглу (пустой купол) в координатах x, y
    width = 250   # Ширина купола
    height = 200  # Высота купола
    
    # Рисуем дугу (верхняя часть)
    # С помощью arc (дуга) рисуется черная линия по верху эллипса, а с помощью line — плоское основание.
    # В Pygame эллипсы не рисуются «от центра». Они вписываются в прямоугольник.
    # rect [x, y, ширина, высота] - воображаемый прямоугольник, в который вписан эллипс
    # 0 и math.pi (3.14) — это углы начала и конца дуги в радианах (верхняя половина)
    # Координата y - height // 2 поднимает эту рамку(250*200) выше, чтобы точка (x, y), 
    # которую ты передал в функцию, стала не левым верхним углом, а серединой основания дома.

    #СНАЧАДА рек
    rect = [x, y - height // 2, width, height]
    # ПОТОМ использую её для заливки
    # Эта команда рисует полный, закрашенный серый овал.
    pygame.draw.ellipse(surface, GRAY, rect) 
    # Дуга (arc) рисует только линию по периметру того же эллипса.
    # 0 и math.pi (3.14) - это углы. В тригонометрии 0 — это крайняя правая точка, а pi — крайняя левая.
    pygame.draw.arc(surface, BLACK, rect, 0, math.pi, 2)
    # Так как дуга рисует только «верх», низ остается открытым. 
    # Эта строка просто проводит прямую черную линию по земле от левого края купола до правого, чтобы закрыть контур.
    pygame.draw.line(surface, BLACK, (x, y), (x + width, y), 2)
    

# ето есимося
def draw_eskimo(surface, x, y):
    #Рисует эскимоса в координатах x, y
    #Туловище
    #Используем эллипс

    # берет 4 точки, чтобы получилась расширяющаяся книзу трапеция. 
    # Точка (x, y) здесь - это шея персонажа.
    body_points = [(x - 40, y + 80), (x + 40, y + 80), (x + 20, y), (x - 20, y)]
    pygame.draw.polygon(surface, (150, 120, 100), body_points) 
    
    # Капюшон большой светло серый круг
    pygame.draw.circle(surface, (220, 220, 220), (x, y), 35)
    
    # Лицо 
    pygame.draw.circle(surface, (235, 200, 180), (x, y), 25)
    
    # Глаза и злой рот 
    # Глаза
    pygame.draw.line(surface, BLACK, (x - 12, y - 5), (x - 4, y - 5), 2)
    pygame.draw.line(surface, BLACK, (x + 4, y - 5), (x + 12, y - 5), 2)
    # Рот дугой вниз
    #Используется та же логика, что и в иглу (arc). Мы берем верхнюю половину эллипса (от 0 до math.pi)
    mouth_rect = [x - 10, y + 5, 20, 15]
    pygame.draw.arc(surface, BLACK, mouth_rect, 0, math.pi, 2)

    # Палка в руке
    pygame.draw.line(surface, BLACK, (x - 30, y + 80), (x - 30, y - 20), 2)

def draw_cat(surface, x, y):
    #Рисует серого кота в координатах x, y
    GRAY = (200, 200, 200)
    
    # Туловище (вытянутый горизонтальный эллипс)
    body_rect = [x, y, 120, 40]
    pygame.draw.ellipse(surface, GRAY, body_rect)
    
    # Голова
    pygame.draw.circle(surface, GRAY, (x + 10, y + 5), 25)
    
    # Ушки (треугольники)
    pygame.draw.polygon(surface, GRAY, [(x - 5, y - 10), (x + 5, y - 30), (x + 15, y - 10)])
    pygame.draw.polygon(surface, GRAY, [(x + 10, y - 10), (x + 20, y - 30), (x + 30, y - 10)])
    
    # Хвост - толстая линия с изгибом
    # Используем несколько точек для имитации подъема хвоста
    pygame.draw.lines(surface, GRAY, False, [(x + 110, y + 20), (x + 150, y + 5), (x + 180, y - 10)], 15)

    # Лапы - простые линии под наклоном
    pygame.draw.line(surface, GRAY, (x + 20, y + 35), (x + 5, y + 55), 10) # передняя
    pygame.draw.line(surface, GRAY, (x + 100, y + 35), (x + 120, y + 55), 10) # задняя
    
    # Глаза точки
    pygame.draw.circle(surface, BLACK, (x + 5, y + 2), 3)
    pygame.draw.circle(surface, BLACK, (x + 15, y + 2), 3)


# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Вызов функции отрисовки фона
    
    screen.fill(SKY_BLUE)
    draw_igloo(screen, 150, 300)
    pygame.draw.rect(screen, WHITE, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    draw_eskimo(screen, 600, 350)
    draw_cat(screen, 50, 450)
    
    # Обновление экрана
    pygame.display.flip()

pygame.quit()
