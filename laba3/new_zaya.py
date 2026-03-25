import pygame
from pygame.draw import *

pygame.init()

# Все параметры зайца теперь можно менять

# Параметры положения и размера
x = 200                    # координата X левого верхнего угла
y = 200                    # координата Y левого верхнего угла
width = 200                # ширина зайца
height = 400               # высота зайца
color = (200, 200, 200)    # цвет зайца

# Параметры тела
body_width_ratio = 0.5     # ширина тела относительно width
body_height_ratio = 0.5    # высота тела относительно height

# Параметры головы
head_size_ratio = 0.25     # размер головы относительно height

# Параметры ушей
ear_height_ratio = 0.33    # высота уха относительно height
ear_width_ratio = 0.125    # ширина уха относительно width
ear_x_offset_ratio = 0.25  # смещение ушей относительно центра головы (от head_size)

# Параметры ног
leg_height_ratio = 0.0625  # высота ноги относительно height
leg_width_ratio = 0.25     # ширина ноги относительно width
leg_x_offset_ratio = 0.25  # смещение ног относительно центра тела (от body_width)

# Параметры глаз, носа и усов
eye_size_ratio = 0.1       # размер глаза относительно head_size
eye_y_offset_ratio = 0.3   # смещение глаз по Y относительно центра головы
eye_x_offset_ratio = 0.3   # смещение глаз по X относительно центра головы
nose_size_ratio = 0.15     # размер носа относительно head_size
nose_y_offset_ratio = 0.4  # смещение носа по Y относительно центра головы
whisker_length_ratio = 0.8 # длина усов относительно head_size
whisker_count = 3          # количество усов с каждой стороны

