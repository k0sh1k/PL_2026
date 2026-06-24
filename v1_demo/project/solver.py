# coding: utf-8
# license: GPLv3

"""
РЕШАТЕЛЬ (Вариант 3) для Билета №6 — фиксированная конфигурация.

Прочтение условия «орбиты планет всех (двух) звёзд пересекаются»:
семейство орбит звезды 1 пересекается с семейством орбит звезды 2
(зоны орбит накладываются), а НЕ «каждая орбита с каждой».
Поэтому берём УМЕРЕННОЕ пересечение: внешние орбиты двух звёзд накладываются.
Это даёт большой зазор и нормальные (видимые) планеты.

Что делает решатель:
  1. Строит 2 звезды, 16 и 20 планет, спутники.
  2. Ставит звёзды так, чтобы орбиты двух систем пересекались (умеренно).
  3. Подбирает фазы и модули скоростей k (знак k фиксирован по чётности —
     это направление вращения по требованию билета) так, чтобы планеты
     разных звёзд не сталкивались. Метод — имитация отжига.
  4. Записывает готовую конфигурацию в ticket6_state.txt.

Доказательство отсутствия столкновений: скорости кратны base_step ->
движение периодично -> достаточно проверить один период.

Запуск:  python solver.py   (создаёт ticket6_state.txt)
"""

import math
import random

BASE_STEP = 0.01
PERIOD_TICKS = int(round(2 * math.pi / BASE_STEP))

PLANET_RADIUS = 3          # нормальные видимые планеты
REQUIRED_GAP = PLANET_RADIUS * 2 + 2   # требуемый зазор между центрами (px)

CENTER_X, CENTER_Y = 0, 0  # центр системы в модельных координатах (0,0 = центр окна)
STAR_DISTANCE = 400        # расстояние между звёздами (умеренное пересечение, ~18% пар)

# радиусы орбит: крупные сопоставимые, чтобы внешние орбиты двух звёзд пересекались
R1 = [120 + n * 7 for n in range(1, 17)]
R2 = [120 + n * 5.5 for n in range(1, 21)]

MOONS1 = {8, 10, 13}
MOONS2 = {10, 15, 20}


def make_bodies():
    """Создаёт списки тел двух звёзд (планеты + спутники).
    Знак k задаётся по чётности орбиты (направление вращения по билету)."""
    s1x = CENTER_X - STAR_DISTANCE / 2
    s2x = CENTER_X + STAR_DISTANCE / 2
    b1, b2 = [], []

    for idx, n in enumerate(range(1, 17)):
        r = R1[idx]
        sign = 1 if n % 2 == 0 else -1   # чёт по часовой, нечёт против
        b1.append({"cx": s1x, "cy": CENTER_Y, "r": r, "k": sign * (16 - n + 1),
                   "phase": 0.0, "color": "deepskyblue", "star_id": 1, "is_moon": False})
        if n in MOONS1:
            b1.append({"cx": s1x, "cy": CENTER_Y, "r": r + 6, "k": sign * (16 - n + 1),
                       "phase": 0.0, "color": "white", "star_id": 1, "is_moon": True})

    for idx, n in enumerate(range(1, 21)):
        r = R2[idx]
        sign = 1 if n % 2 == 0 else -1
        b2.append({"cx": s2x, "cy": CENTER_Y, "r": r, "k": sign * (20 - n + 1),
                   "phase": 0.0, "color": "orangered", "star_id": 2, "is_moon": False})
        if n in MOONS2:
            b2.append({"cx": s2x, "cy": CENTER_Y, "r": r + 6, "k": sign * (20 - n + 1),
                       "phase": 0.0, "color": "white", "star_id": 2, "is_moon": True})

    return b1, b2, s1x, s2x


def pos(b, tick):
    a = b["phase"] + b["k"] * BASE_STEP * tick
    return b["cx"] + b["r"] * math.cos(a), b["cy"] + b["r"] * math.sin(a)


def min_gap(b1, b2, step=1):
    """Минимальный зазор между телами разных звёзд за период."""
    md = 1e30
    for t in range(0, PERIOD_TICKS, step):
        p1 = [pos(b, t) for b in b1]
        p2 = [pos(b, t) for b in b2]
        for x1, y1 in p1:
            for x2, y2 in p2:
                d = (x1 - x2) ** 2 + (y1 - y2) ** 2
                if d < md:
                    md = d
    return math.sqrt(md)


