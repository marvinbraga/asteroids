# Task: Code Quality Improvements

This task details the implementation of all code quality improvements identified in the codebase analysis.

## Prerequisites
- Read and understand the current `game.py`, `constants.py`, and other relevant files
- Have a test environment to run the game after changes
- Use version control to commit changes incrementally

## Task 1: Fix Duplicate Imports
**File**: `game.py`  
**Lines**: 19-20  
**Description**: Remove duplicate import of highscores functions.

**Steps**:
1. Open `game.py`
2. Locate lines 19-20:
   ```python
   from highscores import get_highscores, add_highscore, is_highscore
   from highscores import add_highscore, get_highscores, is_highscore
   ```
3. Remove the second import line
4. Save and test that highscores functionality still works (menu and game over screens)

**Expected Outcome**: No duplicate imports, clean import section.

## Task 2: Remove Duplicate Assignments
**File**: `game.py`  
**Lines**: 67  
**Description**: Remove duplicate assignment of `self.explosion_particles`.

**Steps**:
1. Open `game.py`
2. Locate the `reset_game` method around line 59
3. Find the duplicate:
   ```python
   self.explosion_particles = []
   self.explosion_particles = []
   ```
4. Remove one of the lines
5. Save and test that explosion particles work correctly after game reset

**Expected Outcome**: Single assignment, no redundancy.

## Task 3: Refactor check_collisions Method
**File**: `game.py`  
**Lines**: ~87-280 (approximately 150+ lines)  
**Description**: Break down the large `check_collisions` method into smaller, focused methods.

**Steps**:
1. Identify the logical sections in `check_collisions`:
   - Bullet vs Asteroid collisions
   - Bullet vs UFO collisions
   - Power-up collection
   - Player vs Asteroid collisions
   - Player vs UFO collisions
   - UFO bullet vs Player collisions

2. Create helper methods in the `Game` class:

   **_check_bullet_asteroid_collisions()**:
   ```python
   def _check_bullet_asteroid_collisions(self):
       bullets_to_remove = []
       asteroids_to_remove = []
       new_asteroids = []

       for bullet in self.bullets:
           for asteroid in self.asteroids:
               if bullet.position.distance_to(asteroid.position) < bullet.radius + asteroid.radius:
                   bullets_to_remove.append(bullet)
                   # Handle armored asteroids
                   if hasattr(asteroid, 'hitpoints'):
                       asteroid.hitpoints -= 1
                       if asteroid.hitpoints > 0:
                           break
                   # Destroy asteroid
                   asteroids_to_remove.append(asteroid)
                   self.score += asteroid.score_value
                   if SOUND_EXPLODE:
                       SOUND_EXPLODE.play()
                   new_asteroids.extend(asteroid.split())
                   # Spawn power-up
                   if random.random() < POWERUP_SPAWN_CHANCE:
                       powerup_type = random.choice(POWERUP_TYPES)
                       powerup = PowerUp(asteroid.position, powerup_type)
                       self.powerups.append(powerup)
                   for _ in range(PARTICLE_COUNT_EXPLODE):
                       particle = Particle(asteroid.position)
                       self.explosion_particles.append(particle)
                   break

       # Remove collided objects
       for bullet in bullets_to_remove:
           if bullet in self.bullets:
               self.bullets.remove(bullet)
       for asteroid in asteroids_to_remove:
           if asteroid in self.asteroids:
               self.asteroids.remove(asteroid)

       self.asteroids.extend(new_asteroids)
   ```

   **_check_bullet_ufo_collisions()**:
   ```python
   def _check_bullet_ufo_collisions(self):
       ufo_bullets_to_remove = []
       ufos_to_remove = []
       for bullet in self.bullets:
           for ufo in self.ufos:
               if bullet.position.distance_to(ufo.position) < bullet.radius + ufo.radius:
                   ufo_bullets_to_remove.append(bullet)
                   ufos_to_remove.append(ufo)
                   self.score += UFO_SCORE
                   if SOUND_EXPLODE:
                       SOUND_EXPLODE.play()
                   for _ in range(PARTICLE_COUNT_EXPLODE):
                       particle = Particle(ufo.position)
                       self.explosion_particles.append(particle)
                   break

       for bullet in ufo_bullets_to_remove:
           if bullet in self.bullets:
               self.bullets.remove(bullet)
       for ufo in ufos_to_remove:
           if ufo in self.ufos:
               self.ufos.remove(ufo)
   ```

   **_check_powerup_collection()**:
   ```python
   def _check_powerup_collection(self):
       powerups_to_remove = []
       for powerup in self.powerups:
           if self.player.position.distance_to(powerup.position) < self.player.radius + powerup.radius:
               powerups_to_remove.append(powerup)
               self.apply_powerup(powerup.type)

       for powerup in powerups_to_remove:
           self.powerups.remove(powerup)
   ```

   **_check_player_asteroid_collisions()**:
   ```python
   def _check_player_asteroid_collisions(self):
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
                   if is_highscore(self.score):
                       self.state = 'enter_name'
                   else:
                       self.state = 'game_over'
               else:
                   # Reset player position
                   self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
                   self.player.velocity = pygame.Vector2(0, 0)
               break
   ```

   **_check_player_ufo_collisions()**:
   ```python
   def _check_player_ufo_collisions(self):
       for ufo in self.ufos:
           if self.player.position.distance_to(ufo.position) < self.player.radius + ufo.radius:
               self.lives -= 1
               if self.lives <= 0:
                   self.game_over = True
                   if is_highscore(self.score):
                       self.state = 'enter_name'
                   else:
                       self.state = 'game_over'
               else:
                   self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
                   self.player.velocity = pygame.Vector2(0, 0)
               break
   ```

   **_check_ufo_bullet_player_collisions()**:
   ```python
   def _check_ufo_bullet_player_collisions(self):
       ufo_bullets_to_remove = []
       for bullet in self.ufo_bullets:
           if bullet.position.distance_to(self.player.position) < bullet.radius + self.player.radius:
               # Treat as asteroid collision (lose life)
               self.lives -= 1
               if self.lives <= 0:
                   self.game_over = True
                   if is_highscore(self.score):
                       self.state = 'enter_name'
                   else:
                       self.state = 'game_over'
               else:
                   self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
                   self.player.velocity = pygame.Vector2(0, 0)
               ufo_bullets_to_remove.append(bullet)
               break

       for bullet in ufo_bullets_to_remove:
           if bullet in self.ufo_bullets:
               self.ufo_bullets.remove(bullet)
   ```

