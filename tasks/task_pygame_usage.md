# Task: Better Pygame Usage Practices

This task details the implementation of improved Pygame usage practices for better performance and correctness.

## Prerequisites
- Performance optimizations from `task_performance.md` completed
- Understanding of Pygame timing and display systems
- Test on different hardware to verify improvements

## Task 1: Replace Delta Time Accumulation with Timestamp Timers
**Files**: `player.py`, `powerup.py`, `ufo.py`, `particle.py`  
**Description**: Use `pygame.time.get_ticks()` for timers to avoid floating-point drift.

**Steps**:
1. Update `Player` class for shoot cooldown:
   ```python
   class Player(GameObject):
       def __init__(self, position: pygame.Vector2):
           # ... existing code ...
           self.last_shot_time = 0  # Timestamp

       def update(self, dt: float, keys, screen_width: int, screen_height: int):
           current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds

           # ... existing thrust logic ...

           # Update power-up timer
           if self.powerup_timer > 0:
               self.powerup_timer -= dt
               if self.powerup_timer <= 0:
                   self.shielded = False
                   self.speed_boost = 1.0
                   self.multishot = False

           # ... existing particle logic ...

       def shoot(self):
           current_time = pygame.time.get_ticks() / 1000.0
           if current_time - self.last_shot_time >= self.shoot_cooldown:
               self.last_shot_time = current_time
               if SOUND_SHOOT:
                   SOUND_SHOOT.play()
               # ... rest of shoot logic ...
   ```

2. Update `PowerUp` class:
   ```python
   class PowerUp(GameObject):
       def __init__(self, position: pygame.Vector2, type_: str):
           # ... existing code ...
           self.spawn_time = pygame.time.get_ticks() / 1000.0

       def update(self, dt: float, screen_width: int, screen_height: int):
           current_time = pygame.time.get_ticks() / 1000.0
           self.lifetime = POWERUP_DURATION - (current_time - self.spawn_time)
           if self.lifetime <= 0:
               self.active = False
           self.wrap_position(screen_width, screen_height)
   ```

3. Update `UFO` class for shoot interval:
   ```python
   class UFO(GameObject):
       def __init__(self, position: pygame.Vector2, screen_width: int):
           # ... existing code ...
           self.last_shot_time = 0

       def update(self, dt: float, screen_width: int, screen_height: int, player_pos: pygame.Vector2):
           # ... existing movement logic ...

       def shoot(self, player_pos: pygame.Vector2):
           current_time = pygame.time.get_ticks() / 1000.0
           if current_time - self.last_shot_time >= self.shoot_interval:
               self.last_shot_time = current_time
               # ... rest of shoot logic ...
   ```

4. Update `Particle` class:
   ```python
   class Particle(GameObject):
       def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2 = None):
           # ... existing code ...
           self.spawn_time = pygame.time.get_ticks() / 1000.0

       def update(self, dt: float, screen_width: int, screen_height: int):
           current_time = pygame.time.get_ticks() / 1000.0
           self.lifetime = PARTICLE_LIFETIME - (current_time - self.spawn_time)
           if self.lifetime <= 0:
               self.active = False
           self.position += self.velocity * dt
   ```

5. Test timer accuracy:
   - Shoot cooldown should be consistent
   - Power-ups should last exactly the right time
   - UFO shooting should be regular
   - Particles should fade at consistent rates

**Expected Outcome**: Timers use timestamps, eliminating drift from frame rate variations.

## Task 2: Implement Dirty Rectangle Rendering
**File**: `game.py`  
**Description**: Only update changed screen regions for better performance.

**Steps**:
1. Track dirty rectangles in `Game` class:
   ```python
   def __init__(self):
       # ... existing code ...
       self.dirty_rects = []
       self.use_dirty_rects = True  # Toggle for testing
   ```

