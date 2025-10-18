import pygame
import random
import json
import threading
import queue
from simple_framework import SimpleSettingsWindow, SimpleWindowScaler, SimplePygameField, SimplePygameButton, SimpleImageButton
from os import getcwd
print(getcwd())

class Slider:
    def __init__(self, position, width, height, min_value, max_value, initial_value, on_change):
        self.position = position  # (x, y)
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.on_change = on_change
        self.dragging = False
        self.knob_radius = height // 2

    def draw(self, screen):
        # Draw bar
        bar_rect = pygame.Rect(self.position[0], self.position[1] + self.height // 2 - 2, self.width, 4)
        pygame.draw.rect(screen, (200, 200, 200), bar_rect)
        # Draw knob
        knob_x = self.position[0] + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width)
        knob_y = self.position[1] + self.height // 2
        pygame.draw.circle(screen, (100, 100, 100), (knob_x, knob_y), self.knob_radius)

    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        knob_x = self.position[0] + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width)
        knob_y = self.position[1] + self.height // 2
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (mouse_pos[0] - knob_x)**2 + (mouse_pos[1] - knob_y)**2 <= self.knob_radius**2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = mouse_pos[0] - self.position[0]
            self.value = self.min_value + (rel_x / self.width) * (self.max_value - self.min_value)
            self.value = max(self.min_value, min(self.max_value, self.value))
            self.on_change(self.value)

from definitions import *
from plants import *
from zombie_animations import *
from zombies import Zombie, ConeheadZombie, BucketheadZombie, PoleVaulterZombie
from preloader import preload_all, preload_ui

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5  # Default music volume
        self.sfx_volume = 0.5    # Default sound effects volume
        self.muted = False
        self.current_music = None
        self.music_files = {
            'menu': 'music/crazy_dave.mp3',
            'seed_select': 'music/choose_your_seeds.mp3',

            'music_day': 'music/grasswalk.mp3',
            'music_night': 'music/moongrains.mp3',
            'music_pool': 'music/watery_graves.mp3',
            'music_fog': 'music/rigor_mormist.mp3',
            'music_roof': 'music/graze_the_roof.mp3',

            'X-10': 'music/braniac_maniac.mp3',
            'minigames_X-5': 'music/loonboon.mp3',
            '5-10': 'music/ultimate_battle.mp3',
            'zen_garden': 'music/zen_garden.mp3',

            'win': 'sounds/winmusic.ogg',
            'lose': 'sounds/losemusic.ogg'
        }
        self.sound_effects = {}
        sound_files = {
            'zombie_impact1': 'sounds/splat.ogg',
            'zombie_impact2': 'sounds/splat2.ogg',
            'zombie_impact3': 'sounds/splat3.ogg',
            'cone_impact1': 'sounds/plastichit.ogg',
            'cone_impact2': 'sounds/plastichit2.ogg',
            'bucket_impact1': 'sounds/shieldhit.ogg',
            'bucket_impact2': 'sounds/shieldhit2.ogg',
            'zombie_frozen': 'sounds/frozen.ogg',

            'seed_packet_click':'sounds/seed_lift',
            'plant': 'sounds/plant.ogg',
            'plant2': 'sounds/plant2.ogg',
            'plant_on_water': 'sounds/plant_water.ogg',

            'zombie_death': 'sounds/splat.ogg',

            'zombie_falling1': 'sounds/zombie_falling_1.ogg',
            'zombie_falling2': 'sounds/zombie_falling_2.ogg',

            'zombie_attack1': 'sounds/chomp.ogg',
            'zombie_attack2': 'sounds/chomp2.ogg',

            'zombies_are_coming': 'sounds/awooga.ogg',

            'plant_break': 'sounds/gulp.ogg',

            'bigchomp': 'sounds/bigchomp.ogg',
            'cherrybomb': 'sounds/cherrybomb.ogg',
            'potato_mine': 'sounds/potato_mine.ogg',
            'jalapeno': 'sounds/jalapeno.ogg',
            'firepea': 'sounds/firepea.ogg',
            'butter': 'sounds/butter.ogg',
            'balloon_pop': 'sounds/balloon_pop.ogg',
            'zombie_entering_water': 'sounds/zombie_entering_water.ogg',
            'zombie_splash': 'sounds/zombiesplash.ogg',
            'limbs_pop': 'sounds/limbs_pop.ogg',
            'newspaper_rip': 'sounds/newspaper_rarrgh.ogg',
            'polevault': 'sounds/polevault.ogg',
            'pogo_zombie': 'sounds/pogo_zombie.ogg',
            'digger_zombie': 'sounds/digger_zombie.ogg',
            'ladder_zombie': 'sounds/ladder_zombie.ogg',
            'bungee_scream': 'sounds/bungee_scream.ogg',
            'jackinthebox': 'sounds/jackinthebox.ogg',
            'jack_surprise': 'sounds/jack_surprise.ogg',
            'finalwave': 'sounds/finalwave.ogg',
            'hugewave': 'sounds/hugewave.ogg',
            'readysetplant': 'sounds/readysetplant.ogg',
            'finalfanfare': 'sounds/finalfanfare.ogg',
            'prize': 'sounds/prize.ogg',
            'slotmachine': 'sounds/slotmachine.ogg',
            'buttonclick': 'sounds/buttonclick.ogg',
            'pause': 'sounds/pause.ogg',
            'seedlift': 'sounds/seedlift.ogg',
            'points': 'sounds/points.ogg',
            'boing': 'sounds/boing.ogg',
            'bonk': 'sounds/bonk.ogg',
            'throw': 'sounds/throw.ogg',
            'throw2': 'sounds/throw2.ogg',
            'coin_collect': 'sounds/coin.ogg',
            'shovel': 'sounds/shovel.ogg',
            'explosion': 'sounds/explosion.ogg'
        }
        for name, path in sound_files.items():
            try:
                self.sound_effects[name] = pygame.mixer.Sound(path)
            except:
                self.sound_effects[name] = None
        self.update_volumes()

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        self.update_volumes()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        self.update_volumes()

    def update_volumes(self):
        pygame.mixer.music.set_volume(self.music_volume)
        for sound in self.sound_effects.values():
            if sound:
                sound.set_volume(self.sfx_volume)

    def mute(self):
        self.muted = True
        pygame.mixer.music.set_volume(0)
        for sound in self.sound_effects.values():
            if sound:
                sound.set_volume(0)

    def unmute(self):
        self.muted = False
        self.update_volumes()

    def play_music(self, state):
        if state in self.music_files:
            if self.current_music != state:
                pygame.mixer.music.load(self.music_files[state])
                loops = 0 if state in ['win', 'lose'] else -1
                pygame.mixer.music.play(loops)
                self.current_music = state

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sound(self, sound_name):
        if sound_name in self.sound_effects and self.sound_effects[sound_name]:
            self.sound_effects[sound_name].play()



