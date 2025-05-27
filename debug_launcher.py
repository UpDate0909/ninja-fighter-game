#!/usr/bin/env python3
"""
Обертка для запуска игры с паузой перед закрытием консоли
"""

import sys
import os
import traceback

def main():
    try:
        print("===== ЗАПУСК NINJA GAME С ПЕРЕХВАТОМ ОШИБОК =====")
        print("Если игра завершится с ошибкой, консоль не закроется автоматически.")
        print()
        
        # Импортируем и запускаем основной файл игры
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Пытаемся импортировать build_game и запустить его
        try:
            import build_game
            build_game.main()
        except ImportError as e:
            print(f"Ошибка импорта модуля build_game: {e}")
            print("Пробуем запустить игру напрямую...")
            
            # Если не удалось импортировать build_game, пробуем загрузить main.py напрямую
            try:
                sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ninja_game", "src"))
                from ninja_game.src.main import main
                main()
            except ImportError as e2:
                print(f"Ошибка импорта основного модуля игры: {e2}")
                raise Exception("Не удалось запустить игру") from e2
                
    except Exception as e:
        print("\n===== ПРОИЗОШЛА ОШИБКА =====")
        print(f"Ошибка: {e}")
        print("\nПодробная информация об ошибке:")
        traceback.print_exc()
        
        print("\n===== СОДЕРЖИМОЕ ДИРЕКТОРИЙ =====")
        
        # Выводим содержимое текущей директории
        current_dir = os.getcwd()
        print(f"\nТекущая директория ({current_dir}):")
        try:
            for item in os.listdir(current_dir):
                if os.path.isdir(os.path.join(current_dir, item)):
                    print(f"  [DIR] {item}")
                else:
                    print(f"  [FILE] {item}")
        except Exception as dir_error:
            print(f"Ошибка при чтении директории: {dir_error}")
        
        # Проверяем наличие ninja_game
        ninja_game_dir = os.path.join(current_dir, "ninja_game")
        if os.path.exists(ninja_game_dir):
            print(f"\nДиректория ninja_game ({ninja_game_dir}):")
            try:
                for item in os.listdir(ninja_game_dir):
                    if os.path.isdir(os.path.join(ninja_game_dir, item)):
                        print(f"  [DIR] {item}")
                    else:
                        print(f"  [FILE] {item}")
            except Exception as ng_error:
                print(f"Ошибка при чтении директории ninja_game: {ng_error}")
        else:
            print("\nДиректория ninja_game не найдена!")
        
        # Проверяем наличие src в ninja_game
        src_dir = os.path.join(ninja_game_dir, "src")
        if os.path.exists(src_dir):
            print(f"\nДиректория src ({src_dir}):")
            try:
                for item in os.listdir(src_dir):
                    if os.path.isdir(os.path.join(src_dir, item)):
                        print(f"  [DIR] {item}")
                    else:
                        print(f"  [FILE] {item}")
            except Exception as src_error:
                print(f"Ошибка при чтении директории src: {src_error}")
        else:
            print("\nДиректория src не найдена!")
            
        print("\n===== ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ =====")
        for key, value in os.environ.items():
            if "PATH" in key or "PYTHON" in key:
                print(f"{key}: {value}")
        
        # Пауза перед закрытием
        print("\n===== ПРОГРАММА ЗАВЕРШЕНА С ОШИБКОЙ =====")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    print("\n===== ИГРА ЗАВЕРШЕНА УСПЕШНО =====")
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main() 