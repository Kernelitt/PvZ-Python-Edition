import pygame
import random
from definitions import *
from zombie_animations import get_animation_frames, ZOMBIE_ANIMATIONS
from preloader import preloaded_images

class Zombie:
    def __init__(self, z_type, lane, scaler, game_field):
        self.z_type = z_type
        self.lane = lane
        self.game_field = game_field
        self.x = scaler.scale_x(BASE_WIDTH)
        self.y = scaler.scale_y(160 + lane * self.game_field.cell_height + self.game_field.cell_height / 2 - 50)
        self.normal_speed = 45 * 1 + random.choice([-1,1]) / 10
        self.speed = self.normal_speed
        self.health = ZOMBIE_HEALTH.get(z_type + ' Health', 270)
        self.cone_health = 0
        self.bucket_health = 0
        self.attack_sound_index = random.randint(0, 1)
        self.last_sound_time = 0.0
        self.slow_timer = 0.0
        self.rect = pygame.Rect(self.x, self.y, 150, 100)

        if z_type == "Conehead Zombie":
            self.cone_health = 370
        if z_type == "Buckethead Zombie":
            self.bucket_health = 1100

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in ZOMBIE_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'zombie_{action}']

        # Use preloaded cone animation frames
        self.cone_animation_frames = {}
        for action in ZOMBIE_ANIMATIONS:
            self.cone_animation_frames[action] = preloaded_images[f'cone_{action}']

        # Use preloaded bucket animation frames
        self.bucket_animation_frames = {}
        for action in ZOMBIE_ANIMATIONS:
            self.bucket_animation_frames[action] = preloaded_images[f'bucket_{action}']
        self.current_action = 'walk'
        self.frame_index = 0
        self.animation_timer = 0.0
        self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']
        self.dying = False
        self.to_remove = False

    def update(self, dt):
        self.speed = self.normal_speed if self.slow_timer <= 0 else self.normal_speed * 0.5
        self.slow_timer = max(0, self.slow_timer - dt)

        if self.health <= 0 and not self.dying:
            self.dying = True
            self.current_action = 'death'
            self.frame_index = 0
            self.animation_timer = 0.0
            self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']

        if self.dying:
            if self.current_action == 'death':
                self.animation_timer += dt
                if self.animation_timer >= self.frame_duration:
                    self.animation_timer -= self.frame_duration
                    self.frame_index += 1
                    if self.frame_index >= len(self.animation_frames[self.current_action]):
                        self.to_remove = True
                        return
            return

        # Find the rightmost plant in the lane ahead
        target_col = None
        for col in range(self.game_field.cols - 1, -1, -1):
            cell = self.game_field.grid[self.lane][col]
            if cell['plant'] is not None or cell['base'] is not None:
                plant_x = self.game_field.field_x + col * self.game_field.cell_width
                if self.x > plant_x:
                    target_col = col
                    break
        if target_col is not None:
            # Target the plant
            plant_x = self.game_field.field_x + target_col * self.game_field.cell_width
            if self.x > plant_x + self.game_field.cell_width / 2:
                self.x -= self.speed * dt
                if self.current_action != 'walk':
                    self.current_action = 'walk'
                    self.frame_index = 0
                    self.animation_timer = 0.0
                    self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']
            else:
                # At plant, damage it
                if self.current_action != 'attack':
                    self.current_action = 'attack'
                    self.frame_index = 0
                    self.animation_timer = 0.0
                    self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']
                self.last_sound_time += dt
                if self.last_sound_time > 0.75:
                    self.game_field.game.sound_manager.play_sound(f'zombie_attack{self.attack_sound_index + 1}')
                    self.last_sound_time = 0.0
                cell = self.game_field.grid[self.lane][target_col]
                plant = cell['plant'] if cell['plant'] is not None else cell['base']
                if hasattr(plant, 'health'):
                    plant.health -= 1
                    if plant.health <= 0:
                        if cell['plant'] is not None:
                            cell['plant'] = None
                        else:
                            cell['base'] = None
                        self.game_field.game.sound_manager.play_sound('plant_break')
        else:
            self.x -= self.speed * dt
            if self.current_action != 'walk':
                self.current_action = 'walk'
                self.frame_index = 0
                self.animation_timer = 0.0
                self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer -= self.frame_duration
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.current_action])

    def draw(self, screen):
        # Always draw the basic zombie
        frame = self.animation_frames[self.current_action][self.frame_index]
        scaled_frame = pygame.transform.scale(frame, (325 // 1.2, 290 // 1.2))
        screen.blit(scaled_frame, (self.x-80, self.y-100))
        # If bucket health > 0, draw bucket on top
        if self.bucket_health > 0:
            bucket_frame = self.bucket_animation_frames[self.current_action][self.frame_index]
            scaled_bucket = pygame.transform.scale(bucket_frame, (190 // 1.2, 330 // 1.2))
            screen.blit(scaled_bucket, (self.x+35, self.y-130))
        # If cone health > 0, draw cone on top
        if self.cone_health > 0:
            cone_frame = self.cone_animation_frames[self.current_action][self.frame_index]
            scaled_cone = pygame.transform.scale(cone_frame, (325 // 1.2, 330 // 1.2))
            screen.blit(scaled_cone, (self.x-80, self.y-130))

class ConeZombie(Zombie):
    def __init__(self, z_type, lane, scaler, game_field):
        super().__init__(z_type, lane, scaler, game_field)
        self.cone_health = 370

class BucketZombie(Zombie):
    def __init__(self, z_type, lane, scaler, game_field):
        super().__init__(z_type, lane, scaler, game_field)
        self.bucket_health = 1100

