# Base Screen Size for scaling
BASE_WIDTH, BASE_HEIGHT = 1920, 1080

# 1. Словарь стоимости растений (sun cost)
PLANT_SUN_COST = {
    'Peashooter': 100,
    'Sunflower': 50,
    'Cherry Bomb': 150,
    'Wall Nut': 50,
    'Potato Mine': 25,
    'Snow Pea': 175,
    'Chomper': 150,
    'Repeater': 200,
    'Puff Shroom': 0,
    'Sun Shroom': 25,
    'Fume Shroom': 75,
    'Grave Buster': 75,
    'Hypno Shroom': 75,
    'Scaredy Shroom': 25,
    'Ice Shroom': 75,
    'Doom Shroom': 125,
    'Lily Pad': 25,
    'Squash': 50,
    'Threepeater': 325,
    'Tangle Kelp': 25,
    'Jalapeno': 125,
    'Spikeweed': 100,
    'Torchwood': 175,
    'Tall Nut': 125,
    'Sea Shroom': 0,
    'Plantern': 25,
    'Cactus': 125,
    'Blover': 100,
    'Split Pea': 125,
    'Starfruit': 125,
    'Pumpkin': 125,
    'Magnet Shroom': 100,
    'Cabbage Pult': 100,
    'Flower Pot': 25,
    'Kernel Pult': 100,
    'Coffee Bean': 75,
    'Garlic': 50,
    'Umbrella Leaf': 100,
    'Marigold': 50,
    'Melon Pult': 300
}

# 2. Словарь перезарядки растений (recharge) нужно умножить на 10 для получения нужного значения
PLANT_RECHARGE = {
    'Peashooter': 750,
    'Sunflower': 750,
    'Cherry Bomb': 5000,
    'Wall Nut': 3000,
    'Potato Mine': 3000,
    'Snow Pea': 750,
    'Chomper': 750,
    'Repeater': 750,
    'Puff Shroom': 750,
    'Sun Shroom': 750,
    'Fume Shroom': 750,
    'Grave Buster': 750,
    'Hypno Shroom': 3000,
    'Scaredy Shroom': 750,
    'Ice Shroom': 5000,
    'Doom Shroom': 5000,
    'Lily Pad': 750,
    'Squash': 3000,
    'Threepeater': 750,
    'Tangle Kelp': 3000,
    'Jalapeno': 5000,
    'Spikeweed': 750,
    'Torchwood': 750,
    'Tall Nut': 3000,
    'Sea Shroom': 3000,
    'Plantern': 3000,
    'Cactus': 750,
    'Blover': 750,
    'Split Pea': 750,
    'Starfruit': 750,
    'Pumpkin': 3000,
    'Magnet Shroom': 750,
    'Cabbage Pult': 750,
    'Flower Pot': 750,
    'Kernel Pult': 750,
    'Coffee Bean': 750,
    'Garlic': 750,
    'Umbrella Leaf': 750,
    'Marigold': 3000,
    'Melon Pult': 750
}

PLANT_TIMERS = {
    "Peashooter Fire Rate": 1500,
    "Sunflower Production Rate": 25000,
    "Cherry Bomb Explosion Delay": 1000,
    "Jalapeno Explosion Delay": 1000,
    "Potato Mine Surfacing": 15000,
    "Snow Pea Fire Rate": 1500,
    "Chomper Chew Time": 40000,
    "Chomper Bite Speed": 900,
    "Repeater Fire Rate": 1500,
    "Puff-shroom Fire Rate": 1500,
    "Sun-shroom Production Rate": 25000,
    "Sun-shroom Grow Time": 120000,
    "Fume-shroom Fire Rate": 1500,
    "Grave Buster’s Timer": 4000,
    "Scaredy-shroom Fire Rate": 1500,
    "Ice-shroom Explosion Delay": 1000,
    "Doom-shroom Explosion Delay": 1000,
    "Doom-shroom’s Crater Leaving Time": 180000,
    "Threepeater Fire Rate": 1500,
    "Spikeweed Attack Rate": 1000,
    "Sea-shroom Fire Rate": 1500,
    "Cactus Fire Rate": 1500,
    "Blover Blow Time": 2000,
    "Fog Leave Time": 40000,
    "Split Pea Fire Rate": 1500,
    "Starfruit Fire Rate": 1500,
    "Magnet-shroom Cooldown": 15000,
    "Cabbage-pult Fire Rate": 3000,
    "Kernel-pult Fire Rate": 3000,
    "Kernel-pult’s Chance of Throwing Butter": 0.25,
    "Coffee Bean Delay": 1000,
    "Marigold Production Rate": 25000,
    "Melon-pult Fire Rate": 3000,
}


PLANT_HEALTH = {
    "Basic Plants": 300,
    "Wall Nut": 4000,
    "Tall Nut": 8000,
    "Pumpkin": 4000,
    "Garlic":400
}

PLANT_DAMAGE = {
    "Pea":20,
    "SnowPea":20,
    "Spore":20,
    "FirePea":40,
    "Star":20,
    "Spike":20,
    "Cabbage":40,
    "Kernel":20,
    "Butter":40,
    "Melon":80,

    "CherryBomb":1800,
    "PotatoMine":1800,
    "Squash":1800,
    "DoomShroom":1800,
    "Japanelo":1800,
}

ZOMBIE_HEALTH = {
    "Basic Zombies Health": 270,
    "Conehead Armor": 370,
    "Pole Vaulting Health": 500,
    "Buckethead Armor": 1100,
    "Newspaper Armor": 150,
    "Screen Door Armor": 1100,
    "Football Armor": 1400,
    "Dancing Health": 500,
    "Zomboni Health": 1350,
    "Bobsled Sled Health": 300,
    "Dolphin Rider Health": 500,
    "Jack-In-The-Box Health": 500,
    "Balloon Zombie Balloon": 20,
    "Digger Armor": 100,
    "Pogo Health": 500,
    "Zombie Yeti Health": 1350,
    "Bungee Health": 450,
    "Ladder Armor and Health": 500,
    "Catapult Health": 850,
    "Gargantuar Health": 3000,
    "Imp (I, Zombie)": 70,
    "Dr. Zomboss": 40000,
    "Dr. Zomboss (Extra Health for Minigames)": 20000,
    "Wall-Nut Zombie Health": 1100,
    "Jalapeno Zombie Health": 500,
    "Tall-Nut Zombie Health": 2200,
    "Giga Gargantuar Health": 6000
}

ZOMBIE_COST = {
    'Basic Zombie': 1,
    'Conehead Zombie': 2,
    'Buckethead Zombie': 4
}

PROJECTILE_TEXTURES_PATH = {
    "Pea":"images/ProjectilePea.png",
    "SnowPea":"images/ProjectileSnowPea.png",
    "FirePea":"images/FirePea.png",
    "Star":"images/Projectile_star.png",
    "Spike":"images/ProjectileCactus.png",
    "Cabbage":"images/Cabbagepult_cabbage.png",
    "Kernel":"images/Cornpult_butter.png",
    "Butter":"images/Cornpult_kernal.png",
    "Melon":"images/Melonpult_melon.png",   
    "Spore":"particles/PuffShroom_puff1.png" 
}

WAVE_OPTIONS = {
    "Every": 2,
    "Points":2
}

# Nocturnal plants that sleep during the day
NOCTURNAL_PLANTS = [
    'Puff Shroom',
    'Sun Shroom',
    'Fume Shroom',
    'Hypno Shroom',
    'Scaredy Shroom',
    'Ice Shroom',
    'Doom Shroom',
    'Sea Shroom',
]
