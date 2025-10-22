import pygame
import os
from zombie_animations import *

preloaded_images = {}

def preload_zombie_animations():
    print("Preloading zombie animations...")
    for action in ZOMBIE_ANIMATIONS:
        frames = get_animation_frames(action, 'zombie')
        preloaded_images[f'zombie_{action}'] = [pygame.image.load(f'animations/basic_zombie/Zombie{f:04d}.png').convert_alpha() for f in frames]
        preloaded_images[f'cone_{action}'] = [pygame.image.load(f'animations/cone_zombie/Cone{f:04d}.png').convert_alpha() for f in frames]
        preloaded_images[f'bucket_{action}'] = [pygame.image.load(f'animations/bucket_zombie/Bucket{f:04d}.png').convert_alpha() for f in frames]
    # Preload pole vaulter animations
    for action in POLE_VAULTER_ZOMBIE_ANIMATIONS:
        frames = get_animation_frames(action, 'pole_vaulter_zombie')
        preloaded_images[f'pole_vaulter_{action}'] = [pygame.image.load(f'animations/Zombie_polevaulter/Zombie_polevaulter{f:04d}.png').convert_alpha() for f in frames]
    print("Zombie animations preloaded.")

def preload_plant_animations():
    print("Preloading plant animations...")
    preloaded_images['plant_shadow'] = pygame.image.load('reanim\pot_shadow.png').convert_alpha()
    plant_data = {
        'peashooter': ('peashooter', PEASHOOTER_ANIMATIONS),
        'sunflower': ('sunflower', SUNFLOWER_ANIMATIONS),
        'cherrybomb': ('cherrybomb', CHERRYBOMB_ANIMATIONS),
        'wallnut': ('wallnut', WALLNUT_ANIMATIONS),
        'potato_mine': ('potato_mine', POTATO_MINE_ANIMATIONS),
        'snow_pea': ('snow_pea', SNOW_PEA_ANIMATIONS),
        'chomper': ('chomper', CHOMPER_ANIMATIONS),
        'repeater': ('repeater', REPEATER_ANIMATIONS),
        'lilypad': ('lilypad', LILYPAD_ANIMATIONS),
        'puffshroom': ('puffshroom', PUFFSHROOM_ANIMATIONS),
        'sun_shroom': ('sun_shroom', SUN_SHROOM_ANIMATIONS),
        'fume_shroom': ('fume_shroom', FUME_SHROOM_ANIMATIONS),
        'grave_buster': ('grave_buster', GRAVE_BUSTER_ANIMATIONS),
    }
    for key, (anim_type, anims) in plant_data.items():
        # Try atlas first
        title = anim_type.replace("_", " ").title().replace(" ", "")
        atlas_path = f'animations/Plants/{anim_type}/atlas_{title}0001.png'
        old_title = anim_type.replace("_", " ").title().replace(" ", "_")
        old_sheet_path = f'animations/Plants/{anim_type}/{old_title}.png'
        sheet_path = atlas_path if os.path.exists(atlas_path) else old_sheet_path
        try:
            sheet = pygame.image.load(sheet_path).convert_alpha()
            max_end = max(anim['end_frame'] for anim in anims.values())
            frame_width = sheet.get_width() // max_end
            frame_height = sheet.get_height()
            for action in anims:
                anim = anims[action]
                start_idx = anim['start_frame'] - 1
                frame_count = anim['end_frame'] - anim['start_frame'] + 1
                frames = []
                for i in range(frame_count):
                    x = (start_idx + i) * frame_width
                    if x + frame_width > sheet.get_width():
                        break
                    frame = sheet.subsurface((x, 0, frame_width, frame_height))
                    frames.append(frame)
                preloaded_images[f'{key}_{action}'] = frames
        except Exception as e:
            print(f"Error loading animations for {key}: {e}")
            for action in anims:
                preloaded_images[f'{key}_{action}'] = []

    # Preload sun animations
    frames = get_animation_frames('idle', 'sun')
    preloaded_images['sun_idle'] = frames
    print("Plant animations preloaded.")

