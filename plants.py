import pygame
import time
import math
import random
from definitions import *
from zombie_animations import *
from preloader import preloaded_images

class Projectile:
    def __init__(self, x, y, speed, damage, image, angle=0, proj_type='pea', max_distance=0):
        self.x = x
        self.y = y
        self.start_x = x
        self.speed = speed  # pixels per second
        self.damage = damage
        self.image = image
        self.angle = angle  # in radians, 0 is right
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.active = True
        self.proj_type = proj_type
        self.max_distance = max_distance

    def update(self, dt):
        self.x += self.speed * dt * math.cos(self.angle)
        self.y += self.speed * dt * math.sin(self.angle)
        self.rect.center = (int(self.x), int(self.y))
        # Deactivate if off screen (assuming screen width 1920, height 1080)
        if self.x > 1920 or self.x < 0 or self.y > 1080 or self.y < 0:
            self.active = False
        # Deactivate if exceeded max distance
        if self.max_distance > 0 and self.x - self.start_x > self.max_distance:
            self.active = False

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image,(48,48)), self.rect)

    def collides_with(self, zombie):
        # Simple rect collision
        return self.rect.colliderect(zombie.rect)

class Plant:
    def __init__(self, x, y, name, game, row):
        self.x = x
        self.y = y
        self.name = name

        self.game = game
        self.row = row
        self.health = PLANT_HEALTH.get(name, PLANT_HEALTH.get("Basic Plants", 300))
        self.sun_cost = PLANT_SUN_COST.get(name, 50)
        self.recharge = PLANT_RECHARGE.get(name, 750) * 10 / 1000.0  # convert ms to seconds (multiply by 10 as per comment)
        self.last_action_time = 0
        self.projectiles = []
        self.damage_flash_timer = 0.0
        self.rect = pygame.Rect(self.x, self.y, 160, 160)
    def update(self, dt):
        self.damage_flash_timer = max(0, self.damage_flash_timer - dt)

    def draw(self, screen):
        # Placeholder: draw a rectangle for the plant
        shadow = preloaded_images["plant_shadow"] 
        shadow_scaled = pygame.transform.smoothscale(shadow,(120,60))
        screen.blit(shadow_scaled,(self.x+20,self.y+110))

    def take_damage(self, amount):
        self.health -= amount
        self.damage_flash_timer = 0.2  # Flash for 0.2 seconds
        if self.health <= 0:
            self.health = 0
            # Remove plant from game grid or mark dead
            # This should be handled by game logic

class Peashooter(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x-30, y, "Peashooter", game, row)
        self.rect.x = self.x
        self.projectile_speed = 480  # pixels per second
        self.damage = PLANT_DAMAGE.get("Pea", 20)
        self.fire_rate = PLANT_TIMERS.get("Peashooter Fire Rate", 1500) / 1000.0  # convert ms to seconds
        # Load projectile image
        self.projectile_image = pygame.image.load(PROJECTILE_TEXTURES_PATH["Pea"]).convert_alpha()

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in PEASHOOTER_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'peashooter_{action}']
        self.rect = self.animation_frames['idle'][0].get_rect(center=(self.x, self.y))

        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0
        self.blink_frame_index = 0
        self.blink_timer = 0.0
        self.shoot_frame_index = 0
        self.shoot_timer = 0.0
        self.shoot_bottom_frame_index = 0
        self.shoot_delay = 0.0
        self.shoot_delay_timer = 0.0

    def update(self, dt, zombies):
        # Update idle animation (pauses during blink)
        if self.current_action != 'blink':
            self.idle_timer += dt
            idle_fps = PEASHOOTER_ANIMATIONS['idle']['fps']
            if self.idle_timer >= 1.0 / idle_fps:
                self.idle_timer -= 1.0 / idle_fps
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        # Check if there is a zombie in the same lane ahead
        has_target = any(z for z in zombies if z.lane == self.row and z.x > self.x)
        if has_target:
            if self.shoot_delay == 0.0:
                self.shoot_delay = random.uniform(1.0, 1.5)
            self.shoot_delay_timer += dt
            if self.shoot_delay_timer >= self.shoot_delay:
                current_time = time.time()
                if current_time - self.last_action_time >= self.fire_rate:
                    self.current_action = 'shoot'
                    self.shoot_frame_index = 0
                    self.shoot_timer = 0.0
                    self.shoot_bottom_frame_index = self.idle_frame_index
                    self.shooting_second = False
                    self.shoot()
                    self.last_action_time = current_time
                    self.shoot_delay_timer = 0.0
                    self.shoot_delay = 0.0
        else:
            self.shoot_delay = 0.0
            self.shoot_delay_timer = 0.0

        # Random blink
        if self.current_action == 'idle' and self.idle_frame_index == 0 and random.random() < 0.1:  # low chance per frame
            self.current_action = 'blink'
            self.blink_frame_index = 0
            self.blink_timer = 0.0

        # Update blink animation
        if self.current_action == 'blink':
            self.blink_timer += dt
            blink_fps = PEASHOOTER_ANIMATIONS['blink']['fps']
            if self.blink_timer >= 1.0 / blink_fps:
                self.blink_timer -= 1.0 / blink_fps
                self.blink_frame_index += 1
                if self.blink_frame_index >= len(self.animation_frames['blink']):
                    self.current_action = 'idle'
                    self.blink_frame_index = 0

        # Update shoot animation
        if self.current_action == 'shoot':
            self.shoot_timer += dt
            shoot_fps = PEASHOOTER_ANIMATIONS['shoot']['fps']
            if self.shoot_timer >= 1.0 / shoot_fps:
                self.shoot_timer -= 1.0 / shoot_fps
                self.shoot_frame_index += 1
                if self.shoot_frame_index >= len(self.animation_frames['shoot']):
                    self.current_action = 'idle'
                    self.shoot_frame_index = 0


        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)
        # Remove inactive projectiles
        self.projectiles = [p for p in self.projectiles if p.active]
        super().update(dt)

    def shoot(self):
        proj_x = self.x + 50
        proj_y = self.y + 35
        new_proj = Projectile(proj_x, proj_y, self.projectile_speed, self.damage, self.projectile_image)
        self.projectiles.append(new_proj)
        self.game.sound_manager.play_sound('throw')


    def draw(self, screen):
        super().draw(screen) 
        if self.current_action == 'idle':
            frame = self.animation_frames['idle'][self.idle_frame_index]
        elif self.current_action == 'blink':
            frame = self.animation_frames['idle'][self.idle_frame_index].copy()
            blink_frame = self.animation_frames['blink'][self.blink_frame_index]
            frame.blit(blink_frame, (0,0))
        elif self.current_action == 'shoot':
            # shoot_bottom is the base, shoot_top overlays on head
            frame = self.animation_frames['shoot_bottom'][6].copy()
            shoot_top_frame = self.animation_frames['shoot_top'][self.shoot_frame_index]
            frame.blit(shoot_top_frame, (0,0))
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.smoothscale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x, self.y))
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

