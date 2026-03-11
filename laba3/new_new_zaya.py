import pygame
from pygame.draw import *

pygame.init()

# Глобальные переменные
body_width_ratio = 0.5     # ширина тела относительно width
body_height_ratio = 0.5    # высота тела относительно height
head_size_ratio = 0.25     # размер головы относительно height
ear_height_ratio = 0.33    # высота уха относительно height
ear_width_ratio = 0.125    # ширина уха относительно width
ear_x_offset_ratio = 0.25  # смещение ушей относительно центра головы
leg_height_ratio = 0.0625  # высота ноги относительно height
leg_width_ratio = 0.25     # ширина ноги относительно width
leg_x_offset_ratio = 0.25  # смещение ног относительно центра тела

# Функции рисоавания

def draw_body(surface, x, y, width, height, color):
    '''
    Рисует тело зайца.
    surface - объект pygame.Surface
    x, y - координаты центра изображения
    width, height - ширина и высота изобажения
    color - цвет, заданный в формате, подходящем для pygame.Color
    '''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_head(surface, x, y, size, color):
    '''
    Рисует голову зайца.
    surface - объект pygame.Surface
    x, y - координаты центра изображения
    size - диаметр головы
    color - цвет, заданный в формате, подходящем для pygame.Color
    '''
    circle(surface, color, (x, y), size // 2)


def draw_ear(surface, x, y, width, height, color):
    '''
    Рисует ухо зайца.
    surface - объект pygame.Surface
    x, y - координаты центра изображения
    width, height - ширина и высота изобажения
    color - цвет, заданный в формате, подходящем для pygame.Color
    '''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_leg(surface, x, y, width, height, color):
    '''
    Рисует ногу зайца.
    surface - объект pygame.Surface
    x, y - координаты центра изображения
    width, height - ширина и высота изобажения
    color - цвет, заданный в формате, подходящем для pygame.Color
    '''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_hare(surface, x, y, width, height, body_color, head_color, ear_color, leg_color):
    '''
    Рисует зайца на экране с разными цветами частей.
    surface - объект pygame.Surface
    x, y - координаты левого верхнего угла изображения
    width, height - ширина и высота изобажения
    body_color, head_color, ear_color, leg_color - цвета частей
    '''
    global body_width_ratio, body_height_ratio, head_size_ratio
    global ear_height_ratio, ear_width_ratio, ear_x_offset_ratio
    global leg_height_ratio, leg_width_ratio, leg_x_offset_ratio
    
    body_width = int(width * body_width_ratio)
    body_height = int(height * body_height_ratio)
    body_y = y + body_height // 2
    draw_body(surface, x, body_y, body_width, body_height, body_color)

    head_size = int(height * head_size_ratio)
    draw_head(surface, x, y - head_size // 2, head_size, head_color)

    ear_height = int(height * ear_height_ratio)
    ear_width = int(width * ear_width_ratio)
    ear_y = y - height // 2 + ear_height // 2
    ear_offset = int(head_size * ear_x_offset_ratio)
    for ear_x in (x - ear_offset, x + ear_offset):
        draw_ear(surface, ear_x, ear_y, ear_width, ear_height, ear_color)
    
    leg_height = int(height * leg_height_ratio)
    leg_width = int(width * leg_width_ratio)
    leg_y = y + height // 2 - leg_height // 2
    leg_offset = int(body_width * leg_x_offset_ratio)
    for leg_x in (x - leg_offset, x + leg_offset):
        draw_leg(surface, leg_x, leg_y, leg_width, leg_height, leg_color)


# ========== ИГРА "СОЗДАЙ СВОЕГО ЗАЙЦА" ==========

# Массив цветов
colors = [
    (200, 200, 200),  # серый - 0
    (255, 100, 100),  # красный - 1
    (100, 100, 255),  # синий - 2
    (100, 255, 100),  # зеленый - 3
    (255, 255, 100),  # желтый - 4
    (200, 100, 255),  # фиолетовый - 5
]

# Массив цветов фона (добавил черный и белый)
background_colors = [
    (255, 255, 255),  # белый - 0
    (0, 0, 0),        # черный - 1
    (255, 200, 200),  # светло-розовый - 2
    (200, 255, 200),  # светло-зеленый - 3
    (200, 200, 255),  # светло-синий - 4
    (255, 255, 200),  # светло-желтый - 5
]

# Массив размеров тела
sizes = [
    (150, 300),  # маленький - 0
    (200, 400),  # средний - 1
    (250, 500),  # большой - 2
]

# Массив для толщины ног
leg_thickness = [
    0.15,  # тонкие - 0
    0.25,  # средние - 1
    0.35,  # толстые - 2
]

# Массив для длины ушей
ear_length = [
    0.25,  # короткие - 0
    0.33,  # средние - 1
    0.45,  # длинные - 2
]

# Названия для вывода
color_names = ["серый", "красный", "синий", "зеленый", "желтый", "фиолетовый"]
background_names = ["белый", "черный", "светло-розовый", "светло-зеленый", "светло-синий", "светло-желтый"]
size_names = ["маленький", "средний", "большой"]
leg_names = ["тонкие", "средние", "толстые"]
ear_names = ["короткие", "средние", "длинные"]

def get_number_input(prompt, min_val, max_val):
    
    #Запрашивает число у пользователя и проверяет, что оно в диапазоне
    
    while True:
        try:
            num = int(input(prompt))
            if min_val <= num <= max_val:
                return num
            else:
                print(f"Ошибка! Введите число от {min_val} до {max_val}")
        except ValueError:
            print("Ошибка! Введите целое число")

def get_yes_no_input(prompt):

    #Запрашивает ответ да/нет

    while True:
        answer = input(prompt).lower()
        if answer in ['д', 'да', 'y', 'yes', '']:
            return True
        elif answer in ['н', 'нет', 'n', 'no']:
            return False
        else:
            print("Ошибка! Введите 'д' или 'н'")

print(f"\nПривет! Это игра СОЗДАЙ СВОЕГО ЗАЙЦА!")
print(f"Давайте создадим идеальную зайку!")
print(f"Далее вам предстоит делать выбор.. Будьте внимательны!")
print(f"Удачи.........")
print(f"-" * 50)

# ВЫБОР ЦВЕТА ФОНА
print(f"\nСначала выберите цвет фона:")
for i in range(len(background_colors)):
    print(f"{i}. {background_names[i]}")
background_num = get_number_input(f"Введите номер цвета фона (0-5): ", 0, 5)
background_color = background_colors[background_num]

# Выбор размера тела
print(f"\nСейчас вам нужно будет выбрать размер зайчика")
print(f"\nДоступные размеры тела:")
for i in range(len(sizes)):
    print(f"{i}. {size_names[i]}")

size_num = get_number_input(f"Введите номер размера (0-2): ", 0, 2)
selected_width, selected_height = sizes[size_num]

# Спрашивает про цвета конечностей
print("\n" + "-" * 50)
change_colors = get_yes_no_input(f"В процессе игры этот выбор нельзя изменить!\nХотите менять цвета разных частей? (д/н):\n")

if change_colors:
    # Если да - для каждой конечности выбираем и размер и цвет
    
    # Ноги
    print(f"\nНастройка ног")
    print(f"Выберите толщину ног:")
    for i in range(len(leg_thickness)):
        print(f"{i}. {leg_names[i]}")
    leg_num = get_number_input(f"Номер толщины (0-2): ", 0, 2)
    leg_width_ratio = leg_thickness[leg_num]
    
    print(f"\nВыбери цвет ног:")
    for i in range(len(colors)):
        print(f"{i}. {color_names[i]}")
    leg_num_color = get_number_input(f"Номер цвета (0-5): ", 0, 5)
    leg_color = colors[leg_num_color]
    
    # Уши
    print(f"\nНастройка ушек")
    print(f"Выбери длину ушей:")
    for i in range(len(ear_length)):
        print(f"{i}. {ear_names[i]}")
    ear_num = get_number_input(f"Номер длины (0-2): ", 0, 2)
    ear_height_ratio = ear_length[ear_num]
    
    print(f"\nВыбери цвет ушей:")
    for i in range(len(colors)):
        print(f"{i}. {color_names[i]}")
    ear_num_color = get_number_input(f"Номер цвета (0-5): ", 0, 5)
    ear_color = colors[ear_num_color]
    
    # Голова
    print(f"\nНастройка головы")
    print(f"Выбери цвет головы:")
    for i in range(len(colors)):
        print(f"{i}. {color_names[i]}")
    head_num = get_number_input(f"Номер цвета (0-5): ", 0, 5)
    head_color = colors[head_num]
    
    # Тело
    print(f"\nНастройка тела")
    print(f"Выбери цвет тела:")
    for i in range(len(colors)):
        print(f"{i}. {color_names[i]}")
    body_num = get_number_input(f"Номер цвета (0-5): ", 0, 5)
    body_color = colors[body_num]
    
else:
    # Если нет - выбираем один цвет для всего
    print(f"\nДоступные цвета:")
    for i in range(len(colors)):
        print(f"{i}. {color_names[i]}")
    color_num = get_number_input(f"Введи номер цвета для всего зайца (0-5): ", 0, 5)
    main_color = colors[color_num]
    
    # Ноги
    print(f"\nНастройка ног")
    print(f"Выбери толщину ног:")
    for i in range(len(leg_thickness)):
        print(f"{i}. {leg_names[i]}")
    leg_num = get_number_input(f"Номер толщины (0-2): ", 0, 2)
    leg_width_ratio = leg_thickness[leg_num]
    
    # Уши
    print(f"\nНастройка ушей")
    print(f"Выбери длину ушей:")
    for i in range(len(ear_length)):
        print(f"{i}. {ear_names[i]}")
    ear_num = get_number_input(f"Номер длины (0-2): ", 0, 2)
    ear_height_ratio = ear_length[ear_num]
    
    # Все части одного цвета
    body_color = main_color
    head_color = main_color
    ear_color = main_color
    leg_color = main_color
    body_num = head_num = ear_num_color = leg_num_color = color_num

# Вывод результата
print("\n" + "-" * 50)
print("ТВОЙ ЗАЯЦ ГОТОВ!")
print(f"Цвет фона: {background_names[background_num]}")
print(f"Размер тела: {size_names[size_num]}")
print(f"Ноги: {leg_names[leg_num]}")
print(f"Уши: {ear_names[ear_num]}")

if change_colors:
    print(f"\nЦвета:")
    print(f"- Тело: {color_names[body_num]}")
    print(f"- Голова: {color_names[head_num]}")
    print(f"- Уши: {color_names[ear_num_color]}")
    print(f"- Ноги: {color_names[leg_num_color]}")
else:
    print(f"\nЦвет: {color_names[color_num]}")

input("\nНажми Enter, чтобы увидеть своего зайца...")

# Рисуем зайца
screen = pygame.display.set_mode((600,600))
screen.fill(background_color)  # Используем выбранный цвет фона!

draw_hare(screen, 200, 200, selected_width, selected_height, 
          body_color, head_color, ear_color, leg_color)

pygame.display.update()
clock = pygame.time.Clock()

finished = False
while not finished:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()