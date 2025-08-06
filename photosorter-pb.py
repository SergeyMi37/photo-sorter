# Вот модифицированный код с добавлением прогрессбара:

# ```python
import os
import sorter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def select_source_dir():
    """ Открывает диалог выбора исходного каталога """
    dir_name = filedialog.askdirectory()
    if dir_name:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, dir_name)

def select_target_dir():
    """ Открывает диалог выбора целевого каталога """
    dir_name = filedialog.askdirectory()
    if dir_name:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, dir_name)

def execute_process():
    """ Выполняет основную операцию (копирование, перенос и т.п.) """
    source_dir = source_entry.get()
    target_dir = target_entry.get()
    mode = modes_dict.get(mode_combobox.get())
    
    if not source_dir or not target_dir:
        messagebox.showwarning("Ошибка", "Укажите оба каталога!")
        return
    
    # Блокируем кнопки во время выполнения
    execute_button.config(state=tk.DISABLED)
    exit_button.config(state=tk.DISABLED)
    
    # Создаем прогрессбар
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky='ew')
    root.update()  # Обновляем интерфейс
    
    try:
        # Здесь должна быть ваша логика обработки с обновлением прогрессбара
        # В данном примере просто имитируем прогресс
        total_files = 100  # Это нужно заменить на реальное количество файлов
        for i in range(total_files):
            # Ваш код обработки каждого файла
            progress = (i + 1) / total_files * 100
            progress_bar["value"] = progress
            root.update_idletasks()  # Обновляем прогрессбар
            # Имитация работы
            root.after(50)  # Небольшая задержка для демонстрации
        
        result_message = sorter.photosorter(source_dir, target_dir, mode)
        messagebox.showinfo("Информация", f"Операция '{mode}' выполнена.\n{result_message}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    finally:
        # Восстанавливаем кнопки и удаляем прогрессбар
        execute_button.config(state=tk.NORMAL)
        exit_button.config(state=tk.NORMAL)
        progress_bar.destroy()

# Настройка основного окна
root = tk.Tk()
root.title("Фото-Сортировка. Создание поддиректорий с датой создания и переворотом при необходимости")
root.geometry("850x180")  # Увеличили высоту окна для прогрессбара

# Исходный каталог
initial_directory = os.getcwd()

# Используем grid для размещения элементов
source_label = tk.Label(root, text="Исходный каталог:")
source_label.grid(row=0, column=0, sticky='e')

source_entry = tk.Entry(root, width=100)
source_entry.insert(0, initial_directory)
source_entry.grid(row=0, column=1, padx=(5, 0))

source_browse_button = tk.Button(root, text="Обзор...", command=select_source_dir)
source_browse_button.grid(row=0, column=2, padx=(5, 0))

# Целевой каталог
target_label = tk.Label(root, text="Целевой каталог:")
target_label.grid(row=1, column=0, sticky='e')

target_entry = tk.Entry(root, width=100)
target_entry.insert(0, initial_directory)
target_entry.grid(row=1, column=1, padx=(5, 0))

target_browse_button = tk.Button(root, text="Обзор...", command=select_target_dir)
target_browse_button.grid(row=1, column=2, padx=(5, 0))

# Выбор режима
mode_label = tk.Label(root, text="Режим:")
mode_label.grid(row=2, column=0, sticky='e')

modes_dict = {
    "Только посчитать": "count",
    "Создавать подкаталоги с датой создания и переворачивать": "create",
    "И прикладывать к дате и адрес на основе геолокации": "geotag"
}

modes_list = list(modes_dict.keys())
mode_combobox = ttk.Combobox(root, values=modes_list, width=90)
mode_combobox.current(0)
mode_combobox.grid(row=2, column=1, sticky='w', padx=(5, 0))

# Кнопка запуска
execute_button = tk.Button(root, text="Запустить", command=execute_process)
execute_button.grid(row=2, column=2, sticky='w')

# Кнопка закрытия
exit_button = tk.Button(root, text="Выход", command=root.destroy)
exit_button.grid(row=3, column=1, sticky='w')

def on_escape(event):
    root.destroy()

root.bind('<Escape>', on_escape)

# Запуск основного цикла
root.mainloop()
# ```

# Основные изменения:
# 1. Увеличил высоту окна для размещения прогрессбара
# 2. Добавил прогрессбар в строку 4 (row=4)
# 3. Модифицировал функцию execute_process():
#    - Блокирует кнопки во время выполнения
#    - Создает и отображает прогрессбар
#    - Обновляет прогрессбар во время работы
#    - Удаляет прогрессбар после завершения
#    - Восстанавливает кнопки после завершения

# Примечание: В текущей реализации используется имитация прогресса. Вам нужно будет адаптировать код для обновления прогрессбара в соответствии с реальным прогрессом обработки файлов в вашей функции `sorter.photosorter()`.