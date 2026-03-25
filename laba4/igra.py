"""
Лабораторная работа №4. Игра "Поймай тарелку"

ОТЧЁТ О ВЫПОЛНЕНИИ:
1) Код читабельный и документированный.
   - Все блоки кода снабжены комментариями.
   - Каждая функция имеет docstring.
   - Переменные названы осмысленно (plate_center_x, plate_width, score и т.д.).
2) Реализован подсчёт очков.
   - Глобальная переменная score увеличивается при попадании.
   - Счёт отображается на экране в левом верхнем углу.
   - При попадании в консоль выводится сообщение с текущим количеством очков.
3) Тарелка двигается со случайным отражением от стен.
   - Добавлены переменные скорости vx, vy.
   - При столкновении с границами окна скорость меняет знак (отражение).
   - Тарелка не перерисовывается каждый кадр в случайном месте, а плавно движется.
   - При попадании по тарелке генерируется новая тарелка с новыми параметрами и скоростью.
4) Одновременное присутствие нескольких тарелок на экране.
   - Введён список plates, в котором хранятся параметры каждой тарелки.
   - При запуске создаётся 3 тарелки.
   - Все тарелки двигаются независимо и отражаются от стен.
   - При клике по тарелке она исчезает, а вместо неё появляются две новые (количество растёт).
   - Отрисовка и обновление происходят для всех тарелок каждый кадр.
5) Реализованы уровни, изменение скорости и отражение между тарелками.
   - Введены переменные level и score_for_next_level (для перехода требуется 5 очков).
   - Количество тарелок при переходе на новый уровень увеличивается по формуле: old_count * 5.
   - Диапазон скоростей тарелок увеличивается с уровнем: базовая скорость * (1 + (level-1)*0.3).
   - На 3-м уровне и выше добавлено отражение тарелок друг от друга при столкновении.
6) Реализованы фиксированные 5 уровней сложности, комбо и таймер взрыва.
   - Количество тарелок на уровне: 2, 4, 6, 8, 10.
   - Скорость тарелок увеличивается с уровнем (множитель 1.0, 1.3, 1.6, 1.9, 2.2).
   - Переход на следующий уровень при наборе 5 очков (после 5-го уровня игра продолжается бесконечно).
   - Комбо: серия попаданий без промаха даёт множитель очков (х2-х3-х5-х10.
   - Таймер взрыва всех тарелок: если нет попаданий дольше заданного времени (уменьшается с уровнем), все тарелки исчезают и появляются заново.
   - Добавлены звёзды на фон (маленькие квадратики).
   - После 5-го уровня наступает "вечный уровень" – игра продолжается с максимальными параметрами.

Примечание: частота кадров (FPS = 30) выбрана для плавного движения.
Отрисовка происходит каждый кадр, тарелки движутся непрерывно.
"""

import pygame
from pygame.draw import *
from random import randint, choice
import math

# ИНИЦИАЛИЗАЦИЯ
pygame.init()

# Размеры окна
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поймай тарелку")

# Частота кадров (для плавного движения)
FPS = 30
clock = pygame.time.Clock()

# ЦВЕТА
BLACK = (0, 0, 0)

# Цвета для тарелки (металл и стекло)
METAL_COLORS = [
    (170, 170, 180),  # светлый металл
    (150, 150, 160),  # серый металл
    (190, 190, 200),  # почти белый
    (130, 130, 140)   # тёмный металл
]
GLASS_COLORS = [
    (100, 200, 255),  # голубое стекло
    (120, 220, 255),  # ярко-голубое
    (80, 180, 235),   # тёмно-голубое
    (150, 210, 250)   # нежно-голубое
]

# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# Список тарелок. Каждая тарелка — словарь с понятными ключами:
# center_x, center_y, width, height, metal_color, glass_color, speed_x, speed_y
plates = []

# Список звёзд (маленькие квадратики). Каждая звезда — словарь с ключами: x, y, size, brightness
stars = []

# Счёт игрока
score = 0

# Уровень (1..5)
level = 1
# Очки для перехода на следующий уровень (фиксированное значение для всех уровней)
score_per_level = 5

# Параметры уровней: (количество тарелок, множитель скорости, время таймера в секундах)
LEVEL_PARAMS = {
    1: (2, 1.0, 10),
    2: (4, 1.3, 9),
    3: (6, 1.6, 8),
    4: (8, 1.9, 7),
    5: (10, 2.2, 6)
}

# Базовая максимальная скорость (для первого уровня)
BASE_SPEED = 5

# Комбо: счётчик попаданий подряд и текущий множитель
hits_without_miss = 0
combo_multiplier = 1

# Таймер: время последнего попадания (в миллисекундах)
last_hit_time = 0

