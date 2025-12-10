import pygame
import random
import math
from game_object import GameObject
from constants import ASTEROID_SIZES, GRAY, ASTEROID_COLORS

ASTEROID_MIN_POINTS = 5
ASTEROID_MAX_POINTS = 14
ASTEROID_RADIUS_VARIANCE = (0.8, 1.2)


class Asteroid(GameObject):
    """Asteroid entity with irregular shape, size-based scoring, and splitting behavior.

    Supports different sizes (large, medium, small) and types (normal, fast, armored).
    When destroyed, splits into smaller asteroids. Has random rotation and shape.
    """
    def __init__(self, position: pygame.Vector2, size: str = 'large'):
        velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        velocity.scale_to_length(ASTEROID_SIZES[size]['speed'])
        super().__init__(position, velocity)
        self.size = size
        self.radius = ASTEROID_SIZES[size]['radius']
        self.rotation_speed = random.uniform(-90, 90)  # degrees per second
        self.score_value = ASTEROID_SIZES[size]['score']
        self.type = random.choice(['normal', 'fast', 'armored'])
        # Adjust based on type
        if self.type == 'fast':
            self.velocity.scale_to_length(ASTEROID_SIZES[size]['speed'] * 1.5)
            self.score_value = int(ASTEROID_SIZES[size]['score'] * 1.2)
        elif self.type == 'armored':
            self.hitpoints = 2
            self.score_value = ASTEROID_SIZES[size]['score'] * 2
        else:
            self.hitpoints = 1  # normal
        self.shape_points = self._generate_shape()
        self.color = random.choice(ASTEROID_COLORS)

    def _generate_shape(self) -> list[pygame.Vector2]:
        """Generate irregular asteroid shape"""
        points = []
        num_points = random.randint(ASTEROID_MIN_POINTS, ASTEROID_MAX_POINTS)
        min_radius, max_radius = ASTEROID_RADIUS_VARIANCE
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            distance = self.radius * random.uniform(min_radius, max_radius)
            points.append(pygame.Vector2(math.cos(angle) * distance, math.sin(angle) * distance))
        return points

    def update(self, dt: float, screen_width: int, screen_height: int):
        self.rotation += self.rotation_speed * dt
        self.position += self.velocity * dt
        self.wrap_position(screen_width, screen_height)

    def draw(self, screen: pygame.Surface):
        # Rotate shape points
        rotated_points = []
        for point in self.shape_points:
            rotated = point.rotate(self.rotation)
            rotated_points.append((self.position.x + rotated.x, self.position.y + rotated.y))

        pygame.draw.polygon(screen, self.color, rotated_points, 2)

    def split(self):
        """Return smaller asteroids when destroyed"""
        if self.size == 'large':
            return [Asteroid(self.position, 'medium'), Asteroid(self.position, 'medium')]
        elif self.size == 'medium':
            return [Asteroid(self.position, 'small'), Asteroid(self.position, 'small')]
        else:
            return []