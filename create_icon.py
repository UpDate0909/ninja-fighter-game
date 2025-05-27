#!/usr/bin/env python3
"""
Скрипт для создания простой иконки для игры
"""
import os
from PIL import Image, ImageDraw

def create_ninja_icon():
    # Создаем директорию для иконки, если она не существует
    icon_dir = os.path.join("ninja_game", "assets")
    os.makedirs(icon_dir, exist_ok=True)
    
    # Размер иконки
    icon_size = 256
    img = Image.new('RGBA', (icon_size, icon_size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Фон (круг)
    background_color = (30, 30, 30, 255)
    draw.ellipse((10, 10, icon_size-10, icon_size-10), fill=background_color)
    
    # Рисуем силуэт ниндзя (упрощенный)
    ninja_color = (255, 0, 0, 255)  # Красный
    
    # Голова
    head_center = (icon_size // 2, icon_size // 2 - 30)
    head_radius = icon_size // 6
    draw.ellipse((head_center[0] - head_radius, head_center[1] - head_radius,
                 head_center[0] + head_radius, head_center[1] + head_radius),
                 fill=ninja_color)
    
    # Тело
    body_width = icon_size // 3
    body_height = icon_size // 2
    draw.rectangle((icon_size // 2 - body_width // 2, head_center[1] + head_radius,
                   icon_size // 2 + body_width // 2, head_center[1] + head_radius + body_height),
                  fill=ninja_color)
    
    # Меч
    sword_color = (200, 200, 200, 255)  # Серебристый
    sword_start = (icon_size // 2 + body_width // 2, head_center[1] + head_radius + body_height // 3)
    sword_end = (icon_size - 30, head_center[1] + head_radius - 20)
    draw.line([sword_start, sword_end], fill=sword_color, width=5)
    
    # Сохраняем иконку
    icon_path = os.path.join(icon_dir, "icon.ico")
    img.save(icon_path, format='ICO', sizes=[(256, 256)])
    
    print(f"Иконка создана: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_ninja_icon() 