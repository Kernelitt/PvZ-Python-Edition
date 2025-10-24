import pygame
import random
from definitions import *
from zombie_animations import *
from preloader import preloaded_images
from pygame import surfarray

class Zombie:
    def __init__(self, lane, scaler, game_field):
        self.z_type = 'Basic Zombie'
        self.lane = lane
        self.x = scaler.scale_x(BASE_WIDTH + random.randint(10,100))
        self.y = scaler.scale_y(game_field.cell_height + lane * ((1025 - game_field.cell_height) / 5) + ((1025 - game_field.cell_height) / 5) / 2 - 50)
        self.normal_speed = 60 * 1 + random.choice([-1,1]) / 10
        self.speed = self.normal_speed
        self.health = 270
        self.initial_health = self.health
        self.cone_health = 0
        self.bucket_health = 0
        self.game_field = game_field
        self.attack_sound_index = random.randint(0, 1)
        self.last_sound_time = 0.0
        self.damage_timer = 0.0
        self.slow_timer = 0.0
        self.frozen_effect = False
        self.damage_flash_timer = 0.0
        self.low_health_timer = 0.0
        self.sinking_offset = 0.0
        self.entering_water = False
        self.rect = pygame.Rect(self.x, self.y, 50, 100)
        self.cone_rect = pygame.Rect(self.x, self.y, 50, 100)
        self.bucket_rect = pygame.Rect(self.x, self.y, 50, 100)

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

    def take_damage(self, amount):
        if self.bucket_health > 0:
            self.bucket_health -= amount
            if self.bucket_health <= 0:
                self.bucket_health = 0
            impact_sounds = ['bucket_impact1', 'bucket_impact2']
            self.game_field.game.sound_manager.play_sound(random.choice(impact_sounds))
        elif self.cone_health > 0:
            self.cone_health -= amount
            if self.cone_health <= 0:
                self.cone_health = 0
            impact_sounds = ['cone_impact1', 'cone_impact2']
            self.game_field.game.sound_manager.play_sound(random.choice(impact_sounds))
        else:
            self.health -= amount
            impact_sounds = ['zombie_impact1', 'zombie_impact2', 'zombie_impact3']
            self.game_field.game.sound_manager.play_sound(random.choice(impact_sounds))
        self.damage_flash_timer = 0.1

    def update(self, dt):
        self.slow_timer = max(0, self.slow_timer - dt)
        self.frozen_effect = self.slow_timer > 0
        self.damage_flash_timer = max(0, self.damage_flash_timer - dt)
        dt_effective = dt / 2 if self.frozen_effect else dt

        # Check if entering water rows
        if self.game_field.rows > 5 and self.lane in self.game_field.water_rows:
            if not self.entering_water:
                self.entering_water = True
                self.game_field.game.sound_manager.play_sound('zombie_entering_water')
                self.current_action = 'walk'
                self.frame_index = 0
                self.animation_timer = 0.0
                self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']
            # Gradually sink the zombie
            self.sinking_offset = min(self.sinking_offset + dt * 50, 50)  # Sink up to 50 pixels over time
        else:
            if self.entering_water:
                self.entering_water = False
                self.current_action = 'walk'
                self.frame_index = 0
                self.animation_timer = 0.0
                self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']
                self.sinking_offset = max(self.sinking_offset - dt * 50, 0)

        # Check if health is below 26%
        if self.health <= self.initial_health * 0.26 and self.health > 0:
            self.low_health_timer += dt
            if self.low_health_timer >= 0.01:
                self.health -= 2
                self.low_health_timer = 0.0
                if self.health <= 0:
                    self.health = 0

        if self.health <= self.initial_health * 0.26 and not self.dying:
            self.dying = True
            self.current_action = 'swim_death' if self.entering_water else 'death'
            self.frame_index = 0
            self.animation_timer = 0.0
            self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']

        if self.dying:
            if self.current_action in ['death', 'swim_death']:
                self.animation_timer += dt_effective
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
            if self.game_field.grid[self.lane][col] is not None:
                plant_x = self.game_field.field_x + col * self.game_field.cell_width
                if self.x > plant_x:
                    target_col = col
                    break
        if target_col is not None:
            # Target the plant
            plant_x = self.game_field.field_x + target_col * self.game_field.cell_width
            if self.x > plant_x + self.game_field.cell_width / 2:
                if (3 <= self.frame_index <= 14 or 22 <= self.frame_index <= 38):
                    self.x -= self.speed * dt_effective
                move_action = 'swim' if self.entering_water else 'walk'
                if self.current_action != move_action:
                    self.current_action = move_action
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
                # Keep attacking even in water
                self.last_sound_time += dt_effective
                self.damage_timer += dt_effective
                if self.last_sound_time > 0.75:
                    self.game_field.game.sound_manager.play_sound(f'zombie_attack{self.attack_sound_index + 1}')
                    self.last_sound_time = 0.0
                if self.damage_timer > 0.013:
                    plant = self.game_field.grid[self.lane][target_col]
                    if hasattr(plant, 'health'):
                        plant.health -= 1
                        if plant.health <= 0:
                            self.game_field.grid[self.lane][target_col] = None
                            self.game_field.game.sound_manager.play_sound('plant_break')
                    self.damage_timer = 0.0
        else:
            if (3 <= self.frame_index <= 14 or 25 <= self.frame_index <= 41):
                self.x -= self.speed * dt_effective
            move_action = 'swim' if self.entering_water else 'walk'
            if self.current_action != move_action:
                self.current_action = move_action
                self.frame_index = 0
                self.animation_timer = 0.0
                self.frame_duration = 1.0 / ZOMBIE_ANIMATIONS[self.current_action]['fps']

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.cone_rect.x = int(self.x)
        self.cone_rect.y = int(self.y)
        self.bucket_rect.x = int(self.x)
        self.bucket_rect.y = int(self.y)

        # Update animation
        self.animation_timer += dt_effective
        if self.animation_timer >= self.frame_duration:
            self.animation_timer -= self.frame_duration
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.current_action])

    def draw(self, screen):
        # Always draw the basic zombie
        frame = self.animation_frames[self.current_action][self.frame_index]
        scaled_frame = pygame.transform.scale(frame, (325 // 1.2, 290 // 1.2))
        combined_surface = pygame.Surface((325, 330), pygame.SRCALPHA)
        combined_surface.blit(scaled_frame, (0, 30))
        # If bucket health > 0, draw bucket on top
        if self.bucket_health > 0:
            bucket_frame = self.bucket_animation_frames[self.current_action][self.frame_index]
            scaled_bucket = pygame.transform.scale(bucket_frame, (190 // 1.2, 330 // 1.2))
            combined_surface.blit(scaled_bucket, (110, 0))  # relative positions
        # If cone health > 0, draw cone on top
        if self.cone_health > 0:
            cone_frame = self.cone_animation_frames[self.current_action][self.frame_index]
            scaled_cone = pygame.transform.scale(cone_frame, (325 // 1.2, 330 // 1.2))
            combined_surface.blit(scaled_cone, (0, 0))

        # Visual effects
        if self.damage_flash_timer > 0:
            combined_surface = combined_surface.copy()
            tint = pygame.Surface(combined_surface.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = surfarray.pixels_alpha(tint)
            frame_alpha = surfarray.pixels_alpha(combined_surface)
            tint_alpha[:] = frame_alpha
            del tint_alpha
            del frame_alpha
            combined_surface.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        if self.frozen_effect:
            combined_surface = combined_surface.copy()
            tint = pygame.Surface(combined_surface.get_size(), pygame.SRCALPHA)
            tint.fill((0, 0, 128, 0))
            tint_alpha = surfarray.pixels_alpha(tint)
            frame_alpha = surfarray.pixels_alpha(combined_surface)
            tint_alpha[:] = frame_alpha
            del tint_alpha
            del frame_alpha
            combined_surface.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        if self.sinking_offset > 0:
            # Clip the surface to show only the top part as it sinks
            clip_height = max(0, combined_surface.get_height() - int(self.sinking_offset))
            if clip_height > 0:
                clipped_surface = combined_surface.subsurface((0, 0, combined_surface.get_width(), clip_height))
                screen.blit(clipped_surface, (self.x-160, self.y-130))
            # No need to draw if fully sunk
        else:
            screen.blit(combined_surface, (self.x-160, self.y-130 + self.sinking_offset))

class ConeheadZombie(Zombie):
    def __init__(self, lane, scaler, game_field):
        super().__init__(lane, scaler, game_field)
        self.z_type = 'Conehead Zombie'
        self.cone_health = 370

class BucketheadZombie(Zombie):
    def __init__(self, lane, scaler, game_field):
        super().__init__(lane, scaler, game_field)
        self.z_type = 'Buckethead Zombie'
        self.bucket_health = 1100

class PoleVaulterZombie(Zombie):
    def __init__(self, lane, scaler, game_field):
        super().__init__(lane, scaler, game_field)
        self.z_type = 'Pole Vaulter Zombie'
        self.health = 500
        self.initial_health = self.health
        self.has_pole = True
        self.jumped = False

        # Use preloaded animation frames for pole vaulter
        self.animation_frames = {}
        for action in POLE_VAULTER_ZOMBIE_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'pole_vaulter_{action}']

        self.current_action = 'run'
        self.frame_index = 0
        self.animation_timer = 0.0
        self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']

    def update(self, dt):
        self.slow_timer = max(0, self.slow_timer - dt)
        self.frozen_effect = self.slow_timer > 0
        self.damage_flash_timer = max(0, self.damage_flash_timer - dt)
        dt_effective = dt / 2 if self.frozen_effect else dt

        # Check if health is below 26%
        if self.health <= self.initial_health * 0.26 and self.health > 0:
            self.low_health_timer += dt
            if self.low_health_timer >= 0.01:
                self.health -= 2
                self.low_health_timer = 0.0
                if self.health <= 0:
                    self.health = 0

        if self.health <= self.initial_health * 0.26 and not self.dying:
            self.dying = True
            self.current_action = 'death'
            self.frame_index = 0
            self.animation_timer = 0.0
            self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']

        if self.dying:
            if self.current_action == 'death':
                self.animation_timer += dt_effective
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
            if self.game_field.grid[self.lane][col] is not None:
                plant_x = self.game_field.field_x + col * self.game_field.cell_width
                if self.x > plant_x:
                    target_col = col
                    break

        if target_col != None and not self.jumped:
            # Target the plant
            plant_x = self.game_field.field_x + target_col * self.game_field.cell_width + self.game_field.cell_width
            if self.x > plant_x:
                # Run towards plant
                if self.current_action != 'run':
                    self.current_action = 'run'
                    self.frame_index = 0
                    self.animation_timer = 0.0
                    self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']
                self.animation_timer += dt_effective
                if self.animation_timer >= self.frame_duration:
                    self.animation_timer -= self.frame_duration
                    self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.current_action])
                self.x -= self.speed * dt_effective
            else:
                # At plant, jump over it
                if self.current_action != 'jump':
                    self.current_action = 'jump'
                    self.frame_index = 0
                    self.animation_timer = 0.0
                    self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']
                    self.game_field.game.sound_manager.play_sound(f'polevault')
                elif self.current_action == 'jump':
                    # Update jump animation
                    self.animation_timer += dt_effective
                    if self.animation_timer >= self.frame_duration:
                        self.animation_timer -= self.frame_duration
                        self.frame_index += 1
                        if self.frame_index >= len(self.animation_frames[self.current_action]):
                            # Jump completed, teleport to next cell
                            self.x = plant_x - self.game_field.cell_width * 2
                            self.jumped = True
                            self.speed = self.normal_speed  # Reduce speed after jump
                            self.current_action = 'walk'
                            self.frame_index = 0
                            self.animation_timer = 0.0
                            self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']
        else:
            if not self.jumped:
                # No plant, run normally
                if self.current_action != 'run':
                    self.current_action = 'run'
                    self.frame_index = 0
                    self.animation_timer = 0.0
                    self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']
                self.animation_timer += dt_effective
                if self.animation_timer >= self.frame_duration:
                    self.animation_timer -= self.frame_duration
                    self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.current_action])
                self.x -= self.speed * dt_effective
            else:
                # Behave like basic zombie: attack plants or walk
                if target_col is not None:
                    # Target the plant
                    plant_x = self.game_field.field_x + target_col * self.game_field.cell_width
                    if self.x > plant_x + self.game_field.cell_width / 4:
                        self.x -= self.speed * dt_effective
                        if self.current_action != 'walk':
                            self.current_action = 'walk'
                            self.frame_index = 0
                            self.animation_timer = 0.0
                            self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']
                        self.animation_timer += dt_effective
                        if self.animation_timer >= self.frame_duration:
                            self.animation_timer -= self.frame_duration
                            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.current_action])
                    else:
                        # At plant, damage it
                        if self.current_action != 'attack':
                            self.current_action = 'attack'
                            self.frame_index = 0
                            self.animation_timer = 0.0
                            self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']
                        self.animation_timer += dt_effective
                        if self.animation_timer >= self.frame_duration:
                            self.animation_timer -= self.frame_duration
                            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.current_action])
                        self.last_sound_time += dt_effective
                        self.damage_timer += dt_effective
                        if self.last_sound_time > 0.75:
                            self.game_field.game.sound_manager.play_sound(f'zombie_attack{self.attack_sound_index + 1}')
                            self.last_sound_time = 0.0
                        if self.damage_timer > 0.013:
                            plant = self.game_field.grid[self.lane][target_col]
                            if hasattr(plant, 'health'):
                                plant.health -= 1
                                if plant.health <= 0:
                                    self.game_field.grid[self.lane][target_col] = None
                                    self.game_field.game.sound_manager.play_sound('plant_break')
                            self.damage_timer = 0.0
                else:
                    self.x -= self.speed * dt_effective
                    if self.current_action != 'walk':
                        self.current_action = 'walk'
                        self.frame_index = 0
                        self.animation_timer = 0.0
                        self.frame_duration = 1.0 / POLE_VAULTER_ZOMBIE_ANIMATIONS[self.current_action]['fps']
                    self.animation_timer += dt_effective
                    if self.animation_timer >= self.frame_duration:
                        self.animation_timer -= self.frame_duration
                        self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.current_action])

        self.rect.x = int(self.x)
        self.rect.y = int(self.y + 80)

    def draw(self, screen):
        # Always draw the basic zombie
        frame = self.animation_frames[self.current_action][self.frame_index]
        scaled_frame = pygame.transform.scale(frame, (681 // 1.2, 480 // 1.2))
        combined_surface = pygame.Surface((681, 480), pygame.SRCALPHA)
        combined_surface.blit(scaled_frame, (0, 30))

        # Visual effects
        if self.damage_flash_timer > 0:
            combined_surface = combined_surface.copy()
            tint = pygame.Surface(combined_surface.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = surfarray.pixels_alpha(tint)
            frame_alpha = surfarray.pixels_alpha(combined_surface)
            tint_alpha[:] = frame_alpha
            del tint_alpha
            del frame_alpha
            combined_surface.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        if self.frozen_effect:
            combined_surface = combined_surface.copy()
            tint = pygame.Surface(combined_surface.get_size(), pygame.SRCALPHA)
            tint.fill((0, 0, 128, 0))
            tint_alpha = surfarray.pixels_alpha(tint)
            frame_alpha = surfarray.pixels_alpha(combined_surface)
            tint_alpha[:] = frame_alpha
            del tint_alpha
            del frame_alpha
            combined_surface.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        if self.sinking_offset > 0:
            # Clip the surface to show only the top part as it sinks
            clip_height = max(0, combined_surface.get_height() - int(self.sinking_offset))
            if clip_height > 0:
                clipped_surface = combined_surface.subsurface((0, 0, combined_surface.get_width(), clip_height))
                screen.blit(clipped_surface, (self.x - 283, self.y - 270))
            # No need to draw if fully sunk
        else:
            screen.blit(combined_surface, (self.x - 283, self.y - 270 + self.sinking_offset))
