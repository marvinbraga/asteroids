import pygame
import random
from game_object import GameObject
from constants import PARTICLE_LIFETIME, PARTICLE_SPEED, PARTICLE_COLORS

class Particle(GameObject):
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2 = None):
        if velocity is None:
            angle = random.uniform(0, 360)
            speed = random.uniform(50, PARTICLE_SPEED)
            velocity = pygame.Vector2(speed, 0).rotate(angle)
        super().__init__(position, velocity)
        self.lifetime = PARTICLE_LIFETIME
        self.color = random.choice(PARTICLE_COLORS)

    def update(self, dt: float, screen_width: int, screen_height: int):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
        self.position += self.velocity * dt
        # Optional: fade velocity or wrap

    def draw(self, screen: pygame.Surface):
        if self.lifetime <= 0:
            return

        size = 5  # Fixed size
        alpha = int(255 * (self.lifetime / PARTICLE_LIFETIME))

        # Create surface with alpha
        particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, (*self.color, alpha), (size, size), size)

        # Blit to screen
        screen.blit(particle_surf, self.position - pygame.Vector2(size, size))