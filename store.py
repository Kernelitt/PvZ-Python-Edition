import pygame,json
from simple_framework import SimpleImageButton, SimplePygameButton
from definitions import PLANT_SUN_COST, ZOMBIE_HEALTH

class StoreItem:
    def __init__(self, icon_path, cost, position_index, page, action):
        self.icon = pygame.image.load(icon_path)
        self.cost = cost
        self.position_index = position_index
        self.page = page
        self.action = action

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
        sample_plants = ['Store_PacketUpgrade']
        positions = [(960, 350),(1100, 350),(1240, 350),(1380, 350),(880, 530),(1020, 530),(1160, 530),(1300, 530)]
        for i, plant in enumerate(sample_plants):
            icon_path = f'images/{plant}.png'  # Assuming images are named like Peashooter.png
            cost = 100
            position_index = i
            page = 1
            action = lambda p=plant, c=cost: self.purchase_item(p, c)
            item = StoreItem(icon_path, cost, position_index, page, action)
            self.items.append(item)

    def purchase_item(self, plant_name, cost):
        user_data = self.game.user
        if user_data.get('coins', 0) >= cost:
            user_data['coins'] -= cost
            if plant_name == 'Store_PacketUpgrade':
                if user_data['max_seeds'] < 10:  # Max limit of 10 seeds
                    user_data['max_seeds'] += 1
                    user_data['seed_upgrade_count'] += 1
                    print(f"Purchased seed upgrade, max seeds now {user_data['max_seeds']}")
                else:
                    print("Max seeds already reached")
                    return  # Don't save if not upgraded
            else:
                # Add to purchased items or upgrades
                purchased = user_data.get('purchased', [])
                if plant_name not in purchased:
                    purchased.append(plant_name)
                    user_data['purchased'] = purchased
            # Save user data
            user_data_copy = user_data.copy()
            user_data_copy['completed_levels'] = list(user_data['completed_levels'])
            with open('user.json', 'w') as f:
                json.dump(user_data_copy, f)
            print(f"Purchased {plant_name} for {cost} coins")
        else:
            print("Not enough coins")

    def update(self, event):
        for button in self.buttons:
            button.update(event)
        for item in self.items:
            if item.page == self.current_page:
                # Create button on the fly using position_index
                positions = [(960, 350),(1100, 350),(1240, 350),(1380, 350),(880, 530),(1020, 530),(1160, 530),(1300, 530)]
                pos = positions[item.position_index]
                button = SimpleImageButton(pos, (130, 130), item.icon, None, item.action)
                button.update(event)

    def draw(self):
        # Draw background
        self.screen.blit(self.bg_image, (0, 0))

        self.screen.blit(self.bg_car, (600, 230))

        for button in self.buttons:
            button.draw(self.screen,self.game.font)

        # Draw items on current page
        for item in self.items:
            if item.page == self.current_page:
                positions = [(960, 350),(1100, 350),(1240, 350),(1380, 350),(880, 530),(1020, 530),(1160, 530),(1300, 530)]
                pos = positions[item.position_index]
                button = SimpleImageButton(pos, (130, 130), item.icon, None, item.action)
                button.draw(self.screen)
                # Draw cost text
                self.screen.blit(self.cost_bg, (pos[0] + 10, pos[1] + 130))
                cost_text = self.game.pico_font.render(str(item.cost), True, (0, 0, 0))
                self.screen.blit(cost_text, (pos[0] + 30, pos[1] + 140))
