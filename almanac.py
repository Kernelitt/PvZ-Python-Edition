import pygame
from simple_framework import SimpleImageButton, SimplePygameButton
from definitions import PLANT_SUN_COST
from zombie_animations import get_animation_frames

class Almanac:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.scaler = game.scaler

        # Load background image for almanac index
        self.bg_image = pygame.image.load('images/Almanac_IndexBack.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (self.game.width, self.game.height))

        # Load button images
        self.plant_bg_img = pygame.image.load('images/Almanac_PlantBack.png')
        self.zombie_bg_img = pygame.image.load('images/Almanac_ZombieBack.png')

        self.plant_button_img = pygame.image.load('images/SeedChooser_Button.png')
        self.plant_button_img_hover = pygame.image.load('images/SeedChooser_Button_Glow.png')

        self.zombie_button_img = pygame.image.load('images/SeedChooser_Button.png')
        self.zombie_button_img_hover = pygame.image.load('images/SeedChooser_Button_Glow.png')

        self.close_button_img = pygame.image.load('images/Almanac_CloseButton.png')
        self.close_button_hover_img = pygame.image.load('images/Almanac_CloseButtonHighlight.png')

        # Scale buttons appropriately
        button_width = self.scaler.scale_x(156*2)
        button_height = self.scaler.scale_y(42*2)
        close_button_size = self.scaler.scale(178, 52)

        # Positions for buttons (example positions, can be adjusted)
        plant_button_pos = (self.scaler.scale_x(400), self.scaler.scale_y(600))
        zombie_button_pos = (self.scaler.scale_x(1100), self.scaler.scale_y(600))
        close_button_pos = (self.game.width - close_button_size[0] - self.scaler.scale_x(20), self.scaler.scale_y(20))

        # Create buttons
        self.plant_button = SimpleImageButton(
            plant_button_pos,
            (button_width, button_height),
            self.plant_button_img,
            self.plant_button_img_hover,
            self.on_plant_button
        )
        self.zombie_button = SimpleImageButton(
            zombie_button_pos,
            (button_width, button_height),
            self.zombie_button_img,
            self.zombie_button_img_hover,
            self.on_zombie_button
        )
        self.close_button = SimpleImageButton(
            close_button_pos,
            close_button_size,
            self.close_button_img,
            self.close_button_hover_img,
            self.on_close_button
        )

        # Current section: 'index', 'plants', or 'zombies'
        self.current_section = 'index'

        # Plants section
        self.plants_list = list(PLANT_SUN_COST.keys())
        self.selected_plant = 'Peashooter'
        self.plant_buttons = []
        cols = 8
        rows = 7
        button_width = self.scaler.scale_x(90)
        button_height = self.scaler.scale_y(125)
        x_start = self.scaler.scale_x(287)
        y_start = self.scaler.scale_y(170)
        spacing_x = self.scaler.scale_x(93)
        spacing_y = self.scaler.scale_y(140)
        for i, plant in enumerate(self.plants_list):
            if i >= cols * rows:
                break
            row = i // cols
            col = i % cols
            x = x_start + col * spacing_x
            y = y_start + row * spacing_y
            button = SimplePygameButton(
                (x, y),
                (button_width, button_height),
                [],
                lambda p=plant: self.select_plant(p),
                (150, 150, 200)
            )
            self.plant_buttons.append(button)
        # Close button for plants
        self.plants_close_button = SimpleImageButton(
            (self.game.width - self.scaler.scale_x(178) - self.scaler.scale_x(20), self.scaler.scale_y(20)),
            self.scaler.scale(178, 52),
            self.close_button_img,
            self.close_button_hover_img,
            self.on_close_plants
        )
        # Load plants section images
        self.plants_ground = pygame.image.load('images/Almanac_GroundDay.jpg')
        self.plant_card_bg = pygame.image.load('images/Almanac_PlantCard.png')
        # Plant animations
        self.plant_animations = {}
        self.idle_frames = {}
        for plant in self.plants_list:
            frames = []
            i = 1
            while True:
                try:
                    frame = pygame.image.load(f'animations/Plants/{plant.lower()}/{plant}{i:04d}.png')
                    frames.append(frame)
                    i += 1
                except:
                    break
            if frames:
                self.plant_animations[plant] = frames
                plant_type = plant.lower().replace(' ', '_')
                idle_frames = get_animation_frames('idle', plant_type)
                if not idle_frames and plant_type == 'lilypad':
                    idle_frames = get_animation_frames('blink', plant_type)
                if not idle_frames:
                    idle_frames = list(range(1, len(frames) + 1))
                self.idle_frames[plant] = idle_frames
            else:
                self.plant_animations[plant] = None
                self.idle_frames[plant] = []
        self.current_frame = 0
        self.animation_timer = 0.0
        self.frame_duration = 0.1

        # Colors for description tags
        self.keyword_color = "#0C24F8"
        self.stat_color = "#F80C0C"
        self.flavor_color = "#A77814"
        self.nocturnal_color = "#800080"  # purple

    def on_plant_button(self):
        self.current_section = 'plants'
        # For now, just print or could add more UI for plants section
        print("Almanac: Plants section selected")

    def on_zombie_button(self):
        self.current_section = 'zombies'
        # For now, just print or could add more UI for zombies section
        print("Almanac: Zombies section selected")

    def on_close_button(self):
        self.game.state = 'menu'

    def select_plant(self, plant):
        self.selected_plant = plant

    def on_close_plants(self):
        self.current_section = 'index'

    def update_animation(self, dt):
        if self.current_section == 'plants':
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer -= self.frame_duration
                if self.idle_frames.get(self.selected_plant) and self.idle_frames[self.selected_plant]:
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames[self.selected_plant])

    def parse_description_line(self, line):
        if line.strip() == "{SHORTLINE}":
            return [("SHORTLINE", None)]
        parts = []
        current_color = self.flavor_color
        i = 0
        while i < len(line):
            if line[i] == '{':
                j = line.find('}', i)
                if j != -1:
                    tag = line[i+1:j]
                    i = j + 1
                    if tag == "KEYWORD":
                        current_color = self.keyword_color
                    elif tag == "STAT":
                        current_color = self.stat_color
                    elif tag == "FLAVOR":
                        current_color = self.flavor_color
                    elif tag == "NOCTURNAL":
                        current_color = self.nocturnal_color
                    elif tag == "SHORTLINE":
                        parts.append(("SHORTLINE", None))
                        break
                    else:
                        pass
                else:
                    parts.append((line[i:], current_color))
                    break
            else:
                j = line.find('{', i)
                if j == -1:
                    parts.append((line[i:], current_color))
                    break
                else:
                    parts.append((line[i:j], current_color))
                    i = j
        return parts

    def wrap_text(self, text, max_width):
        if not text or text.strip() == "{SHORTLINE}":
            return [text]
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if self.game.small_font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def update(self, event):
        if self.current_section == 'index':
            self.plant_button.update(event)
            self.zombie_button.update(event)
            self.close_button.update(event)
        elif self.current_section == 'plants':
            for button in self.plant_buttons:
                button.update(event)
            self.plants_close_button.update(event)

    def draw(self):
        # Draw background
        self.screen.blit(self.bg_image, (0, 0))

        # Draw plant button base image
        self.screen.blit(pygame.transform.scale(self.plant_button_img, self.plant_button.size), self.plant_button.position)
        # If hovered, draw hover image on top as overlay
        if self.plant_button.hovered and self.plant_button.hover_image:
            self.screen.blit(pygame.transform.scale(self.plant_button.hover_image, self.plant_button.size), self.plant_button.position)

        # Draw zombie button base image
        self.screen.blit(pygame.transform.scale(self.zombie_button_img, self.zombie_button.size), self.zombie_button.position)
        # If hovered, draw hover image on top as overlay
        if self.zombie_button.hovered and self.zombie_button.hover_image:
            self.screen.blit(pygame.transform.scale(self.zombie_button.hover_image, self.zombie_button.size), self.zombie_button.position)

        # Draw close button base image
        self.screen.blit(pygame.transform.scale(self.close_button_img, self.close_button.size), self.close_button.position)
        # If hovered, draw hover image on top as overlay
        if self.close_button.hovered and self.close_button.hover_image:
            self.screen.blit(pygame.transform.scale(self.close_button.hover_image, self.close_button.size), self.close_button.position)

        # Draw current section UI
        font = self.game.font
        if self.current_section == 'plants':
            self.screen.blit(self.plant_bg_img, (0,0))
            # Draw grid
            for i, button in enumerate(self.plant_buttons):
                plant = self.plants_list[i]
                scaled_seed = pygame.transform.scale(self.game.seed_image, button.size)
                self.screen.blit(scaled_seed, button.position)
                if plant in self.game.plant_icons:
                    icon = self.game.plant_icons[plant]
                    scaled_icon = pygame.transform.scale(icon, (int(button.size[0]*0.8), int(button.size[1]*0.6)))
                    icon_rect = scaled_icon.get_rect(center=(button.position[0] + button.size[0]//2, button.position[1] + button.size[1]//2))
                    self.screen.blit(scaled_icon, icon_rect)
                if plant == self.selected_plant:
                    pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(button.position, button.size), 3)
            # Draw plant display
            ground_x = self.scaler.scale_x(1350)
            ground_y = self.scaler.scale_y(150)
            self.screen.blit(self.plants_ground, (ground_x, ground_y))
            if self.plant_animations[self.selected_plant]:
                frame = self.plant_animations[self.selected_plant][self.current_frame]
                scaled_frame = pygame.transform.scale(frame, (self.scaler.scale_x(150), self.scaler.scale_y(150)))
                self.screen.blit(scaled_frame, (ground_x + self.scaler.scale_x(50), ground_y + self.scaler.scale_y(50)))
            # Plant card
            card_x = self.scaler.scale_x(1200)
            card_y = self.scaler.scale_y(100)
            self.screen.blit(self.plant_card_bg, (card_x, card_y))
            # Name
            name = self.game.lawn_strings.get(self.selected_plant.upper().replace(' ', '_'), self.selected_plant)
            name_text = self.game.font.render(name, True, "#AD8B2C")
            self.screen.blit(name_text, (card_x + self.scaler.scale_x(196), card_y + self.scaler.scale_y(400)))
            # Description
            desc_key = self.selected_plant.upper().replace(' ', '_') + '_DESCRIPTION'
            desc = self.game.lawn_strings.get(desc_key, "")
            header_key = self.selected_plant.upper().replace(' ', '_') + '_DESCRIPTION_HEADER'
            header = self.game.lawn_strings.get(header_key, "")
            y_offset = card_y + self.scaler.scale_y(500)
            # Header
            wrapped_header = self.wrap_text(header, 550)
            for line in wrapped_header:
                rendered = self.game.small_font.render(line, True, (25,25,200))
                self.screen.blit(rendered, (card_x + self.scaler.scale_x(48), y_offset))
                y_offset += self.scaler.scale_y(20)
            y_offset += self.scaler.scale_y(10)  # space
            # Description
            for line in desc.split('\n'):
                wrapped_lines = self.wrap_text(line, 550)
                for wrapped_line in wrapped_lines:
                    parts = self.parse_description_line(wrapped_line)
                    current_x = card_x + self.scaler.scale_x(20) + 24
                    for part in parts:
                        if part[0] == "SHORTLINE":
                            pygame.draw.rect(self.screen, (0,0,0), (current_x, y_offset, self.scaler.scale_x(100), 2))
                            y_offset += self.scaler.scale_y(5)
                            break
                        else:
                            text, color = part
                            rendered = self.game.small_font.render(text, True, color)
                            self.screen.blit(rendered, (current_x, y_offset))
                            current_x += rendered.get_width()
                    y_offset += self.scaler.scale_y(30)
            # Close button
            self.plants_close_button.draw(self.screen)
        elif self.current_section == 'zombies':
            self.screen.blit(self.zombie_bg_img, (0,0))
