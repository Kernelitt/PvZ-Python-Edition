# Animations Configuration
# This file defines the frame ranges for different animations.
# Assuming frames are named like Zombie0001.png, Peashooter0001.png, etc.
# Adjust the ranges based on your actual frame sequences.

ZOMBIE_ANIMATIONS = {
    'walk': {
        'start_frame': 46,
        'end_frame': 92,
        'loop': True,
        'fps': 12  # frames per second for this animation
    },
    'attack': {
        'start_frame': 139,
        'end_frame': 178,
        'loop': True,
        'fps': 24
    },
    'death': {
        'start_frame': 179,
        'end_frame': 217,
        'loop': False,
        'fps': 24
    },
}

POLE_VAULTER_ZOMBIE_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 13,
        'loop': True,
        'fps': 12  # frames per second for this animation
    },
    'run': {
        'start_frame': 13,
        'end_frame': 50,
        'loop': True,
        'fps': 24  # frames per second for this animation
    },
    'walk': {
        'start_frame': 94,
        'end_frame': 138,
        'loop': True,
        'fps': 24  # frames per second for this animation
    },
    'jump': {
        'start_frame': 51,
        'end_frame': 93,
        'loop': True,
        'fps': 24  # frames per second for this animation
    },
    'attack': {
        'start_frame': 166,
        'end_frame': 193,
        'loop': True,
        'fps': 24
    },
    'death': {
        'start_frame': 139,
        'end_frame': 165,
        'loop': False,
        'fps': 24
    },
}

PEASHOOTER_ANIMATIONS = {
    'idle': {
        'start_frame': 80,
        'end_frame': 104,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'shoot': {
        'start_frame': 55,
        'end_frame': 79,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    },
    'shoot_top': {
        'start_frame': 55,
        'end_frame': 79,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'shoot_bottom': {
        'start_frame': 5,
        'end_frame': 29,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'blink': {
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    }
}

SUNFLOWER_ANIMATIONS = {
    'frame_width':160,
    'blink': {
        'start_frame': 1,
        'end_frame': 4,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'idle': {
        'start_frame': 5,
        'end_frame': 25,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    }
}

CHERRYBOMB_ANIMATIONS = {
    'idle': {
        'start_frame': 15,
        'end_frame': 27,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'active': {
        'start_frame': 1,
        'end_frame': 14,
        'loop': False,
        'fps': 12,
        'sprite_sheet': True
    }
}

WALLNUT_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 16,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    }
}

POTATO_MINE_ANIMATIONS = {
    'not_armed': {
        'start_frame': 1,
        'end_frame': 8,
        'loop': True,
        'fps': 6,
        'sprite_sheet': True
    },
    'arming': {
        'start_frame': 1,
        'end_frame': 12,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'idle': {
        'start_frame': 1,
        'end_frame': 12,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'explode': {
        'start_frame': 1,
        'end_frame': 1,
        'loop': True,
        'fps': 1,
        'sprite_sheet': True
    },
    'blink': { # when idle
        'start_frame': 1,
        'end_frame': 3,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
}

SNOW_PEA_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 25,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'shoot': {
        'start_frame': 1,
        'end_frame': 25,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    },
    'shoot_top': {
        'start_frame': 1,
        'end_frame': 25,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'shoot_bottom': {
        'start_frame': 1,
        'end_frame': 25,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'blink': {
        'start_frame': 1,
        'end_frame': 5,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    }
}

CHOMPER_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 26,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
        'attack': {
        'start_frame': 1,
        'end_frame': 24,
        'loop': False,
        'fps': 12,
        'sprite_sheet': True
    },
        'chewing': {
        'start_frame': 1,
        'end_frame': 18,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
        'chewing_to_idle': {
        'start_frame': 1,
        'end_frame': 26,
        'loop': False,
        'fps': 12,
        'sprite_sheet': True
    }
}

REPEATER_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 25,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'shoot': {
        'start_frame': 1,
        'end_frame': 50,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    },
    'shoot_top': {
        'start_frame': 1,
        'end_frame': 50,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'shoot_bottom': {
        'start_frame': 1,
        'end_frame': 25,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'blink': {
        'start_frame': 1,
        'end_frame': 5,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    }
}

PUFFSHROOM_ANIMATIONS = {
    'blink': {
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    },
    'idle': {
        'start_frame': 1,
        'end_frame': 17,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'shoot': {
        'start_frame': 1,
        'end_frame': 13,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    },
    'sleep': {
        'start_frame': 1,
        'end_frame': 17,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
}

SUN_SHROOM_ANIMATIONS = {
    'blink': { #small
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    },
    'idle': { #small
        'start_frame': 1,
        'end_frame': 13,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'idle_big': {
        'start_frame': 1,
        'end_frame': 13,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'grow': {
        'start_frame': 1,
        'end_frame': 11,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    },
    'sleep_small': {
        'start_frame': 1,
        'end_frame': 10,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'sleep_big': {
        'start_frame': 1,
        'end_frame': 13,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
}

FUME_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 17,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'sleep': {
        'start_frame': 1,
        'end_frame': 18,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    }
}

GRAVE_BUSTER_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 39,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    }
}

HYPNO_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 20,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'sleep': {
        'start_frame': 1,
        'end_frame': 20,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    }
}

SCAREDY_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 16,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'sleep': {
        'start_frame': 1,
        'end_frame': 16,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    }
}

ICE_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 21,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'sleep': {
        'start_frame': 1,
        'end_frame': 17,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    }
}

DOOM_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 24,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    },
    'sleep': {
        'start_frame': 1,
        'end_frame': 25,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    }
}

LILYPAD_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 1,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    },
    'blink': {
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 24,
        'sprite_sheet': True
    }
}

SQUASH_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 20,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    }
}

SUN_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 12,
        'loop': True,
        'fps': 12,
        'sprite_sheet': True
    }
}

