#!/usr/bin/env python3
"""
Файл для запуска игры из корневой директории проекта.
"""

import sys
import os
import importlib.util

def run_game():
    # Находим путь к основному файлу игры
    main_module_path = os.path.join("ninja_game", "src", "main.py")
    
    if not os.path.exists(main_module_path):
        print(f"Ошибка: Не найден файл {main_module_path}")
        return
    
    # Добавляем путь к директории проекта в sys.path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_dir)
    
    # Загружаем модуль main как спецификацию
    spec = importlib.util.spec_from_file_location("main", main_module_path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    
    # Запускаем функцию main из загруженного модуля
    main_module.main()

if __name__ == "__main__":
    run_game() 