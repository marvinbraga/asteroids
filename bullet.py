import pygame
from game_object import GameObject
from constants import BULLET_RADIUS, BULLET_LIFETIME, BULLET_COLOR


class Bullet(GameObject):
    """Projectile fired by player or UFO with limited lifetime.

    Moves in a straight line with constant velocity. Automatically deactivates
    after lifetime expires or wraps around screen edges.
    """
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
        # Create glow surface
        glow_radius = int(self.radius * 3)
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        center = (glow_radius, glow_radius)

        # Draw Glow
        pygame.draw.circle(glow_surf, (*BULLET_COLOR, 100), center, int(self.radius * 2))
        
        # Draw Core
        pygame.draw.circle(glow_surf, BULLET_COLOR, center, self.radius)
        
        # Blit
        screen.blit(glow_surf, (self.position.x - glow_radius, self.position.y - glow_radius))