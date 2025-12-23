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
            bullet.lifetime = 1.5 # Shorter lifetime
            # Ufo bullets should probably be a different color, but using standard for now or we can override draw in a subclass if needed.
            # Actually, standard Bullet class uses BULLET_COLOR. UFO bullet could use Red if passed or subclassed.
            # For now, yellow bullets from UFO are fine or we can change bullet color logic later.
            return bullet
        return None

    def draw(self, screen: pygame.Surface):
        # Shape points (relative to center 0,0)
        points = [
            pygame.Vector2(0, -self.radius),
            pygame.Vector2(-self.radius, self.radius),
            pygame.Vector2(self.radius, self.radius)
        ]
        
        glow_size = int(self.radius * 2.5)
        glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        center = pygame.Vector2(glow_size, glow_size)

        local_points = [p + center for p in points]

        # Draw Glow
        glow_color = (*UFO_COLOR, 100)
        pygame.draw.polygon(glow_surf, glow_color, local_points, 5)

        # Draw Core
        pygame.draw.polygon(glow_surf, UFO_COLOR, local_points, 2)

        screen.blit(glow_surf, self.position - center)