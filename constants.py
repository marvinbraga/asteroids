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