2. Modify draw methods to collect rects instead of drawing directly:
   ```python
   def draw_game(self):
       if not self.use_dirty_rects:
           # Original drawing code
           self.asteroids.draw(self.screen)
           self.bullets.draw(self.screen)
           self.powerups.draw(self.screen)
           self.ufos.draw(self.screen)
           self.ufo_bullets.draw(self.screen)
           self.explosion_particles.draw(self.screen)
           self.player.draw(self.screen)

           # UI
           score_text = self._get_cached_text("score", f"Score: {self.score}", WHITE)
           lives_text = self._get_cached_text("lives", f"Lives: {self.lives}", WHITE)
           level_text = self._get_cached_text("level", f"Level: {self.level}", WHITE)
           self.screen.blit(score_text, (UI_SCORE_X, UI_SCORE_Y))
           self.screen.blit(lives_text, (UI_LIVES_X, UI_LIVES_Y))
           self.screen.blit(level_text, (UI_LEVEL_X, UI_LEVEL_Y))

           if self.game_over:
               game_over_text = self._get_cached_text("game_over", "GAME OVER - Press R to restart, M for menu", RED)
               self.screen.blit(game_over_text, (self.screen_width // 2 - UI_GAME_OVER_X_OFFSET, UI_GAME_OVER_Y))

           pygame.display.flip()
           return

       # Dirty rects mode
       self.dirty_rects = []

       # Clear previous positions (simulate background)
       # For simplicity, we'll track all object positions
       old_positions = getattr(self, '_old_positions', {})

       # Draw background (if needed)
       # self.screen.fill(BLACK, background_rect)  # If we had a background

       # Draw all sprites and collect their rects
       sprite_rects = []
       sprite_rects.extend(self.asteroids.draw(self.screen))
       sprite_rects.extend(self.bullets.draw(self.screen))
       sprite_rects.extend(self.powerups.draw(self.screen))
       sprite_rects.extend(self.ufos.draw(self.screen))
       sprite_rects.extend(self.ufo_bullets.draw(self.screen))
       sprite_rects.extend(self.explosion_particles.draw(self.screen))
       player_rect = self.player.draw(self.screen)
       if player_rect:
           sprite_rects.append(player_rect)

       # Draw UI and collect rects
       score_text = self._get_cached_text("score", f"Score: {self.score}", WHITE)
       score_rect = self.screen.blit(score_text, (UI_SCORE_X, UI_SCORE_Y))
       sprite_rects.append(score_rect)

       lives_text = self._get_cached_text("lives", f"Lives: {self.lives}", WHITE)
       lives_rect = self.screen.blit(lives_text, (UI_LIVES_X, UI_LIVES_Y))
       sprite_rects.append(lives_rect)

       level_text = self._get_cached_text("level", f"Level: {self.level}", WHITE)
       level_rect = self.screen.blit(level_text, (UI_LEVEL_X, UI_LEVEL_Y))
       sprite_rects.append(level_rect)

       if self.game_over:
           game_over_text = self._get_cached_text("game_over", "GAME OVER - Press R to restart, M for menu", RED)
           game_over_rect = self.screen.blit(game_over_text, (self.screen_width // 2 - UI_GAME_OVER_X_OFFSET, UI_GAME_OVER_Y))
           sprite_rects.append(game_over_rect)

       # Combine old and new positions for dirty rects
       all_rects = sprite_rects[:]
       for rect in old_positions.values():
           all_rects.append(rect)

       # Update dirty rects
       self.dirty_rects = all_rects

       # Store current positions for next frame
       self._old_positions = {id(obj): obj.rect for obj in self.asteroids.sprites() + self.bullets.sprites() + self.powerups.sprites() + self.ufos.sprites() + self.ufo_bullets.sprites() + self.explosion_particles.sprites()}
       if hasattr(self.player, 'rect'):
           self._old_positions[id(self.player)] = self.player.rect
   ```

3. Update the main draw method:
   ```python
   def draw(self):
       self.screen.fill(BLACK)  # Clear screen

       if self.state in ('playing', 'game_over'):
           self.draw_game()
       elif self.state == 'menu':
           self.draw_menu()
       elif self.state == 'highscores':
           self.draw_highscores()
       elif self.state == 'enter_name':
           self.draw_enter_name()

       # Update display
       if self.use_dirty_rects and self.dirty_rects:
           pygame.display.update(self.dirty_rects)
       else:
           pygame.display.flip()
   ```

4. Ensure all drawable objects have a `rect` attribute (Pygame Sprites have this automatically).

5. For menu and other states, implement similar dirty rect tracking.

6. Test performance:
   - Measure FPS with and without dirty rects
   - Verify no visual artifacts
   - Toggle `use_dirty_rects` to compare

**Expected Outcome**: Only changed screen regions are updated, potentially better performance especially with many static objects.

## Testing and Validation
- Timer accuracy: verify shoot rates, power-up durations are consistent across frame rates
- Visual correctness: ensure dirty rects don't cause tearing or missing updates
- Performance: benchmark with various object counts
- Compatibility: test on different Pygame versions and hardware

## Completion Criteria
- All timers use timestamp-based logic
- Dirty rectangle rendering implemented and tested
- No visual or functional regressions
- Measurable performance improvements where applicable