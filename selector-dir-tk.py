# 
import os
from tkinter import Tk, filedialog
import sorter

def select_directory(tit=''):
    root = Tk()
    root.withdraw()  # Скрываем основное окно
    folder = filedialog.askdirectory(title=tit)
    root.destroy()
    return folder if folder else os.getcwd()

s = select_directory("Выберите исходную директорию с фотографиями")
t = select_directory("Выберите целевую директорию для сохранения обработанных фотографий")
print(f"Выбраны: \n{s}\n{t}")
# y N 
sorter.photosorter(s,t)