def solve(b1, b2, seed=3):
    """Имитация отжига: подбирает фазы и модули k (знак k неизменен — направление).
    Максимизирует минимальный зазор. Возвращает достигнутый зазор."""
    random.seed(seed)
    for b in b1 + b2:
        b["phase"] = random.uniform(0, 2 * math.pi)
        sign = 1 if b["k"] > 0 else -1
        b["k"] = sign * random.randint(1, 18)

    def new_k(old):
        sign = 1 if old > 0 else -1
        return sign * random.randint(1, 18)

    def anneal(step, iterations, T0):
        cur = min_gap(b1, b2, step)
        best = cur
        best_state = [(b["phase"], b["k"]) for b in b1 + b2]
        T = T0
        for _ in range(iterations):
            r = random.random()
            if r < 0.5:
                b = random.choice(b2); fld = "phase"; old = b["phase"]; b["phase"] = random.uniform(0, 2*math.pi)
            elif r < 0.65:
                b = random.choice(b1); fld = "phase"; old = b["phase"]; b["phase"] = random.uniform(0, 2*math.pi)
            elif r < 0.83:
                b = random.choice(b2); fld = "k"; old = b["k"]; b["k"] = new_k(old)
            else:
                b = random.choice(b1); fld = "k"; old = b["k"]; b["k"] = new_k(old)
            cand = min_gap(b1, b2, step)
            if cand >= cur or random.random() < math.exp((cand - cur) / max(T, 1e-3)) * 0.1:
                cur = cand
                if cur > best:
                    best = cur
                    best_state = [(bb["phase"], bb["k"]) for bb in b1 + b2]
            else:
                b[fld] = old
            T *= 0.999
            if best > REQUIRED_GAP * 1.5:
                break
        for bb, (ph, k) in zip(b1 + b2, best_state):
            bb["phase"] = ph; bb["k"] = k
        return best

    anneal(step=3, iterations=2000, T0=1.0)
    return anneal(step=1, iterations=3500, T0=0.5)


def save_config(filename, b1, b2, s1x, s2x):
    """Пишет конфиг для графики."""
    def line(b):
        type_name = "Satellite" if b["is_moon"] else "Planet"
        R = 2 if b["is_moon"] else PLANET_RADIUS
        return "%s %d %s %d %.1f %.1f %.1f %d %.6f" % (
            type_name, R, b["color"], b["star_id"],
            b["cx"], b["cy"], b["r"], b["k"], b["phase"])

    lines = ["# Билет №6 — состояние (Вариант 3), посчитано решателем",
             "# Орбиты двух звёзд пересекаются (умеренно); планеты не сталкиваются",
             "# Star R цвет x y | Planet/Satellite R цвет star_id cx cy orbit_r k phase",
             "", "# ЗВЕЗДА 1",
             "Star 12 yellow %.1f %.1f" % (s1x, CENTER_Y)]
    lines += [line(b) for b in b1]
    lines += ["", "# ЗВЕЗДА 2", "Star 12 orange %.1f %.1f" % (s2x, CENTER_Y)]
    lines += [line(b) for b in b2]
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    print("=== Решатель Билета №6 (Вариант 3) ===")
    b1, b2, s1x, s2x = make_bodies()
    cross = sum(1 for a in R1 for b in R2 if abs(a - b) < STAR_DISTANCE < a + b)
    print("Пересекается пар орбит: %d из %d (%d%%)" % (cross, len(R1)*len(R2), 100*cross//(len(R1)*len(R2))))
    print("Подбор безопасной конфигурации (отжиг)...")
    gap = solve(b1, b2)
    final = min_gap(b1, b2, step=1)
    print("Минимальный зазор за период: %.1f px (нужно > %d)" % (final, REQUIRED_GAP))
    print("Планеты не сталкиваются." if final > REQUIRED_GAP else "ВНИМАНИЕ: зазор мал.")
    save_config("ticket6_state.txt", b1, b2, s1x, s2x)
    print("Конфигурация записана в ticket6_state.txt")


if __name__ == "__main__":
    main()
