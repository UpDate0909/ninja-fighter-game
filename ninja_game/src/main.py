# Main Python file for the Ninja Game
# This file will contain the main game loop and logic.

import pygame
import sys
import os

# Функция для получения пути к ресурсам, работает для PyInstaller
def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, работает как для разработки, 
        так и для исполняемого файла PyInstaller """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
        print(f"Запуск из PyInstaller bundle. Base path: {base_path}")
    except Exception:
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print(f"Запуск из обычного Python. Base path: {base_path}")
    
    result = os.path.join(base_path, relative_path)
    print(f"Полный путь к {relative_path}: {result}")
    return result

# Добавляем путь к директории проекта в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)

# Определяем относительные пути к ресурсам
if "NINJA_GAME_ASSETS" in os.environ:
    ASSETS_DIR = os.environ["NINJA_GAME_ASSETS"]
    print(f"Используем переменную окружения для ассетов: {ASSETS_DIR}")
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    print(f"Используем вычисленный путь для ассетов: {ASSETS_DIR}")

# Используем относительный импорт, который будет работать в любом случае
try:
    # Если запускаем как модуль
    from .ninja import Ninja
    print("Импортировали Ninja из пакета (.ninja)")
except ImportError:
    # Если запускаем как скрипт напрямую
    try:
        from ninja import Ninja
        print("Импортировали Ninja напрямую (ninja)")
    except ImportError:
        print("Не удалось импортировать модуль ninja. Попробуем найти его вручную...")
        ninja_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ninja.py")
        if os.path.exists(ninja_path):
            print(f"Файл ninja.py найден по пути: {ninja_path}")
            import importlib.util
            spec = importlib.util.spec_from_file_location("ninja", ninja_path)
            ninja_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ninja_module)
            Ninja = ninja_module.Ninja
            print("Импортировали Ninja из файла")
        else:
            print(f"Ошибка: Файл ninja.py не найден по пути: {ninja_path}")
            raise ImportError("Не удалось импортировать модуль ninja")

def main():
    pygame.init()
    pygame.mixer.init() # Initialize the mixer

    # Load Sounds
    jump_sound = None
    attack_sound = None
    hit_sound = None
    game_over_sound = None
    try:
        print("Загружаем звуки...")
        sound_paths = {
            "jump": os.path.join(ASSETS_DIR, "sounds", "jump.wav"),
            "attack": os.path.join(ASSETS_DIR, "sounds", "attack.wav"),
            "hit": os.path.join(ASSETS_DIR, "sounds", "hit.wav"),
            "game_over": os.path.join(ASSETS_DIR, "sounds", "game_over.wav")
        }
        
        # Проверяем существование файлов
        for sound_name, sound_path in sound_paths.items():
            if os.path.exists(sound_path):
                print(f"Файл {sound_name} найден: {sound_path}")
            else:
                print(f"ПРЕДУПРЕЖДЕНИЕ: Файл {sound_name} не найден: {sound_path}")
        
        jump_sound = pygame.mixer.Sound(sound_paths["jump"])
        attack_sound = pygame.mixer.Sound(sound_paths["attack"])
        hit_sound = pygame.mixer.Sound(sound_paths["hit"])
        game_over_sound = pygame.mixer.Sound(sound_paths["game_over"])
        print("Звуки загружены успешно")
    except pygame.error as e:
        print(f"Ошибка при загрузке звуков: {e}")
        # Sound variables will remain None if loading failed for any


    # Set screen dimensions
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ninja Game")

    # Colors
    white = (255, 255, 255)
    red = (255, 0, 0)
    ground_color = (100, 200, 100) # A shade of green

    # Ground properties
    ground_height = 50
    ground_rect = pygame.Rect(0, screen_height - ground_height, screen_width, ground_height)

    # Create a Ninja instance
    ninja_width = 50
    ninja_height = 50

    player_ninja_start_x = screen_width // 4
    ninja2_start_x = (screen_width // 4) * 3

    player_ninja = Ninja(x=player_ninja_start_x, y=ground_rect.top - ninja_height, 
                           width=ninja_width, height=ninja_height, 
                           color=red, speed=5, ground_level=ground_rect.top)

    # Create a second Ninja instance
    blue = (0, 0, 255)
    ninja2 = Ninja(x=ninja2_start_x, y=ground_rect.top - ninja_height, 
                   width=ninja_width, height=ninja_height,
                   color=blue, speed=5, ground_level=ground_rect.top)

    # Game State
    game_active = True
    winner_message = ""
    message_font = pygame.font.Font(None, 74)
    instruction_font = pygame.font.Font(None, 30)

    clock = pygame.time.Clock()
    running = True

    while running:
        if game_active:
            # Reset is_walking for the player_ninja at the start of each frame.
            if player_ninja: player_ninja.is_walking = False
            if ninja2: ninja2.is_walking = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # Player 1 controls
                    if event.key == pygame.K_LEFT:
                        if player_ninja: player_ninja.move_left()
                    if event.key == pygame.K_RIGHT:
                        if player_ninja: player_ninja.move_right()
                    if event.key == pygame.K_SPACE: # Jump key
                        if player_ninja: 
                            player_ninja.jump()
                            if jump_sound: jump_sound.play()
                    if event.key == pygame.K_f: # Attack key
                        if player_ninja: 
                            player_ninja.start_attack()
                            if attack_sound: attack_sound.play()

                    # Player 2 controls
                    if event.key == pygame.K_a: # P2 Left
                        if ninja2: ninja2.move_left()
                    if event.key == pygame.K_d: # P2 Right
                        if ninja2: ninja2.move_right()
                    if event.key == pygame.K_w: # P2 Jump
                        if ninja2: 
                            ninja2.jump()
                            if jump_sound: jump_sound.play()
                    if event.key == pygame.K_q: # P2 Attack
                        if ninja2: 
                            ninja2.start_attack()
                            if attack_sound: attack_sound.play()
            
            # Handle continuous key presses for walking state
            keys = pygame.key.get_pressed()
            if player_ninja:
                if keys[pygame.K_LEFT]: player_ninja.move_left()
                if keys[pygame.K_RIGHT]: player_ninja.move_right()
            if ninja2:
                if keys[pygame.K_a]: ninja2.move_left()
                if keys[pygame.K_d]: ninja2.move_right()

            # Update game state
            if player_ninja: player_ninja.update_position(screen_width)
            if ninja2: ninja2.update_position(screen_width)

            # Hit Detection Logic
            if player_ninja and ninja2:
                # Player Ninja attacking Ninja2
                if player_ninja.is_attacking and player_ninja.attack_hitbox_rect is not None and \
                   not player_ninja.has_landed_hit_this_attack:
                    if player_ninja.attack_hitbox_rect.colliderect(ninja2.get_body_rect()):
                        ninja2.take_damage(player_ninja.attack_damage)
                        if hit_sound: hit_sound.play()
                        player_ninja.has_landed_hit_this_attack = True
                        print("Player Ninja hit Ninja2! Ninja2 health:", ninja2.current_health) 

                # Ninja2 attacking Player Ninja
                if ninja2.is_attacking and ninja2.attack_hitbox_rect is not None and \
                   not ninja2.has_landed_hit_this_attack:
                    if ninja2.attack_hitbox_rect.colliderect(player_ninja.get_body_rect()):
                        player_ninja.take_damage(ninja2.attack_damage)
                        if hit_sound: hit_sound.play()
                        ninja2.has_landed_hit_this_attack = True
                        print("Ninja2 hit Player Ninja! Player health:", player_ninja.current_health)
            
            # Check for game over condition
            p1_dead = player_ninja and player_ninja.current_health <= 0
            p2_dead = ninja2 and ninja2.current_health <= 0

            if p1_dead and p2_dead:
                winner_message = "It's a Draw!"
                game_active = False
                if game_over_sound: game_over_sound.play() # Or a specific draw sound
            elif p1_dead:
                winner_message = "Ninja 2 Wins!"
                game_active = False
                if game_over_sound: game_over_sound.play()
            elif p2_dead:
                winner_message = "Ninja 1 Wins!"
                game_active = False
                if game_over_sound: game_over_sound.play()

            # Drawing code for active game
            screen.fill(white)
            pygame.draw.rect(screen, ground_color, ground_rect)
            if player_ninja: player_ninja.draw(screen)
            if ninja2: ninja2.draw(screen)

            # Optional: Draw hitboxes for debugging
            if player_ninja and player_ninja.attack_hitbox_rect is not None and player_ninja.is_attacking:
                pygame.draw.rect(screen, (255, 0, 255), player_ninja.attack_hitbox_rect, 2) 
            if ninja2 and ninja2.attack_hitbox_rect is not None and ninja2.is_attacking:
                pygame.draw.rect(screen, (255, 0, 255), ninja2.attack_hitbox_rect, 2)

        else: # Game is not active (Game Over)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if player_ninja and ninja2: # Ensure ninjas exist
                            player_ninja.reset(player_ninja_start_x, ground_rect.top)
                            ninja2.reset(ninja2_start_x, ground_rect.top)
                        game_active = True
                        winner_message = ""
            
            # Drawing code for game over screen
            screen.fill(white) # Or a different background color for game over
            pygame.draw.rect(screen, ground_color, ground_rect) # Draw ground

            if winner_message:
                win_text_surface = message_font.render(winner_message, True, (0,0,0)) # Black color
                win_text_rect = win_text_surface.get_rect(center=(screen_width/2, screen_height/2 - 50))
                screen.blit(win_text_surface, win_text_rect)

            instruction_text_surface = instruction_font.render("Press 'R' to Restart", True, (0,0,0))
            instruction_text_rect = instruction_text_surface.get_rect(center=(screen_width/2, screen_height/2 + 50))
            screen.blit(instruction_text_surface, instruction_text_rect)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
