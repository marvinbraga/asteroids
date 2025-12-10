import pygame
import random
from game_object import GameObject
from bullet import Bullet
from constants import UFO_RADIUS, UFO_SPEED, UFO_SHOOT_INTERVAL, BULLET_SPEED, UFO_COLOR

class UFO(GameObject):
    def __init__(self, position: pygame.Vector2, screen_width: int):
        velocity = pygame.Vector2(UFO_SPEED if random.random() > 0.5 else -UFO_SPEED, 0)
        super().__init__(position, velocity)
        self.radius = UFO_RADIUS
        self.screen_width = screen_width
        self.last_shot_time = 0
        self.shoot_interval = UFO_SHOOT_INTERVAL

    def update(self, dt: float, screen_width: int, screen_height: int, player_pos: pygame.Vector2):
        self.position += self.velocity * dt
        # Horizontal wrap
        if self.position.x < 0:
            self.position.x = screen_width
        elif self.position.x > screen_width:
            self.position.x = 0

    def shoot(self, player_pos: pygame.Vector2):
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_shot_time >= self.shoot_interval:
            self.last_shot_time = current_time
            direction = (player_pos - self.position).normalize()
            bullet = Bullet(self.position, direction * (BULLET_SPEED * 0.7))  # Slower bullets
            return bullet
        return None

    def draw(self, screen: pygame.Surface):
        # Simple triangle shape
        points = [
            (self.position.x, self.position.y - self.radius),
            (self.position.x - self.radius, self.position.y + self.radius),
            (self.position.x + self.radius, self.position.y + self.radius)
        ]
        pygame.draw.polygon(screen, UFO_COLOR, points, 2)