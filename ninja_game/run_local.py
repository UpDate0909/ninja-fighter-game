#!/usr/bin/env python3
"""
Файл для запуска игры из директории ninja_game.
"""

import sys
import os

# Добавляем путь к директории src в sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# Импортируем и запускаем main
try:
    from src.main import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что вы запускаете игру из директории ninja_game") 