class Sunflower(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Sunflower", game, row)
        self.sun_production_rate = PLANT_TIMERS.get("Sunflower Production Rate", 24000) / 1000.0  # 24 seconds
        self.sun_timer = 0.0
        self.suns = []  # List to hold spawned suns
        self.first_sun = True  # Flag for faster first sun production

        # Use preloaded animation frames
        self.animation_frames = {}
        for action_name, action_data in SUNFLOWER_ANIMATIONS.items():
            if isinstance(action_data, dict):  # Проверяем значение (словарь), не ключ
                key = f'sunflower_{action_name}'
                if key in preloaded_images:
                    self.animation_frames[action_name] = preloaded_images[key]
                else:
                    print(f"Warning: {key} not found in preloaded_images")

        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        # Produce sun
        effective_rate = self.sun_production_rate / 2 if self.first_sun else self.sun_production_rate
        self.sun_timer += dt
        if self.sun_timer >= effective_rate:
            # Spawn a sun object instead of directly adding to sun_count
            sun_x = self.x + 50  # Position relative to sunflower
            sun_y = self.y + 20
            new_sun = Sun(sun_x, sun_y, self.game)
            self.suns.append(new_sun)
            self.game.sound_manager.play_sound('sun')
            self.sun_timer = 0.0
            if self.first_sun:
                self.first_sun = False

        # Update suns
        for sun in self.suns:
            sun.update(dt)

        # Update idle animation
        self.idle_timer += dt
        idle_fps = SUNFLOWER_ANIMATIONS['idle']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        super().update(dt)

    def draw(self, screen):
        super().draw(screen) 
        frame = self.animation_frames['idle'][self.idle_frame_index]
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x-20, self.y))
        # Draw suns
        for sun in self.suns:
            sun.draw(screen)

class CherryBomb(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Cherry Bomb", game, row)
        self.explosion_delay = PLANT_TIMERS.get("Cherry Bomb Explosion Delay", 1000) / 1000.0
        self.timer = self.explosion_delay
        self.exploded = False

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in CHERRYBOMB_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'cherrybomb_{action}']
        self.rect = self.animation_frames['idle'][0].get_rect(center=(self.x, self.y))
        self.current_action = 'active'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        if self.exploded:
            return
        self.timer -= dt
        if self.timer <= 0:
            self.explode()
            return
        # Update idle animation
        self.idle_timer += dt
        idle_fps = CHERRYBOMB_ANIMATIONS['active']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        super().update(dt)

    def explode(self):
        self.exploded = True
        damage = PLANT_DAMAGE.get("CherryBomb", 1800)
        # Damage zombies in a 3x3 area around the plant
        plant_row = self.row
        plant_col = int((self.x - self.game.main_game.game_field.field_x) // self.game.main_game.game_field.cell_width)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r = plant_row + dr
                c = plant_col + dc
                if 0 <= r < self.game.main_game.game_field.rows and 0 <= c < self.game.main_game.game_field.cols:
                    # Damage zombies in this cell's lane
                    for zombie in self.game.main_game.zombies:
                        if zombie.lane == r and abs(zombie.x - (self.game.main_game.game_field.field_x + c * self.game.main_game.game_field.cell_width)) < self.game.main_game.game_field.cell_width:
                            zombie.take_damage(damage)
        # Remove plant from grid
        self.game.main_game.game_field.grid[self.row][plant_col] = None
        self.game.sound_manager.play_sound('cherrybomb')

    def draw(self, screen):
        super().draw(screen) 
        if self.exploded:
            return
        frame = self.animation_frames['idle'][self.idle_frame_index]
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (200, 200))
        screen.blit(scaled_frame, (self.x, self.y))