class GameField:
    def __init__(self, scaler, width, height, game):
        self.game = game
        self.scaler = scaler
        self.screen_width = width
        self.screen_height = height
        self.rows = 5
        self.cols = 9
        self.cell_width = self.scaler.scale_x((1770 - 450) / 9)  # Adjusted cell width
        self.cell_height = self.scaler.scale_y((1025 - 160) / 5)  # Adjusted cell height
        self.field_x = self.scaler.scale_x(450)  # Top-left x
        self.field_y = self.scaler.scale_y(160)  # Top-left y
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]  # Placeholder for plants
        self.plant_classes = {
            'Peashooter': Peashooter,
            'Sunflower': Sunflower,
            'Cherry Bomb': CherryBomb,
            'Wall Nut': WallNut,
            'Potato Mine': PotatoMine,
            'Snow Pea': SnowPea,
            'Chomper': Chomper,
            'Repeater': Repeater,
            'Lily Pad': LilyPad,
            'Puff Shroom': PuffShroom,
            'Sun Shroom': SunShroom,
            'Fume Shroom': FumeShroom,
            'Grave Buster': GraveBuster,
        }

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.field_x + col * self.cell_width
                y = self.field_y + row * self.cell_height
                pygame.draw.rect(screen, (0, 255, 0), (x, y, self.cell_width, self.cell_height), 2)  # Green border
                # Draw plant if present
                plant = self.grid[row][col]
                if plant:
                    if hasattr(plant, 'draw'):
                        plant.draw(screen)
                    else:
                        plant_rect = pygame.Rect(x + 5, y + 5, self.cell_width - 10, self.cell_height - 10)
                        pygame.draw.rect(screen, plant['color'], plant_rect)

    def handle_click(self, pos, selected_plant):
        x, y = pos
        if self.field_x <= x < self.field_x + self.cols * self.cell_width and self.field_y <= y < self.field_y + self.rows * self.cell_height:
            col = (x - self.field_x) // self.cell_width
            row = (y - self.field_y) // self.cell_height
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if selected_plant:
                    # Check recharge timer
                    if self.game.main_game.seed_recharge_timers[selected_plant['name']] > 0:
                        print("Seed is recharging!")
                        return
                    # Plant in the cell if empty
                    if self.grid[row][col] is None:
                        sun_cost = PLANT_SUN_COST.get(selected_plant['name'], 0)
                        if self.game.main_game.sun_count >= sun_cost:
                            self.game.main_game.sun_count -= sun_cost
                            plant_class = self.plant_classes.get(selected_plant['name'])
                            if plant_class:
                                x_pos = self.field_x + col * self.cell_width + 5
                                y_pos = self.field_y + row * self.cell_height + 5
                                plant = plant_class(x_pos, y_pos, self.game, row)
                                self.grid[row][col] = plant
                                self.game.sound_manager.play_sound('plant')
                                print(f"Planted {selected_plant['name']} at cell ({row}, {col})")
                            else:
                                health = PLANT_HEALTH.get(selected_plant['name'], PLANT_HEALTH.get('Basic Plants', 300))
                                self.grid[row][col] = {'name': selected_plant['name'], 'color': selected_plant.get('color', (255,0,0)), 'health': health}
                                self.game.sound_manager.play_sound('plant')
                                print(f"Planted {selected_plant['name']} at cell ({row}, {col})")
                            # Reset recharge timer
                            self.game.main_game.seed_recharge_timers[selected_plant['name']] = PLANT_RECHARGE[selected_plant['name']] / 100
                            self.game.main_game.selected_seed = None
                        else:
                            print("Not enough sun!")
                else:
                    print(f"Clicked on cell ({row}, {col}) - No plant selected")

    def remove_plant(self, pos):
        x, y = pos
        if self.field_x <= x < self.field_x + self.cols * self.cell_width and self.field_y <= y < self.field_y + self.rows * self.cell_height:
            col = (x - self.field_x) // self.cell_width
            row = (y - self.field_y) // self.cell_height
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if self.grid[row][col] is not None:
                    self.grid[row][col] = None
                    print(f"Removed plant at cell ({row}, {col})")

class MainMenu:
    def __init__(self, game):
        self.game = game

        # Load animation frames for main menu
        self.animation_frames = [pygame.image.load(f'animations/main_menu/Selectorscreen{f:04d}.png') for f in range(1, 41)]
        self.current_frame = 0
        self.animation_timer = 0.0
        self.frame_duration = 1.0 / 24
        self.playing_animation = True

        self.image_buttons = []

        # Adventure button
        adventure_normal = pygame.image.load('reanim/SelectorScreen_Adventure_button.png')
        adventure_hover = pygame.image.load('reanim/SelectorScreen_Adventure_highlight.png')
        adventure_button = SimpleImageButton(
            (game.scaler.scale_x(1000), game.scaler.scale_y(160)),
            (game.scaler.scale_x(adventure_normal.get_width()*1.6), game.scaler.scale_y(adventure_normal.get_height()*1.6)),
            adventure_normal,
            adventure_hover,
            self.start_game
        )
        self.image_buttons.append(adventure_button)

        # Mini-Games button
        minigames_normal = pygame.image.load('reanim/SelectorScreen_Minigames_button.png')
        minigames_hover = pygame.image.load('reanim/SelectorScreen_Minigames_highlight.png')
        minigames_button = SimpleImageButton(
            (game.scaler.scale_x(1000), game.scaler.scale_y(320)),
            (game.scaler.scale_x(minigames_normal.get_width()*1.6), game.scaler.scale_y(minigames_normal.get_height()*1.6)),
            minigames_normal,
            minigames_hover,
            self.open_minigames
        )
        self.image_buttons.append(minigames_button)

        # Puzzle button
        puzzle_normal = pygame.image.load('reanim/SelectorScreen_Puzzles_button.png')
        puzzle_hover = pygame.image.load('reanim/SelectorScreen_Puzzles_highlight.png')
        puzzle_button = SimpleImageButton(
            (game.scaler.scale_x(1000), game.scaler.scale_y(470)),
            (game.scaler.scale_x(puzzle_normal.get_width()*1.6), game.scaler.scale_y(puzzle_normal.get_height()*1.6)),
            puzzle_normal,
            puzzle_hover,
            self.open_puzzle
        )
        self.image_buttons.append(puzzle_button)

        # Survival button
        survival_normal = pygame.image.load('reanim/SelectorScreen_Survival_button.png')
        survival_hover = pygame.image.load('reanim/SelectorScreen_Survival_highlight.png')
        survival_button = SimpleImageButton(
            (game.scaler.scale_x(1000), game.scaler.scale_y(610)),
            (game.scaler.scale_x(survival_normal.get_width()*1.6), game.scaler.scale_y(survival_normal.get_height()*1.6)),
            survival_normal,
            survival_hover,
            self.open_survival
        )
        self.image_buttons.append(survival_button)

        almanac_button = SimpleImageButton(
            (game.scaler.scale_x(850), game.scaler.scale_y(800)),
            (game.scaler.scale_x(99*1.6), game.scaler.scale_y(99*1.6)),
            pygame.image.load('images/SelectorScreen_Almanac.png'),
            pygame.image.load('images/SelectorScreen_AlmanacHighlight.png'),
            self.open_almanac
        )
        self.image_buttons.append(almanac_button)

        store_button = SimpleImageButton(
            (game.scaler.scale_x(960), game.scaler.scale_y(850)),
            (game.scaler.scale_x(130*1.6), game.scaler.scale_y(89*1.6)),
            pygame.image.load('images/SelectorScreen_Store.png'),
            pygame.image.load('images/SelectorScreen_StoreHighlight.png'),
            self.open_store
        )
        self.image_buttons.append(store_button)

        help_button = SimpleImageButton(
            (game.scaler.scale_x(1270), game.scaler.scale_y(950)),
            (game.scaler.scale_x(48*2), game.scaler.scale_y(22*2)),
            pygame.image.load('images/SelectorScreen_Help1.png'),
            pygame.image.load('images/SelectorScreen_Help2.png'),
            self.open_help
        )
        self.image_buttons.append(help_button)

        options_button = SimpleImageButton(
            (game.scaler.scale_x(1400), game.scaler.scale_y(1000)),
            (game.scaler.scale_x(81*1.2), game.scaler.scale_y(31*1.2)),
            pygame.image.load('images/SelectorScreen_Options1.png'),
            pygame.image.load('images/SelectorScreen_Options2.png'),
            self.open_settings
        )
        self.image_buttons.append(options_button)

        quit_button = SimpleImageButton(
            (game.scaler.scale_x(1530), game.scaler.scale_y(970)),
            (game.scaler.scale_x(47*2), game.scaler.scale_y(27*2)),
            pygame.image.load('images/SelectorScreen_Quit1.png'),
            pygame.image.load('images/SelectorScreen_Quit2.png'),
            self.quit_game
        )
        self.image_buttons.append(quit_button)

        # Text buttons for progress management
        self.text_buttons = []
        complete_button = SimplePygameButton(
            (game.scaler.scale_x(100), game.scaler.scale_y(700)),
            (game.scaler.scale_x(200), game.scaler.scale_y(50)),
            [("Complete All", (50, 15))],
            self.complete_all,
            (0, 128, 0)
        )
        self.text_buttons.append(complete_button)

        reset_button = SimplePygameButton(
            (game.scaler.scale_x(100), game.scaler.scale_y(760)),
            (game.scaler.scale_x(200), game.scaler.scale_y(50)),
            [("Reset Progress", (40, 15))],
            self.reset_progress,
            (128, 0, 0)
        )
        self.text_buttons.append(reset_button)

    def start_game(self):
        self.game.menu = Menu(game=self.game)
        self.game.state = 'level_menu'

    def open_minigames(self):
        print("Mini-Games...")

    def open_puzzle(self):
        print("Puzzle...")

    def open_survival(self):
        print("Survival...")

    def open_almanac(self):
        # Import Almanac class here to avoid circular imports if any
        from almanac import Almanac
        if not hasattr(self.game, 'almanac'):
            self.game.almanac = Almanac(self.game)
        self.game.state = 'almanac'

    def open_store(self):
        from store import Store
        if not hasattr(self.game, 'store'):
            self.game.store = Store(self.game)
        self.game.state = 'store'

    def open_help(self):
        print("Help...")

    def open_settings(self):
        self.game.pause_menu = PauseMenu(self.game, self.game.state)
        self.game.state = 'pause'

    def quit_game(self):
        pygame.quit()
        exit()

    def complete_all(self):
        self.game.user['completed_levels'] = set(self.game.levels.keys())
        self.game.user['unlocked_plants'] = list(PLANT_SUN_COST.keys())
        with open('user.json', 'w') as f:
            json.dump({'completed_levels': list(self.game.user['completed_levels']), 'unlocked_plants': self.game.user['unlocked_plants']}, f)
        print("All levels completed and all plants unlocked.")

    def reset_progress(self):
        self.game.user['completed_levels'] = set()
        self.game.user['unlocked_plants'] = ['Peashooter']
        with open('user.json', 'w') as f:
            json.dump({'completed_levels': list(self.game.user['completed_levels']), 'unlocked_plants': self.game.user['unlocked_plants']}, f)
        print("Progress reset.")

    def update_animation(self, dt):
        if self.playing_animation:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer -= self.frame_duration
                self.current_frame += 1
                if self.current_frame >= len(self.animation_frames):
                    self.current_frame = len(self.animation_frames) - 1
                    self.playing_animation = False

    def update(self, event):
        for button in self.image_buttons:
            button.update(event)
        for button in self.text_buttons:
            button.update(event)

    def draw(self, screen):
        # Draw the current animation frame
        frame = self.animation_frames[self.current_frame]
        screen.blit(frame, (0, 0))

        # Draw image buttons on top
        for button in self.image_buttons:
            button.draw(screen)
        for button in self.text_buttons:
            button.draw(screen,self.game.font)