COIN_SILVER_ANIMATIONS = {
    'frame_width':45,
    'idle': {
        'start_frame': 1,
        'end_frame': 21,
        'loop': True,
        'fps': 24,
        'sprite_sheet': True
    }
}

MAIN_MENU = {
    'awake':{
        'start_frame': 1,
        'end_frame': 14,
        'loop': False,
        'fps': 24    
    },
    'awake2':{
        'start_frame': 15,
        'end_frame': 40,
        'loop': False,
        'fps': 24    
    }
}

CRAZY_DAVE = {
    'appear':{
        'start_frame': 1,
        'end_frame': 18,
        'loop': False,
        'fps': 24    
    },    
    'disappear':{
        'start_frame': 19,
        'end_frame': 33,
        'loop': False,
        'fps': 24    
    },  
    'talk':{
        'start_frame': 34,
        'end_frame': 64,
        'loop': False,
        'fps': 24    
    },  
    'idle':{
        'start_frame': 65,
        'end_frame': 84,
        'loop': False,
        'fps': 24    
    },  
    'scream':{
        'start_frame': 85,
        'end_frame': 147,
        'loop': False,
        'fps': 24    
    },  
}

# Function to get animation frames for a given action and type
def get_animation_frames(action, anim_type='zombie'):
    import pygame
    if anim_type == 'zombie' and action in ZOMBIE_ANIMATIONS:
        anim = ZOMBIE_ANIMATIONS[action]
    elif anim_type == 'peashooter' and action in PEASHOOTER_ANIMATIONS:
        anim = PEASHOOTER_ANIMATIONS[action]
    elif anim_type == 'sunflower' and action in SUNFLOWER_ANIMATIONS:
        anim = SUNFLOWER_ANIMATIONS[action]
    elif anim_type == 'cherrybomb' and action in CHERRYBOMB_ANIMATIONS:
        anim = CHERRYBOMB_ANIMATIONS[action]
    elif anim_type == 'wallnut' and action in WALLNUT_ANIMATIONS:
        anim = WALLNUT_ANIMATIONS[action]
    elif anim_type == 'potato_mine' and action in POTATO_MINE_ANIMATIONS:
        anim = POTATO_MINE_ANIMATIONS[action]
    elif anim_type == 'snow_pea' and action in SNOW_PEA_ANIMATIONS:
        anim = SNOW_PEA_ANIMATIONS[action]
    elif anim_type == 'chomper' and action in CHOMPER_ANIMATIONS:
        anim = CHOMPER_ANIMATIONS[action]
    elif anim_type == 'repeater' and action in REPEATER_ANIMATIONS:
        anim = REPEATER_ANIMATIONS[action]
    elif anim_type == 'puffshroom' and action in PUFFSHROOM_ANIMATIONS:
        anim = PUFFSHROOM_ANIMATIONS[action]
    elif anim_type == 'sun_shroom' and action in SUN_SHROOM_ANIMATIONS:
        anim = SUN_SHROOM_ANIMATIONS[action]
    elif anim_type == 'fume_shroom' and action in FUME_SHROOM_ANIMATIONS:
        anim = FUME_SHROOM_ANIMATIONS[action]
    elif anim_type == 'grave_buster' and action in GRAVE_BUSTER_ANIMATIONS:
        anim = GRAVE_BUSTER_ANIMATIONS[action]
    elif anim_type == 'lilypad' and action in LILYPAD_ANIMATIONS:
        anim = LILYPAD_ANIMATIONS[action]
    elif anim_type == 'sun' and action in SUN_ANIMATIONS:
        anim = SUN_ANIMATIONS[action]
    elif anim_type == 'coin_silver' and action in COIN_SILVER_ANIMATIONS:
        anim = COIN_SILVER_ANIMATIONS[action]
    elif anim_type == 'main_menu' and action in MAIN_MENU:
        anim = MAIN_MENU[action]
    elif anim_type == 'pole_vaulter_zombie' and action in POLE_VAULTER_ZOMBIE_ANIMATIONS:
        anim = POLE_VAULTER_ZOMBIE_ANIMATIONS[action]
    else:
        return []
    if 'sprite_sheet' in anim and anim['sprite_sheet']:
        # Load sprite sheet and split into frames
        if anim_type == 'coin_silver':
            sheet_path = f'animations/collectable/atlas_Coin_silver0001.png'
        elif anim_type == 'sun':
            sheet_path = f'animations/collectable/atlas_Sun0001.png'
        else:
            sheet_path = f'animations/Plants/{anim_type}/{action}.png'  # Adjust path as needed
        try:
            sheet = pygame.image.load(sheet_path)
            frame_count = anim['end_frame'] - anim['start_frame'] + 1
            # Адаптация: используем frame_width из anims, если есть, иначе вычисляем
            frame_width = anim["frame_width"] if "frame_width" in anim else sheet.get_width() // frame_count
            frame_height = sheet.get_height()
            frames = []
            for i in range(frame_count):
                frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frames.append(frame)
            return frames
        except:
            return []
    else:
        return list(range(anim['start_frame'], anim['end_frame'] + 1))


# Example usage:
# frames = get_animation_frames('walk', 'zombie')  # Returns [46, 47, ..., 92]
# frames = get_animation_frames('idle', 'peashooter')  # Returns [1, 2, ..., 30]