3. Replace the original `check_collisions` method with:
   ```python
   def check_collisions(self):
       self._check_bullet_asteroid_collisions()
       self._check_bullet_ufo_collisions()
       self._check_powerup_collection()
       self._check_player_asteroid_collisions()
       self._check_player_ufo_collisions()
       self._check_ufo_bullet_player_collisions()
   ```

4. Test all collision scenarios:
   - Shooting asteroids (normal and armored)
   - Shooting UFOs
   - Collecting power-ups
   - Player hitting asteroids (with/without shield)
   - Player hitting UFOs
   - UFO bullets hitting player

**Expected Outcome**: `check_collisions` is now 10-15 lines calling helper methods. Each collision type is isolated and testable.

## Task 4: Eliminate Duplicate Player Reset Code
**File**: `game.py`  
**Description**: Extract common player reset logic into a reusable method.

**Steps**:
1. Create a new method `_reset_player_position()`:
   ```python
   def _reset_player_position(self):
       self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
       self.player.velocity = pygame.Vector2(0, 0)
   ```

2. Replace all instances of:
   ```python
   self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
   self.player.velocity = pygame.Vector2(0, 0)
   ```
   With:
   ```python
   self._reset_player_position()
   ```

3. Locations to replace:
   - In `_check_player_asteroid_collisions` (when losing life)
   - In `_check_player_ufo_collisions`
   - In `_check_ufo_bullet_player_collisions`

4. Test that player resets correctly in all collision scenarios.

**Expected Outcome**: No duplicate code, single source of truth for player reset.

## Task 5: Replace Magic Numbers with Named Constants
**File**: `game.py` and `constants.py`  
**Description**: Define constants for hardcoded UI positioning values.

**Steps**:
1. Add to `constants.py`:
   ```python
   # UI Positioning
   UI_SCORE_X = 10
   UI_SCORE_Y = 10
   UI_LIVES_X = 10
   UI_LIVES_Y = 50
   UI_LEVEL_X = 10
   UI_LEVEL_Y = 90
   UI_GAME_OVER_X_OFFSET = 200
   UI_GAME_OVER_Y = SCREEN_HEIGHT // 2
   UI_TITLE_X = SCREEN_WIDTH // 2 - 50
   UI_TITLE_Y = SCREEN_HEIGHT // 2 - 100
   UI_START_X = SCREEN_WIDTH // 2 - 100
   UI_START_Y = SCREEN_HEIGHT // 2 - 50
   UI_HIGHSCORES_X = SCREEN_WIDTH // 2 - 120
   UI_HIGHSCORES_Y = SCREEN_HEIGHT // 2
   UI_BACK_X = SCREEN_WIDTH // 2 - 100
   UI_BACK_Y = SCREEN_HEIGHT - 50
   UI_ENTER_NAME_PROMPT_X = SCREEN_WIDTH // 2 - 80
   UI_ENTER_NAME_PROMPT_Y = SCREEN_HEIGHT // 2 - 50
   UI_ENTER_NAME_TEXT_Y = SCREEN_HEIGHT // 2
   UI_PAUSE_TITLE_X = SCREEN_WIDTH // 2 - 50
   UI_PAUSE_TITLE_Y = SCREEN_HEIGHT // 2 - 100
   UI_RESUME_X = SCREEN_WIDTH // 2 - 60
   UI_RESUME_Y = SCREEN_HEIGHT // 2 - 50
   UI_RESTART_X = SCREEN_WIDTH // 2 - 60
   UI_RESTART_Y = SCREEN_HEIGHT // 2
   UI_MENU_X = SCREEN_WIDTH // 2 - 70
   UI_MENU_Y = SCREEN_HEIGHT // 2 + 50
   ```

