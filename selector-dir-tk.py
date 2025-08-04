import os
from tkinter import Tk, filedialog

def select_directory(tit=''):
    root = Tk()
    root.withdraw()  # Скрываем основное окно
    folder = filedialog.askdirectory(title=tit)
    root.destroy()
    return folder if folder else os.getcwd()

sour = select_directory("Выберите исходную директорию с фотографиями")
terg = select_directory("Выберите целевую директорию для сохранения обработанных фотографий")
print(f"Выбраны: \n{sour}\n{terg}")
