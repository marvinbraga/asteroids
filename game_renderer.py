import pygame
import math
from typing import TYPE_CHECKING
from constants import (
    BLACK, WHITE, NEON_CYAN, NEON_MAGENTA, NEON_YELLOW, NEON_GREEN, NEON_ORANGE,
    UI_TITLE_X, UI_TITLE_Y, UI_START_X, UI_START_Y, UI_HIGHSCORES_X, UI_HIGHSCORES_Y,
    UI_BACK_X, UI_BACK_Y, UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y, UI_ENTER_NAME_TEXT_Y,
    UI_PAUSE_TITLE_X, UI_PAUSE_TITLE_Y, UI_RESUME_X, UI_RESUME_Y, UI_RESTART_X, UI_RESTART_Y, UI_MENU_X, UI_MENU_Y,
    UI_SCORE_X, UI_SCORE_Y, UI_LIVES_X, UI_LIVES_Y, UI_LEVEL_X, UI_LEVEL_Y
)

if TYPE_CHECKING:
    from game import Game

class GameRenderer:
    def __init__(self, game: 'Game') -> None:
        self.game = game
        self.stars = self._generate_stars()
        # Initialize custom fonts
        self.font_large = pygame.font.SysFont("consolas", 80, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 24)

    def _generate_stars(self) -> list[tuple[int, int, int, int]]:
        """Generate a static starfield."""
        import random
        stars = []
        for _ in range(100):
            x = random.randint(0, self.game.screen_width)
            y = random.randint(0, self.game.screen_height)
            size = random.randint(1, 2)
            brightness = random.randint(100, 255)
            stars.append((x, y, size, brightness))
        return stars

    def draw_text_neon(self, text: str, font: pygame.font.Font, color: tuple, pos: tuple, center: bool = False, pulse: bool = False) -> None:
        """Draw text with a neon glow effect."""
        # Calculate alpha for pulse
        alpha = 255
        if pulse:
            current_time = pygame.time.get_ticks()
            alpha = int(abs(math.sin(current_time / 500.0)) * 255)
            if alpha < 50: alpha = 50 # Minimum visibility

        # Render Glow
        glow_surf = font.render(text, True, color)
        if pulse:
            glow_surf.set_alpha(alpha)
        
        # Determine position
        rect = glow_surf.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos

        # Draw slight offsets for thickness/glow
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            self.game.screen.blit(glow_surf, (rect.x + dx, rect.y + dy))

        # Core (White)
        core_surf = font.render(text, True, WHITE)
        if pulse:
            core_surf.set_alpha(alpha)
        self.game.screen.blit(core_surf, rect)

    def draw_lives_icons(self, x: int, y: int, lives: int) -> None:
        """Draw miniature player ships to represent lives."""
        icon_scale = 0.6
        spacing = 25
        for i in range(lives):
            # Draw a mini triangle
            pos_x = x + (i * spacing)
            points = [
                (pos_x, y - 10 * icon_scale),
                (pos_x - 7 * icon_scale, y + 7 * icon_scale),
                (pos_x + 7 * icon_scale, y + 7 * icon_scale)
            ]
            pygame.draw.polygon(self.game.screen, NEON_CYAN, points, 2)

    def draw_hud(self) -> None:
        """Draw the in-game Heads-Up Display."""
        # HUD Background Bar (Semi-transparent)
        hud_height = 40
        bar = pygame.Surface((self.game.screen_width, hud_height), pygame.SRCALPHA)
        bar.fill((0, 0, 10, 200)) # Dark transparent blue
        self.game.screen.blit(bar, (0, 0))
        
        # Neon Line Separator
        pygame.draw.line(self.game.screen, NEON_CYAN, (0, hud_height), (self.game.screen_width, hud_height), 2)

        # Score (Left)
        score_str = f"SCORE: {self.game.score:05d}" # Zero padded
        self.draw_text_neon(score_str, self.font_small, NEON_GREEN, (20, 10))

        # Level (Center)
        level_str = f"LEVEL {self.game.level}"
        self.draw_text_neon(level_str, self.font_small, NEON_YELLOW, (self.game.screen_width // 2, 20), center=True)

        # Lives (Right) - Use Icons
        # self.draw_text_neon(f"LIVES", self.font_small, NEON_MAGENTA, (self.game.screen_width - 150, 10))
        self.draw_lives_icons(self.game.screen_width - 100, 25, self.game.lives)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.screen.fill(BLACK)
        
        # Draw Stars
        for x, y, size, brightness in self.stars:
            s = pygame.Surface((size, size))
            s.fill((brightness, brightness, brightness))
            s.set_alpha(brightness)
            self.game.screen.blit(s, (x, y))

        self.game.current_state.draw(screen)
        pygame.display.flip()

    def draw_game(self) -> None:
        # Draw all game entities in correct order (player last for layering)
        for asteroid in self.game.asteroids:
            asteroid.draw(self.game.screen)
        for bullet in self.game.bullets:
            bullet.draw(self.game.screen)
        for powerup in self.game.powerups:
            powerup.draw(self.game.screen)
        for ufo in self.game.ufos:
            ufo.draw(self.game.screen)
        for ufo_bullet in self.game.ufo_bullets:
            ufo_bullet.draw(self.game.screen)
        for particle in self.game.explosion_particles:
            particle.draw(self.game.screen)
        self.game.player.draw(self.game.screen)  # Player on top

        # UI / HUD
        self.draw_hud()

    def draw_pause_overlay(self) -> None:
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200) # Darker pause
        self.game.screen.blit(overlay, (0, 0))

        # Frame
        pygame.draw.rect(self.game.screen, NEON_CYAN, (100, 100, self.game.screen_width-200, self.game.screen_height-200), 2)

        center_x = self.game.screen_width // 2
        
        self.draw_text_neon("SYSTEM PAUSED", self.font_medium, NEON_CYAN, (center_x, 150), center=True)
        
        self.draw_text_neon("RESUME MISSION [R]", self.font_small, WHITE, (center_x, 300), center=True)
        self.draw_text_neon("RESTART SYSTEM [S]", self.font_small, WHITE, (center_x, 350), center=True)
        self.draw_text_neon("ABORT TO MENU  [M]", self.font_small, NEON_ORANGE, (center_x, 400), center=True)

    def draw_menu(self) -> None:
        center_x = self.game.screen_width // 2
        center_y = self.game.screen_height // 2

        # Title
        self.draw_text_neon("ASTEROIDS", self.font_large, NEON_CYAN, (center_x, center_y - 100), center=True)
        self.draw_text_neon("NEON EDITION", self.font_small, NEON_MAGENTA, (center_x, center_y - 40), center=True)

        # Pulsing Start Text
        self.draw_text_neon("PRESS [ENTER] TO START", self.font_medium, NEON_GREEN, (center_x, center_y + 50), center=True, pulse=True)
        
        # Options
        self.draw_text_neon("HIGH SCORES [H]", self.font_small, WHITE, (center_x, center_y + 120), center=True)
        self.draw_text_neon("QUIT SYSTEM [ESC]", self.font_small, NEON_ORANGE, (center_x, center_y + 160), center=True)

    def draw_highscores(self) -> None:
        center_x = self.game.screen_width // 2
        self.draw_text_neon("TOP PILOTS", self.font_medium, NEON_YELLOW, (center_x, 50), center=True)
        
        scores = self.game.get_highscores()
        for i, entry in enumerate(scores):
            color = NEON_CYAN if i == 0 else WHITE
            text = f"{i+1}. {entry['name']} ... {entry['score']}"
            self.draw_text_neon(text, self.font_small, color, (center_x, 120 + i * 40), center=True)
            
        self.draw_text_neon("BACK [ESC]", self.font_small, NEON_ORANGE, (center_x, self.game.screen_height - 50), center=True)

    def draw_enter_name(self) -> None:
        center_x = self.game.screen_width // 2
        center_y = self.game.screen_height // 2
        
        self.draw_text_neon("NEW HIGH SCORE!", self.font_medium, NEON_YELLOW, (center_x, center_y - 80), center=True)
        self.draw_text_neon("ENTER PILOT ID:", self.font_small, WHITE, (center_x, center_y - 20), center=True)
        
        # Name with blinking cursor effect (simulated by pulse or just color)
        name_display = self.game.input_name + "_"
        self.draw_text_neon(name_display, self.font_medium, NEON_CYAN, (center_x, center_y + 30), center=True)