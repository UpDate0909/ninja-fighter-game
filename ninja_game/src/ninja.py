import pygame

class Ninja:
    def __init__(self, x, y, width, height, color, speed, ground_level):
        self.x = x
        self.width = width
        self.height = height
        self.y = y  # Используем переданную позицию y
        self.original_color = color # Store original color
        self.color = color # Current color - will be determined by animation
        self.speed = speed
        self.ground_level = ground_level
        self.facing_direction = 1 # 1 for right, -1 for left

        # Jumping attributes
        self.is_jumping = False
        self.jump_strength = 15 # How high the ninja jumps
        self.vertical_velocity = 0
        self.gravity = 1 # How quickly the ninja falls

        # Health attributes
        self.max_health = 100
        self.current_health = self.max_health

        # Attacking attributes
        self.is_attacking = False
        self.attack_duration = 10 # frames (visual only, hitbox active for shorter)
        self.attack_timer = 0
        self.attack_color = (255, 255, 0) # Yellow
        self.attack_hitbox_rect = None
        self.attack_damage = 10
        self.has_landed_hit_this_attack = False

        # Hit Reaction State
        self.is_hit = False
        self.hit_duration = 15 # frames
        self.hit_timer = 0
        self.hit_color = (200, 0, 0) # Dark Red

        # Store original dimensions for attack animation
        self.original_ninja_width = width 
        self.original_ninja_height = height


        # Animation attributes
        self.is_walking = False
        self.animation_timer = 0
        self.animation_frame_duration = 15 # Change frame every 15 game ticks
        self.current_sprite_frame = 0
        
        # Placeholder for sprite frames
        self.idle_sprites = [
            {'color': self.original_color}, 
            {'color': (min(self.original_color[0]+20,255), min(self.original_color[1]+20,255), min(self.original_color[2]+20,255))}
        ]
        self.walk_sprites = [
            {'color': self.original_color}, 
            {'color': (max(self.original_color[0]-20,0), max(self.original_color[1]-20,0), max(self.original_color[2]-20,0))}
        ]


    def draw(self, screen):
        # Используем self.color как базовый цвет для согласованности
        draw_color = self.color  # Используем self.color вместо self.original_color как базовый
        
        if self.is_walking:
            active_sprite_list = self.walk_sprites
        else:
            active_sprite_list = self.idle_sprites
            
        if active_sprite_list: # Ensure list is not empty
             draw_color = active_sprite_list[self.current_sprite_frame]['color']

        # Attack animation overrides others
        if self.is_attacking:
            draw_color = self.attack_color
        
        # Hit reaction color overrides all other body colors
        if self.is_hit:
            draw_color = self.hit_color
            
        # Создаем основной прямоугольник тела
        body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Рисуем ниндзя вместо простого прямоугольника
        
        # Тело (80% высоты)
        body_height = int(self.height * 0.8)
        body_rect = pygame.Rect(self.x, self.y + self.height - body_height, 
                                self.width, body_height)
        pygame.draw.rect(screen, draw_color, body_rect)
        
        # Голова (круг)
        head_radius = int(self.width * 0.4)
        head_pos = (self.x + self.width // 2, self.y + self.height - body_height - head_radius // 2)
        pygame.draw.circle(screen, draw_color, head_pos, head_radius)
        
        # Маска ниндзя (темная полоса на лице)
        mask_color = (max(0, draw_color[0] - 40), max(0, draw_color[1] - 40), max(0, draw_color[2] - 40))
        mask_height = int(head_radius * 0.3)
        mask_y = head_pos[1] - mask_height // 2
        mask_rect = pygame.Rect(head_pos[0] - head_radius, mask_y, head_radius * 2, mask_height)
        pygame.draw.rect(screen, mask_color, mask_rect)
        
        # Глаза
        eye_color = (255, 255, 255)  # Белые глаза
        eye_radius = int(head_radius * 0.2)
        eye_offset_x = int(head_radius * 0.3)
        
        # Направление взгляда зависит от направления движения
        if self.facing_direction == 1:  # вправо
            left_eye_pos = (head_pos[0] - eye_offset_x, mask_y + mask_height // 2)
            right_eye_pos = (head_pos[0] + eye_offset_x, mask_y + mask_height // 2)
        else:  # влево
            left_eye_pos = (head_pos[0] + eye_offset_x, mask_y + mask_height // 2)
            right_eye_pos = (head_pos[0] - eye_offset_x, mask_y + mask_height // 2)
            
        pygame.draw.circle(screen, eye_color, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, eye_color, right_eye_pos, eye_radius)
        
        # Зрачки (следят за направлением)
        pupil_color = (0, 0, 0)  # Черные зрачки
        pupil_radius = int(eye_radius * 0.5)
        pupil_offset = int(eye_radius * 0.3) * self.facing_direction
        
        pygame.draw.circle(screen, pupil_color, 
                           (left_eye_pos[0] + pupil_offset, left_eye_pos[1]), 
                           pupil_radius)
        pygame.draw.circle(screen, pupil_color, 
                           (right_eye_pos[0] + pupil_offset, right_eye_pos[1]), 
                           pupil_radius)
        
        # Ноги
        leg_width = int(self.width * 0.3)
        leg_height = int(body_height * 0.4)
        leg_spacing = int(self.width * 0.2)
        
        # Левая нога
        left_leg_x = self.x + (self.width // 2) - leg_width - leg_spacing // 2
        pygame.draw.rect(screen, mask_color,
                       pygame.Rect(left_leg_x, self.y + self.height - leg_height,
                                 leg_width, leg_height))
        
        # Правая нога
        right_leg_x = self.x + (self.width // 2) + leg_spacing // 2
        pygame.draw.rect(screen, mask_color,
                       pygame.Rect(right_leg_x, self.y + self.height - leg_height,
                                 leg_width, leg_height))
        
        # Руки и мечи
        if not self.is_attacking:
            # Обычная стойка с мечом
            arm_width = int(self.width * 0.2)
            arm_height = int(self.height * 0.4)
            
            # Меч (ручка)
            sword_handle_width = int(self.width * 0.1)
            sword_handle_height = int(self.width * 0.3)
            
            # Лезвие меча
            sword_blade_width = int(self.width * 0.1)
            sword_blade_height = int(self.height * 0.6)
            
            # Гарда меча
            sword_guard_width = int(self.width * 0.3)
            sword_guard_height = int(self.width * 0.1)
            
            if self.facing_direction == 1:  # вправо
                # Правая рука держит меч
                arm_x = self.x + self.width - arm_width
                arm_y = self.y + self.height - body_height
                pygame.draw.rect(screen, draw_color, 
                               pygame.Rect(arm_x, arm_y, arm_width, arm_height))
                
                # Меч (справа от руки)
                handle_x = arm_x + arm_width
                handle_y = arm_y + arm_height // 2 - sword_handle_height // 2
                
                # Ручка меча
                pygame.draw.rect(screen, (139, 69, 19),  # Коричневый цвет
                               pygame.Rect(handle_x, handle_y, sword_handle_width, sword_handle_height))
                
                # Гарда меча
                guard_x = handle_x + sword_handle_width - sword_guard_width // 2
                guard_y = handle_y - sword_guard_height // 2
                pygame.draw.rect(screen, (192, 192, 192),  # Серебристый цвет
                               pygame.Rect(guard_x, guard_y, sword_guard_width, sword_guard_height))
                
                # Лезвие меча
                blade_x = handle_x + sword_handle_width
                blade_y = handle_y + sword_handle_height // 2 - sword_blade_height // 2
                pygame.draw.rect(screen, (211, 211, 211),  # Светло-серый цвет
                               pygame.Rect(blade_x, blade_y, sword_blade_width, sword_blade_height))
                
                # Левая рука
                pygame.draw.rect(screen, draw_color, 
                               pygame.Rect(self.x, arm_y, arm_width, arm_height))
            else:  # влево
                # Левая рука держит меч
                arm_x = self.x
                arm_y = self.y + self.height - body_height
                pygame.draw.rect(screen, draw_color, 
                               pygame.Rect(arm_x, arm_y, arm_width, arm_height))
                
                # Меч (слева от руки)
                handle_x = arm_x - sword_handle_width
                handle_y = arm_y + arm_height // 2 - sword_handle_height // 2
                
                # Ручка меча
                pygame.draw.rect(screen, (139, 69, 19),  # Коричневый цвет
                               pygame.Rect(handle_x, handle_y, sword_handle_width, sword_handle_height))
                
                # Гарда меча
                guard_x = handle_x - sword_guard_width // 2
                guard_y = handle_y - sword_guard_height // 2
                pygame.draw.rect(screen, (192, 192, 192),  # Серебристый цвет
                               pygame.Rect(guard_x, guard_y, sword_guard_width, sword_guard_height))
                
                # Лезвие меча
                blade_x = handle_x - sword_blade_width
                blade_y = handle_y + sword_handle_height // 2 - sword_blade_height // 2
                pygame.draw.rect(screen, (211, 211, 211),  # Светло-серый цвет
                               pygame.Rect(blade_x, blade_y, sword_blade_width, sword_blade_height))
                
                # Правая рука
                pygame.draw.rect(screen, draw_color, 
                               pygame.Rect(self.x + self.width - arm_width, arm_y, arm_width, arm_height))
        else:
            # Атакующая стойка с мечом
            arm_width = int(self.width * 0.2)
            arm_height = int(self.height * 0.3)
            
            # Меч (ручка)
            sword_handle_width = int(self.width * 0.1)
            sword_handle_height = int(self.width * 0.3)
            
            # Лезвие меча
            sword_blade_width = int(self.width * 0.1)
            sword_blade_height = int(self.height * 0.8)  # Длиннее при атаке
            
            # Гарда меча
            sword_guard_width = int(self.width * 0.3)
            sword_guard_height = int(self.width * 0.1)
            
            if self.facing_direction == 1:  # вправо
                # Руки вытянуты для атаки
                arm_x = self.x + self.width - arm_width
                arm_y = self.y + self.height - body_height + body_height // 4
                pygame.draw.rect(screen, draw_color, 
                               pygame.Rect(arm_x, arm_y, arm_width * 2, arm_height))
                
                # Меч (справа от руки)
                handle_x = arm_x + arm_width * 2 - sword_handle_width // 2
                handle_y = arm_y - sword_handle_height // 2
                
                # Ручка меча
                pygame.draw.rect(screen, (139, 69, 19),  # Коричневый цвет
                               pygame.Rect(handle_x, handle_y, sword_handle_width, sword_handle_height))
                
                # Гарда меча
                guard_x = handle_x + sword_handle_width - sword_guard_width // 2
                guard_y = handle_y + sword_handle_height // 2 - sword_guard_height // 2
                pygame.draw.rect(screen, (192, 192, 192),  # Серебристый цвет
                               pygame.Rect(guard_x, guard_y, sword_guard_width, sword_guard_height))
                
                # Лезвие меча
                blade_x = handle_x + sword_handle_width
                blade_y = handle_y + sword_handle_height // 2 - sword_blade_height // 2
                pygame.draw.rect(screen, (211, 211, 211),  # Светло-серый цвет
                               pygame.Rect(blade_x, blade_y, sword_blade_width, sword_blade_height))
            else:  # влево
                # Руки вытянуты для атаки
                arm_x = self.x - arm_width
                arm_y = self.y + self.height - body_height + body_height // 4
                pygame.draw.rect(screen, draw_color, 
                               pygame.Rect(arm_x, arm_y, arm_width * 2, arm_height))
                
                # Меч (слева от руки)
                handle_x = arm_x - sword_handle_width // 2
                handle_y = arm_y - sword_handle_height // 2
                
                # Ручка меча
                pygame.draw.rect(screen, (139, 69, 19),  # Коричневый цвет
                               pygame.Rect(handle_x, handle_y, sword_handle_width, sword_handle_height))
                
                # Гарда меча
                guard_x = handle_x - sword_guard_width // 2
                guard_y = handle_y + sword_handle_height // 2 - sword_guard_height // 2
                pygame.draw.rect(screen, (192, 192, 192),  # Серебристый цвет
                               pygame.Rect(guard_x, guard_y, sword_guard_width, sword_guard_height))
                
                # Лезвие меча
                blade_x = handle_x - sword_blade_width
                blade_y = handle_y + sword_handle_height // 2 - sword_blade_height // 2
                pygame.draw.rect(screen, (211, 211, 211),  # Светло-серый цвет
                               pygame.Rect(blade_x, blade_y, sword_blade_width, sword_blade_height))

        # Draw Health Bar (using original_ninja_width for consistency if ninja width changes)
        health_bar_width = self.original_ninja_width 
        health_bar_height = 7
        health_bar_y_offset = 10
        health_bar_x = self.x
        health_bar_y = self.y - health_bar_y_offset - health_bar_height

        # Background Bar (red)
        bg_color = (255, 0, 0)
        pygame.draw.rect(screen, bg_color, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Foreground Health Fill (green)
        if self.max_health > 0: # Avoid division by zero if max_health is somehow 0
            fill_width = (self.current_health / self.max_health) * health_bar_width
        else:
            fill_width = 0
        fill_color = (0, 255, 0)
        pygame.draw.rect(screen, fill_color, (health_bar_x, health_bar_y, fill_width, health_bar_height))


    def move_left(self):
        self.x -= self.speed
        self.facing_direction = -1
        self.is_walking = True

    def move_right(self):
        self.x += self.speed
        self.facing_direction = 1
        self.is_walking = True

    def get_body_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0
        
        self.is_hit = True
        self.hit_timer = self.hit_duration
        
        # Interrupt current attack
        if self.is_attacking: # Check if it was attacking
            self.is_attacking = False
            self.attack_timer = 0
            self.attack_hitbox_rect = None # Deactivate hitbox
            # Больше не нужно восстанавливать размеры, так как не меняем их при атаке


    def jump(self):
        if not self.is_jumping: # Can only jump if not already jumping
            self.is_jumping = True
            self.vertical_velocity = -self.jump_strength
            # Jumping is not walking for this animation logic
            self.is_walking = False 
            
    def start_attack(self):
        if not self.is_attacking: # Prevent re-triggering attack while already attacking
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.is_walking = False # Attack animation takes precedence
            self.has_landed_hit_this_attack = False

            # Больше не изменяем размер тела ниндзя при атаке, так как теперь используем меч
            # Хитбокс размещаем в соответствии с положением меча

            # Определяем размеры хитбокса для меча
            hitbox_width = self.width * 0.9  # Длина лезвия меча
            hitbox_height = self.height * 0.15  # Ширина лезвия меча

            # Вычисляем положение хитбокса в зависимости от направления атаки
            if self.facing_direction == 1: # Атака вправо
                # Хитбокс меча располагается справа от ниндзя
                hitbox_x = self.x + self.width + hitbox_width * 0.1
                hitbox_y = self.y + (self.height * 0.3)  # Примерно на уровне руки
            else: # Атака влево
                # Хитбокс меча располагается слева от ниндзя
                hitbox_x = self.x - hitbox_width - hitbox_width * 0.1
                hitbox_y = self.y + (self.height * 0.3)  # Примерно на уровне руки

            self.attack_hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)


    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_frame_duration:
            self.animation_timer = 0
            self.current_sprite_frame = (self.current_sprite_frame + 1)
            
            if self.is_walking:
                if self.walk_sprites: # Check if list is not empty
                    self.current_sprite_frame %= len(self.walk_sprites)
            else: # Idle
                if self.idle_sprites: # Check if list is not empty
                    self.current_sprite_frame %= len(self.idle_sprites)
        
        # Примечание: флаг is_walking сбрасывается в main.py в начале каждого кадра.
        # Если игрок не нажимает клавиши движения, is_walking остается False,
        # что переключает анимацию в режим ожидания (idle)

    def update_position(self, screen_width):
        # Call animation update
        self.update_animation()

        # Handle attack timer
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_hitbox_rect = None # Deactivate hitbox
                # Больше не нужно восстанавливать размеры и позицию, так как не меняем их
        
        # Handle Hit Reaction Timer
        if self.is_hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.is_hit = False

        # Horizontal movement
        # Boundary checks for horizontal movement (screen edges)
        if self.x < 0:
            self.x = 0
        if self.x + self.width > screen_width:
            self.x = screen_width - self.width

        # Vertical movement (jumping and gravity)
        if self.is_jumping:
            self.y += self.vertical_velocity
            self.vertical_velocity += self.gravity

            # Landing logic: check if the bottom of the ninja has reached or passed the ground_level
            if self.y + self.height >= self.ground_level:
                self.y = self.ground_level - self.height # Position ninja exactly on the ground
                self.is_jumping = False
                self.vertical_velocity = 0
    
    def reset(self, start_x, ground_level_val):
        self.current_health = self.max_health
        self.x = start_x
        self.y = ground_level_val - self.height # Correctly position on the ground
        self.ground_level = ground_level_val # Update ninja's own ground_level reference
        
        self.is_attacking = False
        self.is_walking = False
        self.vertical_velocity = 0
        self.is_jumping = False
        self.attack_hitbox_rect = None
        self.has_landed_hit_this_attack = False
        self.facing_direction = 1 # Default to facing right
        self.attack_timer = 0
        self.animation_timer = 0
        self.current_sprite_frame = 0
        
        # Reset hit state
        self.is_hit = False
        self.hit_timer = 0
        
        # Reset dimensions to original
        self.width = self.original_ninja_width
        self.height = self.original_ninja_height # Assuming height might also change in future
