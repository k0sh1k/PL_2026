# coding: utf-8
# license: GPLv3

"""Модуль визуализации (кинематический вариант).
Координаты тел заданы сразу в пикселах относительно центра окна.
"""

header_font = "Arial-16"
window_width = 1000
window_height = 800


def to_screen_x(x):
    """Модельная x -> экранная (центр окна = середина)."""
    return int(x) + window_width // 2


def to_screen_y(y):
    """Модельная y -> экранная."""
    return int(y) + window_height // 2


def create_body_image(space, body):
    """Рисует кружок тела (звезды, планеты или спутника)."""
    x = to_screen_x(body.x)
    y = to_screen_y(body.y)
    r = body.R
    body.image = space.create_oval(x - r, y - r, x + r, y + r, fill=body.color)


def create_orbit_image(space, body):
    """Рисует орбиту тела окружностью (контур)."""
    cx = to_screen_x(body.cx)
    cy = to_screen_y(body.cy)
    r = int(body.orbit_r)
    body.orbit = space.create_oval(cx - r, cy - r, cx + r, cy + r, outline="gray")


def update_system_name(space, system_name):
    """Подпись системы в углу холста."""
    space.create_text(150, 30, text=system_name, font=header_font, fill="white")


def update_object_position(space, body):
    """Перемещает кружок тела в его текущее положение."""
    if body.type == "star":
        return
    x = to_screen_x(body.x)
    y = to_screen_y(body.y)
    r = body.R
    space.coords(body.image, x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    print("This module is not for direct call!")