class WallNut(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Wall Nut", game, row)

        # Use preloaded animation frames
        self.animation_frames = {}
        for action_name, action_data in WALLNUT_ANIMATIONS.items():
            if isinstance(action_data, dict):  # Проверяем значение (словарь), не ключ
                key = f'wallnut_{action_name}'
                if key in preloaded_images:
                    self.animation_frames[action_name] = preloaded_images[key]
                else:
                    print(f"Warning: {key} not found in preloaded_images")
        self.rect = self.animation_frames['idle'][0].get_rect(center=(self.x, self.y))
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        # Update idle animation
        self.idle_timer += dt
        idle_fps = WALLNUT_ANIMATIONS['idle']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        super().update(dt)

    def draw(self, screen):
        super().draw(screen) 
        frame = self.animation_frames['idle'][self.idle_frame_index]
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x, self.y))

class PotatoMine(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Potato Mine", game, row)
        self.arming_delay = PLANT_TIMERS.get("Potato Mine Surfacing", 15000) / 1000.0
        self.timer = self.arming_delay
        self.armed = False
        self.exploded = False

        # Animation state
        self.current_action = 'not_armed'
        self.not_armed_frame_index = 0
        self.not_armed_timer = 0.0
        self.arming_frame_index = 0
        self.arming_timer = 0.0
        self.idle_frame_index = 0
        self.idle_timer = 0.0
        self.blink_frame_index = 0
        self.blink_timer = 0.0
        self.explode_frame_index = 0
        self.explode_timer = 0.0
        self.blink_chance = 0.1  # Chance to blink per frame

        # Use preloaded animation frames
        self.animation_frames = {}
        for name,action in POTATO_MINE_ANIMATIONS.items():
            if isinstance(action, dict):  # Проверяем значение (словарь), не ключ
                key = f'potato_mine_{name}'
                if key in preloaded_images:
                    self.animation_frames[name] = preloaded_images[key]
                else:
                    print(f"Warning: {key} not found in preloaded_images")
        print(self.animation_frames)
    def update(self, dt):
        if self.exploded:
            return
        if self.health <= 0 and self.armed:
            self.current_action = 'explode'
            self.explode_frame_index = 0
            self.explode_timer = 0.0
            self.explode()
            return

        # State transitions
        if self.current_action == 'not_armed':
            # Update not_armed animation
            self.not_armed_timer += dt
            not_armed_fps = POTATO_MINE_ANIMATIONS['not_armed']['fps']
            self.not_armed_frame_index = 0
            # Check if arming should start
            self.timer -= dt
            if self.timer <= 0:
                self.current_action = 'arming'
                self.arming_frame_index = 0
                self.arming_timer = 0.0

        elif self.current_action == 'arming':
            # Update arming animation
            self.arming_timer += dt
            arming_fps = POTATO_MINE_ANIMATIONS['arming']['fps']
            if self.arming_timer >= 1.0 / arming_fps:
                self.arming_timer -= 1.0 / arming_fps
                self.arming_frame_index += 1
                if self.arming_frame_index >= len(self.animation_frames['arming']):
                    self.armed = True
                    self.current_action = 'idle'
                    self.idle_frame_index = 0
                    self.idle_timer = 0.0

        elif self.current_action in ['idle', 'blink']:
            # Check if zombie is stepping on it
            for zombie in self.game.main_game.zombies:
                if zombie.lane == self.row and self.rect.colliderect(zombie.rect):
                    self.current_action = 'explode'
                    self.explode_frame_index = 0
                    self.explode_timer = 0.0
                    self.explode()
                    return

            # Update idle animation
            if self.current_action == 'idle':
                self.idle_timer += dt
                idle_fps = POTATO_MINE_ANIMATIONS['idle']['fps']
                if self.idle_timer >= 1.0 / idle_fps:
                    self.idle_timer -= 1.0 / idle_fps
                    self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

                # Random blink
                if random.random() < self.blink_chance:
                    self.current_action = 'blink'
                    self.blink_frame_index = 0
                    self.blink_timer = 0.0

            # Update blink animation
            elif self.current_action == 'blink':
                self.blink_timer += dt
                blink_fps = POTATO_MINE_ANIMATIONS['blink']['fps']
                if self.blink_timer >= 1.0 / blink_fps:
                    self.blink_timer -= 1.0 / blink_fps
                    self.blink_frame_index += 1
                    if self.blink_frame_index >= len(self.animation_frames['blink']):
                        self.current_action = 'idle'
                        self.blink_frame_index = 0

        super().update(dt)

    def explode(self):
        self.exploded = True
        damage = PLANT_DAMAGE.get("PotatoMine", 1800)
        # Damage zombies in the same cell
        plant_row = self.row
        plant_col = int((self.x - self.game.main_game.game_field.field_x) // self.game.main_game.game_field.cell_width)
        r = plant_row
        c = plant_col
        if 0 <= r < self.game.main_game.game_field.rows and 0 <= c < self.game.main_game.game_field.cols:
            for zombie in self.game.main_game.zombies:
                if zombie.lane == r and abs(zombie.x - (self.game.main_game.game_field.field_x + c * self.game.main_game.game_field.cell_width)) < self.game.main_game.game_field.cell_width:
                    zombie.take_damage(damage)
        # Remove plant from grid
        self.game.main_game.game_field.grid[self.row][plant_col] = None
        self.game.sound_manager.play_sound('potato_mine')

    def draw(self, screen):
        if self.exploded:
            return
        if self.current_action == 'not_armed':
            frame = self.animation_frames['not_armed'][self.not_armed_frame_index]
        elif self.current_action == 'arming':
            frame = self.animation_frames['arming'][self.arming_frame_index]
        elif self.current_action == 'idle':
            frame = self.animation_frames['idle'][self.idle_frame_index]
        elif self.current_action == 'blink':
            frame = self.animation_frames['idle'][self.idle_frame_index].copy()
            blink_frame = self.animation_frames['blink'][self.blink_frame_index]
            frame.blit(blink_frame, (0,0))
        else:
            frame = self.animation_frames['idle'][self.idle_frame_index]  # fallback
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x, self.y))

