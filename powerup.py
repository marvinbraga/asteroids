import pygame
from game_object import GameObject
from constants import POWERUP_RADIUS, POWERUP_COLORS, POWERUP_DURATION


class PowerUp(GameObject):
    def __init__(self, position: pygame.Vector2, type_: str):
        super().__init__(position)
        self.type = type_
        self.radius = POWERUP_RADIUS
        self.color = POWERUP_COLORS[type_]
        self.spawn_time = pygame.time.get_ticks() / 1000.0

    def update(self, dt: float, screen_width: int, screen_height: int):
        current_time = pygame.time.get_ticks() / 1000.0
        self.lifetime = POWERUP_DURATION - (current_time - self.spawn_time)
        if self.lifetime <= 0:
            self.active = False
        self.wrap_position(screen_width, screen_height)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)