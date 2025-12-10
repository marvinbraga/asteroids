import pygame
import random
import math
from game_object import GameObject
from constants import ASTEROID_SIZES, GRAY


class Asteroid(GameObject):
    def __init__(self, position: pygame.Vector2, size: str = 'large'):
        velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        velocity.scale_to_length(ASTEROID_SIZES[size]['speed'])
        super().__init__(position, velocity)
        self.size = size
        self.radius = ASTEROID_SIZES[size]['radius']
        self.rotation_speed = random.uniform(-90, 90)  # degrees per second
        self.score_value = ASTEROID_SIZES[size]['score']
        self.shape_points = self._generate_shape()

    def _generate_shape(self):
        """Generate irregular asteroid shape"""
        points = []
        num_points = random.randint(6, 12)
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            distance = self.radius * random.uniform(0.8, 1.2)
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

        pygame.draw.polygon(screen, GRAY, rotated_points, 2)

    def split(self):
        """Return smaller asteroids when destroyed"""
        if self.size == 'large':
            return [Asteroid(self.position, 'medium'), Asteroid(self.position, 'medium')]
        elif self.size == 'medium':
            return [Asteroid(self.position, 'small'), Asteroid(self.position, 'small')]
        else:
            return []