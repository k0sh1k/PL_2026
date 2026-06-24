# coding: utf-8
# license: GPLv3

"""
ГЛАВНЫЙ (графический) модуль — Вариант 3.

Читает готовую конфигурацию ticket6_state.txt (её посчитал solver.py)
и показывает анимацию. Сам ничего не подбирает.

Порядок работы:
  1) python solver.py       — создаёт ticket6_state.txt
  2) python solar_main.py   — показывает анимацию

Кнопка «Скрыть/Показать орбиты» включает и выключает отображение орбит.
"""

import tkinter
from solar_vis import *
from solar_model import *
from solar_input import *

perform_execution = False
space_objects = []
orbits_visible = True


def execution():
    """Один кадр анимации: сдвинуть углы, пересчитать координаты, перерисовать."""
    step_angles(space_objects)
    update_positions(space_objects)
    for body in space_objects:
        update_object_position(space, body)
    if perform_execution:
        space.after(20, execution)


def start_execution():
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution
    execution()


def stop_execution():
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution


def toggle_orbits():
    """Кнопка показа/скрытия орбит."""
    global orbits_visible
    orbits_visible = not orbits_visible
    state = "normal" if orbits_visible else "hidden"
    for obj in space_objects:
        if getattr(obj, "orbit", None) is not None:
            space.itemconfig(obj.orbit, state=state)
    orbits_button['text'] = "Скрыть орбиты" if orbits_visible else "Показать орбиты"


def load():
    """Читает конфиг, проверяет безопасность (для контроля) и рисует."""
    global space_objects
    space_objects = read_space_objects_data_from_file("ticket6_state.txt")

    # контрольная проверка: подтверждаем, что конфиг безопасен (по периоду)
    if is_safe(space_objects):
        print("Проверка: планеты разных звёзд не сталкиваются.")
    else:
        print("ВНИМАНИЕ: в конфиге обнаружены сближения — перезапустите solver.py")

    update_positions(space_objects)
    # сначала орбиты (под телами), потом тела
    for obj in space_objects:
        if obj.type in ("planet", "satellite"):
            create_orbit_image(space, obj)
    for obj in space_objects:
        create_body_image(space, obj)


def main():
    global space, start_button, orbits_button

    root = tkinter.Tk()
    root.title("Билет №6 - Солнечная система (Вариант 3)")
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)

    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)

    orbits_button = tkinter.Button(frame, text="Скрыть орбиты", command=toggle_orbits)
    orbits_button.pack(side=tkinter.LEFT)

    update_system_name(space, "Билет №6: две звезды")
    load()

    root.mainloop()


if __name__ == "__main__":
    main()
