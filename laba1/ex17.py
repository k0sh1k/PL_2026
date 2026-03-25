from turtle import *

speed(10)
pensize(5)

# Читаем шрифт из файла
digits = {}

with open('font.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):  # пропускаем пустые строки и комментарии
            continue
        
        # Формат: цифра: x1,y1 x2,y2 x3,y3 ...
        parts = line.split(':')
        digit = int(parts[0])
        coords = []
        
        points = parts[1].strip().split()
        for point in points:
            x, y = map(int, point.split(','))
            coords.append((x, y))
        
        digits[digit] = coords

def draw_digit(d, x, y, size=30):
    if d not in digits:
        return
    
    coords = digits[d]
    
    # Перемещаемся к первой точке без рисования
    pu()
    first_x, first_y = coords[0]
    goto(x + first_x * size, y + first_y * size)
    pd()
    
    # Рисуем остальные точки
    for dx, dy in coords[1:]:
        goto(x + dx * size, y + dy * size)

# Рисуем индекс 142300
x_start = -300
index = [1, 4, 2, 3, 0, 0]

for i, d in enumerate(index):
    draw_digit(d, x_start + i * 100, 0, 30)

done()