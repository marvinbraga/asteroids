import pygame
from abc import ABC, abstractmethod


class GameObject(pygame.sprite.Sprite, ABC):
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2 = None):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.velocity = velocity or pygame.Vector2(0, 0)
        self.rotation = 0.0
        self.radius = 0.0  # For collision detection
        self.active = True  # To mark for removal
        # Set rect for sprite collision
        self.rect = pygame.Rect(position.x - self.radius, position.y - self.radius, self.radius * 2, self.radius * 2)
        # Sprite needs image, but we'll draw manually
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

    @abstractmethod
    def update(self, dt: float):
        """Update object state"""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """Draw the object"""
        pass

    def wrap_position(self, screen_width: int, screen_height: int):
        """Wrap position around screen edges"""
        if self.position.x < 0:
            self.position.x = screen_width
        elif self.position.x > screen_width:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = screen_height
        elif self.position.y > screen_height:
            self.position.y = 0

        # Update rect
        self.rect.center = (self.position.x, self.position.y)