#!/usr/bin/env python3
"""
Скрипт для создания исполняемого файла с помощью PyInstaller
"""

import os
import subprocess
import shutil
import sys

def build_executable():
    # Имя исходного файла Python
    source_file = "build_game.py"
    
    # Имя исполняемого файла (без расширения .exe)
    exe_name = "NinjaGame"
    
    # Проверяем наличие исходного файла
    if not os.path.exists(source_file):
        print(f"Ошибка: Исходный файл {source_file} не найден.")
        return
    
    # Строим команду для PyInstaller
    command = [
        "pyinstaller",
        "--onefile",  # Создает один исполняемый файл
        "--windowed",  # Без консольного окна
        f"--name={exe_name}",  # Имя выходного файла
        "--icon=ninja_game/assets/icon.ico" if os.path.exists("ninja_game/assets/icon.ico") else "",
        "--add-data=ninja_game/assets;ninja_game/assets",  # Добавляем ресурсы игры
        "--hidden-import=pygame",
        "--hidden-import=pygame.mixer",
        "--hidden-import=pygame.font",
        "--hidden-import=pygame.draw",
        "--hidden-import=pygame.display",
        "--hidden-import=pygame.event",
        "--hidden-import=pygame.key",
        "--hidden-import=pygame.rect",
        source_file
    ]
    
    # Удаляем пустые элементы
    command = [cmd for cmd in command if cmd]
    
    try:
        # Запускаем PyInstaller
        print("Запуск PyInstaller для создания исполняемого файла...")
        subprocess.run(command, check=True)
        
        print(f"Исполняемый файл успешно создан: dist/{exe_name}.exe")
        print("Вы можете запустить игру, дважды щелкнув по этому файлу.")
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании исполняемого файла: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")

if __name__ == "__main__":
    build_executable() 