class SnowPea(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x-30, y, "Snow Pea", game, row)
        self.projectile_speed = 480
        self.damage = PLANT_DAMAGE.get("SnowPea", 20)
        self.fire_rate = PLANT_TIMERS.get("Snow Pea Fire Rate", 1500) / 1000.0
        self.projectile_image = pygame.image.load(PROJECTILE_TEXTURES_PATH["SnowPea"]).convert_alpha()

        # Use preloaded animation frames
        self.animation_frames = {}
        for action_name, action_data in SNOW_PEA_ANIMATIONS.items():
            if isinstance(action_data, dict):  # Проверяем значение (словарь), не ключ
                key = f'snow_pea_{action_name}'
                if key in preloaded_images:
                    self.animation_frames[action_name] = preloaded_images[key]
                else:
                    print(f"Warning: {key} not found in preloaded_images")
        self.rect = self.animation_frames['idle'][0].get_rect(center=(self.x, self.y))
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0
        self.blink_frame_index = 0
        self.blink_timer = 0.0
        self.shoot_frame_index = 0
        self.shoot_timer = 0.0
        self.shoot_bottom_frame_index = 0
        self.shoot_delay = 0.0
        self.shoot_delay_timer = 0.0

    def update(self, dt, zombies):
        # Update idle animation (pauses during blink)
        if self.current_action != 'blink':
            self.idle_timer += dt
            idle_fps = SNOW_PEA_ANIMATIONS['idle']['fps']
            if self.idle_timer >= 1.0 / idle_fps:
                self.idle_timer -= 1.0 / idle_fps
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        # Check if there is a zombie in the same lane ahead
        has_target = any(z for z in zombies if z.lane == self.row and z.x > self.x)
        if has_target:
            if self.shoot_delay == 0.0:
                self.shoot_delay = random.uniform(1.0, 1.5)
            self.shoot_delay_timer += dt
            if self.shoot_delay_timer >= self.shoot_delay:
                current_time = time.time()
                if current_time - self.last_action_time >= self.fire_rate:
                    self.current_action = 'shoot'
                    self.shoot_frame_index = 0
                    self.shoot_timer = 0.0
                    self.shoot_bottom_frame_index = self.idle_frame_index
                    self.shoot()
                    self.last_action_time = current_time
                    self.shoot_delay_timer = 0.0
                    self.shoot_delay = 0.0
        else:
            self.shoot_delay = 0.0
            self.shoot_delay_timer = 0.0

        # Random blink
        if self.current_action == 'idle' and self.idle_frame_index == 0 and random.random() < 0.1:
            self.current_action = 'blink'
            self.blink_frame_index = 0
            self.blink_timer = 0.0

        # Update blink animation
        if self.current_action == 'blink':
            self.blink_timer += dt
            blink_fps = SNOW_PEA_ANIMATIONS['blink']['fps']
            if self.blink_timer >= 1.0 / blink_fps:
                self.blink_timer -= 1.0 / blink_fps
                self.blink_frame_index += 1
                if self.blink_frame_index >= len(self.animation_frames['blink']):
                    self.current_action = 'idle'
                    self.blink_frame_index = 0

        # Update shoot animation
        if self.current_action == 'shoot':
            self.shoot_timer += dt
            shoot_fps = SNOW_PEA_ANIMATIONS['shoot']['fps']
            if self.shoot_timer >= 1.0 / shoot_fps:
                self.shoot_timer -= 1.0 / shoot_fps
                self.shoot_frame_index += 1
                if self.shoot_frame_index >= len(self.animation_frames['shoot']):
                    self.current_action = 'idle'
                    self.shoot_frame_index = 0

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)
        self.projectiles = [p for p in self.projectiles if p.active]

        super().update(dt)

    def shoot(self):
        proj_x = self.x + 50
        proj_y = self.y + 35
        new_proj = Projectile(proj_x, proj_y, self.projectile_speed, self.damage, self.projectile_image, proj_type='snowpea')
        self.projectiles.append(new_proj)
        self.game.sound_manager.play_sound('throw')

    def draw(self, screen):
        super().draw(screen) 
        if self.current_action == 'idle':
            frame = self.animation_frames['idle'][self.idle_frame_index]
        elif self.current_action == 'blink':
            frame = self.animation_frames['idle'][self.idle_frame_index].copy()
            blink_frame = self.animation_frames['blink'][self.blink_frame_index]
            frame.blit(blink_frame, (0,0))
        elif self.current_action == 'shoot':
            frame = self.animation_frames['shoot_bottom'][6].copy()
            shoot_top_frame = self.animation_frames['shoot_top'][self.shoot_frame_index]
            frame.blit(shoot_top_frame, (0,0))
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (180, 180))
        screen.blit(scaled_frame, (self.x, self.y))
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

