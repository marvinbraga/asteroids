import pygame
from game_object import GameObject
from constants import BULLET_RADIUS, BULLET_LIFETIME, WHITE


class Bullet(GameObject):
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__(position, velocity)
        self.radius = BULLET_RADIUS
        self.lifetime = BULLET_LIFETIME
        self.age = 0

    def update(self, dt: float, screen_width: int, screen_height: int):
        self.age += dt
        if self.age >= self.lifetime:
            self.active = False
            return

        self.position += self.velocity * dt
        self.wrap_position(screen_width, screen_height)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), self.radius)