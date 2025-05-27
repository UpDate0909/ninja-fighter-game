Ninja Game - Local multiplayer fighting game
Game Description
Ninja Game is a simple 2D fighting game with local multiplayer mode,
created in Python using the Pygame library. In the game,
two ninjas fight against each other using swords. 
Each player controls his character by moving him around the screen,
performing jumps and attacks. The goal of the game is to reduce the enemy's health to zero.

Features
- Local multiplayer mode for two players
- Simple and intuitive controls
- Animated ninja characters with swords
- Health and attack system
- Sound effects for jumps, attacks and hits

Installation and launch
Requirements
- Python 3.6 or higher
- Pygame library

Method 1: Run from source
1.	Clone the repository:
   git clone [https://github.com/UpDate0909/ninja-game-test.git]
   cd ninja-game
2.	Install the required dependencies:
   pip install pygame
3.	Run the game:
   python run_game.py


Method 2: Creating an executable file (Windows only)
1.	Clone the repository and install the necessary dependencies:
   git clone https://github.com/UpDate0909/ninja-game-test.git
   cd ninja-game
   pip install pygame pyinstaller pillow
2.	Create an executable file using PyInstaller:
   pyinstaller --onefile --windowed --add-data “ninja_game/assets;ninja_game/assets” --hidden-import=pygame run_game.py
3. Locate the executable file in the dist folder and run it by double-clicking it.

Controls
Player 1 (red ninja)
- Left/Right Arrow: Move left/right
- Spacebar: Jump
- F: Attack
Player 2 (blue ninja)
- A/D: Move left/right
- W: Jump
- Q: Attack

Project structure
ninja-game/
│
├─── ninja_game/ # Main game directory
│ ├─── assets/ # Game resources
│ │ ├──── sounds/ # Sound effects
│ │ │ └──── sprites/ # Images (if available)
│ │
│ └─── src/ # Source code
│ ├─── __init__.py # Package initialization
│ ├─── main.py # Main game file
│ └─── ninja.py # Class Ninja
│
└──── run_game.py # File to run the game

Description of the main files
- run_game.py: The entry point for running the game. Imports and calls the main function from the main.py module.
- ninja_game/src/main.py: Contains the main game loop, input processing, rendering, and game logic.
- ninja_game/src/ninja.py: Defines the Ninja class, which represents the game character. Contains methods for movement, jumping, attacking, and rendering.
- ninja_game/assets/sounds/: Directory with sound files:
- jump.wav: Jump sound
- attack.wav: Attack sound
- hit.wav: Sound of hitting
- game_over.wav: Game over sound

Gameplay
1. The game starts with two ninjas on opposite sides of the screen.
2. Players control their characters using the appropriate keys.
3.	The goal is to attack the enemy and reduce their health to zero.
4.	When one player's health reaches zero, the game ends and a winner is declared.
5.	Press the 'R' key to restart the game after it ends.

Development
Technologies used
- Python 3
- Pygame (for graphics, sound and input processing)

Possible improvements
- Adding menus
- Improved graphics and animations
- Additional characters
- Different levels and arenas
- Special moves and combos
License
MIT License 
 Author
@UpDate0909


**************************************** 


Ninja Game - Локальный многопользовательский файтинг
Описание игры
Ninja Game - это простой 2D-файтинг с локальным многопользовательским режимом,
созданный на Python с использованием библиотеки Pygame.
В игре два ниндзя сражаются друг против друга, используя мечи. 
Каждый игрок управляет своим персонажем, перемещая его по экрану,
выполняя прыжки и атаки. Цель игры - уменьшить здоровье противника до нуля.

Особенности
•	Локальный многопользовательский режим для двух игроков
•	Простое и интуитивно понятное управление
•	Анимированные персонажи-ниндзя с мечами
•	Система здоровья и атак
•	Звуковые эффекты для прыжков, атак и попаданий
Установка и запуск
Требования
•	Python 3.6 или выше
•	Библиотека Pygame

Способ 1: Запуск из исходного кода
1.	Клонируйте репозиторий:
   git clone https://github.com/UpDate0909/ninja-game-test.git
   cd ninja-game
2.	Установите необходимые зависимости:
   pip install pygame
3.	Запустите игру:
   python run_game.py


Способ 2: Создание исполняемого файла (только для Windows)
1.	Клонируйте репозиторий и установите необходимые зависимости:
   git clone https://github.com/UpDate0909/ninja-game-test.git
   cd ninja-game
   pip install pygame pyinstaller pillow
2.	Создайте исполняемый файл с помощью PyInstaller:
   pyinstaller --onefile --windowed --add-data "ninja_game/assets;ninja_game/assets" --hidden-import=pygame run_game.py
3.	Найдите исполняемый файл в папке dist и запустите его двойным щелчком.
   
Управление
Игрок 1 (красный ниндзя)
•	Стрелка влево/вправо: Движение влево/вправо
•	Пробел: Прыжок
•	F: Атака
Игрок 2 (синий ниндзя)
•	A/D: Движение влево/вправо
•	W: Прыжок
•	Q: Атака

Структура проекта
ninja-game/
│
├── ninja_game/                # Основная директория игры
│   ├── assets/                # Ресурсы игры
│   │   ├── sounds/            # Звуковые эффекты
│   │   └── sprites/           # Изображения (если есть)
│   │
│   └── src/                   # Исходный код
│       ├── __init__.py        # Инициализация пакета
│       ├── main.py            # Главный файл игры
│       └── ninja.py           # Класс Ninja
│
└── run_game.py                # Файл для запуска игры

Описание основных файлов
•	run_game.py: Точка входа для запуска игры. Импортирует и вызывает функцию main из модуля main.py.
•	ninja_game/src/main.py: Содержит основной игровой цикл, обработку ввода, отрисовку и логику игры.
•	ninja_game/src/ninja.py: Определяет класс Ninja, который представляет игрового персонажа. Содержит методы для движения, прыжков, атак и отрисовки.
•	ninja_game/assets/sounds/: Директория со звуковыми файлами:
•	jump.wav: Звук прыжка
•	attack.wav: Звук атаки
•	hit.wav: Звук попадания
•	game_over.wav: Звук окончания игры

Игровой процесс
1.	Игра начинается с двумя ниндзя на противоположных сторонах экрана.
2.	Игроки управляют своими персонажами, используя соответствующие клавиши.
3.	Цель - атаковать противника и уменьшить его здоровье до нуля.
4.	Когда здоровье одного из игроков достигает нуля, игра заканчивается, и объявляется победитель.
5.	Для перезапуска игры после окончания нажмите клавишу 'R'.

   
Разработка
Используемые технологии
•	Python 3
•	Pygame (для графики, звука и обработки ввода)
Возможные улучшения
•	Добавление меню
•	Улучшенная графика и анимации
•	Дополнительные персонажи
•	Разные уровни и арены
•	Специальные приемы и комбо

Лицензия
MIT License 

 Автор
@UpDate0909
