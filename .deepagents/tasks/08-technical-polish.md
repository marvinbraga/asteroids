# Task 08: Implementar Polimento Técnico

## Objetivo
Melhorar performance e organização do código usando Groups, refatoração e otimização.

## Melhorias
- Usar pygame.sprite.Group para entidades.
- Refatorar Game em métodos menores.
- Otimizar updates e draws.

## Passos de Implementação

### 1. Migrar para Groups
Em game.py:
```python
# In __init__
self.player_group = pygame.sprite.GroupSingle(self.player)
self.asteroid_group = pygame.sprite.Group()
self.bullet_group = pygame.sprite.Group()
self.ufo_group = pygame.sprite.Group()
self.powerup_group = pygame.sprite.Group()
self.particle_group = pygame.sprite.Group()

# Populate groups
for asteroid in self.asteroids:
    self.asteroid_group.add(asteroid)
# Similarly for others

# In reset_game
self.player_group.empty()
self.player_group.add(Player(...))
self.asteroid_group.empty()
# etc.

# In update
self.player_group.update(dt, keys, self.screen_width, self.screen_height)
self.asteroid_group.update(dt, self.screen_width, self.screen_height)
self.bullet_group.update(dt, self.screen_width, self.screen_height)
# etc.

# In draw
self.player_group.draw(self.screen)
self.asteroid_group.draw(self.screen)
# etc.
```

### 2. Refatorar Game.update
Quebrar em métodos:
```python
def update(self, dt):
    self.update_input(dt)
    self.update_entities(dt)
    self.check_collisions()
    self.check_level_complete()

def update_input(self, dt):
    # Handle shooting, etc.

def update_entities(self, dt):
    # Update all groups

def check_collisions(self):
    # Separate into sub-methods: bullet_asteroid, player_asteroid, etc.
```

### 3. Otimizações
- Usar spritecollide para colisões:
```python
# Example for bullet-asteroid
hits = pygame.sprite.groupcollide(self.bullet_group, self.asteroid_group, True, False)
for bullet, asteroids in hits.items():
    for asteroid in asteroids:
        # Handle destruction
```

- Lazy loading de assets: Carregar sons/imagens só quando necessário.
- Limitar particles: Manter max 100 particles ativas.

### 4. Profiling
Usar cProfile para identificar gargalos:
```python
import cProfile
pr = cProfile.Profile()
pr.enable()
# Run game loop
pr.disable()
pr.print_stats(sort='time')
```

Otimizar loops aninhados, reduzir cálculos por frame.

## Testes
- Performance igual ou melhor com Groups.
- Código mais legível e modular.
- Jogo roda sem lag mesmo com muitas entidades.

## Notas
- Groups facilitam colisões e drawing.
- Refatoração torna manutenção mais fácil.
- Continuar profiling após mudanças.