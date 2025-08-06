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
    
    # Добавьте сюда вашу логику для выбранной операции
    print(f"Источник: {source_dir}, Цель: {target_dir}, Режим: {mode}")
    result_message = sorter.photosorter(source_dir,target_dir,mode)
    messagebox.showinfo("Информация", f"Операция '{mode}' выполнена.\n{result_message}")


# Настройка основного окна
root = tk.Tk()
root.title("Фото-Сортировка. Создание поддиректорий с датой создания и переворотом при необходимости")
root.geometry("850x130")
# Установка иконки окна (для Windows нужен формат .ico)
#root.iconbitmap("doc/icon.ico")  # icon.ico - имя файла вашей иконки
# Исходный каталог
initial_directory = os.getcwd()

# Используем grid для размещения элементов
source_label = tk.Label(root, text="Исходный каталог:")
source_label.grid(row=0, column=0, sticky='e')  # Помещаем элемент в первую строку, нулевой столбец

source_entry = tk.Entry(root, width=100)
source_entry.insert(0, initial_directory)  # Устанавливаем начальное значение
source_entry.grid(row=0, column=1, padx=(5, 0))  # Расположили рядом справа от лейбла

source_browse_button = tk.Button(root, text="Обзор...", command=select_source_dir)
source_browse_button.grid(row=0, column=2, padx=(5, 0))  # Расположили справа от поля ввода

# Целевой каталог
target_label = tk.Label(root, text="Целевой каталог:")
target_label.grid(row=1, column=0, sticky='e')  # Следующая строка

target_entry = tk.Entry(root, width=100)
target_entry.grid(row=1, column=1, padx=(5, 0))

target_browse_button = tk.Button(root, text="Обзор...", command=select_target_dir)
target_browse_button.grid(row=1, column=2, padx=(5, 0))


# Выбор режима
mode_label = tk.Label(root, text="Режим:")
mode_label.grid(row=2, column=0, sticky='e')

#modes = ["Только посчитать файлы", "Создавать подкаталоги с датой создания и переворачивать", "И прикладывать к дате и адрес на основе геолокации"]
# Готовим словарь режимов
modes_dict = {
    "Только посчитать": "count",
    "Создавать подкаталоги с датой создания и переворачивать": "create",
    "И прикладывать к дате и адрес на основе геолокации": "geotag"
}

# Список отображаемых значений
modes_list = list(modes_dict.keys())

mode_combobox = ttk.Combobox(root, values=modes_list,width=90)
mode_combobox.current(0)  # Устанавливаем первый пункт по умолчанию
mode_combobox.grid(row=2, column=1,sticky='w', padx=(5, 0))

# Кнопка запуска
execute_button = tk.Button(root, text="Запустить", command=execute_process)
#execute_button.place(x=350, y=230)
execute_button.grid(row=2, column=2, sticky='w')

# Кнопка закрытия
exit_button = tk.Button(root, text="Выход", command=root.destroy)
#exit_button.place(x=420, y=230)
exit_button.grid(row=3, column=1, sticky='w')

def on_escape(event):
    root.destroy()  # Закрываем главное окно приложения

root.bind('<Escape>', on_escape)

# Запуск основного цикла
root.mainloop()
