import pygame
from zombie_animations import (
    get_animation_frames, ZOMBIE_ANIMATIONS, PEASHOOTER_ANIMATIONS, SUNFLOWER_ANIMATIONS,
    CHERRYBOMB_ANIMATIONS, WALLNUT_ANIMATIONS, POTATO_MINE_ANIMATIONS, SNOW_PEA_ANIMATIONS,
    CHOMPER_ANIMATIONS, REPEATER_ANIMATIONS, PUFF_SHROOM_ANIMATIONS, SUN_SHROOM_ANIMATIONS,
    FUME_SHROOM_ANIMATIONS, GRAVE_BUSTER_ANIMATIONS, SUN_ANIMATIONS, LILYPAD_ANIMATIONS
)

preloaded_images = {}

def preload_zombie_animations():
    print("Preloading zombie animations...")
    for action in ZOMBIE_ANIMATIONS:
        frames = get_animation_frames(action, 'zombie')
        preloaded_images[f'zombie_{action}'] = [pygame.image.load(f'animations/basic_zombie/Zombie{f:04d}.png').convert_alpha() for f in frames]
        preloaded_images[f'cone_{action}'] = [pygame.image.load(f'animations/cone_zombie/Cone{f:04d}.png').convert_alpha() for f in frames]
        preloaded_images[f'bucket_{action}'] = [pygame.image.load(f'animations/bucket_zombie/Bucket{f:04d}.png').convert_alpha() for f in frames]
    print("Zombie animations preloaded.")

def preload_plant_animations():
    print("Preloading plant animations...")
    plant_data = {
        'peashooter': ('peashooter', PEASHOOTER_ANIMATIONS, 'Peashooter'),
        'sunflower': ('sunflower', SUNFLOWER_ANIMATIONS, 'Sunflower'),
        'cherrybomb': ('cherrybomb', CHERRYBOMB_ANIMATIONS, 'Cherrybomb'),
        'wallnut': ('wallnut', WALLNUT_ANIMATIONS, 'Wallnut'),
        'potato_mine': ('potato_mine', POTATO_MINE_ANIMATIONS, 'PotatoMine'),
        'snow_pea': ('snow_pea', SNOW_PEA_ANIMATIONS, 'SnowPea'),
        'chomper': ('chomper', CHOMPER_ANIMATIONS, 'Chomper'),
        'repeater': ('repeater', REPEATER_ANIMATIONS, 'Repeater'),
        'lilypad': ('lilypad', LILYPAD_ANIMATIONS, 'LilyPad'),
        'puffshroom': ('puffshroom', PUFF_SHROOM_ANIMATIONS, 'PuffShroom'),
        'sun_shroom': ('sun_shroom', SUN_SHROOM_ANIMATIONS, 'SunShroom'),
        'fume_shroom': ('fume_shroom', FUME_SHROOM_ANIMATIONS, 'FumeShroom'),
        'grave_buster': ('grave_buster', GRAVE_BUSTER_ANIMATIONS, 'GraveBuster'),
    }
    for key, (anim_type, anims, filename_prefix) in plant_data.items():
        for action in anims:
            frames = get_animation_frames(action, anim_type)
            preloaded_images[f'{key}_{action}'] = [pygame.image.load(f'animations/Plants/{key.replace("_", "")}/{filename_prefix}{f:04d}.png').convert_alpha() for f in frames]

    # Preload sun animations
    frames = get_animation_frames('idle', 'sun')
    preloaded_images['sun_idle'] = [pygame.image.load(f'animations/sun/Sun{f:04d}.png').convert_alpha() for f in frames]
    print("Plant animations preloaded.")

def preload_sun_animations():
    print("Preloading sun animations...")
    frames = get_animation_frames('idle', 'sun')
    preloaded_images['sun_idle'] = [pygame.image.load(f'animations/sun/Sun{f:04d}.png').convert_alpha() for f in frames]
    print("Sun animations preloaded.")

def preload_ui():
    print("Preloading UI images...")
    preloaded_images['challenge_background'] = pygame.image.load('images/Challenge_Background.png').convert()
    preloaded_images['challenge_window'] = pygame.image.load('images/Challenge_Window.png').convert_alpha()
    preloaded_images['challenge_window_highlight'] = pygame.image.load('images/Challenge_Window_Highlight.png').convert_alpha()
    preloaded_images['survival_thumbnails'] = pygame.image.load('images/Survival_Thumbnails.jpg').convert()
    preloaded_images['almanac_closebutton'] = pygame.image.load('images/Almanac_CloseButton.png').convert_alpha()
    preloaded_images['almanac_closebuttonhighlight'] = pygame.image.load('images/Almanac_CloseButtonHighlight.png').convert_alpha()
    print("UI images preloaded.")

def preload_all():
    preload_zombie_animations()
    preload_plant_animations()
    preload_sun_animations()
    preload_ui()