2. Update `draw_game()`:
   ```python
   score_text = self.font.render(f"Score: {self.score}", True, WHITE)
   lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
   level_text = self.font.render(f"Level: {self.level}", True, WHITE)
   self.screen.blit(score_text, (UI_SCORE_X, UI_SCORE_Y))
   self.screen.blit(lives_text, (UI_LIVES_X, UI_LIVES_Y))
   self.screen.blit(level_text, (UI_LEVEL_X, UI_LEVEL_Y))

   if self.game_over:
       game_over_text = self.font.render("GAME OVER - Press R to restart, M for menu", True, RED)
       self.screen.blit(game_over_text, (self.screen_width // 2 - UI_GAME_OVER_X_OFFSET, UI_GAME_OVER_Y))
   ```

3. Update `draw_menu()`:
   ```python
   title = self.font.render("ASTEROIDS", True, WHITE)
   start = self.font.render("Press ENTER to Start", True, WHITE)
   highscores = self.font.render("Press H for High Scores", True, WHITE)

   self.screen.blit(title, (UI_TITLE_X, UI_TITLE_Y))
   self.screen.blit(start, (UI_START_X, UI_START_Y))
   self.screen.blit(highscores, (UI_HIGHSCORES_X, UI_HIGHSCORES_Y))
   ```

4. Update `draw_highscores()`:
   ```python
   title = self.font.render("HIGH SCORES", True, WHITE)
   self.screen.blit(title, (self.screen_width // 2 - 70, 50))
   scores = get_highscores()
   for i, entry in enumerate(scores):
       text = self.font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, WHITE)
       self.screen.blit(text, (self.screen_width // 2 - 100, 100 + i * 40))
   back = self.font.render("Press ESC to go back", True, WHITE)
   self.screen.blit(back, (UI_BACK_X, UI_BACK_Y))
   ```

5. Update `draw_enter_name()`:
   ```python
   prompt = self.font.render("Enter your name:", True, WHITE)
   name_text = self.font.render(self.input_name, True, WHITE)
   self.screen.blit(prompt, (UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y))
   self.screen.blit(name_text, (self.screen_width // 2 - len(self.input_name)*5, UI_ENTER_NAME_TEXT_Y))
   ```

6. Update `draw_pause_overlay()`:
   ```python
   pause_text = self.font.render("PAUSED", True, WHITE)
   resume_text = self.font.render("R: Resume", True, WHITE)
   restart_text = self.font.render("S: Restart", True, WHITE)
   menu_text = self.font.render("M: Main Menu", True, WHITE)

   self.screen.blit(pause_text, (UI_PAUSE_TITLE_X, UI_PAUSE_TITLE_Y))
   self.screen.blit(resume_text, (UI_RESUME_X, UI_RESUME_Y))
   self.screen.blit(restart_text, (UI_RESTART_X, UI_RESTART_Y))
   self.screen.blit(menu_text, (UI_MENU_X, UI_MENU_Y))
   ```

7. Test all UI screens to ensure positioning is correct.

**Expected Outcome**: No magic numbers in UI code, all positioning defined in constants.

## Task 6: Standardize Type Hints
**File**: `game.py` and other classes  
**Description**: Add consistent type hints throughout the codebase.

**Steps**:
1. Add imports at top of `game.py`:
   ```python
   from typing import List, Optional
   ```

2. Add type hints to `Game` class methods:
   ```python
   def __init__(self) -> None:
   def apply_difficulty(self) -> None:
   def reset_game(self) -> None:
   def spawn_asteroids(self) -> None:
   def check_collisions(self) -> None:
   def apply_powerup(self, type_: str) -> None:
   def update(self, dt: float) -> None:
   def draw(self) -> None:
   def draw_game(self) -> None:
   def draw_pause_overlay(self) -> None:
   def draw_menu(self) -> None:
   def draw_highscores(self) -> None:
   def draw_enter_name(self) -> None:
   def run(self) -> None:
   ```

3. Add type hints to private methods created in Task 3-4.

4. Add type hints to other classes if missing (Player, Asteroid, etc.).

5. Run a type checker like mypy to verify:
   ```bash
   pip install mypy
   mypy game.py
   ```

6. Fix any type errors found.

**Expected Outcome**: Consistent type hints, better IDE support and code documentation.

## Testing and Validation
- Run the game after each task to ensure no regressions
- Test all collision scenarios
- Verify UI positioning is maintained
- Check for any import errors or syntax issues
- Use a linter like flake8 to check code quality improvements

## Completion Criteria
- All duplicate code removed
- `check_collisions` refactored into smaller methods
- Magic numbers replaced with constants
- Type hints added consistently
- Game runs without errors and maintains all functionality