class Chomper(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Chomper", game, row)
        self.eating_cooldown = PLANT_TIMERS.get("Chomper Cooldown", 40000) / 1000.0  
        self.chewing_duration = PLANT_TIMERS.get("Chomper Chewing Duration", 900) / 1000.0  
        self.last_eat_time = 0.0
        self.chewing_timer = 0.0

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in CHOMPER_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'chomper_{action}']
        self.rect = self.animation_frames['idle'][0].get_rect(center=(self.x, self.y))
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0
        self.attack_frame_index = 0
        self.attack_timer = 0.0
        self.chewing_frame_index = 0
        self.chewing_to_idle_frame_index = 0
        self.chewing_to_idle_timer = 0.0

    def update(self, dt, zombies):
        current_time = time.time()

        # Check for zombies in range if idle and cooldown passed
        if self.current_action == 'idle' and current_time - self.last_eat_time >= self.eating_cooldown:
            cell_width = self.game.main_game.game_field.cell_width
            for zombie in zombies:
                if zombie.lane == self.row and self.x <= zombie.x <= self.x + cell_width * 2:
                    # Eat the zombie
                    zombie.take_damage(9000)  # Instant kill
                    self.current_action = 'attack'
                    self.attack_frame_index = 0
                    self.attack_timer = 0.0
                    self.last_eat_time = current_time
                    self.game.sound_manager.play_sound('chomp')
                    break

        # Update animations based on state
        if self.current_action == 'idle':
            self.idle_timer += dt
            idle_fps = CHOMPER_ANIMATIONS['idle']['fps']
            if self.idle_timer >= 1.0 / idle_fps:
                self.idle_timer -= 1.0 / idle_fps
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        elif self.current_action == 'attack':
            self.attack_timer += dt
            attack_fps = CHOMPER_ANIMATIONS['attack']['fps']
            if self.attack_timer >= 1.0 / attack_fps:
                self.attack_timer -= 1.0 / attack_fps
                self.attack_frame_index += 1
                if self.attack_frame_index >= len(self.animation_frames['attack']):
                    self.current_action = 'chewing'
                    self.chewing_frame_index = 0
                    self.chewing_timer = 0.0

        elif self.current_action == 'chewing':
            self.chewing_timer += dt
            chewing_fps = CHOMPER_ANIMATIONS['chewing']['fps']
            if self.chewing_timer >= 1.0 / chewing_fps:
                self.chewing_timer -= 1.0 / chewing_fps
                self.chewing_frame_index = (self.chewing_frame_index + 1) % len(self.animation_frames['chewing'])
            if self.chewing_timer >= self.chewing_duration:
                self.current_action = 'chewing_to_idle'
                self.chewing_to_idle_frame_index = 0
                self.chewing_to_idle_timer = 0.0

        elif self.current_action == 'chewing_to_idle':
            self.chewing_to_idle_timer += dt
            chewing_to_idle_fps = CHOMPER_ANIMATIONS['chewing_to_idle']['fps']
            if self.chewing_to_idle_timer >= 1.0 / chewing_to_idle_fps:
                self.chewing_to_idle_timer -= 1.0 / chewing_to_idle_fps
                self.chewing_to_idle_frame_index += 1
                if self.chewing_to_idle_frame_index >= len(self.animation_frames['chewing_to_idle']):
                    self.current_action = 'idle'
                    self.idle_frame_index = 0
                    self.idle_timer = 0.0

        super().update(dt)

    def draw(self, screen):
        super().draw(screen) 
        if self.current_action == 'idle':
            frame = self.animation_frames['idle'][self.idle_frame_index]
        elif self.current_action == 'attack':
            frame = self.animation_frames['attack'][self.attack_frame_index]
        elif self.current_action == 'chewing':
            frame = self.animation_frames['chewing'][self.chewing_frame_index]
        elif self.current_action == 'chewing_to_idle':
            frame = self.animation_frames['chewing_to_idle'][self.chewing_to_idle_frame_index]
        else:
            frame = self.animation_frames['idle'][0]  # fallback
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (200, 200))
        screen.blit(scaled_frame, (self.x, self.y-40))

