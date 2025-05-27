@echo off
echo Устанавливаем необходимые зависимости...
pip install pygame pyinstaller pillow

echo Создаем иконку для игры...
python create_icon.py

echo Создаем исполняемый файл игры...
pyinstaller NinjaGame.spec

echo.
echo Проверяем, был ли создан exe-файл...
if exist dist\NinjaGame.exe (
    echo.
    echo Сборка завершена успешно!
    echo Исполняемый файл находится в папке dist\NinjaGame.exe
    echo.
    echo Вы можете запустить игру, дважды щелкнув по этому файлу.
    echo.
    pause
) else (
    echo.
    echo Ошибка: Исполняемый файл не был создан.
    echo Проверьте сообщения об ошибках выше.
    echo.
    pause
) 