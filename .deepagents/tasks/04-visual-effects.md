# Task 04: Implementar Efeitos Visuais Aprimorados

## Objetivo
Adicionar partículas para explosões, melhorar thrust visual e variar formas de asteroides.

## Componentes
- Sistema de partículas para explosões.
- Partículas de thrust.
- Asteroides com formas e cores variadas.

## Passos de Implementação

### 1. Atualizar constants.py
Adicionar constantes para partículas:
```python
# Particles
PARTICLE_LIFETIME = 1.0
PARTICLE_COUNT_EXPLODE = 8
PARTICLE_SPEED = 200
PARTICLE_COLORS = [(255, 255, 0), (255, 165, 0), (255, 0, 0)]  # Yellow, Orange, Red

# Asteroid variations
ASTEROID_COLORS = [(128, 128, 128), (160, 160, 160), (100, 100, 100), (140, 140, 140)]
```

### 2. Criar particle.py
Classe Particle:
```python
import pygame
import random
from game_object import GameObject
from constants import PARTICLE_LIFETIME, PARTICLE_SPEED, PARTICLE_COLORS

class Particle(GameObject):
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2 = None):
        if velocity is None:
            angle = random.uniform(0, 360)
            speed = random.uniform(50, PARTICLE_SPEED)
            velocity = pygame.Vector2(speed, 0).rotate(angle)
        super().__init__(position, velocity)
        self.lifetime = PARTICLE_LIFETIME
        self.color = random.choice(PARTICLE_COLORS)

    def update(self, dt: float, screen_width: int, screen_height: int):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
        self.position += self.velocity * dt
        # Optional: fade velocity or wrap

    def draw(self, screen: pygame.Surface):
        alpha = int(255 * (self.lifetime / PARTICLE_LIFETIME))
        color_with_alpha = (*self.color, alpha)
        # Note: pygame.draw.circle doesn't support alpha directly
        # For simplicity, use solid color and size fade
        size = max(1, int(5 * (self.lifetime / PARTICLE_LIFETIME)))
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), size)
```

### 3. Modificar asteroid.py
Variar cores e formas:
```python
# In Asteroid.__init__
self.color = random.choice(ASTEROID_COLORS)

# In _generate_shape, vary number of points more
num_points = random.randint(5, 14)  # Was 6-12

# In draw
pygame.draw.polygon(screen, self.color, rotated_points, 2)
```

### 4. Modificar player.py
Adicionar partículas de thrust:
```python
# In Player.__init__
self.thrust_particles = []

# In update, after setting thrusting
if self.thrusting:
    # Spawn thrust particles occasionally
    if random.random() < 0.5:  # Adjust frequency
        direction = pygame.Vector2(0, 1).rotate(self.rotation)  # Backwards
        particle_pos = self.position + direction * (self.radius + 5)
        particle_vel = direction * random.uniform(100, 200) + self.velocity * 0.5
        particle = Particle(particle_pos, particle_vel)
        self.thrust_particles.append(particle)

# Update particles
self.thrust_particles = [p for p in self.thrust_particles if p.active]
for particle in self.thrust_particles:
    particle.update(dt, screen_width, screen_height)

# In draw, after drawing ship
for particle in self.thrust_particles:
    particle.draw(screen)
```

### 5. Modificar game.py
Adicionar lista de particles de explosão:
```python
# In Game.__init__
self.explosion_particles = []

# In check_collisions, after destroying asteroid/UFO
for _ in range(PARTICLE_COUNT_EXPLODE):
    particle = Particle(asteroid.position)  # Or ufo.position
    self.explosion_particles.append(particle)

# Update particles
self.explosion_particles = [p for p in self.explosion_particles if p.active]
for particle in self.explosion_particles:
    particle.update(dt, self.screen_width, self.screen_height)

# In draw, after drawing entities
for particle in self.explosion_particles:
    particle.draw(self.screen)
```

Reset em reset_game:
```python
self.explosion_particles = []
```

## Testes
- Destruir asteroides mostra explosão de partículas coloridas.
- Acelerar mostra partículas de thrust atrás da nave.
- Asteroides têm cores e formas variadas.
- Partículas desaparecem após ~1 segundo.

## Notas
- Para alpha real, usar Surface com alpha, mas para simplicidade, fade de tamanho.
- Ajustar frequências para performance (não muitas particles).
- Possível expansão: Partículas para power-ups ou tiros.