# Task: Architectural Refactors

This task details the implementation of major architectural improvements to enhance maintainability, extensibility, and code organization.

## Prerequisites
- All previous tasks completed
- Understanding of design patterns (State, Factory, Observer/Event)
- Plan for incremental refactoring to avoid breaking the game

## Task 1: Implement State Pattern for Game States
**Files**: `game.py`, new `game_states.py`  
**Description**: Extract game states into separate classes following the State pattern.

**Steps**:
1. Create `game_states.py`:
   ```python
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
                   elif event.key == pygame.K_q or event.key == pygame.K_3:
                       self.game.running = False

       def draw(self, screen):
           screen.fill((0, 0, 0))
           title = self.game.font.render("ASTEROIDS", True, WHITE)
           start = self.game.font.render("Press ENTER to Start", True, WHITE)
           highscores = self.game.font.render("Press H for High Scores", True, WHITE)

           screen.blit(title, (UI_TITLE_X, UI_TITLE_Y))
           screen.blit(start, (UI_START_X, UI_START_Y))
           screen.blit(highscores, (UI_HIGHSCORES_X, UI_HIGHSCORES_Y))

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
   ```

2. Modify `Game` class:
   ```python
   from game_states import MenuState, PlayingState, GameOverState, HighscoresState, EnterNameState

   class Game:
       def __init__(self, ...):
           # ... existing init ...
           self.states = {
               'menu': MenuState(self),
               'playing': PlayingState(self),
               'game_over': GameOverState(self),
               'highscores': HighscoresState(self),
               'enter_name': EnterNameState(self)
           }
           self.current_state = self.states['menu']
           self.state_name = 'menu'

       def change_state(self, new_state_name):
           if self.current_state:
               self.current_state.exit()
           self.current_state = self.states[new_state_name]
           self.state_name = new_state_name
           self.current_state.enter()

       def handle_input(self, events, keys):
           self.current_state.handle_input(events, keys)

       def update(self, dt):
           self.current_state.update(dt)

       def draw(self):
           self.current_state.draw(self.screen)
           pygame.display.flip()  # Or use dirty rects
   ```

3. Update `run()` method:
   ```python
   def run(self):
       running = True
       while running:
           dt = self.clock.tick(self.fps) / 1000.0

           events = pygame.event.get()
           keys = pygame.key.get_pressed()

           for event in events:
               if event.type == pygame.QUIT:
                   running = False

           self.handle_input(events, keys)

           if self.state_name == 'playing' and not self.game_over:
               self.update(dt)

           if self.state_name == 'playing' and self.game_over:
               if self.is_highscore(self.score):
                   self.change_state('enter_name')

           self.draw()

       pygame.quit()
   ```

4. Extract `update_game_logic()` from `update()`:
   ```python
   def update_game_logic(self, dt, keys):
       # Move game logic here from the old update method
       # Update player, bullets, asteroids, etc.
       # Check collisions, spawn objects, etc.
   ```

5. Test all state transitions and functionality.

**Expected Outcome**: Game states are modular classes, easier to add new states or modify existing ones.

## Task 2: Extract CollisionManager
**Files**: `game.py`, new `collision_manager.py`  
**Description**: Move all collision logic to a dedicated manager class.

**Steps**:
1. Create `collision_manager.py`:
   ```python
   import pygame
   from constants import SOUND_EXPLODE, UFO_SCORE, POWERUP_SPAWN_CHANCE, POWERUP_TYPES, PARTICLE_COUNT_EXPLODE

   class CollisionManager:
       def __init__(self, game):
           self.game = game

       def check_collisions(self):
           self._check_bullet_asteroid_collisions()
           self._check_bullet_ufo_collisions()
           self._check_powerup_collection()
           self._check_player_asteroid_collisions()
           self._check_player_ufo_collisions()
           self._check_ufo_bullet_player_collisions()

       # Copy all collision methods from Game class, adapted to use self.game
       def _check_bullet_asteroid_collisions(self):
           # ... collision logic, using self.game for access to groups and methods ...

       # Similarly for other collision methods
   ```

2. Update `Game` class:
   ```python
   from collision_manager import CollisionManager

   class Game:
       def __init__(self, ...):
           # ... existing init ...
           self.collision_manager = CollisionManager(self)

       def check_collisions(self):
           self.collision_manager.check_collisions()
   ```

3. Move all collision methods from `Game` to `CollisionManager`, updating references.

4. Test all collision scenarios still work.

**Expected Outcome**: Collision logic separated, `Game` class less cluttered.

## Task 3: Implement Custom Event System
**Files**: `game.py`, `collision_manager.py`, new `event_manager.py`  
**Description**: Use Pygame custom events for decoupling game components.

