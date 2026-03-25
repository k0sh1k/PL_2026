from turtle import*


speed(10)
pensize(5)

# Координаты для каждой цифры в формате (x, y)
# Масштабируем умножением на size

digits = {
    0: [(0, 0), (0, 2), (1, 2), (1, 0), (0, 0)],
    1: [(0, 1), (1, 2), (1, 0)],
    2: [(0, 2), (1, 2), (1, 1), (0, 0), (1, 0)],
    3: [(0, 2), (1, 2), (0, 1), (1, 1), (0, 0)],
    4: [(0, 2), (0, 1), (1, 1), (2, 1), (1, 0)]
}

def draw_digit(d, x, y, size=30):
    pu()
    # Перемещаемся к 1ой точке цифры без рисования
    first_x, first_y = digits[d][0]
    goto(x + first_x * size, y + first_y * size)
    pd()
    
    # Рисуем остальные точки
    for dx, dy in digits[d][1:]:
        goto(x + dx * size, y + dy * size)

# Индекс 142300
x_start = -300
index = [1, 4, 2, 3, 0, 0]

for i, d in enumerate(index):
    draw_digit(d, x_start + i * 100, 0, 30)

done()