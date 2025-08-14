import os
from sorter import photosorter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json

CONFIG_FILE = "photosorter_config.json"

def load_config():
    """Загружает конфигурацию из файла"""
    default_config = {
        "source_dir": os.getcwd(),
        "target_dir": "",
        "geo_round": 3,
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
        "geo_round": round_entry.get(),
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
        result_message = photosorter(
            source_dir,
            target_dir,
            mode,
            progress_callback=update_progress,
            geo_rou=round_entry.get()
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

class CreateToolTip:
    def __init__(self, widget, text='widget info'):
        self.waittime = 500   # задержка перед показом в миллисекундах
        self.wraplength = 180 # длина строки текста подсказки
        self.widget = widget
        self.text = text
        
        # привязываем события Enter и Leave
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()
    
    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
    
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)
    
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    
    def showtip(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")  # координаты позиции внутри виджета
        x += self.widget.winfo_rootx() + 25      # добавляем смещение относительно окна приложения
        y += self.widget.winfo_rooty() + 20
        
        # создаём временное окно сверху текущего виджета
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)       # скрываем стандартное оформление окна
        self.tw.wm_geometry("+%d+%d" % (x, y))  # устанавливаем позицию окна
        
        # создаем лейбл с текстом подсказки
        label = tk.Label(self.tw, text=self.text, justify='left',
                        background="#ffffff", relief='solid', borderwidth=1,
                        wraplength=self.wraplength)
        label.pack(ipadx=1)
    
    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

#==============================================================
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

round_entry = tk.Entry(root, width=10)
round_entry.insert(0, config.get("geo_round",4))
round_entry.grid(row=3, column=2, padx=(5, 0))


# Создание всплывающей подсказки
entry_tool_tip = CreateToolTip(round_entry, 'Точность геокодирования, количество знаков после запятой у широты и долготы.')

# Прогресс-бар и метка (изначально скрыты)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=830, mode="determinate")
progress_label = tk.Label(root, text="")

def on_escape(event):
    save_config()
    root.destroy()

root.bind('<Escape>', on_escape)

root.mainloop()