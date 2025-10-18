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

SCREENDOOR_ZOMBIE_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 30,  # Adjust based on actual frames
        'loop': True,
        'fps': 12
    },
    'idle2': {
        'start_frame': 31,
        'end_frame': 45,  # Adjust based on actual frames
        'loop': True,
        'fps': 12
    },
    'walk': {
        'start_frame': 46,
        'end_frame': 92,  # Adjust based on actual frames
        'loop': True,
        'fps': 12
    }

}
PEASHOOTER_ANIMATIONS = {
    'idle': {
        'start_frame': 80,
        'end_frame': 104,  # Adjust based on actual frames
        'loop': True,
        'fps': 12
    },
    'shoot': {
        'start_frame': 55,
        'end_frame': 79,  # Use shoot_top frames for timing
        'loop': False,
        'fps': 24
    },
    'shoot_top': {
        'start_frame': 55,
        'end_frame': 79,  # Adjust based on actual frames
        'loop': True,
        'fps': 24
    },
    'shoot_bottom': {
        'start_frame': 5,
        'end_frame': 29,  # Adjust based on actual frames
        'loop': True,
        'fps': 24
    },
    'blink': {
        'start_frame': 1,
        'end_frame': 5,  # Adjust based on actual frames
        'loop': False,
        'fps': 24
    }
}

SUNFLOWER_ANIMATIONS = {
    'idle': {
        'start_frame': 5,
        'end_frame': 29,
        'loop': True,
        'fps': 12
    }
}

CHERRYBOMB_ANIMATIONS = {
    'idle': {
        'start_frame': 15,
        'end_frame': 27,
        'loop': True,
        'fps': 12
    },
    'active': {
        'start_frame': 1,
        'end_frame': 14,
        'loop': False,
        'fps': 12
    }
}

WALLNUT_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 16,
        'loop': True,
        'fps': 12
    }
}

POTATO_MINE_ANIMATIONS = {
    'not_armed': {
        'start_frame': 1,
        'end_frame': 8,
        'loop': True,
        'fps': 6
    },
    'arming': {
        'start_frame': 9,
        'end_frame': 20,
        'loop': True,
        'fps': 12
    },
    'idle': {
        'start_frame': 21,
        'end_frame': 32,
        'loop': True,
        'fps': 12
    },
    'explode': {
        'start_frame': 36,
        'end_frame': 36,
        'loop': True,
        'fps': 1
    },
    'blink': { # when idle
        'start_frame': 33,
        'end_frame': 35,
        'loop': True,
        'fps': 12
    },
}

SNOW_PEA_ANIMATIONS = {
    'idle': {
        'start_frame': 80,
        'end_frame': 104,  # Adjust based on actual frames
        'loop': True,
        'fps': 12
    },
    'shoot': {
        'start_frame': 55,
        'end_frame': 79,  # Use shoot_top frames for timing
        'loop': False,
        'fps': 24
    },
    'shoot_top': {
        'start_frame': 55,
        'end_frame': 79,  # Adjust based on actual frames
        'loop': True,
        'fps': 24
    },
    'shoot_bottom': {
        'start_frame': 5,
        'end_frame': 29,  # Adjust based on actual frames
        'loop': True,
        'fps': 24
    },
    'blink': {
        'start_frame': 1,
        'end_frame': 5,  # Adjust based on actual frames
        'loop': False,
        'fps': 24
    }
}

CHOMPER_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 26,
        'loop': True,
        'fps': 12
    },
        'attack': {
        'start_frame': 27,
        'end_frame': 50,
        'loop': False,
        'fps': 12
    },
        'chewing': {
        'start_frame': 51,
        'end_frame': 68,
        'loop': True,
        'fps': 12
    },
        'chewing_to_idle': {
        'start_frame': 69,
        'end_frame': 94,
        'loop': False,
        'fps': 12
    }
}