**Steps**:
1. Create `event_manager.py`:
   ```python
   import pygame

   # Custom event types
   ASTEROID_DESTROYED = pygame.USEREVENT + 1
   UFO_DESTROYED = pygame.USEREVENT + 2
   PLAYER_HIT = pygame.USEREVENT + 3
   POWERUP_COLLECTED = pygame.USEREVENT + 4
   LEVEL_COMPLETE = pygame.USEREVENT + 5

   class EventManager:
       @staticmethod
       def post_asteroid_destroyed(position, score_value):
           pygame.event.post(pygame.event.Event(ASTEROID_DESTROYED,
               {'position': position, 'score': score_value}))

       @staticmethod
       def post_ufo_destroyed(position, score):
           pygame.event.post(pygame.event.Event(UFO_DESTROYED,
               {'position': position, 'score': score}))

       @staticmethod
       def post_player_hit():
           pygame.event.post(pygame.event.Event(PLAYER_HIT))

       @staticmethod
       def post_powerup_collected(type_):
           pygame.event.post(pygame.event.Event(POWERUP_COLLECTED,
               {'type': type_}))

       @staticmethod
       def post_level_complete(level):
           pygame.event.post(pygame.event.Event(LEVEL_COMPLETE,
               {'level': level}))
   ```

2. Update collision methods to post events:
   ```python
   from event_manager import EventManager

   def _check_bullet_asteroid_collisions(self):
       # ... collision detection ...
       for bullet, asteroids in hits.items():
           for asteroid in asteroids:
               # ... destroy logic ...
               EventManager.post_asteroid_destroyed(asteroid.position, asteroid.score_value)
               # ... spawn particles, powerups ...
   ```

3. Update `Game` to handle events:
   ```python
   def handle_events(self, events):
       for event in events:
           if event.type == event_manager.ASTEROID_DESTROYED:
               self.score += event.score
               # Spawn particles, etc.
           elif event.type == event_manager.PLAYER_HIT:
               self.lives -= 1
               # Handle player hit
           # ... other events ...
   ```

4. Integrate event handling into the main loop.

5. Test that events trigger correct actions.

**Expected Outcome**: Components communicate via events, better decoupling.

## Task 4: Implement Factory Pattern for Object Creation
**Files**: New `factories.py`, update spawns in `game.py` and `collision_manager.py`  
**Description**: Centralize object creation logic.

**Steps**:
1. Create `factories.py`:
   ```python
   import pygame
   from asteroid import Asteroid
   from bullet import Bullet
   from powerup import PowerUp
   from ufo import UFO
   from particle import Particle
   from constants import ASTEROID_SIZES

   class AsteroidFactory:
       @staticmethod
       def create(position, size='large'):
           return Asteroid(position, size)

   class BulletFactory:
       @staticmethod
       def create(position, velocity):
           return Bullet(position, velocity)

   class PowerUpFactory:
       @staticmethod
       def create(position, type_):
           return PowerUp(position, type_)

   class UFOFactory:
       @staticmethod
       def create(position, screen_width):
           return UFO(position, screen_width)

   class ParticleFactory:
       @staticmethod
       def create_explosion(position):
           return Particle(position)

       @staticmethod
       def create_thrust(position, velocity):
           return Particle(position, velocity)
   ```

2. Update spawn code to use factories:
   ```python
   from factories import AsteroidFactory, PowerUpFactory, UFOFactory, ParticleFactory

   def spawn_asteroids(self):
       # ... existing logic ...
       asteroid = AsteroidFactory.create(pos, 'large')
       self.asteroids.add(asteroid)
   ```

3. Update collision spawns similarly.

**Expected Outcome**: Object creation centralized, easier to modify spawn logic.

## Task 5: Externalize Configuration
**Files**: `constants.py`, new `config.json`, update `game.py`  
**Description**: Move game configuration to external JSON file.

**Steps**:
1. Create `config.json`:
   ```json
   {
     "difficulty": {
       "easy": {"lives": 5, "ufo_chance": 0.02},
       "normal": {"lives": 3, "ufo_chance": 0.05},
       "hard": {"lives": 2, "ufo_chance": 0.08}
     },
     "gameplay": {
       "initial_level": 1,
       "level_asteroid_increase": 2,
       "base_asteroids": 4,
       "speed_increase_per_level": 0.1
     }
   }
   ```

2. Load config in `Game.__init__()`:
   ```python
   import json
   with open('config.json', 'r') as f:
       self.config = json.load(f)
   ```

3. Update code to use `self.config` instead of constants.

4. Allow runtime config changes (e.g., difficulty selection updates config).

**Expected Outcome**: Configuration externalized, easier to tweak without code changes.

## Testing and Validation
- All game states work correctly
- Collision detection unchanged
- Events trigger proper responses
- Object creation works
- Config changes affect gameplay

## Completion Criteria
- State pattern implemented for all game states
- Collision logic in separate manager
- Custom events used for component communication
- Factory pattern for object creation
- Configuration externalized to JSON
- Code is more modular and maintainable