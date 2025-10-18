import pygame
from simple_framework import SimpleImageButton, SimplePygameButton
from definitions import PLANT_SUN_COST, ZOMBIE_HEALTH

class StoreItem:
    def __init__(self, icon_path, cost, position, page, action):
        self.icon = pygame.image.load(icon_path)
        self.cost = cost
        self.position = position
        self.page = page
        self.button = SimpleImageButton(position, (130, 130), self.icon, None, action)

class Store:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.scaler = game.scaler
        self.current_page = 1

        # Load background image for almanac index
        self.bg_image = pygame.image.load('images/Store_Background.png')
        self.bg_car = pygame.image.load('images/Store_Car.png')

        self.cost_bg = pygame.image.load('images/Store_PriceTag.png')
        self.buttons = []
        self.items = []

        # Add close button
        self.buttons.append(SimplePygameButton(
                (10, 10),(170, 40),
                [("Close",(0,0))],
                lambda: self.on_close_button(),(150, 150, 200)))

        # Add sample store items (plants)
        self.add_store_items()
        
    def on_close_button(self):
        self.game.state = 'menu'

    def add_store_items(self):
        # Sample items: some plants from PLANT_SUN_COST
        sample_plants = ['Store_PacketUpgrade','Store_PacketUpgrade','Store_PacketUpgrade','Store_PacketUpgrade']
        positions = [(960, 350),(1100, 350),(1240, 350),(1380, 350)]
        for i, plant in enumerate(sample_plants):
            icon_path = f'images/{plant}.png'  # Assuming images are named like Peashooter.png
            cost = 100
            position = positions[i]
            page = 1
            action = lambda p=plant, c=cost: self.purchase_item(p, c)
            item = StoreItem(icon_path, cost, position, page, action)
            self.items.append(item)

    def purchase_item(self, plant_name, cost):
        user_data = self.game.user
        if user_data.get('coins', 0) >= cost:
            user_data['coins'] -= cost
            # Add to purchased items or upgrades
            purchased = user_data.get('purchased', [])
            if plant_name not in purchased:
                purchased.append(plant_name)
                user_data['purchased'] = purchased
            # Save user data
            
            print(f"Purchased {plant_name} for {cost} coins")
        else:
            print("Not enough coins")

    def update(self, event):
        for button in self.buttons:
            button.update(event)
        for item in self.items:
            if item.page == self.current_page:
                item.button.update(event)

    def draw(self):
        # Draw background
        self.screen.blit(self.bg_image, (0, 0))

        self.screen.blit(self.bg_car, (600, 230))

        for button in self.buttons:
            button.draw(self.screen,self.game.font)

        # Draw items on current page
        for item in self.items:
            if item.page == self.current_page:
                item.button.draw(self.screen)
                # Draw cost text
                self.screen.blit(self.cost_bg, (item.position[0] + 10, item.position[1] + 130))
                cost_text = self.game.pico_font.render(str(item.cost), True, (0, 0, 0))
                self.screen.blit(cost_text, (item.position[0] + 30, item.position[1] + 140))
