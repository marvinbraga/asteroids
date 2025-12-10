import pygame
from game_object import GameObject
from bullet import Bullet
from constants import (
    PLAYER_RADIUS, PLAYER_ROTATION_SPEED, PLAYER_THRUST, PLAYER_MAX_SPEED,
    PLAYER_DRAG, PLAYER_SHOOT_COOLDOWN, BULLET_SPEED, WHITE, ORANGE
)
import math


class Player(GameObject):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position)
        self.radius = PLAYER_RADIUS
        self.rotation_speed = PLAYER_ROTATION_SPEED
        self.thrust = PLAYER_THRUST
        self.max_speed = PLAYER_MAX_SPEED
        self.drag = PLAYER_DRAG
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.last_shot = 0
        self.thrusting = False

    def update(self, dt: float, keys, screen_width: int, screen_height: int):
        # Rotation
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation -= self.rotation_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation += self.rotation_speed * dt

        # Thrust
        self.thrusting = keys[pygame.K_UP] or keys[pygame.K_w]
        if self.thrusting:
            direction = pygame.Vector2(0, -1).rotate(self.rotation)
            self.velocity += direction * self.thrust * dt

        # Limit speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # Apply drag
        self.velocity *= self.drag

        # Update position
        self.position += self.velocity * dt
        self.wrap_position(screen_width, screen_height)

        # Update cooldown
        self.last_shot += dt

    def shoot(self):
        if self.last_shot >= self.shoot_cooldown:
            self.last_shot = 0
            direction = pygame.Vector2(0, -1).rotate(self.rotation)
            bullet_pos = self.position + direction * (self.radius + 5)
            return Bullet(bullet_pos, direction * BULLET_SPEED)
        return None

    def draw(self, screen: pygame.Surface):
        # Ship shape (triangle)
        points = [
            pygame.Vector2(0, -self.radius),
            pygame.Vector2(-self.radius * 0.7, self.radius * 0.7),
            pygame.Vector2(self.radius * 0.7, self.radius * 0.7)
        ]

        # Rotate points
        rotated_points = []
        for point in points:
            rotated = point.rotate(self.rotation)
            rotated_points.append((self.position.x + rotated.x, self.position.y + rotated.y))

        # Draw ship
        pygame.draw.polygon(screen, WHITE, rotated_points, 2)

        # Draw thrust flame
        if self.thrusting:
            flame_points = [
                pygame.Vector2(-self.radius * 0.3, self.radius * 0.7),
                pygame.Vector2(0, self.radius * 1.2),
                pygame.Vector2(self.radius * 0.3, self.radius * 0.7)
            ]
            rotated_flame = []
            for point in flame_points:
                rotated = point.rotate(self.rotation)
                rotated_flame.append((self.position.x + rotated.x, self.position.y + rotated.y))
            pygame.draw.polygon(screen, ORANGE, rotated_flame)