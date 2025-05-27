@echo off
echo Устанавливаем необходимые зависимости...
pip install pygame pyinstaller pillow

echo Создаем иконку для игры...
python create_icon.py

echo Создаем отладочную версию исполняемого файла...
pyinstaller NinjaGame_Debug.spec

echo Создаем утилиту отладки ресурсов...
pyinstaller DebugAssets.spec

echo.
echo Сборка инструментов отладки завершена.

if exist dist\NinjaGame_Debug.exe (
    echo.
    echo Отладочная версия игры: dist\NinjaGame_Debug.exe
) else (
    echo.
    echo Ошибка: Отладочная версия игры не была создана.
)

if exist dist\DebugAssets.exe (
    echo.
    echo Утилита отладки ресурсов: dist\DebugAssets.exe
    echo Запускаем утилиту отладки ресурсов...
    dist\DebugAssets.exe
) else (
    echo.
    echo Ошибка: Утилита отладки ресурсов не была создана.
)

echo.
echo Нажмите любую клавишу для выхода...
pause 