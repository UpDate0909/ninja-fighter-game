@echo off
echo Запуск игры в режиме отладки...
echo.
echo Устанавливаем pygame, если он еще не установлен...
pip install pygame

echo.
echo Запускаем игру...
python build_game.py

echo.
echo Игра завершена. Нажмите любую клавишу для выхода.
pause 