import pygame
import random
from game_object import GameObject
from bullet import Bullet
from particle import Particle
from constants import (
    PLAYER_RADIUS, PLAYER_ROTATION_SPEED, PLAYER_THRUST, PLAYER_MAX_SPEED,
    PLAYER_DRAG, PLAYER_SHOOT_COOLDOWN, BULLET_SPEED, WHITE, ORANGE,
    SOUND_SHOOT, THRUST_CHANNEL, SOUND_THRUST
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
        self.last_shot_time = 0
        self.thrusting = False
        self.thrust_particles = pygame.sprite.Group()

        # Power-up attributes
        self.shielded = False
        self.speed_boost = 1.0
        self.multishot = False
        self.powerup_timer = 0
        self.invincible_timer = 0

    def reset_powerups(self) -> None:
        """Reset all power-up effects."""
        self.shielded = False
        self.speed_boost = 1.0
        self.multishot = False
        self.powerup_timer = 0
        self.invincible_timer = 0

    def update(self, dt: float, keys, screen_width: int, screen_height: int):
        current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds

        # Update invincibility timer
        self.invincible_timer = max(0, self.invincible_timer - dt)

        # Track thrusting state
        was_thrusting = self.thrusting

        # Rotation
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation -= self.rotation_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation += self.rotation_speed * dt

        # Thrust
        self.thrusting = keys[pygame.K_UP] or keys[pygame.K_w]

        if self.thrusting and not was_thrusting:
            if THRUST_CHANNEL:
                THRUST_CHANNEL.play(SOUND_THRUST, loops=-1)
        elif not self.thrusting and was_thrusting:
            if THRUST_CHANNEL:
                THRUST_CHANNEL.stop()
        if self.thrusting:
            direction = pygame.Vector2(0, -1).rotate(self.rotation)
            effective_thrust = self.thrust * self.speed_boost
            self.velocity += direction * effective_thrust * dt

        # Limit speed
        effective_max_speed = self.max_speed * self.speed_boost
        if self.velocity.length() > effective_max_speed:
            self.velocity.scale_to_length(effective_max_speed)

        # Apply drag
        self.velocity *= self.drag

        # Update position
        self.position += self.velocity * dt
        self.wrap_position(screen_width, screen_height)

        # Update power-up timer
        if self.powerup_timer > 0:
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:
                self.reset_powerups()

        # Spawn thrust particles
        if self.thrusting:
            if random.random() < 0.5:  # Adjust frequency
                direction = pygame.Vector2(0, 1).rotate(self.rotation)  # Backwards
                particle_pos = self.position + direction * (self.radius + 5)
                particle_vel = direction * random.uniform(100, 200) + self.velocity * 0.5
                particle = Particle(particle_pos, particle_vel)
                self.thrust_particles.add(particle)

        # Update particles
        self.thrust_particles.update(dt, screen_width, screen_height)

    def shoot(self):
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time
            if SOUND_SHOOT:
                SOUND_SHOOT.play()
            direction = pygame.Vector2(0, -1).rotate(self.rotation)
            bullet_pos = self.position + direction * (self.radius + 5)
            bullets = [Bullet(bullet_pos, direction * BULLET_SPEED)]
            if self.multishot:
                # Add side bullets
                side_angle = 15  # degrees
                left_dir = direction.rotate(-side_angle)
                right_dir = direction.rotate(side_angle)
                bullets.append(Bullet(bullet_pos, left_dir * BULLET_SPEED))
                bullets.append(Bullet(bullet_pos, right_dir * BULLET_SPEED))
            return bullets
        return []

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

        # Draw thrust particles
        self.thrust_particles.draw(screen)

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