class Repeater(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x-30, y, "Repeater", game, row)
        self.projectile_speed = 480  # pixels per second
        self.damage = PLANT_DAMAGE.get("Pea", 20)
        self.fire_rate = PLANT_TIMERS.get("Repeater Fire Rate", 1500) / 1000.0  # convert ms to seconds
        # Load projectile image
        self.projectile_image = pygame.image.load(PROJECTILE_TEXTURES_PATH["Pea"]).convert_alpha()
        self.shooting_second = False
        self.second_shot_timer = 0.0

        # Use preloaded animation frames
        self.animation_frames = {}
        for action_name, action_data in REPEATER_ANIMATIONS.items():
            if isinstance(action_data, dict):  # Проверяем значение (словарь), не ключ
                key = f'repeater_{action_name}'
                if key in preloaded_images:
                    self.animation_frames[action_name] = preloaded_images[key]
                else:
                    print(f"Warning: {key} not found in preloaded_images")
        self.rect = self.animation_frames['idle'][0].get_rect(center=(self.x, self.y))
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0
        self.blink_frame_index = 0
        self.blink_timer = 0.0
        self.shoot_frame_index = 0
        self.shoot_timer = 0.0
        self.shoot_bottom_frame_index = 0
        self.shoot_delay = 0.0
        self.shoot_delay_timer = 0.0

    def update(self, dt, zombies):
        # Update idle animation (pauses during blink)
        if self.current_action != 'blink':
            self.idle_timer += dt
            idle_fps = REPEATER_ANIMATIONS['idle']['fps']
            if self.idle_timer >= 1.0 / idle_fps:
                self.idle_timer -= 1.0 / idle_fps
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        # Check if there is a zombie in the same lane ahead
        has_target = any(z for z in zombies if z.lane == self.row and z.x > self.x)
        if has_target:
            if self.shoot_delay == 0.0:
                self.shoot_delay = random.uniform(1.0, 1.5)
            self.shoot_delay_timer += dt
            if self.shoot_delay_timer >= self.shoot_delay:
                current_time = time.time()
                if current_time - self.last_action_time >= self.fire_rate:
                    self.current_action = 'shoot'
                    self.shoot_frame_index = 0
                    self.shoot_timer = 0.0
                    self.shoot_bottom_frame_index = self.idle_frame_index
                    self.shooting_second = False
                    self.shoot()
                    self.last_action_time = current_time
                    self.shoot_delay_timer = 0.0
                    self.shoot_delay = 0.0
        else:
            self.shoot_delay = 0.0
            self.shoot_delay_timer = 0.0

        # Random blink
        if self.current_action == 'idle' and self.idle_frame_index == 0 and random.random() < 0.1:  # low chance per frame
            self.current_action = 'blink'
            self.blink_frame_index = 0
            self.blink_timer = 0.0

        # Update blink animation
        if self.current_action == 'blink':
            self.blink_timer += dt
            blink_fps = REPEATER_ANIMATIONS['blink']['fps']
            if self.blink_timer >= 1.0 / blink_fps:
                self.blink_timer -= 1.0 / blink_fps
                self.blink_frame_index += 1
                if self.blink_frame_index >= len(self.animation_frames['blink']):
                    self.current_action = 'idle'
                    self.blink_frame_index = 0

        # Update shoot animation
        if self.current_action == 'shoot':
            self.shoot_timer += dt
            shoot_fps = REPEATER_ANIMATIONS['shoot']['fps']
            if self.shoot_timer >= 1.0 / shoot_fps:
                self.shoot_timer -= 1.0 / shoot_fps
                self.shoot_frame_index += 1
                if self.shoot_frame_index >= len(self.animation_frames['shoot']):
                    self.current_action = 'idle'
                    self.shoot_frame_index = 0

        if self.shooting_second:
            self.second_shot_timer -= dt
            if self.second_shot_timer <= 0:
                # shoot second
                proj_x = self.x + 50
                proj_y = self.y + 35
                new_proj = Projectile(proj_x, proj_y, self.projectile_speed, self.damage, self.projectile_image)
                self.projectiles.append(new_proj)
                self.game.sound_manager.play_sound('throw')
                self.shooting_second = False

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)
        # Remove inactive projectiles
        self.projectiles = [p for p in self.projectiles if p.active]

        super().update(dt)

    def shoot(self):
        # First shot
        proj_x = self.x + 50
        proj_y = self.y + 35
        new_proj = Projectile(proj_x, proj_y, self.projectile_speed, self.damage, self.projectile_image)
        self.projectiles.append(new_proj)
        self.game.sound_manager.play_sound('throw')
        # Set up second shot
        self.shooting_second = True
        self.second_shot_timer = 0.3  # 150 ms delay for second shot

    def draw(self, screen):
        super().draw(screen) 
        if self.current_action == 'idle':
            frame = self.animation_frames['idle'][self.idle_frame_index]
        elif self.current_action == 'blink':
            frame = self.animation_frames['idle'][self.idle_frame_index].copy()
            blink_frame = self.animation_frames['blink'][self.blink_frame_index]
            frame.blit(blink_frame, (0,0))
        elif self.current_action == 'shoot':
            # shoot_bottom is the base, shoot_top overlays on head
            frame = self.animation_frames['shoot_bottom'][6].copy()
            shoot_top_frame = self.animation_frames['shoot_top'][self.shoot_frame_index]
            frame.blit(shoot_top_frame, (0,0))
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (180, 180))
        screen.blit(scaled_frame, (self.x, self.y))
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

class LilyPad(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Lily Pad", game, row)

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in LILYPAD_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'lilypad_{action}']
        self.current_action = 'blink'
        self.blink_frame_index = 0
        self.blink_timer = 0.0

    def update(self, dt):
        # Update blink animation
        self.blink_timer += dt
        blink_fps = LILYPAD_ANIMATIONS['blink']['fps']
        if self.blink_timer >= 1.0 / blink_fps:
            self.blink_timer -= 1.0 / blink_fps
            self.blink_frame_index = (self.blink_frame_index + 1) % len(self.animation_frames['blink'])

        super().update(dt)

    def draw(self, screen):
        frame = self.animation_frames['blink'][self.blink_frame_index]
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x, self.y))

