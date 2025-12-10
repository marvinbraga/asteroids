import pygame
from abc import ABC, abstractmethod
from typing import Protocol


class Drawable(Protocol):
    def draw(self, screen: pygame.Surface) -> None: ...


class Updatable(Protocol):
    def update(self, dt: float, screen_width: int, screen_height: int) -> None: ...


class GameObject(pygame.sprite.Sprite, ABC, Drawable, Updatable):
    """Base class for all game entities with position, velocity, and collision."""

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2 = None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.position: pygame.Vector2 = position
        self.velocity: pygame.Vector2 = velocity or pygame.Vector2(0, 0)
        self.rotation: float = 0.0
        self.radius: float = 0.0  # For collision detection
        self.active: bool = True  # To mark for removal
        # Set rect for sprite collision
        self.rect = pygame.Rect(position.x - self.radius, position.y - self.radius, self.radius * 2, self.radius * 2)
        # Sprite needs image, but we'll draw manually
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

    @abstractmethod
    def update(self, dt: float, screen_width: int, screen_height: int) -> None:
        """Update object state based on delta time and screen bounds."""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Render the object to the screen."""
        pass

    def wrap_position(self, screen_width: int, screen_height: int) -> None:
        """Wrap position around screen edges for seamless movement."""
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