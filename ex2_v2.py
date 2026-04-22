import random

def generate_sorted_array():
    """Создаёт случайный отсортированный массив целых чисел.
       Размер N от 5 до 15, числа от -30 до 30."""
    N = random.randint(5, 15)
    arr = []
    for shtoto in range(N):
        arr.append(random.randint(-30, 30))
    arr.sort()
    return arr

def find_pair_with_binary_search(arr, K):
    n = len(arr)
    
    for i in range(n):
        target = K - arr[i]  # число кот нужно найти в паре
        
        # Ищем target в массиве начиная с i+1 (чтобы не использовать один элемент дважды)
        left = i + 1
        right = n - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return (arr[i], arr[mid])  # нашли пару!
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
    
    return None  # пары нет

# Основная программа с подсчётом неудачных попыток
attempts = 0
Flag = 0
while Flag == 0:
    attempts += 1
    arr = generate_sorted_array()
    K = random.randint(-50, 50)
    pair = find_pair_with_binary_search(arr, K)
    
    if pair is not None:
        print(f"Удачная попытка #{attempts}")
        print(f"Массив: {arr}")
        print(f"K = {K}")
        print(f"Найденная пара: {pair[0]} + {pair[1]} = {K}")
        Flag = 1
    else:
        # Неудачная попытка, продолжаем
        pass