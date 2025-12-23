# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (5, 5, 20)  # Deep space blue
WHITE = (220, 220, 255)  # Slightly blueish white
GRAY = (128, 128, 128)

# Neon Palette
NEON_CYAN = (0, 255, 255)
NEON_MAGENTA = (255, 0, 255)
NEON_PURPLE = (180, 0, 255)
NEON_GREEN = (50, 255, 50)
NEON_RED = (255, 50, 50)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 150, 0)
NEON_BLUE = (50, 100, 255)

# Aliases for backward compatibility or specific usage
ORANGE = NEON_ORANGE
RED = NEON_RED

# Player
PLAYER_COLOR = NEON_CYAN
PLAYER_RADIUS = 15
PLAYER_ROTATION_SPEED = 350  # More responsive turning
PLAYER_THRUST = 200  # pixels per second squared
PLAYER_MAX_SPEED = 300
PLAYER_DRAG = 0.96  # More friction (easier to stop)
PLAYER_SHOOT_COOLDOWN = 0.15  # Faster shooting

# Bullet
BULLET_COLOR = NEON_YELLOW
BULLET_RADIUS = 3
BULLET_SPEED = 400
BULLET_LIFETIME = 2.0

# Asteroid sizes
ASTEROID_SIZES = {
    'large': {'radius': 40, 'speed': 30, 'score': 20},
    'medium': {'radius': 20, 'speed': 40, 'score': 50},
    'small': {'radius': 10, 'speed': 50, 'score': 100}
}

# Game
INITIAL_LIVES = 3
INITIAL_LEVEL = 1
LEVEL_ASTEROID_INCREASE = 2
BASE_ASTEROIDS = 3  # Start with fewer asteroids
ASTEROID_SPAWN_DISTANCE = 100
SPEED_INCREASE_PER_LEVEL = 0.05
SPEED_INCREASE_PER_LEVEL = 0.05

# UI
FONT_SIZE = 36

# Particles
PARTICLE_LIFETIME = 1.0
PARTICLE_COUNT_EXPLODE = 12
PARTICLE_SPEED = 200
PARTICLE_COLORS = [NEON_ORANGE, NEON_RED, NEON_YELLOW, WHITE]

# Asteroid variations
ASTEROID_COLORS = [NEON_MAGENTA, NEON_PURPLE, (200, 50, 200)]

# UFO
UFO_RADIUS = 15
UFO_SPEED = 100
UFO_SHOOT_INTERVAL = 2.5
UFO_SPAWN_LEVEL = 3
UFO_SPAWN_CHANCE = 0.05
UFO_SCORE = 200
UFO_COLOR = NEON_RED

# Power-ups
POWERUP_TYPES = ['shield', 'speed', 'multishot']
POWERUP_RADIUS = 10
POWERUP_DURATION = 10.0
POWERUP_SPAWN_CHANCE = 0.2
POWERUP_COLORS = {'shield': NEON_BLUE, 'speed': NEON_GREEN, 'multishot': NEON_ORANGE}

# Player mechanics
PARTICLE_FREQUENCY = 0.5  # Chance per frame to spawn thrust particle
MULTISHOT_ANGLE = 15  # Degrees for side bullets
SPEED_BOOST_MULTIPLIER = 1.5  # Multiplier for speed power-up

# Sounds
import pygame
import os
from typing import Optional

SOUNDS_DIR = 'assets/sounds'
SOUND_SHOOT = None
SOUND_EXPLODE = None
SOUND_THRUST = None
MUSIC_BACKGROUND = os.path.join(SOUNDS_DIR, 'background.mp3')
THRUST_CHANNEL = None
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.6

def load_sounds() -> tuple[Optional[pygame.mixer.Sound], ...]:
    sounds = []
    sound_files = ['shoot.wav', 'explode.wav', 'thrust.wav']
    for file in sound_files:
        path = os.path.join(SOUNDS_DIR, file)
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(SFX_VOLUME)
                sounds.append(sound)
            else:
                sounds.append(None)
        except pygame.error as e:
            print(f"Warning: Could not load {file}: {e}")
            sounds.append(None)
    return tuple(sounds)

# UI Positioning
UI_SCORE_X = 10
UI_SCORE_Y = 10
UI_LIVES_X = 10
UI_LIVES_Y = 50
UI_LEVEL_X = 10
UI_LEVEL_Y = 90
UI_GAME_OVER_X_OFFSET = 200
UI_GAME_OVER_Y = SCREEN_HEIGHT // 2
UI_TITLE_X = SCREEN_WIDTH // 2 - 50
UI_TITLE_Y = SCREEN_HEIGHT // 2 - 100
UI_START_X = SCREEN_WIDTH // 2 - 100
UI_START_Y = SCREEN_HEIGHT // 2 - 50
UI_HIGHSCORES_X = SCREEN_WIDTH // 2 - 120
UI_HIGHSCORES_Y = SCREEN_HEIGHT // 2
UI_BACK_X = SCREEN_WIDTH // 2 - 100
UI_BACK_Y = SCREEN_HEIGHT - 50
UI_ENTER_NAME_PROMPT_X = SCREEN_WIDTH // 2 - 80
UI_ENTER_NAME_PROMPT_Y = SCREEN_HEIGHT // 2 - 50
UI_ENTER_NAME_TEXT_Y = SCREEN_HEIGHT // 2
UI_PAUSE_TITLE_X = SCREEN_WIDTH // 2 - 50
UI_PAUSE_TITLE_Y = SCREEN_HEIGHT // 2 - 100
UI_RESUME_X = SCREEN_WIDTH // 2 - 60
UI_RESUME_Y = SCREEN_HEIGHT // 2 - 50
UI_RESTART_X = SCREEN_WIDTH // 2 - 60
UI_RESTART_Y = SCREEN_HEIGHT // 2
UI_MENU_X = SCREEN_WIDTH // 2 - 70
UI_MENU_Y = SCREEN_HEIGHT // 2 + 50

def init_channels():
    global THRUST_CHANNEL
    THRUST_CHANNEL = pygame.mixer.Channel(1)