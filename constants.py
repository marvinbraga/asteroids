# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Player
PLAYER_RADIUS = 15
PLAYER_ROTATION_SPEED = 300  # degrees per second
PLAYER_THRUST = 200  # pixels per second squared
PLAYER_MAX_SPEED = 300
PLAYER_DRAG = 0.99
PLAYER_SHOOT_COOLDOWN = 0.2

# Bullet
BULLET_RADIUS = 3
BULLET_SPEED = 400
BULLET_LIFETIME = 2.0

# Asteroid sizes
ASTEROID_SIZES = {
    'large': {'radius': 40, 'speed': 50, 'score': 20},
    'medium': {'radius': 20, 'speed': 80, 'score': 50},
    'small': {'radius': 10, 'speed': 120, 'score': 100}
}

# Game
INITIAL_LIVES = 3
INITIAL_LEVEL = 1
LEVEL_ASTEROID_INCREASE = 2
BASE_ASTEROIDS = 4
ASTEROID_SPAWN_DISTANCE = 100
SPEED_INCREASE_PER_LEVEL = 0.1

# UI
FONT_SIZE = 36

# Particles
PARTICLE_LIFETIME = 1.0
PARTICLE_COUNT_EXPLODE = 8
PARTICLE_SPEED = 200
PARTICLE_COLORS = [(255, 255, 0), (255, 165, 0), (255, 0, 0)]  # Yellow, Orange, Red

# Asteroid variations
ASTEROID_COLORS = [(128, 128, 128), (160, 160, 160), (100, 100, 100), (140, 140, 140)]

# UFO
UFO_RADIUS = 15
UFO_SPEED = 100
UFO_SHOOT_INTERVAL = 2.5
UFO_SPAWN_LEVEL = 3
UFO_SPAWN_CHANCE = 0.05
UFO_SCORE = 200
UFO_COLOR = (255, 0, 0)  # Red

# Power-ups
POWERUP_TYPES = ['shield', 'speed', 'multishot']
POWERUP_RADIUS = 10
POWERUP_DURATION = 10.0
POWERUP_SPAWN_CHANCE = 0.2
POWERUP_COLORS = {'shield': (0, 255, 255), 'speed': (255, 255, 0), 'multishot': (255, 0, 255)}

# Sounds
import pygame
import os

SOUNDS_DIR = 'assets/sounds'
SOUND_SHOOT = None
SOUND_EXPLODE = None
SOUND_THRUST = None
MUSIC_BACKGROUND = os.path.join(SOUNDS_DIR, 'background.mp3')
THRUST_CHANNEL = None
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.6

def load_sounds():
    global SOUND_SHOOT, SOUND_EXPLODE, SOUND_THRUST
    try:
        SOUND_SHOOT = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'shoot.wav')) if os.path.exists(os.path.join(SOUNDS_DIR, 'shoot.wav')) else None
        SOUND_EXPLODE = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'explode.wav')) if os.path.exists(os.path.join(SOUNDS_DIR, 'explode.wav')) else None
        SOUND_THRUST = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'thrust.wav')) if os.path.exists(os.path.join(SOUNDS_DIR, 'thrust.wav')) else None
        if SOUND_SHOOT:
            SOUND_SHOOT.set_volume(SFX_VOLUME)
        if SOUND_EXPLODE:
            SOUND_EXPLODE.set_volume(SFX_VOLUME)
        if SOUND_THRUST:
            SOUND_THRUST.set_volume(SFX_VOLUME)
    except Exception as e:
        print(f"Warning: Could not load sounds: {e}")
        SOUND_SHOOT = SOUND_EXPLODE = SOUND_THRUST = None

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