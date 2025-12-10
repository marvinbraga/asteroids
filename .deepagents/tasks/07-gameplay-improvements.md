# Task 07: Implementar Melhorias em Gameplay

## Objetivo
Adicionar variedade aos asteroides, upgrades automáticos e dificuldade ajustável.

## Melhorias
- Asteroides variados (cores, tipos especiais).
- Upgrades a cada 5 níveis (vida extra).
- Menu de dificuldade.

## Passos de Implementação

### 1. Variedade em Asteroides
Modificar asteroid.py:
```python
# In __init__, add type
self.type = random.choice(['normal', 'fast', 'armored'])  # Add to constants

# Adjust speed and score based on type
if self.type == 'fast':
    self.velocity.scale_to_length(ASTEROID_SIZES[size]['speed'] * 1.5)
    self.score_value = int(ASTEROID_SIZES[size]['score'] * 1.2)
elif self.type == 'armored':
    self.hitpoints = 2  # Need 2 hits
    self.score_value = ASTEROID_SIZES[size]['score'] * 2

# In draw, vary color by type
if self.type == 'fast':
    color = (200, 200, 200)  # Lighter
elif self.type == 'armored':
    color = (100, 100, 150)  # Bluish
else:
    color = GRAY
pygame.draw.polygon(screen, color, rotated_points, 2)
```

Em game.py, check_collisions:
```python
# For armored asteroids
if hasattr(asteroid, 'hitpoints'):
    asteroid.hitpoints -= 1
    if asteroid.hitpoints > 0:
        # Don't destroy yet
        bullets_to_remove.append(bullet)
        break
    else:
        # Destroy
        asteroids_to_remove.append(asteroid)
        # ... rest
```

### 2. Upgrades Automáticos
Em game.py, após level up:
```python
if self.level % 5 == 0:
    self.lives += 1  # Extra life
    # Optional: show message
```

### 3. Dificuldade Ajustável
Adicionar dificuldade em menu:
```python
# In Game.__init__
self.difficulty = 'normal'  # 'easy', 'normal', 'hard'

# Modify constants based on difficulty
def apply_difficulty(self):
    if self.difficulty == 'easy':
        self.initial_lives = 5
        self.ufo_spawn_chance = 0.02
    elif self.difficulty == 'hard':
        self.initial_lives = 2
        self.ufo_spawn_chance = 0.08
    # etc.
```

Em menu, adicionar seleção de dificuldade:
```python
# In draw_menu
difficulty_text = self.font.render(f"Difficulty: {self.difficulty.upper()}", True, WHITE)
change_diff = self.font.render("4/5: Change Difficulty", True, WHITE)
self.screen.blit(difficulty_text, (self.screen_width // 2 - 80, self.screen_height // 2 + 100))
self.screen.blit(change_diff, (self.screen_width // 2 - 100, self.screen_height // 2 + 150))

# In key handling for menu
elif event.key == pygame.K_4:  # Cycle difficulty
    difficulties = ['easy', 'normal', 'hard']
    current_index = difficulties.index(self.difficulty)
    self.difficulty = difficulties[(current_index + 1) % len(difficulties)]
    self.apply_difficulty()
```

Salvar dificuldade em arquivo ou settings.

## Testes
- Asteroides fast se movem mais rápido, armored precisam 2 hits.
- A cada 5 níveis, ganha vida extra.
- Menu permite escolher dificuldade, afetando vidas e spawn de UFOs.

## Notas
- Balancear para não tornar muito fácil/difícil.
- Feedback visual para tipos de asteroid (cores).
- Dificuldade pode afetar mais parâmetros (velocidade, pontos).