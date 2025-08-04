# # Обычно уже установлен
# sudo apt-get install libncurses5-dev libncursesw5-dev  # Для Debian/Ubuntu

# Для Windows:
# Установите windows-curses:
# bash
# pip install windows-curses
import os
import curses

def select_directory(start_path="."):
    """TUI-выбор директории в стиле MC"""
    try:
        screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        screen.keypad(True)
        
        current_path = os.path.abspath(start_path)
        selected_idx = 0
        
        while True:
            items = [".."] + [d for d in os.listdir(current_path) 
                          if os.path.isdir(os.path.join(current_path, d))]
            
            screen.clear()
            screen.addstr(0, 0, f"Директория: {current_path}")
            
            for idx, item in enumerate(items):
                screen.addstr(idx + 2, 0, 
                            f"{'>' if idx == selected_idx else ' '} {item}",
                            curses.A_REVERSE if idx == selected_idx else curses.A_NORMAL)
            
            key = screen.getch()
            
            if key == curses.KEY_UP and selected_idx > 0:
                selected_idx -= 1
            elif key == curses.KEY_DOWN and selected_idx < len(items) - 1:
                selected_idx += 1
            elif key in (curses.KEY_ENTER, 10, 13):  # Enter
                chosen = items[selected_idx]
                new_path = os.path.dirname(current_path) if chosen == ".." \
                          else os.path.join(current_path, chosen)
                if os.path.exists(new_path):
                    current_path = new_path
                    selected_idx = 0
            elif key == ord("q"):
                break
                
    finally:
        curses.endwin()
    
    return current_path

if __name__ == "__main__":
    path = select_directory("")
    print(f"\nВыбрано: {path}")