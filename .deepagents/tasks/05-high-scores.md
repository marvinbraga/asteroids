# Task 05: Implementar Sistema de High Scores

## Objetivo
Salvar e exibir top 10 pontuações persistentes com nomes.

## Funcionalidades
- Salvar high scores em JSON.
- Tela de leaderboard.
- Entrada de nome ao bater recorde.

## Passos de Implementação

### 1. Criar highscores.py
Módulo para gerenciar high scores:
```python
import json
import os

HIGHSCORES_FILE = 'highscores.json'

def load_highscores():
    if os.path.exists(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_highscores(scores):
    with open(HIGHSCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def add_highscore(name, score):
    scores = load_highscores()
    scores.append({'name': name, 'score': score})
    scores.sort(key=lambda x: x['score'], reverse=True)
    scores = scores[:10]  # Keep top 10
    save_highscores(scores)
    return scores

def get_highscores():
    return load_highscores()

def is_highscore(score):
    scores = get_highscores()
    if len(scores) < 10:
        return True
    return score > scores[-1]['score']
```

### 2. Adicionar Estados ao Game
Em game.py, adicionar estados:
```python
# Possible states: 'menu', 'playing', 'game_over', 'highscores', 'enter_name'
self.state = 'menu'
```

### 3. Modificar run Loop
Em run():
```python
while running:
    dt = self.clock.tick(self.fps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if self.state == 'menu':
                if event.key == pygame.K_RETURN:
                    self.state = 'playing'
                    self.reset_game()
                elif event.key == pygame.K_h:
                    self.state = 'highscores'
            elif self.state == 'highscores':
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
            elif self.state == 'game_over':
                if event.key == pygame.K_r:
                    self.state = 'playing'
                    self.reset_game()
                elif event.key == pygame.K_m:
                    self.state = 'menu'
            elif self.state == 'enter_name':
                # Handle name input (see below)

    if self.state == 'playing':
        if not self.game_over:
            self.update(dt)
        else:
            self.state = 'game_over'
    # Other states don't update

    self.draw()
```

### 4. Draw para Estados
Modificar draw():
```python
def draw(self):
    self.screen.fill(BLACK)

    if self.state == 'playing' or self.state == 'game_over':
        # Existing draw code
        self.player.draw(self.screen)
        # ... all entities
        # UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        # ...
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to restart, M for menu", True, RED)
            self.screen.blit(game_over_text, (self.screen_width // 2 - 200, self.screen_height // 2))

    elif self.state == 'menu':
        title = self.font.render("ASTEROIDS", True, WHITE)
        start = self.font.render("Press ENTER to Start", True, WHITE)
        highscores = self.font.render("Press H for High Scores", True, WHITE)
        self.screen.blit(title, (self.screen_width // 2 - 50, self.screen_height // 2 - 100))
        self.screen.blit(start, (self.screen_width // 2 - 100, self.screen_height // 2 - 50))
        self.screen.blit(highscores, (self.screen_width // 2 - 120, self.screen_height // 2))

    elif self.state == 'highscores':
        title = self.font.render("HIGH SCORES", True, WHITE)
        self.screen.blit(title, (self.screen_width // 2 - 70, 50))
        scores = get_highscores()
        for i, entry in enumerate(scores):
            text = self.font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, WHITE)
            self.screen.blit(text, (self.screen_width // 2 - 100, 100 + i * 40))
        back = self.font.render("Press ESC to go back", True, WHITE)
        self.screen.blit(back, (self.screen_width // 2 - 100, self.screen_height - 50))

    elif self.state == 'enter_name':
        prompt = self.font.render("Enter your name:", True, WHITE)
        name_text = self.font.render(self.input_name, True, WHITE)
        self.screen.blit(prompt, (self.screen_width // 2 - 80, self.screen_height // 2 - 50))
        self.screen.blit(name_text, (self.screen_width // 2 - len(self.input_name)*5, self.screen_height // 2))

    pygame.display.flip()
```

### 5. Entrada de Nome
Adicionar atributos em __init__:
```python
self.input_name = ""
```

Em run, para enter_name:
```python
elif self.state == 'enter_name':
    if event.key == pygame.K_RETURN and self.input_name:
        add_highscore(self.input_name, self.score)
        self.input_name = ""
        self.state = 'highscores'
    elif event.key == pygame.K_BACKSPACE:
        self.input_name = self.input_name[:-1]
    else:
        self.input_name += event.unicode.upper()  # Limit to uppercase
```

Modificar game_over para check highscore:
```python
if self.game_over:
    if is_highscore(self.score):
        self.state = 'enter_name'
    else:
        # Stay in game_over
```

### 6. Reset Game
Em reset_game, set state to 'playing' if called from restart.

## Testes
- Após game over, se score alto, pede nome.
- Nome salvo e aparece em high scores.
- Menu acessível, high scores mostram corretamente.
- Navegação entre estados funciona.

## Notas
- Limitar nome a 3-5 caracteres.
- High scores persistem entre sessões.
- Possível expansão: Data/hora dos scores.