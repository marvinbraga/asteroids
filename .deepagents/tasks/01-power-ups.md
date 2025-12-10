# Task 01: Implementar Power-ups e Itens Coletáveis

## Objetivo
Adicionar power-ups coletáveis que aparecem ao destruir asteroides, fornecendo vantagens temporárias ao jogador.

## Tipos de Power-ups
- **Shield**: Protege contra 1 colisão com asteroide/UFO.
- **Speed Boost**: Aumenta velocidade da nave por 10 segundos.
- **Multishot**: Permite tiros triplos por 10 segundos.

## Passos de Implementação

### 1. Atualizar constants.py
Adicionar constantes para power-ups:
```python
# Power-ups
POWERUP_TYPES = ['shield', 'speed', 'multishot']
POWERUP_RADIUS = 10
POWERUP_DURATION = 10.0
POWERUP_SPAWN_CHANCE = 0.2
POWERUP_COLORS = {'shield': (0, 255, 255), 'speed': (255, 255, 0), 'multishot': (255, 0, 255)}
```

### 2. Criar powerup.py
Nova classe PowerUp herdando de GameObject:
```python
import pygame
from game_object import GameObject
from constants import POWERUP_RADIUS, POWERUP_TYPES, POWERUP_COLORS

class PowerUp(GameObject):
    def __init__(self, position: pygame.Vector2, type_: str):
        super().__init__(position)
        self.type = type_
        self.radius = POWERUP_RADIUS
        self.color = POWERUP_COLORS[type_]
        self.lifetime = 10.0  # seconds before disappearing

    def update(self, dt: float, screen_width: int, screen_height: int):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
        self.wrap_position(screen_width, screen_height)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
```

### 3. Modificar player.py
Adicionar atributos para power-ups no Player:
```python
# In Player.__init__
self.shielded = False
self.speed_boost = 1.0
self.multishot = False
self.powerup_timer = 0
```

Modificar update para aplicar boosts:
```python
# In Player.update, after existing code
if self.powerup_timer > 0:
    self.powerup_timer -= dt
    if self.powerup_timer <= 0:
        self.shielded = False
        self.speed_boost = 1.0
        self.multishot = False
else:
    # Apply boosts
    effective_thrust = self.thrust * self.speed_boost
    effective_max_speed = self.max_speed * self.speed_boost
    # Use effective_thrust and effective_max_speed in movement calculations
```

Modificar shoot para multishot:
```python
def shoot(self):
    if self.last_shot >= self.shoot_cooldown:
        self.last_shot = 0
        direction = pygame.Vector2(0, -1).rotate(self.rotation)
        bullet_pos = self.position + direction * (self.radius + 5)
        bullets = [Bullet(bullet_pos, direction * BULLET_SPEED)]
        if self.multishot:
            # Add side bullets
            side_angle = 15  # degrees
            left_dir = direction.rotate(-side_angle)
            right_dir = direction.rotate(side_angle)
            bullets.append(Bullet(bullet_pos, left_dir * BULLET_SPEED))
            bullets.append(Bullet(bullet_pos, right_dir * BULLET_SPEED))
        return bullets
    return []
```

### 4. Modificar game.py
Adicionar lista de power-ups:
```python
# In Game.__init__
self.powerups = []
```

Spawn power-ups em check_collisions:
```python
# After asteroid destruction
if random.random() < POWERUP_SPAWN_CHANCE:
    powerup_type = random.choice(POWERUP_TYPES)
    powerup = PowerUp(asteroid.position, powerup_type)
    self.powerups.append(powerup)
```

Coleta de power-ups:
```python
# Add after bullet/asteroid collisions
powerups_to_remove = []
for powerup in self.powerups:
    if self.player.position.distance_to(powerup.position) < self.player.radius + powerup.radius:
        powerups_to_remove.append(powerup)
        self.apply_powerup(powerup.type)

for powerup in powerups_to_remove:
    self.powerups.remove(powerup)
```

Adicionar método apply_powerup:
```python
def apply_powerup(self, type_: str):
    self.player.powerup_timer = POWERUP_DURATION
    if type_ == 'shield':
        self.player.shielded = True
    elif type_ == 'speed':
        self.player.speed_boost = 1.5
    elif type_ == 'multishot':
        self.player.multishot = True
```

Modificar colisão player-asteroid para considerar shield:
```python
# In check_collisions, player vs asteroid
for asteroid in self.asteroids:
    if self.player.position.distance_to(asteroid.position) < self.player.radius + asteroid.radius:
        if self.player.shielded:
            self.player.shielded = False
            # Destroy asteroid without losing life
            if asteroid in self.asteroids:
                self.asteroids.remove(asteroid)
                self.score += asteroid.score_value
                new_asteroids = asteroid.split()
                self.asteroids.extend(new_asteroids)
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Reset player
                self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
                self.player.velocity = pygame.Vector2(0, 0)
        break
```

Update e draw power-ups:
```python
# In update
self.powerups = [p for p in self.powerups if p.active]
for powerup in self.powerups:
    powerup.update(dt, self.screen_width, self.screen_height)

# In draw
for powerup in self.powerups:
    powerup.draw(self.screen)
```

### 5. Atualizar __init__.py ou imports
Adicionar import para PowerUp em game.py.

## Testes
- Destruir asteroides e verificar spawn de power-ups.
- Coletar power-ups e verificar efeitos (velocidade, multishot, shield).
- Verificar expiração dos efeitos após 10 segundos.
- Shield protege contra 1 colisão.

## Notas
- Power-ups devem wrap around como outros objetos.
- Cores distintas para identificação visual.
- Possível expansão: Mais tipos de power-ups no futuro.