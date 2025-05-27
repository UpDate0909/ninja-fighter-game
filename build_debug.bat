@echo off
echo Устанавливаем необходимые зависимости...
pip install pygame pyinstaller pillow

echo Создаем иконку для игры...
python create_icon.py

echo Создаем отладочную версию исполняемого файла...
pyinstaller NinjaGame_Debug.spec

echo.
echo Проверяем, был ли создан exe-файл...
if exist dist\NinjaGame_Debug.exe (
    echo.
    echo Сборка отладочной версии завершена успешно!
    echo Исполняемый файл находится в папке dist\NinjaGame_Debug.exe
    echo.
    echo Вы можете запустить игру, дважды щелкнув по этому файлу.
    echo Будет отображаться консоль с сообщениями об ошибках.
    echo.
    echo Запускаем отладочную версию...
    dist\NinjaGame_Debug.exe
    pause
) else (
    echo.
    echo Ошибка: Отладочный исполняемый файл не был создан.
    echo Проверьте сообщения об ошибках выше.
    echo.
    pause
) 