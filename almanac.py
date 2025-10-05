import pygame
from simple_framework import SimpleImageButton

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

    def update(self, event):
        self.plant_button.update(event)
        self.zombie_button.update(event)
        self.close_button.update(event)

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
        elif self.current_section == 'zombies':

            self.screen.blit(self.zombie_bg_img, (0,0))