class PuffShroom(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Puff Shroom", game, row)
        self.projectiles = []
        self.projectile_speed = 480
        self.damage = PLANT_DAMAGE.get("Puffshroom", 20)
        self.fire_rate = PLANT_TIMERS.get("Puffshroom Fire Rate", 1500) / 1000.0
        self.projectile_image = pygame.image.load(PROJECTILE_TEXTURES_PATH["Spore"]).convert_alpha()
        self.asleep = not self.game.main_game.is_day  # Sleep during day

        # Use preloaded animation frames
        self.animation_frames = {}
        for action_name, action_data in PUFFSHROOM_ANIMATIONS.items():
            if isinstance(action_data, dict):  # Проверяем значение (словарь), не ключ
                key = f'puffshroom_{action_name}'
                if key in preloaded_images:
                    self.animation_frames[action_name] = preloaded_images[key]
                else:
                    print(f"Warning: {key} not found in preloaded_images")
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0
        self.blink_frame_index = 0
        self.blink_timer = 0.0
        self.shoot_frame_index = 0
        self.shoot_timer = 0.0
        self.sleep_frame_index = 0
        self.sleep_timer = 0.0

    def update(self, dt, zombies):
        self.asleep = self.game.main_game.is_day  # Sleep during day

        if self.asleep:
            # Update sleep animation
            self.sleep_timer += dt
            sleep_fps = PUFFSHROOM_ANIMATIONS['sleep']['fps']
            if self.sleep_timer >= 1.0 / sleep_fps:
                self.sleep_timer -= 1.0 / sleep_fps
                self.sleep_frame_index = (self.sleep_frame_index + 1) % len(self.animation_frames['sleep'])
            return  # No actions when asleep

        # Update idle animation (pauses during blink/shoot)
        if self.current_action not in ['blink', 'shoot']:
            self.idle_timer += dt
            idle_fps = PUFFSHROOM_ANIMATIONS['idle']['fps']
            if self.idle_timer >= 1.0 / idle_fps:
                self.idle_timer -= 1.0 / idle_fps
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        # Check for targets within 3 cells
        cell_width = self.game.main_game.game_field.cell_width
        has_target = any(z for z in zombies if z.lane == self.row and z.x > self.x and z.x - self.x <= 3 * cell_width)
        if has_target:
            current_time = time.time()
            if current_time - self.last_action_time >= self.fire_rate:
                self.current_action = 'shoot'
                self.shoot_frame_index = 0
                self.shoot_timer = 0.0
                self.shoot()
                self.last_action_time = current_time

        # Random blink
        if self.current_action == 'idle' and self.idle_frame_index == 0 and random.random() < 0.1:
            self.current_action = 'blink'
            self.blink_frame_index = 0
            self.blink_timer = 0.0

        # Update blink animation
        if self.current_action == 'blink':
            self.blink_timer += dt
            blink_fps = PUFFSHROOM_ANIMATIONS['blink']['fps']
            if self.blink_timer >= 1.0 / blink_fps:
                self.blink_timer -= 1.0 / blink_fps
                self.blink_frame_index += 1
                if self.blink_frame_index >= len(self.animation_frames['blink']):
                    self.current_action = 'idle'
                    self.blink_frame_index = 0

        # Update shoot animation
        if self.current_action == 'shoot':
            self.shoot_timer += dt
            shoot_fps = PUFFSHROOM_ANIMATIONS['shoot']['fps']
            if self.shoot_timer >= 1.0 / shoot_fps:
                self.shoot_timer -= 1.0 / shoot_fps
                self.shoot_frame_index += 1
                if self.shoot_frame_index >= len(self.animation_frames['shoot']):
                    self.current_action = 'idle'
                    self.shoot_frame_index = 0

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)
        self.projectiles = [p for p in self.projectiles if p.active]

        super().update(dt)

    def shoot(self):
        proj_x = self.x + 60
        proj_y = self.y + 100
        max_distance = 3 * self.game.main_game.game_field.cell_width
        new_proj = Projectile(proj_x, proj_y, self.projectile_speed, self.damage, self.projectile_image, proj_type='puff', max_distance=max_distance)
        self.projectiles.append(new_proj)
        self.game.sound_manager.play_sound('throw')

    def draw(self, screen):
        if self.asleep:
            frame = self.animation_frames['sleep'][self.sleep_frame_index]
        else:
            if self.current_action == 'idle':
                frame = self.animation_frames['idle'][self.idle_frame_index]
            elif self.current_action == 'blink':
                frame = self.animation_frames['idle'][self.idle_frame_index].copy()
                blink_frame = self.animation_frames['blink'][self.blink_frame_index]
                frame.blit(blink_frame, (0,0))
            elif self.current_action == 'shoot':
                frame = self.animation_frames['shoot'][self.shoot_frame_index]
            else:
                frame = self.animation_frames['idle'][self.idle_frame_index]  # fallback
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (80, 80))
        screen.blit(scaled_frame, (self.x+40, self.y+40))
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

class SunShroom(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Sun Shroom", game, row)
        self.sun_production_rate = PLANT_TIMERS.get("Sun-shroom Production Rate", 25000) / 1000.0  # 25 seconds
        self.grow_time = PLANT_TIMERS.get("Sun-shroom Grow Time", 120000) / 1000.0  # 120 seconds
        self.sun_timer = 0.0
        self.grow_timer = self.grow_time
        self.suns = []  # List to hold spawned suns

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in SUN_SHROOM_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'sun_shroom_{action}']
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        # Only produce suns at night
        if not self.game.main_game.is_day:
            # Update grow timer
            self.grow_timer = max(0, self.grow_timer - dt)
            # Produce sun
            self.sun_timer += dt
            if self.sun_timer >= self.sun_production_rate:
                # Spawn a sun object
                sun_x = self.x + 50  # Position relative to sunshroom
                sun_y = self.y + 20
                if self.grow_timer > 0:
                    # Small sun
                    new_sun = Sun(sun_x, sun_y, self.game, sun_type='sunshroom', value=15, size=(80, 80))
                else:
                    # Normal sun
                    new_sun = Sun(sun_x, sun_y, self.game, sun_type='sunshroom', value=25, size=(160, 160))
                self.suns.append(new_sun)
                self.sun_timer = 0.0

        # Update suns
        for sun in self.suns:
            sun.update(dt)
        # Remove collected suns
        self.suns = [s for s in self.suns if not s.collected]

        # Update idle animation
        self.idle_timer += dt
        idle_fps = SUN_SHROOM_ANIMATIONS['idle']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        super().update(dt)

    def draw(self, screen):
        frame = self.animation_frames['idle'][self.idle_frame_index]
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x, self.y))
        # Draw suns
        for sun in self.suns:
            sun.draw(screen)