# новые глаза
def draw_eyes(surface, head_x, head_y, head_size):
    '''
    Рисует глаза зайца (маленькие черные кружочки)
    surface - объект pygame.Surface
    head_x, head_y - координаты центра головы
    head_size - диаметр головы
    '''
    eye_size = int(head_size * eye_size_ratio)  # размер глаза
    eye_y = head_y - int(head_size * eye_y_offset_ratio)  # позиция по Y
    eye_offset = int(head_size * eye_x_offset_ratio)  # расстояние между глазами
    
    # Левый глаз - КРУЖОК!
    circle(surface, (0, 0, 0), (head_x - eye_offset, eye_y), eye_size // 2)
    
    # Правый глаз - КРУЖОК!
    circle(surface, (0, 0, 0), (head_x + eye_offset, eye_y), eye_size // 2)

def draw_hare(surface, x, y, width, height, color):
    '''
    Рисует зайца на экране.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    width, height - ширина и высота изобажения
    color - цвет, заданный в формате, подходящем для pygame.Color
    '''
    
    # Принимает width и height, возвращает кортеж (ширина_тела, высота_тела)
    # Умножает общие размеры на коэффициенты тела
    calc_body = lambda w, h: (int(w * body_width_ratio), int(h * body_height_ratio))
    
    # Принимает height, возвращает размер головы (диаметр)
    # head_size_ratio = 0.25, значит голова будет 25 проц от высоты зайца
    calc_head = lambda h: int(h * head_size_ratio)
    
    # Принимает width и height, возвращает (ширина_уха, высота_уха)
    # Уши уже общих размеров
    calc_ear = lambda w, h: (int(w * ear_width_ratio), int(h * ear_height_ratio))
    
    # Принимает width и height, возвращает (ширина ноги, высота ноги)
    calc_leg = lambda w, h: (int(w * leg_width_ratio), int(h * leg_height_ratio))
    
    # Принимает размер и коэффициент, возвращает смещение в пикселях
    # Используется для позиционирования ушей и ног относительно центра
    calc_offset = lambda size, ratio: int(size * ratio)
    
    # Принимает Y верхнего угла и высоту тела, возвращает Y центра тела
    # Тело рисуется от верхнего угла + половина высоты тела
    get_body_y = lambda y, bh: y + bh // 2
    
    # Принимает Y верхнего угла и размер головы, возвращает Y центра головы
    # Голова выше верхнего угла на половину своего размера
    get_head_y = lambda y, hs: y - hs // 2
    
    # Принимает Y верхнего угла, высоту зайца и высоту уха, возвращает Y центра ушей
    # Уши на уровне: верх зайца + половина высоты уха
    get_ear_y = lambda y, h, eh: y - h // 2 + eh // 2
    
    # Принимает Y верхнего угла, высоту зайца и высоту ноги, возвращает Y центра ног
    # Ноги внизу: низ зайца - половина высоты ноги
    get_leg_y = lambda y, h, lh: y + h // 2 - lh // 2
    
    # Принимает размер головы, возвращает кортеж (размер_носа, смещение_носа)
    # Нос рассчитывается относительно головы
    calc_nose = lambda hs: (
        int(hs * nose_size_ratio),      # размер носа (15проц от головы)
        int(hs * nose_y_offset_ratio)   # смещение вниз (40проц от головы)
    )
    
    # Принимает размер головы, возвращает длину усов
    calc_whisker = lambda hs: int(hs * whisker_length_ratio)
    
    # Вычисляем размеры тела через лямбду
    body_width, body_height = calc_body(width, height)

    # Вычисляем Y центра тела через лямбду
    body_y = get_body_y(y, body_height)

    # Рисуе тело
    draw_body(surface, x, body_y, body_width, body_height, color)

    # Вычисляем размер головы через лямбду
    head_size = calc_head(height)

    # Вычисляем Y центра головы через лямбду
    head_center_y = get_head_y(y, head_size)

    # Рисуем голову
    draw_head(surface, x, head_center_y, head_size, color)
    
    # Отдельная функция для глаз
    draw_eyes(surface, x, head_center_y, head_size)
    
    # Получаем параметры носа через лямбду
    nose_size, nose_y_offset = calc_nose(head_size)

    # Вычисляем Y носа (центр головы + смещение)
    nose_y = head_center_y + nose_y_offset

    # Рисуем нос (розовый кружок)
    circle(surface, (255, 150, 150), (x, nose_y), nose_size // 2)
    
    # Получаем длину усов через лямбду
    whisker_length = calc_whisker(head_size)

    # Y позиция усов (чуть ниже центра головы)
    whisker_y = head_center_y + int(head_size * 0.2)

    # Рисуем по 3 уса с каждой стороны
    for i in range(whisker_count):
        y_offset = i * 5 - 5  # -5, 0, 5 - чтобы усы были веером
        # Левые усы
        line(surface, (100, 100, 100), 
             (x - 10, whisker_y + y_offset), 
             (x - whisker_length, whisker_y + y_offset - 5))
        # Правые усы
        line(surface, (100, 100, 100), 
             (x + 10, whisker_y + y_offset), 
             (x + whisker_length, whisker_y + y_offset - 5))

    # Получаем размеры ушей через лямбду
    ear_width, ear_height = calc_ear(width, height)

    # Получаем Y позицию ушей через лямбду
    ear_y = get_ear_y(y, height, ear_height)

    # Получаем смещение ушей от центра через лямбду
    ear_offset = calc_offset(head_size, ear_x_offset_ratio)

    # Рисуем два уха (левое и правое)
    for ear_x in (x - ear_offset, x + ear_offset):
        draw_ear(surface, ear_x, ear_y, ear_width, ear_height, color)
    
    # Получаем размеры ног через лямбду
    leg_width, leg_height = calc_leg(width, height)

    # Получаем Y позицию ног через лямбду
    leg_y = get_leg_y(y, height, leg_height)

    # Получаем смещение ног от центра через лямбду
    leg_offset = calc_offset(body_width, leg_x_offset_ratio)

    # Рисуем две ноги (левую и правую)
    for leg_x in (x - leg_offset, x + leg_offset):
        draw_leg(surface, leg_x, leg_y, leg_width, leg_height, color)

def draw_body(surface, x, y, width, height, color):
    '''Рисует тело зайца.'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_head(surface, x, y, size, color):
    '''Рисует голову зайца.'''
    circle(surface, color, (x, y), size // 2)


def draw_ear(surface, x, y, width, height, color):
    '''Рисует ухо зайца.'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_leg(surface, x, y, width, height, color):
    '''Рисует ногу зайца.'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))

# Рисуем зайца
draw_hare(screen, x, y, width, height, color)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()