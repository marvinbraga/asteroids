# Task 03: Implementar Efeitos Sonoros e Música

## Objetivo
Adicionar sons para ações do jogo e música de fundo para aumentar a imersão.

## Assets Necessários
- shoot.wav: Som de tiro (curto, ~0.5s)
- explode.wav: Som de explosão (curto, ~1s)
- thrust.wav: Som de thrust (loop curto, ~0.2s)
- background.mp3: Música de fundo (loop, ~2-3 min)

Criar pasta assets/sounds/ e adicionar arquivos (gratuitos ou gerados).

## Passos de Implementação

### 1. Inicializar Mixer
Modificar main.py:
```python
import pygame
pygame.init()
pygame.mixer.init()  # Add this
# ... rest of code
```

### 2. Carregar Sons
Criar função em game.py ou constants.py para carregar sons:
```python
# In constants.py
import pygame
import os

# Sounds
SOUNDS_DIR = 'assets/sounds'
SOUND_SHOOT = None
SOUND_EXPLODE = None
SOUND_THRUST = None
MUSIC_BACKGROUND = os.path.join(SOUNDS_DIR, 'background.mp3')

def load_sounds():
    global SOUND_SHOOT, SOUND_EXPLODE, SOUND_THRUST
    SOUND_SHOOT = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'shoot.wav'))
    SOUND_EXPLODE = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'explode.wav'))
    SOUND_THRUST = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'thrust.wav'))
    # Set volumes if needed
    SOUND_SHOOT.set_volume(0.5)
    SOUND_EXPLODE.set_volume(0.7)
    SOUND_THRUST.set_volume(0.3)
```

Chamar load_sounds() no Game.__init__.

### 3. Música de Fundo
Em Game.__init__, após load_sounds():
```python
pygame.mixer.music.load(MUSIC_BACKGROUND)
pygame.mixer.music.play(-1)  # Loop indefinitely
pygame.mixer.music.set_volume(0.5)
```

Pausar/retomar música em pausa:
```python
# In run loop, when pausing
if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
    # ... existing pause logic
    if self.state == 'paused':
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
```

### 4. Sons de Eventos

#### Tiro (Player.shoot)
Em player.py, shoot():
```python
def shoot(self):
    if self.last_shot >= self.shoot_cooldown:
        self.last_shot = 0
        # Play sound
        from constants import SOUND_SHOOT
        if SOUND_SHOOT:
            SOUND_SHOOT.play()
        # ... rest of code
```

#### Explosões (Game.check_collisions)
Após destruir asteroid/UFO:
```python
# After score += ...
from constants import SOUND_EXPLODE
if SOUND_EXPLODE:
    SOUND_EXPLODE.play()
```

#### Thrust (Player.update)
Em player.py update():
```python
# Track thrusting state
was_thrusting = self.thrusting
self.thrusting = keys[pygame.K_UP] or keys[pygame.K_w]

if self.thrusting and not was_thrusting:
    # Start thrust sound loop
    from constants import SOUND_THRUST
    if SOUND_THRUST:
        SOUND_THRUST.play(-1)  # Loop
elif not self.thrusting and was_thrusting:
    # Stop thrust sound
    pygame.mixer.stop()  # Or more precisely, stop the channel
    # Better: use channels
```

Para thrust, usar canais para controle preciso:
```python
# In constants.py
THRUST_CHANNEL = None

def init_channels():
    global THRUST_CHANNEL
    THRUST_CHANNEL = pygame.mixer.Channel(1)  # Reserve channel 1 for thrust

# In Game.__init__, after load_sounds
init_channels()

# In Player.update
if self.thrusting and not was_thrusting:
    if THRUST_CHANNEL:
        THRUST_CHANNEL.play(SOUND_THRUST, loops=-1)
elif not self.thrusting and was_thrusting:
    if THRUST_CHANNEL:
        THRUST_CHANNEL.stop()
```

### 5. Volume e Configurações
Adicionar constantes para volumes em constants.py:
```python
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.6

# Set in load_sounds
pygame.mixer.music.set_volume(MUSIC_VOLUME)
SOUND_SHOOT.set_volume(SFX_VOLUME)
# etc.
```

Possível menu de opções para ajustar volumes.

## Testes
- Música toca continuamente em background.
- Som de tiro ao atirar.
- Som de explosão ao destruir objetos.
- Som de thrust ao acelerar, para ao parar.
- Volumes adequados (não muito altos).

## Notas
- Arquivos de som devem ser curtos para evitar lag.
- Se pygame.mixer não suportar formato, converter para .wav.
- Para distribuição, incluir assets no repositório ou como extras.