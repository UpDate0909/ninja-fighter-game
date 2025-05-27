#!/usr/bin/env python3
"""
Простой запуск игры напрямую из исходников
"""
import os
import sys
import subprocess

def main():
    try:
        print("===== ПРЯМОЙ ЗАПУСК NINJA GAME =====")
        
        # Устанавливаем pygame, если он не установлен
        try:
            import pygame
            print("Pygame уже установлен.")
        except ImportError:
            print("Устанавливаем pygame...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            import pygame
            print("Pygame успешно установлен.")
        
        # Добавляем пути к директориям
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(current_dir, "ninja_game", "src")
        
        # Проверяем наличие директории src
        if not os.path.exists(src_path):
            print(f"Ошибка: Директория src не найдена по пути {src_path}")
            return
        
        # Добавляем пути в sys.path
        sys.path.append(current_dir)
        sys.path.append(src_path)
        
        # Запускаем игру
        print(f"Запускаем игру из {src_path}...")
        
        # Получаем полный путь к main.py
        main_path = os.path.join(src_path, "main.py")
        if not os.path.exists(main_path):
            print(f"Ошибка: Файл main.py не найден по пути {main_path}")
            return
        
        # Запускаем с помощью subprocess для отображения вывода в консоли
        result = subprocess.run([sys.executable, main_path], cwd=current_dir)
        
        if result.returncode != 0:
            print(f"Игра завершилась с кодом ошибки: {result.returncode}")
        else:
            print("Игра успешно завершена.")
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main() 