class FumeShroom(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Fume Shroom", game, row)

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in FUME_SHROOM_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'fume_shroom_{action}']
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        # Update idle animation
        self.idle_timer += dt
        idle_fps = FUME_SHROOM_ANIMATIONS['idle']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        super().update(dt)

    def draw(self, screen):
        super().draw(screen) 
        frame = self.animation_frames['idle'][self.idle_frame_index]
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (160, 130))
        screen.blit(scaled_frame, (self.x, self.y))

class GraveBuster(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Grave Buster", game, row)

        # Use preloaded animation frames
        self.animation_frames = {}
        for action in GRAVE_BUSTER_ANIMATIONS:
            self.animation_frames[action] = preloaded_images[f'grave_buster_{action}']
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        # Update idle animation
        self.idle_timer += dt
        idle_fps = GRAVE_BUSTER_ANIMATIONS['idle']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

        super().update(dt)

    def draw(self, screen):
        frame = self.animation_frames['idle'][self.idle_frame_index]
        if self.damage_flash_timer > 0:
            frame = frame.copy()
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((128, 0, 0, 0))
            tint_alpha = pygame.surfarray.pixels_alpha(tint)
            frame_alpha = pygame.surfarray.pixels_alpha(frame)
            tint_alpha[:] = frame_alpha
            frame.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x, self.y))

class Sun:
    def __init__(self, x, y, game, sun_type='sunflower', value=25, size=(160, 160)):
        self.x = x
        self.y = y
        self.game = game
        self.sun_type = sun_type  # 'sunflower' or 'sky'
        self.value = value
        self.size = size
        self.collected = False
        self.animation_frames = preloaded_images['sun_idle']
        self.current_frame = 0
        self.frame_timer = 0.0
        self.frame_duration = 1.0 / SUN_ANIMATIONS['idle']['fps']
        self.rect = self.animation_frames[0].get_rect(center=(self.x, self.y))

        if sun_type == 'sunflower':
            # Arc up and fall
            self.speed_x = random.choice([-30, 30])  # random left or right
            self.speed_y = -100  # upward
            self.gravity = 200
            self.target_y = y + 100  # fall to below sunflower
        elif sun_type == 'sunshroom':
            # Fall straight down 1 cell
            self.speed_x = 0
            self.speed_y = 50  # downward
            self.gravity = 0
            self.target_y = y + 80  # fall 1 cell (assuming cell width ~80)
        elif sun_type == 'sky':
            # Fall from sky
            self.speed_x = 0
            self.speed_y = 50  # downward
            self.gravity = 0  # no gravity, constant fall

    def update(self, dt):
        if self.collected:
            return
        # Animate sun
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        # Move sun
        if hasattr(self, 'speed_x'):
            self.x += self.speed_x * dt
        self.speed_y += self.gravity * dt
        self.y += self.speed_y * dt
        if self.sun_type == 'sunflower':
            if self.y >= self.target_y:
                self.y = self.target_y
                self.speed_y = 0
                self.speed_x = 0
        elif self.sun_type == 'sunshroom':
            if self.y >= self.target_y:
                self.y = self.target_y
                self.speed_y = 0
                self.speed_x = 0
        elif self.sun_type == 'sky':
            if self.y > self.game.height - 100:
                self.y = self.game.height - 100
                self.speed_y = 0
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        if self.collected:
            return
        frame = self.animation_frames[self.current_frame]
        scaled_frame = pygame.transform.scale(frame, self.size)
        screen.blit(scaled_frame, (self.rect.x, self.rect.y))

    def collect(self):
        self.collected = True
        self.game.main_game.sun_count += self.value
        self.game.sound_manager.play_sound('points')

class Coin:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.value = 10
        self.collected = False
        self.animation_frames = {}
        self.animation_frames = preloaded_images["coin_silver"]

        self.current_frame = 0
        self.frame_timer = 0.0
        self.frame_duration = 1.0 / COIN_SILVER_ANIMATIONS['idle']['fps']
        self.rect = self.animation_frames[0].get_rect(center=(self.x, self.y))


        # Fall straight down
        self.speed_x = 0
        self.speed_y = 50  # downward
        self.gravity = 0  # no gravity, constant fall

    def update(self, dt):
        if self.collected:
            return
        # Animate coin
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        # Move coin
        self.y += self.speed_y * dt
        if self.y > self.game.height - 100:
            self.y = self.game.height - 100
            self.speed_y = 0
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        if self.collected:
            return
        frame = self.animation_frames[self.current_frame]
        scaled_frame = pygame.transform.scale(frame, (80, 80))  # Smaller than sun
        screen.blit(scaled_frame, (self.rect.x, self.rect.y))

    def collect(self):
        self.collected = True
        self.game.main_game.coin_count += self.value
        self.game.sound_manager.play_sound('points')