# ФУНКЦИЯ ГЕНЕРАЦИИ ЗВЁЗД
def generate_stars(num_stars=200):
    """
    Создаёт список звёзд (маленьких квадратиков) со случайными координатами,
    размером и яркостью.
    """
    stars_list = []
    for _ in range(num_stars):
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        size = randint(1, 3)           # размер квадратика 1-3 пикселя
        brightness = randint(100, 255) # яркость от серого до белого
        stars_list.append({'x': x, 'y': y, 'size': size, 'brightness': brightness})
    return stars_list

# ФУНКЦИЯ ОТРИСОВКИ ЗВЁЗД
def draw_stars():
    """
    Рисует все звёзды как маленькие залитые квадратики.
    """
    for star in stars:
        color = (star['brightness'], star['brightness'], star['brightness'])
        rect(screen, color, (star['x'], star['y'], star['size'], star['size']))

# ФУНКЦИЯ ГЕНЕРАЦИИ НОВОЙ ТАРЕЛКИ (возвращает словарь)
def new_plate():
    """
    Создаёт новую тарелку со случайными параметрами.
    Скорость зависит от текущего уровня.
    Возвращает словарь с ключами:
    center_x, center_y, width, height, metal_color, glass_color, speed_x, speed_y
    """
    global level
    # Случайные размеры
    width = randint(100, 250)
    height = randint(40, 80)
    # Случайные координаты (с учётом размеров, чтобы тарелка полностью помещалась)
    center_x = randint(width // 2 + 10, WIDTH - width // 2 - 10)
    center_y = randint(height // 2 + 10, HEIGHT - height // 2 - 10)
    # Случайные цвета
    metal_color = METAL_COLORS[randint(0, len(METAL_COLORS) - 1)]
    glass_color = GLASS_COLORS[randint(0, len(GLASS_COLORS) - 1)]
    # Скорость зависит от уровня (множитель)
    speed_mult = LEVEL_PARAMS[level][1]
    max_speed = BASE_SPEED * speed_mult
    speed_x = randint(-int(max_speed), int(max_speed))
    speed_y = randint(-int(max_speed), int(max_speed))
    while speed_x == 0 and speed_y == 0:
        speed_x = randint(-int(max_speed), int(max_speed))
        speed_y = randint(-int(max_speed), int(max_speed))

    return {
        'center_x': center_x,
        'center_y': center_y,
        'width': width,
        'height': height,
        'metal_color': metal_color,
        'glass_color': glass_color,
        'speed_x': speed_x,
        'speed_y': speed_y
    }

# ФУНКЦИЯ ОБНОВЛЕНИЯ ПОЗИЦИИ ОДНОЙ ТАРЕЛКИ (с отражением от стен)
def update_position(plate):
    """
    Обновляет координаты тарелки в соответствии со скоростью.
    Если тарелка касается границ окна, меняет направление скорости (отражение)
    и корректирует координату, чтобы тарелка не выходила за границы.
    """
    # Обновляем координаты
    plate['center_x'] += plate['speed_x']
    plate['center_y'] += plate['speed_y']

    # Проверка столкновения с левой/правой стеной
    if plate['center_x'] - plate['width'] // 2 <= 0:
        plate['center_x'] = plate['width'] // 2 + 1
        plate['speed_x'] = -plate['speed_x']
    elif plate['center_x'] + plate['width'] // 2 >= WIDTH:
        plate['center_x'] = WIDTH - plate['width'] // 2 - 1
        plate['speed_x'] = -plate['speed_x']

    # Проверка столкновения с верхней/нижней стеной
    if plate['center_y'] - plate['height'] // 2 <= 0:
        plate['center_y'] = plate['height'] // 2 + 1
        plate['speed_y'] = -plate['speed_y']
    elif plate['center_y'] + plate['height'] // 2 >= HEIGHT:
        plate['center_y'] = HEIGHT - plate['height'] // 2 - 1
        plate['speed_y'] = -plate['speed_y']

# ФУНКЦИЯ ОТРАЖЕНИЯ ТАРЕЛОК ДРУГ ОТ ДРУГА (только для уровня >= 3)
def reflect_plates(plate1, plate2):
    """
    Обрабатывает упругое столкновение двух тарелок.
    Изменяет скорости plate1 и plate2.
    """
    # Разница координат
    dx = plate1['center_x'] - plate2['center_x']
    dy = plate1['center_y'] - plate2['center_y']
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    # Нормаль
    nx = dx / distance
    ny = dy / distance
    # Относительная скорость
    dvx = plate1['speed_x'] - plate2['speed_x']
    dvy = plate1['speed_y'] - plate2['speed_y']
    dot = dvx * nx + dvy * ny
    if dot < 0:
        # Импульс (массы считаем одинаковыми)
        impulse = 2 * dot / 2   # 2*m/(m+m) = 1, упрощённо
        plate1['speed_x'] -= impulse * nx
        plate1['speed_y'] -= impulse * ny
        plate2['speed_x'] += impulse * nx
        plate2['speed_y'] += impulse * ny

# ФУНКЦИЯ ПРОВЕРКИ СТОЛКНОВЕНИЙ МЕЖДУ ВСЕМИ ТАРЕЛКАМИ
def handle_collisions():
    """
    Проверяет все пары тарелок на столкновение.
    Если уровень >= 3, вызывает reflect_plates.
    """
    global level
    if level < 3:
        return
    for i in range(len(plates)):
        for j in range(i + 1, len(plates)):
            plate1 = plates[i]
            plate2 = plates[j]
            # Проверяем пересечение прямоугольников (упрощённо)
            left1 = plate1['center_x'] - plate1['width'] // 2
            right1 = plate1['center_x'] + plate1['width'] // 2
            top1 = plate1['center_y'] - plate1['height'] // 2
            bottom1 = plate1['center_y'] + plate1['height'] // 2
            left2 = plate2['center_x'] - plate2['width'] // 2
            right2 = plate2['center_x'] + plate2['width'] // 2
            top2 = plate2['center_y'] - plate2['height'] // 2
            bottom2 = plate2['center_y'] + plate2['height'] // 2
            if not (right1 < left2 or right2 < left1 or bottom1 < top2 or bottom2 < top1):
                reflect_plates(plate1, plate2)

# ФУНКЦИЯ ПОВЫШЕНИЯ УРОВНЯ (с фиксированными параметрами)
def increase_level():
    """
    Увеличивает уровень, обновляет количество тарелок в соответствии с LEVEL_PARAMS,
    сбрасывает комбо и таймер.
    Если достигнут максимальный уровень (5), выводит сообщение и не повышает.
    """
    global level, plates, score, last_hit_time, hits_without_miss, combo_multiplier
    if level < 5:
        level += 1
        print(f"Уровень повышен! Теперь уровень {level}")
        # Пересоздаём тарелки с новыми параметрами
        plates.clear()
        target_count = LEVEL_PARAMS[level][0]
        for _ in range(target_count):
            plates.append(new_plate())
        # Сбрасываем комбо и таймер
        hits_without_miss = 0
        combo_multiplier = 1
        last_hit_time = pygame.time.get_ticks()
    else:
        # После 5 уровня игра продолжается, уровень не повышается
        print("Максимальный уровень достигнут. Игра продолжается в вечном режиме.")

# ФУНКЦИЯ ВЗРЫВА ВСЕХ ТАРЕЛОК ПО ТАЙМЕРУ
def timeout_explosion():
    """
    Удаляет все текущие тарелки и создаёт новые (с параметрами текущего уровня).
    Сбрасывает комбо и таймер.
    """
    global plates, last_hit_time, hits_without_miss, combo_multiplier
    print("Таймер сработал! Все тарелки взорваны и заменены новыми.")
    plates.clear()
    target_count = LEVEL_PARAMS[level][0]
    for _ in range(target_count):
        plates.append(new_plate())
    # Сбрасываем комбо и таймер
    hits_without_miss = 0
    combo_multiplier = 1
    last_hit_time = pygame.time.get_ticks()

# ФУНКЦИЯ ОБНОВЛЕНИЯ КОМБО (вызывается при попадании)
def update_combo():
    """
    Обновляет множитель комбо на основе hits_without_miss.
    """
    global combo_multiplier, hits_without_miss
    if hits_without_miss >= 20:
        combo_multiplier = 10
    elif hits_without_miss >= 10:
        combo_multiplier = 5
    elif hits_without_miss >= 5:
        combo_multiplier = 3
    elif hits_without_miss >= 2:
        combo_multiplier = 2
    else:
        combo_multiplier = 1

# ФУНКЦИЯ РИСОВАНИЯ ОДНОЙ ТАРЕЛКИ
def draw_plate(plate):
    """
    Рисует тарелку на экране, используя переданные параметры.
    """
    # Корпус (эллипс)
    ellipse(screen, plate['metal_color'],
            (plate['center_x'] - plate['width'] // 2,
             plate['center_y'] - plate['height'] // 2,
             plate['width'], plate['height']))

    # Купол (половинный эллипс над корпусом)
    cupola_width = plate['width'] // 2
    cupola_height = plate['height'] // 2
    ellipse(screen, plate['glass_color'],
            (plate['center_x'] - cupola_width // 2,
             plate['center_y'] - plate['height'] // 2 - cupola_height // 2,
             cupola_width, cupola_height))

# ФУНКЦИЯ ПРОВЕРКИ ПОПАДАНИЯ
def check_hit(event):
    """
    Проверяет, попал ли клик мыши в какую-либо тарелку.
    Если попал, увеличивает счёт с учётом комбо, удаляет тарелку и добавляет две новые.
    При достижении порога очков повышает уровень.
    При промахе сбрасывает комбо.
    """
    global score, plates, level, score_per_level, hits_without_miss, combo_multiplier, last_hit_time
    mx, my = event.pos

    # Ищем, в какую тарелку попали
    hit_index = -1
    for i, plate in enumerate(plates):
        left = plate['center_x'] - plate['width'] // 2
        right = plate['center_x'] + plate['width'] // 2
        top = plate['center_y'] - plate['height'] // 2 - (plate['height'] // 2) // 2
        bottom = plate['center_y'] + plate['height'] // 2
        if left <= mx <= right and top <= my <= bottom:
            hit_index = i
            break

    if hit_index != -1:
        # Попадание
        hits_without_miss += 1
        update_combo()
        points = 1 * combo_multiplier
        score += points
        print(f"Попадание! +{points} очков (комбо x{combo_multiplier}). Всего: {score}")
        # Обновляем таймер последнего попадания
        last_hit_time = pygame.time.get_ticks()

        # Удаляем тарелку, в которую попали
        plates.pop(hit_index)
        # Добавляем две новые тарелки
        plates.append(new_plate())
        plates.append(new_plate())

        # Проверяем переход на следующий уровень (только если level < 5)
        if level < 5 and score >= level * score_per_level:
            increase_level()
    else:
        # Промах
        if hits_without_miss > 0:
            print("Промах! Серия прервана.")
        hits_without_miss = 0
        combo_multiplier = 1

# ФУНКЦИЯ ОТРИСОВКИ ИНТЕРФЕЙСА (счёт, уровень, комбо, таймер)
def draw_ui():
    """
    Отображает текущий счёт, уровень, множитель комбо и оставшееся время до взрыва.
    """
    # Используем более стильный шрифт (если Arial недоступен, Pygame подставит дефолтный)
    font = pygame.font.SysFont('Georgia', 36, bold=True)
    # Шрифт для таймера можно сделать чуть меньше или обычный
    font_timer = pygame.font.SysFont('Georgia', 32)

    # Счёт и уровень (с добавлением (Eternal) для вечного режима)
    if level == 5:
        level_text = f"Score: {score}  Level: {level} (Вечный режим)"
    else:
        level_text = f"Score: {score}  Level: {level}"
    text = font.render(level_text, True, (124, 31, 191))
    screen.blit(text, (10, 10))

    # Комбо 
    if combo_multiplier > 1:
        combo_text = font.render(f"Combo x{combo_multiplier}", True, (168, 50, 66))
        screen.blit(combo_text, (10, 50))

    # Таймер 
    timeout_seconds = LEVEL_PARAMS[level][2]
    time_left = max(0, timeout_seconds - (pygame.time.get_ticks() - last_hit_time) / 1000.0)
    timer_text = font_timer.render(f"Timeout: {time_left:.1f}s", True, (45, 228, 237))
    screen.blit(timer_text, (WIDTH - 200, 10))

# ОСНОВНОЙ ИГРОВОЙ ЦИКЛ

# Генерируем звёзды
stars = generate_stars(250)

# Создаёт начальные тарелки для первого уровня
target_count = LEVEL_PARAMS[1][0]
for _ in range(target_count):
    plates.append(new_plate())

# Инициализируем время последнего попадания (чтобы таймер не сработал сразу)
last_hit_time = pygame.time.get_ticks()

running = True
while running:
    # 1. Обрабатываем все накопившиеся события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_hit(event)

    # 2. Обновляем позиции всех тарелок
    for plate in plates:
        update_position(plate)

    # 3. Обрабатываем столкновения между тарелками (если уровень >=3)
    handle_collisions()

    # 4. Проверяем таймер взрыва
    current_time = pygame.time.get_ticks()
    timeout_duration_ms = LEVEL_PARAMS[level][2] * 1000
    if current_time - last_hit_time > timeout_duration_ms:
        timeout_explosion()

    # 5. Очищаем экран
    screen.fill(BLACK)

    # 6. Рисуем звёзды (фон)
    draw_stars()

    # 7. Рисуем все тарелки
    for plate in plates:
        draw_plate(plate)

    # 8. Рисуем интерфейс
    draw_ui()

    # 9. Обновляем экран
    pygame.display.update()

    # 10. Контролируем частоту кадров
    clock.tick(FPS)

# Завершаем работу Pygame
pygame.quit()