@echo off
echo Устанавливаем необходимые зависимости...
pip install pygame pyinstaller pillow

echo Создаем иконку для игры...
python create_icon.py

echo Собираем лаунчер с отладкой...
pyinstaller NinjaGame_Launcher.spec

echo.
echo Проверяем, был ли создан exe-файл...
if exist dist\NinjaGame_Launcher.exe (
    echo.
    echo Сборка лаунчера завершена успешно!
    echo Исполняемый файл находится в папке dist\NinjaGame_Launcher.exe
    echo.
    echo Лаунчер отображает подробную информацию об ошибках и не закрывается автоматически.
    echo.
    echo Запускаем лаунчер...
    dist\NinjaGame_Launcher.exe
) else (
    echo.
    echo Ошибка: Лаунчер не был создан.
    echo Проверьте сообщения об ошибках выше.
    echo.
    pause
) 