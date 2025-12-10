import pygame
from typing import TYPE_CHECKING
from constants import (
    BLACK, WHITE, UI_TITLE_X, UI_TITLE_Y, UI_START_X, UI_START_Y, UI_HIGHSCORES_X, UI_HIGHSCORES_Y,
    UI_BACK_X, UI_BACK_Y, UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y, UI_ENTER_NAME_TEXT_Y,
    UI_PAUSE_TITLE_X, UI_PAUSE_TITLE_Y, UI_RESUME_X, UI_RESUME_Y, UI_RESTART_X, UI_RESTART_Y, UI_MENU_X, UI_MENU_Y,
    UI_SCORE_X, UI_SCORE_Y, UI_LIVES_X, UI_LIVES_Y, UI_LEVEL_X, UI_LEVEL_Y
)

if TYPE_CHECKING:
    from game import Game

class GameRenderer:
    def __init__(self, game: 'Game') -> None:
        self.game = game

    def draw(self, screen: pygame.Surface) -> None:
        self.game.screen.fill(BLACK)
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

        # UI
        score_text = self.game._get_cached_text("score", f"Score: {self.game.score}", WHITE)
        lives_text = self.game._get_cached_text("lives", f"Lives: {self.game.lives}", WHITE)
        level_text = self.game._get_cached_text("level", f"Level: {self.game.level}", WHITE)
        self.game.screen.blit(score_text, (UI_SCORE_X, UI_SCORE_Y))
        self.game.screen.blit(lives_text, (UI_LIVES_X, UI_LIVES_Y))
        self.game.screen.blit(level_text, (UI_LEVEL_X, UI_LEVEL_Y))

    def draw_pause_overlay(self) -> None:
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.game.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.game.font.render("PAUSED", True, WHITE)
        resume_text = self.game.font.render("R: Resume", True, WHITE)
        restart_text = self.game.font.render("S: Restart", True, WHITE)
        menu_text = self.game.font.render("M: Main Menu", True, WHITE)

        self.game.screen.blit(pause_text, (UI_PAUSE_TITLE_X, UI_PAUSE_TITLE_Y))
        self.game.screen.blit(resume_text, (UI_RESUME_X, UI_RESUME_Y))
        self.game.screen.blit(restart_text, (UI_RESTART_X, UI_RESTART_Y))
        self.game.screen.blit(menu_text, (UI_MENU_X, UI_MENU_Y))

    def draw_menu(self) -> None:
        title = self.game.font.render("ASTEROIDS", True, WHITE)
        start = self.game.font.render("Press ENTER to Start", True, WHITE)
        highscores = self.game.font.render("Press H for High Scores", True, WHITE)
        quit_text = self.game.font.render("Press ESC to Quit", True, WHITE)

        self.game.screen.blit(title, (UI_TITLE_X, UI_TITLE_Y))
        self.game.screen.blit(start, (UI_START_X, UI_START_Y))
        self.game.screen.blit(highscores, (UI_HIGHSCORES_X, UI_HIGHSCORES_Y))
        self.game.screen.blit(quit_text, (UI_HIGHSCORES_X, UI_HIGHSCORES_Y + 50))

    def draw_highscores(self) -> None:
        title = self.game.font.render("HIGH SCORES", True, WHITE)
        self.game.screen.blit(title, (self.game.screen_width // 2 - 70, 50))
        scores = self.game.get_highscores()
        for i, entry in enumerate(scores):
            text = self.game.font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, WHITE)
            self.game.screen.blit(text, (self.game.screen_width // 2 - 100, 100 + i * 40))
        back = self.game.font.render("Press ESC to go back", True, WHITE)
        self.game.screen.blit(back, (UI_BACK_X, UI_BACK_Y))

    def draw_enter_name(self) -> None:
        prompt = self.game.font.render("Enter your name:", True, WHITE)
        name_text = self.game.font.render(self.game.input_name, True, WHITE)
        self.game.screen.blit(prompt, (UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y))
        self.game.screen.blit(name_text, (self.game.screen_width // 2 - len(self.game.input_name)*5, UI_ENTER_NAME_TEXT_Y))