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
                if event.key == pygame.K_RETURN or event.key == pygame.K_1:
                    self.game.change_state('playing')
                    self.game.reset_game()
                elif event.key == pygame.K_h or event.key == pygame.K_2:
                    self.game.change_state('highscores')
                elif event.key == pygame.K_q or event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title = self.game.font.render("ASTEROIDS", True, WHITE)
        start = self.game.font.render("Press ENTER to Start", True, WHITE)
        highscores = self.game.font.render("Press H for High Scores", True, WHITE)
        quit_text = self.game.font.render("Press ESC to Quit", True, WHITE)

        screen.blit(title, (UI_TITLE_X, UI_TITLE_Y))
        screen.blit(start, (UI_START_X, UI_START_Y))
        screen.blit(highscores, (UI_HIGHSCORES_X, UI_HIGHSCORES_Y))
        screen.blit(quit_text, (UI_HIGHSCORES_X, UI_HIGHSCORES_Y + 50))

class PlayingState(GameState):
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.game.update_game_logic(dt, keys)

    def draw(self, screen):
        self.game.draw_game()

class GameOverState(GameState):
    def handle_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.change_state('playing')
                    self.game.reset_game()
                elif event.key == pygame.K_m:
                    self.game.change_state('menu')

    def draw(self, screen):
        self.game.draw_game()  # Draw game elements first
        game_over_text = self.game.font.render("GAME OVER - Press R to restart, M for menu", True, RED)
        screen.blit(game_over_text, (self.game.screen_width // 2 - 200, self.game.screen_height // 2))

class HighscoresState(GameState):
    def handle_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state('menu')

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title = self.game.font.render("HIGH SCORES", True, WHITE)
        screen.blit(title, (self.game.screen_width // 2 - 70, 50))
        scores = self.game.get_highscores()
        for i, entry in enumerate(scores):
            text = self.game.font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, WHITE)
            screen.blit(text, (self.game.screen_width // 2 - 100, 100 + i * 40))
        back = self.game.font.render("Press ESC to go back", True, WHITE)
        screen.blit(back, (UI_BACK_X, UI_BACK_Y))

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
        self.game.draw_game()  # Show final game state
        prompt = self.game.font.render("Enter your name:", True, WHITE)
        name_text = self.game.font.render(self.game.input_name, True, WHITE)
        screen.blit(prompt, (UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y))
        screen.blit(name_text, (self.game.screen_width // 2 - len(self.game.input_name)*5, UI_ENTER_NAME_TEXT_Y))