REPEATER_ANIMATIONS = {
    'idle': {
        'start_frame': 80,
        'end_frame': 104,  # Adjust based on actual frames
        'loop': True,
        'fps': 12
    },
    'shoot': {
        'start_frame': 30,
        'end_frame': 79,  # Use shoot_top frames for timing
        'loop': False,
        'fps': 24
    },
    'shoot_top': {
        'start_frame': 30,
        'end_frame': 79,  # Adjust based on actual frames
        'loop': True,
        'fps': 24
    },
    'shoot_bottom': {
        'start_frame': 5,
        'end_frame': 29,  # Adjust based on actual frames
        'loop': True,
        'fps': 24
    },
    'blink': {
        'start_frame': 1,
        'end_frame': 5,  # Adjust based on actual frames
        'loop': False,
        'fps': 24
    }
}

PUFF_SHROOM_ANIMATIONS = {
    'blink': {
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 24
    },
    'idle': {
        'start_frame': 5,
        'end_frame': 21,
        'loop': True,
        'fps': 12
    },
    'shoot': {
        'start_frame': 22,
        'end_frame': 34,
        'loop': False,
        'fps': 24
    },
    'sleep': {
        'start_frame': 35,
        'end_frame': 51,
        'loop': True,
        'fps': 12
    },
}

SUN_SHROOM_ANIMATIONS = {
    'blink': { #small
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 24
    },
    'idle': { #small
        'start_frame': 5,
        'end_frame': 17,
        'loop': True,
        'fps': 12
    },
    'idle_big': {
        'start_frame': 5,
        'end_frame': 17,
        'loop': True,
        'fps': 24
    },
    'grow': {
        'start_frame': 28,
        'end_frame': 38,
        'loop': False,
        'fps': 24
    },
    'sleep_small': {
        'start_frame': 18,
        'end_frame': 27,
        'loop': True,
        'fps': 24
    },
    'sleep_big': {
        'start_frame': 39,
        'end_frame': 51,
        'loop': True,
        'fps': 24
    },
}

FUME_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 5,
        'end_frame': 21,
        'loop': True,
        'fps': 12
    },
    'sleep': {
        'start_frame': 51,
        'end_frame': 68,
        'loop': True,
        'fps': 12
    }
}

GRAVE_BUSTER_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 39,
        'loop': True,
        'fps': 24
    }
}

HYPNO_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 20,
        'loop': True,
        'fps': 24
    },
    'sleep': {
        'start_frame': 21,
        'end_frame': 40,
        'loop': True,
        'fps': 24
    }
}

SCAREDY_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 6,
        'end_frame': 21,
        'loop': True,
        'fps': 24
    },
    'sleep': {
        'start_frame': 71,
        'end_frame': 86,
        'loop': True,
        'fps': 24
    }
}

ICE_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 21,
        'loop': True,
        'fps': 24
    },
    'sleep': {
        'start_frame': 22,
        'end_frame': 38,
        'loop': True,
        'fps': 24
    }
}

DOOM_SHROOM_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 24,
        'loop': True,
        'fps': 24
    },
    'sleep': {
        'start_frame': 53,
        'end_frame': 77,
        'loop': True,
        'fps': 24
    }
}

LILYPAD_ANIMATIONS = {
    'blink': {
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 24
    }
}

SQUASH_ANIMATIONS = {
    'idle': {
        'start_frame': 5,
        'end_frame': 24,
        'loop': True,
        'fps': 24
    }
}

SUN_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 13,
        'loop': True,
        'fps': 12
    }
}

COIN_SILVER_ANIMATIONS = {
    'idle': {
        'start_frame': 1,
        'end_frame': 21,
        'loop': True,
        'fps': 24
    }
}

MAIN_MENU = {
    'awake':{
        'start_frame': 1,
        'end_frame': 40,
        'loop': False,
        'fps': 24    
    }
}

# Function to get animation frames for a given action and type
def get_animation_frames(action, anim_type='zombie'):
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
    elif anim_type == 'puffshroom' and action in PUFF_SHROOM_ANIMATIONS:
        anim = PUFF_SHROOM_ANIMATIONS[action]
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
    return list(range(anim['start_frame'], anim['end_frame'] + 1))

# Example usage:
# frames = get_animation_frames('walk', 'zombie')  # Returns [46, 47, ..., 92]
# frames = get_animation_frames('idle', 'peashooter')  # Returns [1, 2, ..., 30]
