#!/usr/bin/env python3
"""
Скрипт для отладки проблем с ресурсами
"""

import os
import sys
import pygame

def analyze_resources():
    print("\n===== ОТЛАДКА ПУТЕЙ К РЕСУРСАМ =====\n")
    
    # Текущая директория
    print(f"Текущая директория: {os.getcwd()}")
    print(f"sys.executable: {sys.executable}")
    
    try:
        # Проверка PyInstaller
        if hasattr(sys, '_MEIPASS'):
            print(f"Запущено из PyInstaller. _MEIPASS = {sys._MEIPASS}")
            base_dir = sys._MEIPASS
        else:
            print("Запущено напрямую (не через PyInstaller)")
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        print(f"Базовая директория: {base_dir}")
        
        # Проверка структуры директорий
        ninja_game_dir = os.path.join(base_dir, "ninja_game")
        assets_dir = os.path.join(ninja_game_dir, "assets")
        sounds_dir = os.path.join(assets_dir, "sounds")
        
        print("\nПроверяем наличие директорий:")
        print(f"ninja_game: {os.path.exists(ninja_game_dir)} ({ninja_game_dir})")
        print(f"assets: {os.path.exists(assets_dir)} ({assets_dir})")
        print(f"sounds: {os.path.exists(sounds_dir)} ({sounds_dir})")
        
        # Проверяем содержимое директорий
        if os.path.exists(assets_dir):
            print("\nСодержимое директории assets:")
            for item in os.listdir(assets_dir):
                item_path = os.path.join(assets_dir, item)
                if os.path.isdir(item_path):
                    print(f"  [DIR] {item}")
                else:
                    print(f"  [FILE] {item} ({os.path.getsize(item_path)} bytes)")
        
        if os.path.exists(sounds_dir):
            print("\nСодержимое директории sounds:")
            for item in os.listdir(sounds_dir):
                item_path = os.path.join(sounds_dir, item)
                if os.path.isdir(item_path):
                    print(f"  [DIR] {item}")
                else:
                    print(f"  [FILE] {item} ({os.path.getsize(item_path)} bytes)")
        
        # Проверяем загрузку звуков
        print("\nПытаемся инициализировать pygame и загрузить звуки:")
        pygame.mixer.init()
        
        sound_files = {
            "jump": os.path.join(sounds_dir, "jump.wav"),
            "attack": os.path.join(sounds_dir, "attack.wav"),
            "hit": os.path.join(sounds_dir, "hit.wav"),
            "game_over": os.path.join(sounds_dir, "game_over.wav")
        }
        
        for name, path in sound_files.items():
            print(f"Звук {name}: ", end="")
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    print(f"загружен успешно ({path})")
                except Exception as e:
                    print(f"ошибка загрузки: {e} ({path})")
            else:
                print(f"файл не найден ({path})")
        
        print("\n===== ОТЛАДКА ЗАВЕРШЕНА =====\n")
        
    except Exception as e:
        print(f"Произошла ошибка при анализе ресурсов: {e}")

if __name__ == "__main__":
    analyze_resources()
    input("Нажмите Enter для выхода...") 