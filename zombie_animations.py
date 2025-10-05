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
        'fps': 12
    },
    # Add more animations as needed, e.g., 'idle', 'hurt', etc.
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
        'fps': 12
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

LILYPAD_ANIMATIONS = {
    'blink': {
        'start_frame': 1,
        'end_frame': 4,
        'loop': False,
        'fps': 12
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

MAIN_MENU = {
    'awake':{
        'start_frame': 1,
        'end_frame': 40,
        'loop': True,
        'fps': 48      
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
    elif anim_type == 'sun' and action in SUN_ANIMATIONS:
        anim = SUN_ANIMATIONS[action]
    elif anim_type == 'main_menu' and action in MAIN_MENU:
        anim = MAIN_MENU[action]
    else:
        return []
    return list(range(anim['start_frame'], anim['end_frame'] + 1))

# Example usage:
# frames = get_animation_frames('walk', 'zombie')  # Returns [46, 47, ..., 92]
# frames = get_animation_frames('idle', 'peashooter')  # Returns [1, 2, ..., 30]
