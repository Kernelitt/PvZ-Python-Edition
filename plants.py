import pygame
import time
import math
import random
from definitions import *
from zombie_animations import *

class Projectile:
    def __init__(self, x, y, speed, damage, image, angle=0):
        self.x = x
        self.y = y
        self.speed = speed  # pixels per second
        self.damage = damage
        self.image = image
        self.angle = angle  # in radians, 0 is right
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.active = True

    def update(self, dt):
        self.x += self.speed * dt * math.cos(self.angle)
        self.y += self.speed * dt * math.sin(self.angle)
        self.rect.center = (int(self.x), int(self.y))
        # Deactivate if off screen (assuming screen width 1920, height 1080)
        if self.x > 1920 or self.x < 0 or self.y > 1080 or self.y < 0:
            self.active = False

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image,(32,32)), self.rect)

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

    def update(self, dt):
        # Base plant does nothing
        pass

    def draw(self, screen):
        # Placeholder: draw a rectangle for the plant
        pygame.draw.rect(screen, (0, 188, 0), (self.x + 50, self.y + 70, 70, 70))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            # Remove plant from game grid or mark dead
            # This should be handled by game logic

class Peashooter(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x-30, y, "Peashooter", game, row)
        self.projectile_speed = 480  # pixels per second
        self.damage = PLANT_DAMAGE.get("Pea", 20)
        self.fire_rate = PLANT_TIMERS.get("Peashooter Fire Rate", 1500) / 1000.0  # convert ms to seconds
        # Load projectile image
        self.projectile_image = pygame.image.load(PROJECTILE_TEXTURES_PATH["Pea"]).convert_alpha()

        # Load animation frames
        self.animation_frames = {}
        for action in PEASHOOTER_ANIMATIONS:
            frames = get_animation_frames(action, 'peashooter')
            self.animation_frames[action] = [pygame.image.load(f'animations/peashooter/Peashooter{f:04d}.png') for f in frames]
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
                    self.shoot_bottom_frame_index = self.idle_frame_index  # start from current idle frame
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

    def shoot(self):
        # Create a new projectile starting at plant's position
        proj_x = self.x + 50  # start at right edge of plant
        proj_y = self.y + 35  # roughly middle height of plant
        new_proj = Projectile(proj_x, proj_y, self.projectile_speed, self.damage, self.projectile_image)
        self.projectiles.append(new_proj)

    def draw(self, screen):
        if self.current_action == 'idle':
            frame = self.animation_frames['idle'][self.idle_frame_index]
        elif self.current_action == 'blink':
            frame = self.animation_frames['idle'][self.idle_frame_index].copy()
            blink_frame = self.animation_frames['blink'][self.blink_frame_index]
            frame.blit(blink_frame, (0,0))
        elif self.current_action == 'shoot':
            # shoot_bottom is the base, shoot_top overlays on head
            frame = self.animation_frames['shoot_bottom'][self.shoot_bottom_frame_index].copy()
            shoot_top_frame = self.animation_frames['shoot_top'][self.shoot_frame_index]
            frame.blit(shoot_top_frame, (0,0))
        scaled_frame = pygame.transform.scale(frame, (180, 180))
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

        # Load animation frames
        self.animation_frames = {}
        for action in SUNFLOWER_ANIMATIONS:
            frames = get_animation_frames(action, 'sunflower')
            self.animation_frames[action] = [pygame.image.load(f'animations/sunflower/Sunflower{f:04d}.png') for f in frames]
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        # Produce sun
        self.sun_timer += dt
        if self.sun_timer >= self.sun_production_rate:
            # Spawn a sun object instead of directly adding to sun_count
            sun_x = self.x + 50  # Position relative to sunflower
            sun_y = self.y + 20
            new_sun = Sun(sun_x, sun_y, self.game)
            self.suns.append(new_sun)
            self.sun_timer = 0.0

        # Update suns
        for sun in self.suns:
            sun.update(dt)

        # Update idle animation
        self.idle_timer += dt
        idle_fps = SUNFLOWER_ANIMATIONS['idle']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

    def draw(self, screen):
        frame = self.animation_frames['idle'][self.idle_frame_index]
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x-20, self.y))
        # Draw suns
        for sun in self.suns:
            sun.draw(screen)

class CherryBomb(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Cherry Bomb", game, row)

        # Load animation frames
        self.animation_frames = {}
        for action in CHERRYBOMB_ANIMATIONS:
            frames = get_animation_frames(action, 'cherrybomb')
            self.animation_frames[action] = [pygame.image.load(f'animations/cherry_bomb/Cherrybomb{f:04d}.png') for f in frames]
        self.current_action = 'idle'
        self.idle_frame_index = 0
        self.idle_timer = 0.0

    def update(self, dt):
        # Update idle animation
        self.idle_timer += dt
        idle_fps = CHERRYBOMB_ANIMATIONS['idle']['fps']
        if self.idle_timer >= 1.0 / idle_fps:
            self.idle_timer -= 1.0 / idle_fps
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.animation_frames['idle'])

    def draw(self, screen):
        frame = self.animation_frames['idle'][self.idle_frame_index]
        scaled_frame = pygame.transform.scale(frame, (200, 200))
        screen.blit(scaled_frame, (self.x, self.y))

class WallNut(Plant):
    def __init__(self, x, y, game, row):
        super().__init__(x, y, "Wall Nut", game, row)

        # Load animation frames
        self.animation_frames = {}
        for action in WALLNUT_ANIMATIONS:
            frames = get_animation_frames(action, 'wallnut')
            self.animation_frames[action] = [pygame.image.load(f'animations/wallnut/Wallnut{f:04d}.png') for f in frames]
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

    def draw(self, screen):
        frame = self.animation_frames['idle'][self.idle_frame_index]
        scaled_frame = pygame.transform.scale(frame, (160, 160))
        screen.blit(scaled_frame, (self.x, self.y))

class Sun:
    def __init__(self, x, y, game, sun_type='sunflower'):
        self.x = x
        self.y = y
        self.game = game
        self.sun_type = sun_type  # 'sunflower' or 'sky'
        self.collected = False
        self.animation_frames = []
        frames = get_animation_frames('idle', 'sun')
        for f in frames:
            img = pygame.image.load(f'animations/sun/Sun{f:04d}.png').convert_alpha()
            self.animation_frames.append(img)
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
        elif self.sun_type == 'sky':
            if self.y > self.game.height - 100:
                self.y = self.game.height - 100
                self.speed_y = 0
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        if self.collected:
            return
        frame = self.animation_frames[self.current_frame]
        scaled_frame = pygame.transform.scale(frame, (80, 80))
        screen.blit(scaled_frame, (self.rect.x, self.rect.y))

    def collect(self):
        self.collected = True
        self.game.main_game.sun_count += 25
        self.game.sound_manager.play_sound('plant')