class SeedSelect:
    def __init__(self, game, background, banned_plants):
        self.game = game
        self.background = background
        self.banned_plants = banned_plants
        self.seed_bank_bg = pygame.image.load('images/SeedBank.png')
        # Scale by 1.8 like seedbank
        self.seed_bank_bg = pygame.transform.smoothscale(self.seed_bank_bg, (self.seed_bank_bg.get_width() * 1.8, self.seed_bank_bg.get_height() * 1.8))

        # Load seed chooser background
        self.seed_chooser_bg = pygame.image.load('images/SeedChooser_Background.png')
        # Scale by 1.8 like seedbank
        self.seed_chooser_bg = pygame.transform.smoothscale(self.seed_chooser_bg, (self.seed_chooser_bg.get_width() * 1.8, self.seed_chooser_bg.get_height() * 1.8))

        # Seed selection data
        self.all_plants = [p for p in PLANT_SUN_COST.keys() if p in self.game.user['unlocked_plants'] and p not in self.banned_plants]
        self.selected_plants = []
        self.plant_buttons = []
        self.start_game_button = None

        # Create buttons for seed selection
        button_width = game.scaler.scale_x(75)
        button_height = game.scaler.scale_y(105)
        x_start = game.scaler.scale_x(30)
        y_start = game.scaler.scale_y(220)
        spacing_x = game.scaler.scale_x(90)
        spacing_y = game.scaler.scale_y(115)
        cols = 8  # Number of columns for buttons
        for i, plant in enumerate(self.all_plants):
            row = i // cols
            col = i % cols
            x = x_start + col * spacing_x
            y = y_start + row * spacing_y
            button = SimplePygameButton(
                (x, y),
                (button_width, button_height),
                [],  # No text
                lambda p=plant: self.toggle_plant_selection(p),
                (150, 150, 200)  # Background color
            )
            self.plant_buttons.append(button)
        
    def toggle_plant_selection(self, plant):
        if plant in self.selected_plants:
            self.selected_plants.remove(plant)
        elif len(self.selected_plants) < self.game.user['max_seeds']:
            self.selected_plants.append(plant)
        self.update_start_button()

    def update_start_button(self):
        if len(self.selected_plants) > 0:
            if self.start_game_button is None:
                self.start_game_button = SimplePygameButton(
                    (self.game.scaler.scale_x(250), self.game.scaler.scale_y(900)),
                    (self.game.scaler.scale_x(300), self.game.scaler.scale_y(60)),
                    [("Start Game", (self.game.scaler.scale_x(50), self.game.scaler.scale_y(15)))],
                    self.begin_game,
                    (0, 128, 0)
                )
        else:
            if self.start_game_button:
                self.start_game_button = None

    def begin_game(self):
        self.game.seed_packets = [{'name': plant, 'icon': self.game.plant_icons.get(plant, self.game.seed_image)} for plant in self.selected_plants]
        self.game.main_game = MainGame(self.game, self.game.selected_level)
        self.game.pre_animation_delay = 1.0
        self.game.pending_state = 'game'
        self.game.target_offset_pending = -250 * self.game.bg_scale_factor
        print("Starting game with selected seeds:", self.selected_plants)

    def draw_seed_bank(self, screen):
        # Draw background
        screen.blit(self.seed_bank_bg, (0, 0))
        if not self.game.animating:
            screen.blit(self.seed_chooser_bg, (0, 155))
            screen.blit(self.game.font.render(self.game.lawn_strings.get("CHOOSE_YOUR_PLANTS"),True, "#F1C70B"), (self.game.scaler.scale_x(200), self.game.scaler.scale_y(160)))
        # Draw selected seeds
        seed_x_start = self.game.scaler.scale_x(80 * 2)
        seed_y = self.game.scaler.scale_y(6 * 2)
        seed_w = self.game.scaler.scale_x(45 * 2)
        seed_h = self.game.scaler.scale_y(65 * 2)
        offset = self.game.scaler.scale_x(5 * 2)
        for i, seed_name in enumerate(self.selected_plants):
            rect = pygame.Rect(seed_x_start + i * (seed_w + offset), seed_y, seed_w, seed_h)
            scaled_seed = pygame.transform.smoothscale(self.game.seed_image, (seed_w, seed_h))
            screen.blit(scaled_seed, rect)
            # Draw plant icon on top
            if seed_name in self.game.plant_icons:
                icon = self.game.plant_icons[seed_name]
                scaled_icon = pygame.transform.smoothscale(icon, (int(seed_w * 0.8), int(seed_h * 0.6)))
                icon_rect = scaled_icon.get_rect(center=rect.center)
                screen.blit(scaled_icon, icon_rect)
            # Draw white border to indicate selected
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            # Draw plant cost below the seed packet
            cost = PLANT_SUN_COST.get(seed_name, 0)
            cost_text = self.game.small_font.render(str(cost), True, (0, 0, 0))
            cost_rect = cost_text.get_rect(center=(rect.x + seed_w // 2, rect.y + seed_h -10))
            screen.blit(cost_text, cost_rect)

    def get_button_tooltip(self, mouse_pos):
        for i, button in enumerate(self.plant_buttons):
            rect = pygame.Rect(button.position, button.size)
            if rect.collidepoint(mouse_pos):
                plant = self.all_plants[i]
                tooltip_key = plant.upper().replace(' ', '_') + '_TOOLTIP'
                description = self.game.lawn_strings.get(tooltip_key, "")
                localized_plant = self.game.lawn_strings.get(plant.upper().replace(' ', '_'), plant)
                return localized_plant + '\n' + description
        return ""

    def update(self, event):
        if not self.game.animating:
            for button in self.plant_buttons:
                button.update(event)
            if self.start_game_button:
                self.start_game_button.update(event)

    def draw(self, screen):
        # Optimize background rendering by blitting only the visible part
        offset_x = self.game.background_offset
        source_x = max(0, -offset_x)
        width_to_blit = min(self.game.width, self.game.scaled_background.get_width() - source_x)
        if width_to_blit > 0:
            subsurface = self.game.scaled_background.subsurface((source_x, 0, width_to_blit, self.game.height))
            screen.blit(subsurface, (0, 0))
        self.draw_seed_bank(screen)

        if not self.game.animating:
            # Draw seed packets and plant icons on buttons
            for i, button in enumerate(self.plant_buttons):
                # Draw seed packet background
                scaled_seed = pygame.transform.smoothscale(self.game.seed_image, (button.size[0], button.size[1]))
                screen.blit(scaled_seed, button.position)
                # Draw plant icon on top
                plant_name = self.all_plants[i]
                if plant_name in self.game.plant_icons:
                    icon = self.game.plant_icons[plant_name]
                    scaled_icon = pygame.transform.smoothscale(icon, (int(button.size[0] * 0.8), int(button.size[1] * 0.6)))
                    icon_rect = scaled_icon.get_rect(center=(button.position[0] + button.size[0] // 2, button.position[1] + button.size[1] // 2))
                    screen.blit(scaled_icon, icon_rect)
                # Draw border if selected
                if plant_name in self.selected_plants:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(button.position, button.size), 3)
                # Draw plant cost below the button
                cost = PLANT_SUN_COST.get(plant_name, 0)
                cost_text = self.game.small_font.render(str(cost), True, (0, 0, 0))
                cost_rect = cost_text.get_rect(center=(button.position[0] + button.size[0] // 2, button.position[1] + button.size[1] - 10))
                screen.blit(cost_text, cost_rect)
            if self.start_game_button:
                self.start_game_button.draw(screen, self.game.font)

            # Draw tooltip text near mouse cursor
            mouse_pos = pygame.mouse.get_pos()
            tooltip_text = self.get_button_tooltip(mouse_pos)
            if tooltip_text:
                lines = tooltip_text.split('\n')
                mouse_x, mouse_y = mouse_pos
                # Calculate max width and total height
                max_width = max(self.game.pico_font.size(line)[0] for line in lines)
                total_height = sum(self.game.pico_font.size(line)[1] for line in lines)
                # Draw background rect
                bg_rect = pygame.Rect(mouse_x + 10, mouse_y + 10, max_width + 10, total_height + 10)
                pygame.draw.rect(screen, (255, 255, 200), bg_rect)
                # Draw text
                y_offset = mouse_y + 15
                for line in lines:
                    tooltip_surface = self.game.pico_font.render(line, True, (0, 0, 0))
                    screen.blit(tooltip_surface, (mouse_x + 15, y_offset))
                    y_offset += self.game.pico_font.get_height()

class PauseMenu:
    def __init__(self, game, previous_state):
        self.game = game
        self.previous_state = previous_state
        self.width = game.width
        self.height = game.height
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        # Semi-transparent background
        self.bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.bg_surface.fill((0, 0, 0, 128))  # Semi-transparent gray

        # UI elements
        self.music_slider = Slider(
            (self.center_x - 150, self.center_y - 100),
            300, 30, 0.0, 1.0, self.game.sound_manager.music_volume,
            lambda v: self.game.sound_manager.set_music_volume(v)
        )
        self.sfx_slider = Slider(
            (self.center_x - 150, self.center_y - 50),
            300, 30, 0.0, 1.0, self.game.sound_manager.sfx_volume,
            lambda v: self.game.sound_manager.set_sfx_volume(v)
        )

        # Buttons
        button_width = 200
        button_height = 50
        self.resume_button = SimplePygameButton(
            (self.center_x - button_width // 2, self.center_y),
            (button_width, button_height),
            [("Resume", (50, 15))],
            self.resume_game,
            (0, 128, 0)
        )
        self.restart_button = SimplePygameButton(
            (self.center_x - button_width // 2, self.center_y + 60),
            (button_width, button_height),
            [("Restart Level", (30, 15))],
            self.restart_level,
            (128, 128, 0)
        ) if self.previous_state == 'game' else None
        self.exit_button = SimplePygameButton(
            (self.center_x - button_width // 2, self.center_y + 120 if self.restart_button else self.center_y + 60),
            (button_width, button_height),
            [("Exit to Menu", (30, 15))],
            self.exit_to_menu,
            (128, 0, 0)
        )

    def resume_game(self):
        self.game.state = self.previous_state

    def restart_level(self):
        if self.previous_state == 'game':
            self.game.main_game = MainGame(self.game, self.game.selected_level)
            self.game.state = 'game'

    def exit_to_menu(self):
        self.game.state = 'menu'
        self.game.main_menu.playing_animation = True

    def update(self, event):
        self.music_slider.update(event)
        self.sfx_slider.update(event)
        self.resume_button.update(event)
        if self.restart_button:
            self.restart_button.update(event)
        self.exit_button.update(event)

    def draw(self):
        # Draw current state first
        if self.previous_state == 'game':
            self.game.main_game.draw(self.game.screen)
        elif self.previous_state == 'seed_select':
            self.game.seed_select.draw(self.game.screen)

        # Draw semi-transparent background
        self.game.screen.blit(self.bg_surface, (0, 0))

        # Draw UI
        # Labels
        music_label = self.game.small_font.render("Music Volume", True, (255, 255, 255))
        self.game.screen.blit(music_label, (self.center_x - 150, self.center_y - 130))
        sfx_label = self.game.small_font.render("Sound Volume", True, (255, 255, 255))
        self.game.screen.blit(sfx_label, (self.center_x - 150, self.center_y - 80))

        self.music_slider.draw(self.game.screen)
        self.sfx_slider.draw(self.game.screen)
        self.resume_button.draw(self.game.screen, self.game.font)
        if self.restart_button:
            self.restart_button.draw(self.game.screen, self.game.font)
        self.exit_button.draw(self.game.screen, self.game.font)

class MainGame:
    def __init__(self, game, level_name):
        self.game = game
        self.level_data = game.levels[level_name]
        print(self.level_data['background'])
        if self.level_data['background'] in ['background2.png', 'background4.png', 'background6.png']:
            self.is_day = False
        else:
            self.is_day = True

        if 'background1.png' in self.level_data['background']:
            self.music = 'music_day'
        elif 'background2.png' in self.level_data['background']:
            self.music = 'music_night'
        elif 'background3.png' in self.level_data['background']:
            self.music = 'music_pool'
        elif 'background4.png' in self.level_data['background']:
            self.music = 'music_fog'
        elif 'background5.png' in self.level_data['background']:
            self.music = 'music_roof'
        else:
            self.music = 'X-10'

        self.zombies_on_level = self.level_data['zombies']

        self.game_field = GameField(game.scaler, game.width, game.height, game)
        self.sun_count = self.level_data['start_sun']
        self.coin_count = self.game.user['coins']
        self.coins = []
        self.selected_seed = None
        self.hotbar_height = game.scaler.scale_y(100 * 2)
        self.wave_number = 1
        self.wave_points = 1
        self.initial_timer = 15.0  # 5 seconds
        self.zombies = []
        self.current_wave_zombies = []
        self.wave_active = False
        self.wave_timer = 0.0
        self.initial_wave_hp = 0
        self.max_waves = self.level_data['waves']
        self.debug_mode = False
        self.dt = 0
        self.game_won = False
        self.sky_suns = []
        self.sky_sun_timer = 0.0
        self.sky_sun_interval = random.uniform(3.0, 6.0)
        self.sky_sun_timer = self.sky_sun_interval  # Start falling immediately
        # Initialize seed recharge timers as mutable dict with 0 (ready) for each plant
        self.seed_recharge_timers = {plant: 0 for plant in PLANT_RECHARGE}
        self.selected_shovel = False

    def draw_hotbar(self, screen):
        # Draw hotbar background image
        scaled_seedbank = pygame.transform.smoothscale(self.game.seedbank_image, (self.game.scaler.scale_x(self.game.seedbank_image.get_width()), self.game.scaler.scale_y(self.game.seedbank_image.get_height())))
        screen.blit(scaled_seedbank, (0, 0))
        # Draw sun count
        sun_text = self.game.small_font.render(f"{self.sun_count}", True, "#000000")
        screen.blit(sun_text, (self.game.scaler.scale_x(30 * 2), self.game.scaler.scale_y(65 * 2)))

        # Draw coin count
        coin_text = self.game.small_font.render(f"{self.coin_count}", True, "#000000")
        screen.blit(coin_text, (self.game.scaler.scale_x(30 * 2), self.game.scaler.scale_y(85 * 2)))

        # Draw seed packets
        seed_x_start = self.game.scaler.scale_x(80 * 2)
        seed_y = self.game.scaler.scale_y(8 * 2)
        seed_w = self.game.scaler.scale_x(45 * 2)
        seed_h = self.game.scaler.scale_y(65 * 2)
        offset = self.game.scaler.scale_x(5 * 2)

        mouse_pos = pygame.mouse.get_pos()

        for i, seed in enumerate(self.game.seed_packets):
            rect = pygame.Rect(seed_x_start + i * (seed_w + offset), seed_y, seed_w, seed_h)
            # Draw seed packet background
            scaled_seed = pygame.transform.smoothscale(self.game.seed_image, (seed_w, seed_h))
            screen.blit(scaled_seed, rect)
            # Draw plant icon on top
            icon = seed['icon']
            scaled_icon = pygame.transform.smoothscale(icon, (int(seed_w * 1), int(seed_h * 0.7)))
            icon_rect = scaled_icon.get_rect(center=rect.center)
            screen.blit(scaled_icon, icon_rect)
            # Highlight selected seed
            if self.selected_seed == i:
                pygame.draw.rect(screen, "#FFFFFF", rect, 3)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect, 3)
            # Draw plant cost below the seed packet
            cost = PLANT_SUN_COST.get(seed['name'], 0)
            cost_text = self.game.small_font.render(str(cost), True, (0, 0, 0))
            cost_rect = cost_text.get_rect(center=(rect.x + seed_w // 2, rect.y + seed_h -10))
            screen.blit(cost_text, cost_rect)

            # Draw recharge progress bar if recharging
            if self.seed_recharge_timers[seed['name']] > 0:
                recharge_time = PLANT_RECHARGE[seed['name']] / 100
                progress = self.seed_recharge_timers[seed['name']] / recharge_time
                bar_height = int(seed_h * progress)
                bar_rect = pygame.Rect(rect.x, rect.y + seed_h - bar_height, seed_w, bar_height)
                pygame.draw.rect(screen, (128, 128, 128, 128), bar_rect)  # Semi-transparent gray bar from bottom

            # Draw seed name only on hover
            if rect.collidepoint(mouse_pos):
                localized_name = self.game.lawn_strings.get(seed['name'].upper().replace(' ', '_'), seed['name'])
                name_text = self.game.pico_font.render(localized_name, True, (0, 0, 0))
                text_width, text_height = name_text.get_size()
                bg_rect = pygame.Rect(rect.x, rect.y + seed_h + self.game.scaler.scale_y(5 * 2), text_width + 10, text_height + 10)
                pygame.draw.rect(screen, (255, 255, 200), bg_rect)
                screen.blit(name_text, (rect.x + 5, rect.y + seed_h + self.game.scaler.scale_y(5 * 2) + 5))

        # Draw shovel
        shovel_x = seed_x_start + len(self.game.seed_packets) * (seed_w + offset) + 50
        shovel_rect = pygame.Rect(shovel_x, seed_y, 140, 144)
        scaled_shovel_bank = pygame.transform.smoothscale(self.game.shovel_bank_image, (140, 144))
        screen.blit(scaled_shovel_bank, shovel_rect)
        scaled_shovel_icon = pygame.transform.smoothscale(self.game.shovel_image, (120, 120))
        icon_rect = scaled_shovel_icon.get_rect(center=shovel_rect.center)
        screen.blit(scaled_shovel_icon, icon_rect)
        if self.selected_shovel:
            pygame.draw.rect(screen, "#FFFFFF", shovel_rect, 4)
        else:
            pygame.draw.rect(screen, (0, 0, 0), shovel_rect, 4)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if 0 <= mouse_y <= self.hotbar_height:
                    seed_x_start = self.game.scaler.scale_x(80 * 2)
                    seed_y = self.game.scaler.scale_y(10 * 2)
                    seed_w = self.game.scaler.scale_x(45 * 2)
                    seed_h = self.game.scaler.scale_y(65 * 2)
                    offset = self.game.scaler.scale_x(5 * 2)
                    for i in range(len(self.game.seed_packets)):
                        rect = pygame.Rect(seed_x_start + i * (seed_w + offset), seed_y, seed_w, seed_h)
                        if rect.collidepoint(event.pos):
                            if self.seed_recharge_timers[self.game.seed_packets[i]['name']] > 0:
                                continue
                            self.selected_seed = i
                            self.selected_shovel = False
                            print(f"Selected seed: {self.game.seed_packets[i]['name']}")
                            break
                    # Check shovel click
                    shovel_x = seed_x_start + len(self.game.seed_packets) * (seed_w + offset)
                    shovel_rect = pygame.Rect(shovel_x, seed_y, 140, 144)
                    if shovel_rect.collidepoint(event.pos):
                        self.selected_shovel = True
                        self.game.sound_manager.play_sound('shovel')
                        self.selected_seed = None
                        print("Selected shovel")
                else:
                    # Check if clicked on any suns to collect
                    for row in range(self.game_field.rows):
                        for col in range(self.game_field.cols):
                            plant = self.game_field.grid[row][col]
                            if plant and hasattr(plant, 'suns'):
                                for sun in plant.suns:
                                    if sun.rect.collidepoint(event.pos) and not sun.collected:
                                        sun.collect()
                                        break
                    # Check sky suns
                    for sun in self.sky_suns:
                        if sun.rect.collidepoint(event.pos) and not sun.collected:
                            sun.collect()
                            break
                    # Check coins
                    for coin in self.coins:
                        if coin.rect.collidepoint(event.pos) and not coin.collected:
                            coin.collect()
                            self.coin_count += coin.value
                            self.game.user['coins'] = self.coin_count
                            user_data = self.game.user.copy()
                            user_data['completed_levels'] = list(user_data['completed_levels'])
                            with open('user.json', 'w') as f:
                                json.dump(user_data, f)
                            break
                    # Plant on game field
                    if self.selected_seed is not None:
                        plant = self.game.seed_packets[self.selected_seed]
                        self.game_field.handle_click(event.pos, plant)
                    elif self.selected_shovel:
                        self.game_field.remove_plant(event.pos)
                        self.game.sound_manager.play_sound('plant1') if random.random() > 0.5 else self.game.sound_manager.play_sound('plant2')
                        self.selected_shovel = False
            elif event.button == 3:
                self.selected_seed = None
                self.selected_shovel = False

    def update_wave(self, dt):
        self.dt = dt

        # Updates that run always, even during initial timer
        # Decrement seed recharge timers
        for plant_name in self.seed_recharge_timers:
            if self.seed_recharge_timers[plant_name] > 0:
                self.seed_recharge_timers[plant_name] -= dt
                if self.seed_recharge_timers[plant_name] < 0:
                    self.seed_recharge_timers[plant_name] = 0

        # Spawn sky suns only during day
        if self.is_day:
            self.sky_sun_timer += dt
            if self.sky_sun_timer >= self.sky_sun_interval:
                # Spawn at random x at top
                sun_x = random.randint(0, self.game.width - 80)  # assuming sun size 80
                sun_y = 0  # at top of screen
                new_sun = Sun(sun_x, sun_y, self.game, sun_type='sky')
                self.sky_suns.append(new_sun)
                self.sky_sun_timer = 0.0
                self.sky_sun_interval = random.uniform(6.0, 9.0)  # shorter interval for testing

        # Update suns from all sunflowers
        for row in range(self.game_field.rows):
            for col in range(self.game_field.cols):
                plant = self.game_field.grid[row][col]
                if plant and hasattr(plant, 'suns'):
                    for sun in plant.suns:
                        sun.update(dt)

        # Update sky suns
        for sun in self.sky_suns:
            sun.update(dt)

        # Remove collected sky suns
        self.sky_suns = [s for s in self.sky_suns if not s.collected]

        # Update coins
        for coin in self.coins:
            coin.update(dt)

        # Remove collected coins
        self.coins = [c for c in self.coins if not c.collected]

        # Update plants
        for row in range(self.game_field.rows):
            for col in range(self.game_field.cols):
                plant = self.game_field.grid[row][col]
                if plant and hasattr(plant, 'update'):
                    if isinstance(plant, (Peashooter, SnowPea, Repeater,PuffShroom,Chomper)):
                        plant.update(dt, self.zombies)
                    else:
                        plant.update(dt)

        # Remove collected suns from sunflowers
        for row in range(self.game_field.rows):
            for col in range(self.game_field.cols):
                plant = self.game_field.grid[row][col]
                if plant and hasattr(plant, 'suns'):
                    plant.suns = [s for s in plant.suns if not s.collected]

        if self.initial_timer > 0:
            self.initial_timer -= dt
            return

        # Wave logic starts after initial timer
        # If no active wave, start a new wave
        if not self.wave_active and self.wave_number <= self.max_waves:
            self.start_wave()

        # Update zombies
        for zombie in self.zombies:
            zombie.update(dt)

        # Check projectile collisions
        for zombie in self.zombies:
            for row in range(self.game_field.rows):
                for col in range(self.game_field.cols):
                    plant = self.game_field.grid[row][col]
                    if plant and hasattr(plant, 'projectiles'):
                        for projectile in plant.projectiles[:]:
                            if projectile.collides_with(zombie):
                                if projectile.proj_type == 'snowpea':
                                    zombie.slow_timer = 10.0
                                zombie.take_damage(projectile.damage)
                                plant.projectiles.remove(projectile)
                                break

        # Check for lose condition: if any zombie reaches the house (x < 0)
        if any(z.x < 0 for z in self.zombies):
            print("You lose!")
            self.game.thread_running = False
            self.game.fade_alpha = 0
            self.game.fade_color = (0, 0, 0)
            self.game.state = 'lose'
            self.game.sound_manager.play_music('lose')
            return

        # Spawn coins on zombie death
        for zombie in self.zombies:
            if zombie.health <= 0 and getattr(zombie, 'to_remove', False):
                coin = Coin(zombie.x, zombie.y, self.game)
                self.coins.append(coin)

        # Remove zombies that are off screen or dead
        self.zombies = [z for z in self.zombies if z.x > -50 and (z.health > 0 or not getattr(z, 'to_remove', False))]
        self.current_wave_zombies = [z for z in self.current_wave_zombies if z in self.zombies]

        # Check wave end conditions
        total_hp = sum(z.health + z.cone_health + z.bucket_health for z in self.current_wave_zombies)
        self.wave_timer += dt

        # Wave ends if total HP < 50% initial or 25 seconds passed
        if total_hp < self.initial_wave_hp * 0.5 or self.wave_timer >= 25.0 and self.wave_number < self.max_waves:
            self.wave_active = False
            self.wave_timer = 0.0
            self.wave_number += 1

        if self.wave_number >= self.max_waves and not self.zombies:
            self.game.user['completed_levels'].add(self.game.selected_level)
            # Reward: unlock Sunflower if not already unlocked
            if self.level_data["unlocked_plants"] not in self.game.user['unlocked_plants']:
                self.game.user['unlocked_plants'].append(self.level_data["unlocked_plants"][0])
            # Save to user.json
            with open('user.json', 'w') as f:
                json.dump({'completed_levels': list(self.game.user['completed_levels']), 'unlocked_plants': self.game.user['unlocked_plants']}, f)   

            print("You win!")
            self.game.thread_running = False
            self.game.fade_alpha = 0
            self.game.fade_color = (255, 255, 255)
            self.game.state = 'win'
            self.game.sound_manager.play_music('win')

    def start_wave(self):
        # Calculate wave points based on wave number
        self.wave_points = WAVE_OPTIONS["Points"] + ((self.wave_number - 1) // WAVE_OPTIONS["Every"]) * WAVE_OPTIONS["Points"]
        self.initial_wave_hp = 0
        self.current_wave_zombies = []

        # Spawn entire wave at once, distributing zombies across lanes
        points_left = self.wave_points
        zombies_to_spawn = []

        # Generate zombies to fill wave points
        while points_left > 0:
            possible = [z for z in ZOMBIE_COST if ZOMBIE_COST[z] <= points_left and z in self.zombies_on_level]
            if not possible:
                break
            z_type = random.choice(possible)
            cost = ZOMBIE_COST[z_type]
            points_left -= cost
            zombies_to_spawn.append(z_type)

        # Shuffle zombies to avoid clustering on one lane
        random.shuffle(zombies_to_spawn)

        for i, z_type in enumerate(zombies_to_spawn):
            lane = random.randint(0,4)
            try:
                zombie = globals()[z_type](lane, self.game.scaler, self.game_field)
            except:
                zombie = Zombie(lane, self.game.scaler, self.game_field)  # Fallback to basic
                
            self.zombies.append(zombie)
            self.current_wave_zombies.append(zombie)
            self.initial_wave_hp += zombie.health + zombie.cone_health + zombie.bucket_health

        self.wave_active = True
        self.wave_timer = 0

    def draw_flag_meter(self, screen):
        frame_width = self.game.flag_meter_image.get_width()
        frame_height = self.game.flag_meter_image.get_height() // 2
        empty_frame = self.game.flag_meter_image.subsurface((0, 0, frame_width, frame_height))
        filled_frame = self.game.flag_meter_image.subsurface((0, frame_height, frame_width, frame_height))
        smoothscale = 0.6
        empty_scaled = pygame.transform.smoothscale(empty_frame, (int(frame_width * smoothscale), int(frame_height * smoothscale)))
        filled_scaled = pygame.transform.smoothscale(filled_frame, (int(frame_width * smoothscale), int(frame_height * smoothscale)))
        bar_width = int(frame_width * smoothscale)
        bar_height = int(frame_height * smoothscale)
        x = self.game.width - bar_width - 20  # 20 px padding from right
        y = self.game.height - bar_height - 20  # 20 px padding from bottom

        # Draw empty bar background
        screen.blit(empty_scaled, (x, y))

        # Calculate fill width proportional to wave progress
        progress = min(max(self.wave_number / self.max_waves, 0), 1)
        fill_width = int(bar_width * progress)

        # Create a filled bar subsurface with width = fill_width
        filled_subsurface = filled_scaled.subsurface((0, 0, fill_width, bar_height))
        screen.blit(filled_subsurface, (x, y))

    def draw(self, screen):
        # Optimize background rendering by blitting only the visible part
        offset_x = self.game.background_offset
        source_x = max(0, -offset_x)
        width_to_blit = min(self.game.width, self.game.scaled_background.get_width() - source_x)
        if width_to_blit > 0:
            subsurface = self.game.scaled_background.subsurface((source_x, 0, width_to_blit, self.game.height))
            screen.blit(subsurface, (0, 0))
        self.game_field.draw(screen)
        if self.selected_seed is not None:
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos
            if self.game_field.field_x <= x < self.game_field.field_x + self.game_field.cols * self.game_field.cell_width and self.game_field.field_y <= y < self.game_field.field_y + self.game_field.rows * self.game_field.cell_height:
                col = (x - self.game_field.field_x) // self.game_field.cell_width
                row = (y - self.game_field.field_y) // self.game_field.cell_height
                if 0 <= row < self.game_field.rows and 0 <= col < self.game_field.cols:
                    if self.game_field.grid[row][col] is None:
                        plant_name = self.game.seed_packets[self.selected_seed]['name']
                        cost = PLANT_SUN_COST.get(plant_name, 0)
                        if self.sun_count >= cost:
                            icon = self.game.plant_icons.get(plant_name)
                            if icon:
                                preview = icon.copy()
                                preview.set_alpha(128)
                                scaled_preview = pygame.transform.smoothscale(preview, (int(self.game_field.cell_width * 0.8), int(self.game_field.cell_height * 0.8)))
                                cell_x = self.game_field.field_x + col * self.game_field.cell_width
                                cell_y = self.game_field.field_y + row * self.game_field.cell_height
                                center_x = cell_x + (self.game_field.cell_width - scaled_preview.get_width()) // 2
                                center_y = cell_y + (self.game_field.cell_height - scaled_preview.get_height()) // 2
                                screen.blit(scaled_preview, (center_x, center_y))
        self.draw_hotbar(screen)
        self.draw_flag_meter(screen)
        for sun in self.sky_suns:
            sun.draw(screen)
        for coin in self.coins:
            coin.draw(screen)
        for zombie in self.zombies:
            zombie.draw(screen)
        if self.selected_shovel:
            mouse_pos = pygame.mouse.get_pos()
            cursor_shovel = pygame.transform.smoothscale(self.game.shovel_image, (40, 40))
            screen.blit(cursor_shovel, (mouse_pos[0] - cursor_shovel.get_width() // 2, mouse_pos[1] - cursor_shovel.get_height() // 2))
        if self.debug_mode:
            # draw wave and points
            wave_text = self.game.small_font.render(f"Wave: {self.wave_number} Points: {self.wave_points}", True, (255, 255, 255))
            screen.blit(wave_text, (self.game.width - wave_text.get_width() - 10, 10))
            fps_text = self.game.small_font.render(f"FPS: {self.game.get_fps()}", True, (255, 255, 255))
            screen.blit(fps_text, (self.game.width - fps_text.get_width() - 10, 10 + wave_text.get_height() + 10))
            # draw zombie info
            for zombie in self.zombies:
                z_text = self.game.small_font.render(f"{zombie.z_type} HP:{zombie.health} Cone:{zombie.cone_health} Bucket:{zombie.bucket_health}", True, (255, 0, 0))
                screen.blit(z_text, (zombie.x, zombie.y - 25))
            # draw plant names
            for row in range(self.game_field.rows):
                for col in range(self.game_field.cols):
                    plant = self.game_field.grid[row][col]
                    if plant:
                        x = self.game_field.field_x + col * self.game_field.cell_width + self.game_field.cell_width // 2
                        y = self.game_field.field_y + row * self.game_field.cell_height + self.game_field.cell_height // 2
                        if isinstance(plant, Peashooter) or isinstance(plant, Sunflower) or isinstance(plant, CherryBomb) or isinstance(plant, WallNut):
                            p_text = self.game.small_font.render(plant.name, True, (0, 255, 0))
                            screen.blit(p_text, (x - p_text.get_width() // 2, y - p_text.get_height() // 2))
                            hp_text = self.game.small_font.render(f"HP:{plant.health}", True, (255, 0, 0))
                            screen.blit(hp_text, (x - hp_text.get_width() // 2, y + 10))

class WelcomeScreen:
    def __init__(self, game):
        self.game = game
        self.logo = pygame.image.load('properties/logo.png')
        self.titlescreen = pygame.image.load('images/titlescreen.png')
        self.pvz_logo = pygame.image.load('images/PvZ_Logo.png')
        self.button = pygame.image.load('images/LoadBar_dirt.png')
        self.button_rect = self.button.get_rect(center=(game.width // 2, game.height // 2 + 200))
        self.phase = 'fade_in'  # fade_in, fade_out, show_titlescreen
        self.alpha = 0
        self.title_alpha = 0
        self.timer = 0.0
        self.fade_duration = 2.0  # 2 seconds for fade in/out

    def update(self, dt):
        self.timer += dt
        if self.phase == 'fade_in':
            self.alpha = min(255, int((self.timer / self.fade_duration) * 255))
            if self.timer >= self.fade_duration:
                self.phase = 'fade_out'
                self.timer = 0.0
        elif self.phase == 'fade_out':
            self.alpha = max(0, 255 - int((self.timer / self.fade_duration) * 255))
            if self.timer >= self.fade_duration:
                preload_all()
                self.phase = 'show_titlescreen'
        elif self.phase == 'show_titlescreen':
            self.title_alpha = min(255, self.title_alpha + dt * 200)  # fade in over ~1.275 seconds

            # Check for button click
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and self.button_rect.collidepoint(mouse_pos):
                self.game.state = 'menu'


    def draw(self, screen):
        if self.phase in ['fade_in', 'fade_out']:
            # Draw logo with alpha
            logo_surface = self.logo.copy()
            logo_surface.set_alpha(self.alpha)
            logo_rect = logo_surface.get_rect(center=(self.game.width // 2, self.game.height // 2))
            screen.blit(logo_surface, logo_rect)
        elif self.phase == 'show_titlescreen':
            # Draw titlescreen background with alpha
            titlescreen_surface = self.titlescreen.copy()
            titlescreen_surface.set_alpha(self.title_alpha)
            screen.blit(titlescreen_surface, (0, 0))
            # Draw PvZ logo with alpha
            logo_surface = self.pvz_logo.copy()
            logo_surface.set_alpha(self.title_alpha)
            pvz_rect = logo_surface.get_rect(center=(self.game.width // 2, self.game.height // 2 - 400))
            screen.blit(logo_surface, pvz_rect)
            # Draw button with alpha
            button_surface = self.button.copy()
            button_surface.set_alpha(self.title_alpha)
            screen.blit(button_surface, self.button_rect)

class Menu:
    def __init__(self, game):
        self.game = game
        self.background = preloaded_images['challenge_background']
        self.window_image = preloaded_images['challenge_window']
        self.window_highlight = preloaded_images['challenge_window_highlight']
        self.close_button = preloaded_images['almanac_closebutton']
        self.close_highlight = preloaded_images['almanac_closebuttonhighlight']
        self.thumbnails = preloaded_images['survival_thumbnails']
        # Load trophy and lock images
        self.trophy_image = pygame.image.load('images/MiniGame_trophy.png')
        self.lock_image = pygame.image.load('images/lock.png')
        # cut thumbnails into list
        self.thumbnail_width = self.thumbnails.get_width() // 11
        self.thumbnail_height = self.thumbnails.get_height()
        self.thumbnails_list = []
        for i in range(11):
            rect = pygame.Rect(i * self.thumbnail_width, 0, self.thumbnail_width, self.thumbnail_height)
            self.thumbnails_list.append(self.thumbnails.subsurface(rect))
        # level buttons
        self.level_buttons = []
        LEVEL_DATA = json.load(open('levels.json'))
        # Generate grid positions: 8 columns, 6 rows, up to 48 levels
        cols = 8
        rows = 6
        start_x = 200
        start_y = 200
        step_x = 200
        step_y = 150
        positions = []
        for r in range(rows):
            for c in range(cols):
                x = start_x + c * step_x
                y = start_y + r * step_y
                positions.append((x, y))
        level_keys = list(LEVEL_DATA.keys())
        for i, (level_key, level_data) in enumerate(LEVEL_DATA.items()):
            if i >= len(positions):
                break  # Limit to 48 levels
            if 'background1.png' in level_data['background']:
                icon_index = 0  # day
            elif 'background2.png' in level_data['background']:
                icon_index = 1  # night
            elif 'background3.png' in level_data['background']:
                icon_index = 2  # pool
            elif 'background4.png' in level_data['background']:
                icon_index = 3  # fog
            elif 'background5.png' in level_data['background']:
                icon_index = 4  # roof
            else:
                icon_index = 0

            # Determine if level is unlocked and completed
            level_index = level_keys.index(level_key)
            unlocked = level_index == 0 or level_keys[level_index - 1] in self.game.user['completed_levels']
            completed = level_key in self.game.user['completed_levels']

            button = {
                'rect': pygame.Rect(positions[i][0], positions[i][1], self.window_image.get_width(), self.window_image.get_height()),
                'level': level_key,
                'icon': self.thumbnails_list[icon_index],
                'hovered': False,
                'unlocked': unlocked,
                'completed': completed
            }
            self.level_buttons.append(button)
        self.close_rect = pygame.Rect(20, 1030, self.close_button.get_width(), self.close_button.get_height())
        self.close_hovered = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in self.level_buttons:
                    button['hovered'] = button['rect'].collidepoint(mouse_pos)
                self.close_hovered = self.close_rect.collidepoint(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.level_buttons:
                        if button['hovered'] and button['unlocked']:
                            self.game.selected_level = button['level']
                            self.game.load_background()
                            self.game.seed_select = SeedSelect(self.game, self.game.levels[self.game.selected_level]['background'], self.game.levels[self.game.selected_level]['banned_plants'])
                            self.game.state = 'seed_select'
                            self.game.post_animation_delay = 1.0
                            self.game.start_animation(-1080 * self.game.bg_scale_factor)
                            break
                    if self.close_hovered:
                        self.game.state = 'menu'


    def draw(self, screen):
        screen.blit(self.background, (0,0))
        for button in self.level_buttons:
            img = self.window_highlight if button['hovered'] else self.window_image
            screen.blit(img, button['rect'])
            # blit icon
            icon_x = button['rect'].x + (button['rect'].width - self.thumbnail_width) // 2
            icon_y = button['rect'].y + (button['rect'].height - self.thumbnail_height - 50) // 2
            screen.blit(button['icon'], (icon_x, icon_y))
            level_text = self.game.font.render(button['level'], True, (0,0,0))
            text_rect = level_text.get_rect(center=(button['rect'].centerx, button['rect'].centery + 40))
            screen.blit(level_text, text_rect)
            # Draw lock if not unlocked
            if not button['unlocked']:
                lock_rect = self.lock_image.get_rect(center=button['rect'].center)
                screen.blit(self.lock_image, lock_rect)
            # Draw trophy if completed
            elif button['completed']:
                trophy_rect = button['rect']
                screen.blit(self.trophy_image, trophy_rect)
        close_img = self.close_highlight if self.close_hovered else self.close_button
        screen.blit(close_img, self.close_rect)

class Game:
    def __init__(self):
        def parse_lawnstrings(filepath):
            strings = {}
            current_key = None
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_key = line[1:-1]
                        strings[current_key] = ''
                    elif current_key and line:
                        if strings[current_key]:
                            strings[current_key] += '\n' + line
                        else:
                            strings[current_key] = line
            return strings

        # Run settings window to select resolution
        from tkinter import Tk
        root = Tk()
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        root.destroy()  # Закрываем окно, чтобы не мешало

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Plants vs Zombies Python Edition")

        # Load levels
        self.levels = json.load(open('levels.json'))
        self.selected_level = '1-1'

        # Load or initialize user progress
        try:
            with open('user.json', 'r') as f:
                self.user = json.load(f)
                self.user['completed_levels'] = set(self.user['completed_levels'])
                if 'coins' not in self.user:
                    self.user['coins'] = 0
                if 'max_seeds' not in self.user:
                    self.user['max_seeds'] = 6
                if 'seed_upgrade_count' not in self.user:
                    self.user['seed_upgrade_count'] = 0
        except FileNotFoundError:
            self.user = {'completed_levels': set(), 'unlocked_plants': ['Peashooter'], 'coins': 0, 'max_seeds': 6, 'seed_upgrade_count': 0}

        # Load images
        self.seedbank_image = pygame.image.load('images/seedbank.png')
        # Scale seedbank by 2
        self.seedbank_image = pygame.transform.smoothscale(self.seedbank_image, (self.seedbank_image.get_width() * 1.8, self.seedbank_image.get_height() * 1.8))
        self.flag_meter_image = pygame.image.load('images/FlagMeter.png')
        seeds_image = pygame.image.load('images/seeds.png')
        # Extract the third seed image (0-indexed as 2)
        self.seed_image = seeds_image.subsurface((2 * 50, 0, 50, 70))

        # Load shovel images
        self.shovel_bank_image = pygame.image.load('images/ShovelBank.png')
        self.shovel_image = pygame.image.load('images/Shovel.png')
        # Scale shovel bank to match seed packet size (will be scaled per draw)
        self.shovel_bank_image = pygame.transform.smoothscale(self.shovel_bank_image, (50 * 1.8, 70 * 1.8))
        # Scale shovel icon appropriately
        self.shovel_image = pygame.transform.smoothscale(self.shovel_image, (40 * 1.8, 40 * 1.8))

        # Load plant icons
        self.plant_icons = {
            'Peashooter': pygame.image.load('animations/Plants/peashooter/Peashooter0080.png'),
            'Sunflower': pygame.image.load('animations/Plants/sunflower/Sunflower0005.png'),
            'Cherry Bomb': pygame.image.load('animations/Plants/cherrybomb/Cherrybomb0015.png'),
            'Wall Nut': pygame.image.load('animations/Plants/wallnut/Wallnut0001.png'),
            'Potato Mine': pygame.image.load('animations/Plants/potatomine/PotatoMine0021.png'),
            'Snow Pea': pygame.image.load('animations/Plants/snowpea/SnowPea0080.png'),
            'Chomper': pygame.image.load('animations/Plants/chomper/Chomper0001.png'),
            'Repeater': pygame.image.load('animations/Plants/repeater/Repeater0080.png'),
            'Puff Shroom': pygame.image.load('animations/Plants/puffshroom/PuffShroom0005.png'),
            'Sun Shroom': pygame.image.load('animations/Plants/sunshroom/SunShroom0005.png'),
            'Fume Shroom': pygame.image.load('animations/Plants/fumeshroom/FumeShroom0005.png'),
            'Grave Buster': pygame.image.load('animations/Plants/gravebuster/GraveBuster0001.png'),
            'Lily Pad': pygame.image.load('animations/Plants/lilypad/LilyPad0001.png'),
        }

        # Load background
        self.load_background()

        # Create scaler for UI elements
        self.scaler = SimpleWindowScaler(BASE_WIDTH, BASE_HEIGHT, self.width, self.height)

        # Font for UI
        self.font = pygame.font.Font('HOUSE_OF_TERROR.ttf', int(self.scaler.scale_y(36)))
        self.small_font = pygame.font.Font('HOUSE_OF_TERROR.ttf', int(self.scaler.scale_y(24)))
        self.pico_font = pygame.font.Font('pico12.ttf', int(self.scaler.scale_y(20)))

        # Load LawnStrings.txt
        self.lawn_strings = parse_lawnstrings('properties/languages/RU-russian.txt')

        # Game state
        self.state = 'menu'
        self.seed_packets = []

        # Initialize sound manager
        self.sound_manager = SoundManager()

        # Initialize states
        self.main_menu = MainMenu(self)
        self.seed_select = SeedSelect(self, self.levels[self.selected_level]['background'], self.levels[self.selected_level]['banned_plants'])
        self.main_game = MainGame(self, self.selected_level)
        self.pause_menu = None
        self.welcome_screen = WelcomeScreen(self)
        preload_ui()
        self.menu = Menu(self)
        self.state = 'welcome'
        self.sound_manager.play_music('menu')

        # Animation variables for background offset
        self.background_offset = 0.0
        self.target_offset = 0.0
        self.start_offset = 0.0
        self.animation_duration = 1.0
        self.animation_timer = 0.0
        self.animating = False
        self.animation_finished = False
        self.pending_state = None
        self.pre_animation_delay = 0.0
        self.post_animation_delay = 0.0
        self.target_offset_pending = 0.0

        # Fade variables for win/lose animations
        self.fade_alpha = 0
        self.fade_color = (255, 255, 255)

        # FPS tracking
        self.fps = 0

        # Threading for update
        self.update_lock = threading.Lock()
        self.update_queue = queue.Queue()
        self.update_thread = None
        self.thread_running = True


    def load_background(self):
        background_image = pygame.image.load("images/"+self.levels[self.selected_level]['background'])
        self.bg_scale_factor = self.height / background_image.get_height()
        scaled_bg_width = int(background_image.get_width() * self.bg_scale_factor)
        scaled_bg_height = self.height
        # Tile the background to make it wider for scrolling animations
        tile_count = 3  # Tile 3 times to ensure enough width for scrolling
        total_width = scaled_bg_width * tile_count
        self.scaled_background = pygame.Surface((total_width, scaled_bg_height))
        for i in range(tile_count):
            self.scaled_background.blit(pygame.transform.smoothscale(background_image, (scaled_bg_width, scaled_bg_height)), (i * scaled_bg_width, 0))

    def draw_background(self, screen, offset_x):
        width_to_blit = min(self.width, self.scaled_background.get_width())
        if width_to_blit > 0:
            subsurface = self.scaled_background.subsurface((0, 0, width_to_blit, self.height))
            screen.blit(subsurface, (offset_x, 0))

    def start_animation(self, target):
        self.target_offset = target
        self.start_offset = self.background_offset
        self.animation_timer = 0.0
        self.animating = True

    def get_fps(self):
        return self.fps

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60) / 1000.0
            self.fps = clock.get_fps()

            # Handle pre-animation delay
            if self.pre_animation_delay > 0:
                self.animating = True
                self.pre_animation_delay -= dt
                if self.pre_animation_delay <= 0:
                    self.pre_animation_delay = 0
                    self.start_animation(self.target_offset_pending)

            # Update animation
            if self.animating and self.pre_animation_delay <= 0:
                self.animation_timer += dt
            if self.animation_timer >= self.animation_duration:
                self.background_offset = self.target_offset
                if self.pending_state:
                    if self.post_animation_delay == 0:
                        self.post_animation_delay = 2.0
                    self.animating = True
                    # Do not reset animating to False here to allow post delay to complete
                else:
                    self.animating = False
            else:
                t = self.animation_timer / self.animation_duration
                # Easing: smoothstep for acceleration and deceleration
                t = t * t * (3 - 2 * t)
                self.background_offset = self.start_offset + (self.target_offset - self.start_offset) * t

            # Handle post-animation delay
            if self.post_animation_delay > 0:
                self.animating = True
                self.post_animation_delay -= dt
                if self.post_animation_delay <= 0:
                    self.post_animation_delay = 0
                    if self.pending_state:
                        self.state = self.pending_state
                        self.pending_state = None
                    self.animating = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        self.main_game.debug_mode = not self.main_game.debug_mode
                    elif event.key == pygame.K_ESCAPE:
                        if self.state in ['game', 'seed_select']:
                            self.pause_menu = PauseMenu(self, self.state)
                            self.state = 'pause'
                        elif self.state == 'pause':
                            self.state = self.pause_menu.previous_state
                        elif self.state == 'almanac':
                            self.state = 'menu'
                            self.main_menu.playing_animation = True
                elif self.state == 'menu':
                    self.main_menu.update(event)
                elif self.state == 'seed_select':
                    self.seed_select.update(event)
                elif self.state == 'game':
                    self.main_game.update(event)
                elif self.state == 'pause':
                    self.pause_menu.update(event)
                elif self.state == 'almanac':
                    self.almanac.update(event)
                elif self.state == 'store':
                    self.store.update(event)
                elif self.state == 'welcome':
                    pass  # no events needed
                elif self.state == 'level_menu':
                    self.menu.handle_events([event])

            # Update animations
            if self.state == 'menu':
                self.main_menu.update_animation(dt)
            elif self.state == 'welcome':
                self.welcome_screen.update(dt)
            elif self.state == 'almanac':
                self.almanac.update_animation(dt)

            if self.state == 'game':
                # Start update thread if not running
                if self.update_thread is None:
                    self.thread_running = True
                    self.update_thread = threading.Thread(target=self.update_loop)
                    self.update_thread.start()
                # Draw protected by lock
                with self.update_lock:
                    self.main_game.draw(self.screen)
            elif self.state in ['win', 'lose']:
                # Draw the game screen
                with self.update_lock:
                    self.main_game.draw(self.screen)
                # Draw fade overlay
                fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                fade_surface.fill((*self.fade_color, self.fade_alpha))
                self.screen.blit(fade_surface, (0, 0))
                # Increase fade alpha
                self.fade_alpha = min(255, self.fade_alpha + 1)
                if self.fade_alpha >= 255:
                    self.state = 'menu'
                    self.main_menu.playing_animation = True
            else:
                # Stop update thread if running
                if self.update_thread is not None:
                    self.thread_running = False
                    self.update_thread.join()
                    self.update_thread = None
                if self.state == 'menu':
                    self.main_menu.draw(self.screen)
                elif self.state == 'seed_select':
                    self.seed_select.draw(self.screen)
                elif self.state == 'pause':
                    self.pause_menu.draw()
                elif self.state == 'almanac':
                    self.almanac.draw()
                elif self.state == 'store':
                    self.store.draw()
                elif self.state == 'welcome':
                    self.welcome_screen.draw(self.screen)
                elif self.state == 'level_menu':
                    self.menu.draw(self.screen)
            pygame.display.flip()
            if self.state == 'game':
                self.sound_manager.play_music(self.main_game.music)
            else:
                self.sound_manager.play_music(self.state)

    def update_loop(self):
        clock = pygame.time.Clock()
        while self.thread_running:
            dt = clock.tick(60) / 1000.0
            with self.update_lock:
                self.main_game.update_wave(dt)

if __name__ == "__main__":
    game = Game()
    game.run()
