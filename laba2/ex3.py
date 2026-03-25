import pygame
from pygame.draw import *
import math

# Настройки окна и цветов
WIDTH, HEIGHT = 800, 600
SKY_BLUE = (220, 230, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ex3")

def draw_igloo(surface, x, y):
    #Рисуем иглу (пустой купол) в координатах x, y
    width = 250   # Ширина купола
    height = 200  # Высота купола
    

    #СНАЧАДА рек
    rect = [x, y - height // 2, width, height]
    # ПОТОМ использую её для заливки
    pygame.draw.ellipse(surface, GRAY, rect)
    
    pygame.draw.arc(surface, BLACK, rect, 0, math.pi, 2)
    pygame.draw.line(surface, BLACK, (x, y), (x + width, y), 2)

def draw_eskimo(surface, x, y, scale=1.0):
    
    # Туловище (трапеция)
    # Все смещения (40, 80, 20) умножаем на scale
    body_points = [
        (x - 40 * scale, y + 80 * scale), 
        (x + 40 * scale, y + 80 * scale), 
        (x + 20 * scale, y), 
        (x - 20 * scale, y)
    ]
    pygame.draw.polygon(surface, (150, 120, 100), body_points)
    
    # Капюшон (радиус 35)
    pygame.draw.circle(surface, (220, 220, 220), (int(x), int(y)), int(35 * scale))
    
    # Лицо (радиус 25)
    pygame.draw.circle(surface, (235, 200, 180), (int(x), int(y)), int(25 * scale))
    
    # Глаза (линии)
    # Смещение глаз и их длина тоже зависят от scale
    pygame.draw.line(surface, BLACK, (x - 12 * scale, y - 5 * scale), (x - 4 * scale, y - 5 * scale), max(1, int(2 * scale)))
    pygame.draw.line(surface, BLACK, (x + 4 * scale, y - 5 * scale), (x + 12 * scale, y - 5 * scale), max(1, int(2 * scale)))
    
    # Рот (дуга)
    # Прямоугольник для дуги масштабируем целиком
    mouth_rect = [x - 10 * scale, y + 5 * scale, 20 * scale, 15 * scale]
    pygame.draw.arc(surface, BLACK, mouth_rect, 0, math.pi, max(1, int(2 * scale)))

    # Палка в руке
    # Длина палки теперь тоже пропорциональна
    pygame.draw.line(surface, BLACK, (x - 30 * scale, y + 80 * scale), (x - 30 * scale, y - 20 * scale), max(1, int(2 * scale)))


def draw_cat(surface, x, y, scale=1.0):
    #Рисует серого кота с масштабированием
    GRAY_CAT = (200, 200, 200)
    
    # Туловище (вытянутый эллипс)
    body_rect = [x, y, 120 * scale, 40 * scale]
    pygame.draw.ellipse(surface, GRAY_CAT, body_rect)
    
    #Голова: Рисуется кругом. Важно, что head_center (центр головы) привязан к координате x туловища. 
    # Если ты двигаешь кота, голова «едет» вместе с ним.
    # Уши: Это два треугольника (polygon). Они рисуются чуть выше головы. 
    # Координаты вершин заданы так, чтобы ушки были острыми и стояли симметрично.

    # Голова (координаты центра относительно x, y)
    head_center = (int(x + 10 * scale), int(y + 5 * scale))
    pygame.draw.circle(surface, GRAY_CAT, head_center, int(25 * scale))
    
    # Ушки (треугольники)
    # Левое ушко
    pygame.draw.polygon(surface, GRAY_CAT, [
        (x - 5 * scale, y - 10 * scale), 
        (x + 5 * scale, y - 30 * scale), 
        (x + 15 * scale, y - 10 * scale)
    ])
    # Правое ушко
    pygame.draw.polygon(surface, GRAY_CAT, [
        (x + 10 * scale, y - 10 * scale), 
        (x + 20 * scale, y - 30 * scale), 
        (x + 30 * scale, y - 10 * scale)
    ])
    
    # Хвост (толстая линия)
    tail_points = [
        (x + 110 * scale, y + 20 * scale), 
        (x + 150 * scale, y + 5 * scale), 
        (x + 180 * scale, y - 10 * scale)
    ]
    pygame.draw.lines(surface, GRAY_CAT, False, tail_points, max(1, int(15 * scale)))

    # Лапы (толстые линии)
    # Передняя
    pygame.draw.line(surface, GRAY_CAT, 
                     (x + 20 * scale, y + 35 * scale), 
                     (x + 5 * scale, y + 55 * scale), max(1, int(10 * scale)))
    # Задняя
    pygame.draw.line(surface, GRAY_CAT, 
                     (x + 100 * scale, y + 35 * scale), 
                     (x + 120 * scale, y + 55 * scale), max(1, int(10 * scale)))
    
    # Глаза (точки)
    pygame.draw.circle(surface, BLACK, (int(x + 5 * scale), int(y + 2 * scale)), max(1, int(3 * scale)))
    pygame.draw.circle(surface, BLACK, (int(x + 15 * scale), int(y + 2 * scale)), max(1, int(3 * scale)))

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Фон (небо и игла)
    screen.fill(SKY_BLUE)
    draw_igloo(screen, 150, 300)
    
    # 2. Снег (рисуем ПЕРЕД персонажами, чтобы перекрыть низ иглу)
    pygame.draw.rect(screen, WHITE, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    # 3. ТРИ ЭСКИМОСА (разные размеры и позиции)
    draw_eskimo(screen, 600, 320, 0.5)  # Маленький (вдалеке)
    draw_eskimo(screen, 500, 400, 1.0)  # Средний
    draw_eskimo(screen, 700, 450, 1.5)  # Большой (на переднем плане)

    # 4. ТРИ КОТА (разные размеры и позиции)
    draw_cat(screen, 50, 420, 0.6)      # Маленький
    draw_cat(screen, 150, 480, 0.9)     # Средний
    draw_cat(screen, 300, 520, 1.2)     # Большой

    # Обновление экрана
    pygame.display.flip()

pygame.quit()