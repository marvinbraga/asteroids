# Task 06: Implementar Menu Inicial e Pausa

## Objetivo
Adicionar menu inicial com opções e funcionalidade de pausa durante o jogo.

## Funcionalidades
- Menu inicial: Start, High Scores, Quit.
- Pausa: Resume, Restart, Quit to Menu.

## Passos de Implementação

### 1. Adicionar Estados
Em game.py __init__:
```python
self.state = 'menu'  # 'menu', 'playing', 'paused', 'highscores', 'enter_name'
```

### 2. Modificar Run Loop
Em run():
```python
while running:
    dt = self.clock.tick(self.fps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if self.state == 'menu':
                if event.key == pygame.K_1 or event.key == pygame.K_RETURN:  # Start
                    self.state = 'playing'
                    self.reset_game()
                elif event.key == pygame.K_2 or event.key == pygame.K_h:  # High Scores
                    self.state = 'highscores'
                elif event.key == pygame.K_3 or event.key == pygame.K_q:  # Quit
                    running = False
            elif self.state == 'playing':
                if event.key == pygame.K_p:  # Pause
                    self.state = 'paused'
            elif self.state == 'paused':
                if event.key == pygame.K_r:  # Resume
                    self.state = 'playing'
                elif event.key == pygame.K_s:  # Restart
                    self.state = 'playing'
                    self.reset_game()
                elif event.key == pygame.K_m:  # Menu
                    self.state = 'menu'
            elif self.state == 'highscores':
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
            # enter_name handled separately

    if self.state == 'playing' and not self.game_over:
        self.update(dt)

    self.draw()
```

### 3. Modificar Draw
Separar draw por estado:
```python
def draw(self):
    self.screen.fill(BLACK)

    if self.state == 'playing':
        self.draw_game()
    elif self.state == 'paused':
        self.draw_game()  # Draw game underneath
        self.draw_pause_overlay()
    elif self.state == 'menu':
        self.draw_menu()
    elif self.state == 'highscores':
        self.draw_highscores()
    elif self.state == 'enter_name':
        self.draw_enter_name()

    pygame.display.flip()

def draw_game(self):
    # Existing game draw code
    self.player.draw(self.screen)
    for bullet in self.bullets:
        bullet.draw(self.screen)
    for asteroid in self.asteroids:
        asteroid.draw(self.screen)
    for ufo in self.ufos:
        ufo.draw(self.screen)
    # UI
    score_text = self.font.render(f"Score: {self.score}", True, WHITE)
    lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
    level_text = self.font.render(f"Level: {self.level}", True, WHITE)
    self.screen.blit(score_text, (10, 10))
    self.screen.blit(lives_text, (10, 50))
    self.screen.blit(level_text, (10, 90))

    if self.game_over:
        game_over_text = self.font.render("GAME OVER", True, RED)
        self.screen.blit(game_over_text, (self.screen_width // 2 - 100, self.screen_height // 2))

def draw_pause_overlay(self):
    # Semi-transparent overlay
    overlay = pygame.Surface((self.screen_width, self.screen_height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    self.screen.blit(overlay, (0, 0))

    # Pause text
    pause_text = self.font.render("PAUSED", True, WHITE)
    resume_text = self.font.render("R: Resume", True, WHITE)
    restart_text = self.font.render("S: Restart", True, WHITE)
    menu_text = self.font.render("M: Main Menu", True, WHITE)

    self.screen.blit(pause_text, (self.screen_width // 2 - 50, self.screen_height // 2 - 100))
    self.screen.blit(resume_text, (self.screen_width // 2 - 60, self.screen_height // 2 - 50))
    self.screen.blit(restart_text, (self.screen_width // 2 - 60, self.screen_height // 2))
    self.screen.blit(menu_text, (self.screen_width // 2 - 70, self.screen_height // 2 + 50))

def draw_menu(self):
    title = self.font.render("ASTEROIDS", True, WHITE)
    start = self.font.render("1/ENTER: Start Game", True, WHITE)
    highscores = self.font.render("2/H: High Scores", True, WHITE)
    quit = self.font.render("3/Q: Quit", True, WHITE)

    self.screen.blit(title, (self.screen_width // 2 - 50, self.screen_height // 2 - 150))
    self.screen.blit(start, (self.screen_width // 2 - 100, self.screen_height // 2 - 50))
    self.screen.blit(highscores, (self.screen_width // 2 - 110, self.screen_height // 2))
    self.screen.blit(quit, (self.screen_width // 2 - 60, self.screen_height // 2 + 50))

def draw_highscores(self):
    # From highscores task
    title = self.font.render("HIGH SCORES", True, WHITE)
    self.screen.blit(title, (self.screen_width // 2 - 70, 50))
    scores = get_highscores()
    for i, entry in enumerate(scores):
        text = self.font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, WHITE)
        self.screen.blit(text, (self.screen_width // 2 - 100, 100 + i * 40))
    back = self.font.render("ESC: Back to Menu", True, WHITE)
    self.screen.blit(back, (self.screen_width // 2 - 100, self.screen_height - 50))

def draw_enter_name(self):
    # From highscores task
    prompt = self.font.render("Enter your name:", True, WHITE)
    name_text = self.font.render(self.input_name, True, WHITE)
    self.screen.blit(prompt, (self.screen_width // 2 - 80, self.screen_height // 2 - 50))
    self.screen.blit(name_text, (self.screen_width // 2 - len(self.input_name)*5, self.screen_height // 2))
```

### 4. Ajustar Game Over
Em update ou check, quando game_over:
```python
if self.game_over and self.state == 'playing':
    if is_highscore(self.score):
        self.state = 'enter_name'
    # Else stay in playing for now, or set to game_over state
```

### 5. Pausar Música/Sons
Integrar com sons task: pausar música em pausa.

## Testes
- Menu inicial aparece primeiro.
- Opções funcionam: start inicia jogo, high scores mostra lista.
- Durante jogo, P pausa e mostra overlay com opções.
- Navegação funciona corretamente.

## Notas
- Usar números ou letras para seleção no menu.
- Overlay semi-transparente para pausa.
- Estados facilitam expansão futura.