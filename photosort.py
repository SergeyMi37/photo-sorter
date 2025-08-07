import os
import sorter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json

CONFIG_FILE = "photosorter_config.json"

def load_config():
    """Загружает конфигурацию из файла"""
    default_config = {
        "source_dir": os.getcwd(),
        "target_dir": "",
        "mode_index": 0
    }
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return default_config

def save_config():
    """Сохраняет текущую конфигурацию в файл"""
    config = {
        "source_dir": source_entry.get(),
        "target_dir": target_entry.get(),
        "mode_index": mode_combobox.current()
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def select_source_dir():
    """Открывает диалог выбора исходного каталога"""
    dir_name = filedialog.askdirectory()
    if dir_name:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, dir_name)

def select_target_dir():
    """Открывает диалог выбора целевого каталога"""
    dir_name = filedialog.askdirectory()
    if dir_name:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, dir_name)

def update_progress(current, total):
    """Обновляет прогресс-бар"""
    progress = (current / total) * 100
    progress_bar['value'] = progress
    progress_label.config(text=f"Обработано {current} из {total} файлов")
    root.update_idletasks()

def execute_process():
    """Выполняет основную операцию"""
    source_dir = source_entry.get()
    target_dir = target_entry.get()
    mode = modes_dict.get(mode_combobox.get())
    
    if not source_dir or not target_dir:
        messagebox.showwarning("Ошибка", "Укажите оба каталога!")
        return
    
    # Блокируем кнопки во время выполнения
    execute_button.config(state=tk.DISABLED)
    exit_button.config(state=tk.DISABLED)
    
    # Показываем прогресс-бар
    progress_bar.grid(row=4, column=0, columnspan=3, sticky='we', padx=5, pady=5)
    progress_bar['value'] = 0
    progress_label.grid(row=5, column=0, columnspan=3)
    root.update_idletasks()
    
    try:
        # Сохраняем текущие настройки
        save_config()
        
        # Передаем функцию обновления прогресса в sorter.photosorter
        result_message = sorter.photosorter(
            source_dir,
            target_dir,
            mode,
            progress_callback=update_progress
        )
        messagebox.showinfo("Информация", f"Операция '{mode}' выполнена.\n{result_message}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    finally:
        # Восстанавливаем интерфейс
        progress_bar.grid_forget()
        progress_label.grid_forget()
        execute_button.config(state=tk.NORMAL)
        exit_button.config(state=tk.NORMAL)

# Настройка основного окна
root = tk.Tk()
root.title("Фото-Сортировка. Создание поддиректорий с датой создания и переворотом при необходимости")
root.geometry("850x180")

# Загружаем сохраненную конфигурацию
config = load_config()

# Элементы интерфейса
source_label = tk.Label(root, text="Исходный каталог:")
source_label.grid(row=0, column=0, sticky='e')

source_entry = tk.Entry(root, width=100)
source_entry.insert(0, config["source_dir"])
source_entry.grid(row=0, column=1, padx=(5, 0))

source_browse_button = tk.Button(root, text="Обзор...", command=select_source_dir)
source_browse_button.grid(row=0, column=2, padx=(5, 0))

target_label = tk.Label(root, text="Целевой каталог:")
target_label.grid(row=1, column=0, sticky='e')

target_entry = tk.Entry(root, width=100)
target_entry.insert(0, config["target_dir"])
target_entry.grid(row=1, column=1, padx=(5, 0))

target_browse_button = tk.Button(root, text="Обзор...", command=select_target_dir)
target_browse_button.grid(row=1, column=2, padx=(5, 0))

mode_label = tk.Label(root, text="Режим:")
mode_label.grid(row=2, column=0, sticky='e')

modes_dict = {
    "Только посчитать": "count",
    "Создавать подкаталоги с датой создания и переворачивать": "create",
    "И прикладывать к дате и адрес на основе геолокации": "geotag"
}

modes_list = list(modes_dict.keys())
mode_combobox = ttk.Combobox(root, values=modes_list, width=90)
mode_combobox.current(config["mode_index"])
mode_combobox.grid(row=2, column=1, sticky='w', padx=(5, 0))

execute_button = tk.Button(root, text="Запустить", command=execute_process)
execute_button.grid(row=2, column=2, sticky='w')

exit_button = tk.Button(root, text="Выход", command=lambda: [save_config(), root.destroy()])
exit_button.grid(row=3, column=1, sticky='w')

# Прогресс-бар и метка (изначально скрыты)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=830, mode="determinate")
progress_label = tk.Label(root, text="")

def on_escape(event):
    save_config()
    root.destroy()

root.bind('<Escape>', on_escape)

root.mainloop()