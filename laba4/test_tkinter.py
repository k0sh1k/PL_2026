import tkinter as tk

# Создаем главное окно
root = tk.Tk()
root.title("Проверка Tkinter")
root.geometry("300x200")

# Добавляем текстовую метку
label = tk.Label(root, text="Tkinter работает!")
label.pack(pady=50)

# Запускаем цикл обработки событий
root.mainloop()