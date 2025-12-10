# Task 02: Implementar Inimigos Adicionais (UFOs)

## Objetivo
Adicionar UFOs como inimigos que se movem horizontalmente, atiram projéteis e aumentam o desafio a partir do nível 3.

## Comportamento dos UFOs
- Movimento horizontal constante, wrap vertical.
- Tiro periódico em direção aproximada do jogador.
- Pontuação: 200 pontos.
- Aparecem a partir do nível 3, com chance baixa.

## Passos de Implementação

### 1. Atualizar constants.py
Adicionar constantes para UFOs:
```python
# UFO
UFO_RADIUS = 15
UFO_SPEED = 100
UFO_SHOOT_INTERVAL = 2.5
UFO_SPAWN_LEVEL = 3
UFO_SPAWN_CHANCE = 0.05
UFO_SCORE = 200
UFO_COLOR = (255, 0, 0)  # Red
```

### 2. Criar ufo.py
Nova classe UFO herdando de GameObject:
```python
import pygame
import random
from game_object import GameObject
from bullet import Bullet
from constants import UFO_RADIUS, UFO_SPEED, UFO_SHOOT_INTERVAL, BULLET_SPEED, UFO_COLOR

class UFO(GameObject):
    def __init__(self, position: pygame.Vector2, screen_width: int):
        velocity = pygame.Vector2(UFO_SPEED if random.random() > 0.5 else -UFO_SPEED, 0)
        super().__init__(position, velocity)
        self.radius = UFO_RADIUS
        self.screen_width = screen_width
        self.last_shot = 0
        self.shoot_interval = UFO_SHOOT_INTERVAL

    def update(self, dt: float, screen_width: int, screen_height: int, player_pos: pygame.Vector2):
        self.last_shot += dt
        self.position += self.velocity * dt
        # Horizontal wrap
        if self.position.x < 0:
            self.position.x = screen_width
        elif self.position.x > screen_width:
            self.position.x = 0

    def shoot(self, player_pos: pygame.Vector2):
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            direction = (player_pos - self.position).normalize()
            bullet = Bullet(self.position, direction * (BULLET_SPEED * 0.7))  # Slower bullets
            return bullet
        return None

    def draw(self, screen: pygame.Surface):
        # Simple triangle shape
        points = [
            (self.position.x, self.position.y - self.radius),
            (self.position.x - self.radius, self.position.y + self.radius),
            (self.position.x + self.radius, self.position.y + self.radius)
        ]
        pygame.draw.polygon(screen, UFO_COLOR, points, 2)
```

### 3. Modificar game.py
Adicionar lista de UFOs e bullets deles:
```python
# In Game.__init__
self.ufos = []
self.ufo_bullets = []
```

Spawn UFOs em update:
```python
# In update, before check_collisions
if self.level >= UFO_SPAWN_LEVEL and len(self.ufos) < 2 and random.random() < UFO_SPAWN_CHANCE:
    # Spawn at top or bottom
    y = 0 if random.random() > 0.5 else self.screen_height
    x = random.randint(0, self.screen_width)
    ufo = UFO(pygame.Vector2(x, y), self.screen_width)
    self.ufos.append(ufo)
```

Update UFOs:
```python
# In update, after asteroids
for ufo in self.ufos:
    ufo.update(dt, self.screen_width, self.screen_height, self.player.position)
    bullet = ufo.shoot(self.player.position)
    if bullet:
        self.ufo_bullets.append(bullet)

self.ufo_bullets = [b for b in self.ufo_bullets if b.active]
for bullet in self.ufo_bullets:
    bullet.update(dt, self.screen_width, self.screen_height)
```

Modificar check_collisions para incluir UFOs e ufo_bullets:
```python
# Bullet vs Asteroid (existing)

# Bullet vs UFO
ufo_bullets_to_remove = []
ufos_to_remove = []
for bullet in self.bullets:
    for ufo in self.ufos:
        if bullet.position.distance_to(ufo.position) < bullet.radius + ufo.radius:
            ufo_bullets_to_remove.append(bullet)
            ufos_to_remove.append(ufo)
            self.score += UFO_SCORE
            break

for bullet in ufo_bullets_to_remove:
    if bullet in self.bullets:
        self.bullets.remove(bullet)
for ufo in ufos_to_remove:
    if ufo in self.ufos:
        self.ufos.remove(ufo)

# UFO bullet vs Player
for bullet in self.ufo_bullets:
    if bullet.position.distance_to(self.player.position) < bullet.radius + self.player.radius:
        # Treat as asteroid collision (lose life)
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
            self.player.velocity = pygame.Vector2(0, 0)
        self.ufo_bullets.remove(bullet)
        break

# Player vs UFO (similar to asteroid)
for ufo in self.ufos:
    if self.player.position.distance_to(ufo.position) < self.player.radius + ufo.radius:
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
            self.player.velocity = pygame.Vector2(0, 0)
        break
```

Draw UFOs e ufo_bullets:
```python
# In draw, after asteroids
for ufo in self.ufos:
    ufo.draw(self.screen)
for bullet in self.ufo_bullets:
    bullet.draw(self.screen)
```

Reset em reset_game:
```python
self.ufos = []
self.ufo_bullets = []
```

### 4. Atualizar imports
Adicionar import para UFO em game.py.

## Testes
- A partir do nível 3, UFOs aparecem esporadicamente.
- UFOs se movem horizontalmente e wrap.
- Atiram bullets em direção do jogador.
- Colisões com bullets do jogador destroem UFOs e dão pontos.
- Colisão com jogador ou bullets do UFO causam perda de vida.

## Notas
- Limitar a 2 UFOs simultâneos para não sobrecarregar.
- Bullets do UFO são mais lentos para balanceamento.
- Possível expansão: UFOs com mais HP ou padrões de movimento complexos.