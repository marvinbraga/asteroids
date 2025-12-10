import pygame
from constants import WHITE, RED, FONT_SIZE, UI_TITLE_X, UI_TITLE_Y, UI_START_X, UI_START_Y, UI_HIGHSCORES_X, UI_HIGHSCORES_Y, UI_BACK_X, UI_BACK_Y, UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y, UI_ENTER_NAME_TEXT_Y

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_input(self, events, keys):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

class MenuState(GameState):
    def handle_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_state('playing')
                    self.game.logic.reset_game()
                elif event.key == pygame.K_h:
                    self.game.change_state('highscores')
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.game.renderer.draw_menu()

class PlayingState(GameState):
    def update(self, dt):
        # Update is handled in Game.run
        pass

    def draw(self, screen):
        self.game.renderer.draw_game()

class GameOverState(GameState):
    def handle_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.change_state('playing')
                    self.game.logic.reset_game()
                elif event.key == pygame.K_m:
                    self.game.change_state('menu')

    def draw(self, screen):
        self.game.renderer.draw_game()  # Draw game elements first
        game_over_text = self.game.font.render("GAME OVER - Press R to restart, M for menu", True, RED)
        screen.blit(game_over_text, (self.game.screen_width // 2 - 200, self.game.screen_height // 2))

class HighscoresState(GameState):
    def handle_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state('menu')

    def draw(self, screen):
        self.game.renderer.draw_highscores()

class EnterNameState(GameState):
    def handle_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.game.input_name:
                    self.game.add_highscore(self.game.input_name, self.game.score)
                    self.game.input_name = ""
                    self.game.change_state('highscores')
                elif event.key == pygame.K_BACKSPACE:
                    self.game.input_name = self.game.input_name[:-1]
                else:
                    if len(self.game.input_name) < 5:
                        self.game.input_name += event.unicode.upper()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.game.renderer.draw_game()  # Show final game state
        self.game.renderer.draw_enter_name()