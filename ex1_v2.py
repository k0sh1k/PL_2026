import random


def bfs_shortest_path(maze, start_x, start_y, N, M):
    """BFS поиск кратчайшего пути до границы (выхода).
    Возвращает: (found, steps, exit_x, exit_y)"""
    
    # Массив расстояний (-1 = не посещена)
    dist = [[-1] * M for _ in range(N)]
    
    # Очередь на массиве (размер N*M)
    ochered = [(0, 0)] * (N * M)
    head = 0
    tail = 0
    
    # Старт
    ochered[tail] = (start_x, start_y)
    tail += 1
    dist[start_x][start_y] = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while head < tail:
        x, y = ochered[head]
        head += 1
        
        # Проверяем, является ли текущая клетка выходом (граница и не старт)
        if (x == 0 or x == N-1 or y == 0 or y == M-1) and (x != start_x or y != start_y):
            return True, dist[x][y], x, y  # все круто
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < M:
                if maze[nx][ny] == '.' and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    ochered[tail] = (nx, ny)
                    tail += 1
    
    return False, -1, -1, -1   # выхода неееет

def generate_array_with_exit():
    """Генерирует лабиринт N x M (случайные размеры 5-12),
    случайно заполненный '.' (проход) и '+' (стена),
    со случайной стартовой клеткой, из которой есть выход на границу.
    Возвращает: (maze, N, M, start_x, start_y)"""
    
    Flag = 0

    while Flag == 0:

        # 1. Случайные размеры
        N = random.randint(5, 12)
        M = random.randint(5, 12)

        # 2. Создаем лабиринт N x M, заполняя каждый элемент в циклах

        array = []
        vse_tochki = []                  
        for i in range(N):
            # создаем новую строку
            row = []                  
            for j in range(M):
                # С вероятностью 30% ставим стену '+', иначе проход '.'
                if random.random() < 0.3:
                    row.append('+')
                else:
                    row.append('.')
                    vse_tochki.append([i, j])
            array.append(row)

        # 3. Proverka na to shto vse_tochki pystoi
        if not vse_tochki:
            continue

        # Выбираем случайный старт
        start_index = random.randint(0, len(vse_tochki) - 1)
        start_x, start_y = vse_tochki[start_index]

        # exit_exists = bfs_has_exit(array, start_x, start_y, N, M)
        found, lishnee1, lishnee2, lishnee3 = bfs_shortest_path(array, start_x, start_y, N, M)
        if found:
            Flag = 1
            return array, N, M, start_x, start_y

# Проверка

maze, N, M, sx, sy = generate_array_with_exit()

print(f"Лабиринт создан!")
print(f"Размер: {N} x {M}")
print(f"Старт: ({sx}, {sy})")

# Печать лабиринта
for i in range(N):
    for j in range(M):
        print(maze[i][j], end=' ')
    print()

# Поиск кратчайшего пути
found, steps, ex, ey = bfs_shortest_path(maze, sx, sy, N, M)

if found:
    print(f"Выход найден! Шагов: {steps}")
    print(f"Координаты выхода: ({ex}, {ey})")
else:
    print(False)