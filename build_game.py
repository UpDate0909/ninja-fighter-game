#!/usr/bin/env python3
"""
Файл для сборки исполняемого файла игры.
"""

import sys
import os
import importlib.util
import subprocess

# Проверяем, установлен ли pygame, и устанавливаем его при необходимости
try:
    import pygame
    print("Pygame уже установлен.")
except ImportError:
    print("Pygame не установлен. Устанавливаем...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame
        print("Pygame успешно установлен.")
    except Exception as e:
        print(f"Ошибка при установке pygame: {e}")
        print("Пожалуйста, установите pygame вручную: pip install pygame")
        sys.exit(1)

# Определяем функцию для получения пути к ресурсам
def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, работает как для разработки, 
        так и для исполняемого файла PyInstaller """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Добавляем путь к директории проекта в sys.path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Переопределяем переменные путей в основном модуле
os.environ["NINJA_GAME_ASSETS"] = resource_path("ninja_game/assets")

def main():
    # Находим путь к основному файлу игры
    main_module_path = os.path.join(project_dir, "ninja_game", "src", "main.py")
    
    if not os.path.exists(main_module_path):
        print(f"Ошибка: Не найден файл {main_module_path}")
        return
    
    # Загружаем модуль main как спецификацию
    spec = importlib.util.spec_from_file_location("main", main_module_path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    
    # Запускаем функцию main из загруженного модуля
    main_module.main()

if __name__ == "__main__":
    main() 