def preload_coin_animations():
    frames = get_animation_frames('idle', 'coin_silver')
    preloaded_images['coin_silver'] = frames
    print("Coin animations preloaded.")

def preload_ui():
    print("Preloading UI images...")
    preloaded_images['challenge_background'] = pygame.image.load('images/Challenge_Background.png').convert()
    preloaded_images['challenge_window'] = pygame.image.load('images/Challenge_Window.png').convert_alpha()
    preloaded_images['challenge_window_highlight'] = pygame.image.load('images/Challenge_Window_Highlight.png').convert_alpha()
    preloaded_images['survival_thumbnails'] = pygame.image.load('images/Survival_Thumbnails.jpg').convert()
    preloaded_images['almanac_closebutton'] = pygame.image.load('images/Almanac_CloseButton.png').convert_alpha()
    preloaded_images['almanac_closebuttonhighlight'] = pygame.image.load('images/Almanac_CloseButtonHighlight.png').convert_alpha()
    print("UI images preloaded.")

def preload_plant_icons():
    plant_data = {
        'Peashooter': ('peashooter', 'idle'),
        'Sunflower': ('sunflower', 'idle'),
        'Cherry Bomb': ('cherrybomb', 'idle'),
        'Wall Nut': ('wallnut', 'idle'),
        'Potato Mine': ('potato_mine', 'idle'),
        'Snow Pea': ('snow_pea', 'idle'),
        'Chomper': ('chomper', 'idle'),
        'Repeater': ('repeater', 'idle'),
        'Puff Shroom': ('puffshroom', 'idle'),
        'Sun Shroom': ('sun_shroom', 'idle'),
        'Fume Shroom': ('fume_shroom', 'idle'),
        'Grave Buster': ('grave_buster', 'idle'),
        'Lily Pad': ('lilypad', 'idle'),
    }
    preloaded_images['plant_icons'] = {}
    for name, (anim_type, action) in plant_data.items():
        # Try icon file first
        title = anim_type.replace("_", " ").title().replace(" ", "")
        icon_path = f'animations/Plants/{anim_type}/icon_{title}0001.png'
        if os.path.exists(icon_path):
            try:
                icon = pygame.image.load(icon_path).convert_alpha()
                preloaded_images['plant_icons'][name] = icon
            except Exception as e:
                print(f"Error loading icon for {name}: {e}")
                preloaded_images['plant_icons'][name] = None
        else:
            # Fallback to atlas or old sheet
            atlas_path = f'animations/Plants/{anim_type}/atlas_{title}0001.png'
            old_sheet_path = f'animations/Plants/{anim_type}/{anim_type.title()}.png'
            sheet_path = atlas_path if os.path.exists(atlas_path) else old_sheet_path
            try:
                sheet = pygame.image.load(sheet_path).convert_alpha()
                if sheet_path == old_sheet_path:
                    # Old single image, use whole as icon
                    icon = sheet
                else:
                    # Atlas sprite sheet, subsurface the first frame of action
                    anims_name = f'{anim_type.upper()}_ANIMATIONS'
                    if anims_name in globals():
                        anims = globals()[anims_name]
                    else:
                        anims_name = f'{anim_type.upper().replace("_", "")}_ANIMATIONS'
                        anims = globals()[anims_name]
                    max_end = max(anim['end_frame'] for anim in anims.values())
                    frame_width = sheet.get_width() // max_end
                    frame_height = sheet.get_height()
                    anim = anims[action]
                    start_idx = anim['start_frame'] - 1
                    icon = sheet.subsurface((start_idx * frame_width, 0, frame_width, frame_height))
                preloaded_images['plant_icons'][name] = icon
            except Exception as e:
                print(f"Error loading icon for {name}: {e}")
                preloaded_images['plant_icons'][name] = None

def preload_all():
    preload_zombie_animations()
    preload_plant_animations()
    preload_coin_animations()
    preload_ui()
    preload_plant_icons()
