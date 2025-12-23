import pygame
from game_object import GameObject
from constants import POWERUP_RADIUS, POWERUP_COLORS, POWERUP_DURATION, WHITE


class PowerUp(GameObject):
    def __init__(self, position: pygame.Vector2, type_: str):
        super().__init__(position)
        self.type = type_
        self.radius = POWERUP_RADIUS
        self.color = POWERUP_COLORS[type_]
        self.spawn_time = pygame.time.get_ticks() / 1000.0
        self.font = pygame.font.SysFont("arial", 12, bold=True)

    def update(self, dt: float, screen_width: int, screen_height: int):
        current_time = pygame.time.get_ticks() / 1000.0
        self.lifetime = POWERUP_DURATION - (current_time - self.spawn_time)
        if self.lifetime <= 0:
            self.active = False
        self.wrap_position(screen_width, screen_height)

    def draw(self, screen: pygame.Surface):
        glow_radius = int(self.radius * 2)
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        center = (glow_radius, glow_radius)

        # Glow
        pygame.draw.circle(glow_surf, (*self.color, 100), center, int(self.radius * 1.5))
        # Core
        pygame.draw.circle(glow_surf, self.color, center, self.radius, 2)
        
        # Text
        letter = self.type[0].upper()
        text = self.font.render(letter, True, WHITE)
        text_rect = text.get_rect(center=center)
        glow_surf.blit(text, text_rect)

        screen.blit(glow_surf, (self.position.x - glow_radius, self.position.y - glow_radius))