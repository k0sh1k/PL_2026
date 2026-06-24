# coding: utf-8
# license: GPLv3

import math

# Кинематический движок: движение тел по окружностям + проверка безопасности.

base_step = 0.01
"""Базовый шаг угла за тик. Скорости кратны ему -> движение периодично."""

collision_tolerance = 7
"""Допустимое расстояние между центрами тел (px). Ближе — столкновение."""


def update_positions(space_objects):
    """Пересчитывает x,y всех тел по их текущему углу."""
    for body in space_objects:
        if body.type == "star":
            continue
        body.x = body.cx + body.orbit_r * math.cos(body.angle)
        body.y = body.cy + body.orbit_r * math.sin(body.angle)


def step_angles(space_objects):
    """Один шаг времени: угол += k*base_step. Знак k задаёт направление."""
    for body in space_objects:
        if body.type == "star":
            continue
        body.angle += body.k * base_step


def position_at(body, tick):
    """Координаты тела на заданном тике (от стартового угла) — для проверки."""
    angle = body.start_angle + body.k * base_step * tick
    return (body.cx + body.orbit_r * math.cos(angle),
            body.cy + body.orbit_r * math.sin(angle))


def min_gap(space_objects, step=1):
    """Минимальный зазор между телами РАЗНЫХ звёзд за весь период.
    Тела одной звезды не проверяем: их орбиты концентрические, не пересекаются.
    """
    star1 = [b for b in space_objects if b.type != "star" and b.star_id == 1]
    star2 = [b for b in space_objects if b.type != "star" and b.star_id == 2]
    period = int(round(2 * math.pi / base_step))
    md = 1e30
    for tick in range(0, period, step):
        p1 = [position_at(b, tick) for b in star1]
        p2 = [position_at(b, tick) for b in star2]
        for x1, y1 in p1:
            for x2, y2 in p2:
                d = (x1 - x2) ** 2 + (y1 - y2) ** 2
                if d < md:
                    md = d
    return math.sqrt(md)


def is_safe(space_objects):
    """True, если за период тела разных звёзд не сближаются ближе, чем их диаметр.
    Порог берём из реального радиуса планет в конфиге (он может быть разным —
    в параметрическом варианте радиус задаёт пользователь), а не из константы.
    Поскольку движение периодично, проверка одного периода доказывает безопасность.
    """
    planets = [b for b in space_objects if b.type == "planet"]
    if not planets:
        return True
    planet_r = max(b.R for b in planets)
    # столкновение, если центры ближе суммы радиусов (двух планет) = диаметр
    threshold = planet_r * 2
    return min_gap(space_objects, step=1) > threshold


if __name__ == "__main__":
    print("This module is not for direct call!")
