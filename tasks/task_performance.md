# Task: Performance Optimizations

This task details the implementation of all performance optimizations identified in the codebase analysis.

## Prerequisites
- Code quality improvements from `task_code_quality.md` should be completed first
- Understand Pygame sprite system and collision detection
- Have performance testing tools (e.g., monitor FPS)
- Test with scenarios involving many objects (bullets, asteroids, particles)

## Task 1: Migrate to Sprite Groups
**Files**: `game.py`, `player.py`, `asteroid.py`, `bullet.py`, `powerup.py`, `particle.py`, `ufo.py`  
**Description**: Replace manual lists with Pygame Sprite Groups for automatic update/draw batching.

**Steps**:
1. Add import to `game.py`:
   ```python
   import pygame.sprite
   ```

2. Modify `Game.__init__()` to use groups:
   ```python
   # Replace lists with groups
   self.asteroids = pygame.sprite.Group()
   self.bullets = pygame.sprite.Group()
   self.powerups = pygame.sprite.Group()
   self.ufos = pygame.sprite.Group()
   self.ufo_bullets = pygame.sprite.Group()
   self.explosion_particles = pygame.sprite.Group()
   self.thrust_particles = pygame.sprite.Group()  # If not already a group in Player
   ```

3. Update `reset_game()`:
   ```python
   def reset_game(self):
       self.player = Player(pygame.Vector2(self.screen_width // 2, self.screen_height // 2))
       self.asteroids.empty()
       self.bullets.empty()
       self.powerups.empty()
       self.ufos.empty()
       self.ufo_bullets.empty()
       self.explosion_particles.empty()
       # ... rest of reset logic
       self.spawn_asteroids()
   ```

4. Modify spawn methods to add to groups:
   - `spawn_asteroids()`: `self.asteroids.add(asteroid)`
   - Player shoot: `self.bullets.add(bullet)` (modify `player.py` to return bullets or add directly)
   - Power-up spawn: `self.powerups.add(powerup)`
   - UFO spawn: `self.ufos.add(ufo)`
   - Particle creation: `self.explosion_particles.add(particle)`

5. Update `update()` method:
   ```python
   def update(self, dt):
       keys = pygame.key.get_pressed()

       # Update player
       self.player.update(dt, keys, self.screen_width, self.screen_height)

       # Update groups
       self.bullets.update(dt, self.screen_width, self.screen_height)
       self.asteroids.update(dt, self.screen_width, self.screen_height)
       self.powerups.update(dt, self.screen_width, self.screen_height)
       self.ufos.update(dt, self.screen_width, self.screen_height)
       self.ufo_bullets.update(dt, self.screen_width, self.screen_height)
       self.explosion_particles.update(dt, self.screen_width, self.screen_height)
       self.player.thrust_particles.update(dt, self.screen_width, self.screen_height)

       # Remove inactive objects
       self.bullets = pygame.sprite.Group(b for b in self.bullets if b.active)
       self.powerups = pygame.sprite.Group(p for p in self.powerups if p.active)
       self.explosion_particles = pygame.sprite.Group(p for p in self.explosion_particles if p.active)
       self.player.thrust_particles = pygame.sprite.Group(p for p in self.player.thrust_particles if p.active)

       # ... rest of update logic
   ```

6. Update `draw_game()` method:
   ```python
   def draw_game(self):
       self.asteroids.draw(self.screen)
       self.bullets.draw(self.screen)
       self.powerups.draw(self.screen)
       self.ufos.draw(self.screen)
       self.ufo_bullets.draw(self.screen)
       self.explosion_particles.draw(self.screen)
       self.player.draw(self.screen)  # Player last to be on top
   ```

7. Update collision detection methods (from code quality task) to work with groups:
   - For bullet-asteroid: iterate through group.sprites()
   - Keep the same logic but adapt to group removal

8. Test thoroughly:
   - All objects spawn and move correctly
   - Collisions still work
   - Objects are removed properly
   - Performance improvement: measure FPS with many objects

**Expected Outcome**: Objects managed by Sprite Groups, automatic batching for update/draw operations.

## Task 2: Optimize Collision Detection with Sprite Groups
**File**: `game.py` (collision methods)  
**Description**: Use Pygame's built-in collision functions for better performance.

**Steps**:
1. Replace manual distance checks with `pygame.sprite.spritecollide` and `pygame.sprite.groupcollide`.

2. Update `_check_bullet_asteroid_collisions()`:
   ```python
   def _check_bullet_asteroid_collisions(self):
       # Use groupcollide for efficient collision detection
       hits = pygame.sprite.groupcollide(self.bullets, self.asteroids, False, False, collided=lambda bullet, asteroid: bullet.position.distance_to(asteroid.position) < bullet.radius + asteroid.radius)

       for bullet, asteroids in hits.items():
           for asteroid in asteroids:
               bullet.active = False  # Mark for removal
               # Handle armored asteroids
               if hasattr(asteroid, 'hitpoints'):
                   asteroid.hitpoints -= 1
                   if asteroid.hitpoints > 0:
                       continue
               # Destroy asteroid
               asteroid.active = False  # Mark for removal
               self.score += asteroid.score_value
               if SOUND_EXPLODE:
                   SOUND_EXPLODE.play()
               new_asteroids = asteroid.split()
               for new_asteroid in new_asteroids:
                   self.asteroids.add(new_asteroid)
               # Spawn power-up
               if random.random() < POWERUP_SPAWN_CHANCE:
                   powerup_type = random.choice(POWERUP_TYPES)
                   powerup = PowerUp(asteroid.position, powerup_type)
                   self.powerups.add(powerup)
               for _ in range(PARTICLE_COUNT_EXPLODE):
                   particle = Particle(asteroid.position)
                   self.explosion_particles.add(particle)

       # Remove inactive objects
       self.bullets = pygame.sprite.Group(b for b in self.bullets if b.active)
       self.asteroids = pygame.sprite.Group(a for a in self.asteroids if a.active)
   ```

3. Update `_check_bullet_ufo_collisions()` similarly:
   ```python
   def _check_bullet_ufo_collisions(self):
       hits = pygame.sprite.groupcollide(self.bullets, self.ufos, False, False, collided=lambda bullet, ufo: bullet.position.distance_to(ufo.position) < bullet.radius + ufo.radius)

       for bullet, ufos in hits.items():
           for ufo in ufos:
               bullet.active = False
               ufo.active = False
               self.score += UFO_SCORE
               if SOUND_EXPLODE:
                   SOUND_EXPLODE.play()
               for _ in range(PARTICLE_COUNT_EXPLODE):
                   particle = Particle(ufo.position)
                   self.explosion_particles.add(particle)

       self.bullets = pygame.sprite.Group(b for b in self.bullets if b.active)
       self.ufos = pygame.sprite.Group(u for u in self.ufos if u.active)
   ```

4. Update `_check_powerup_collection()`:
   ```python
   def _check_powerup_collection(self):
       hits = pygame.sprite.spritecollide(self.player, self.powerups, False, collided=lambda player, powerup: player.position.distance_to(powerup.position) < player.radius + powerup.radius)
       for powerup in hits:
           powerup.active = False
           self.apply_powerup(powerup.type)

       self.powerups = pygame.sprite.Group(p for p in self.powerups if p.active)
   ```

5. For player collisions, keep manual checks since player is not in a group:
   - Player vs asteroids: keep as is, but mark asteroids inactive
   - Player vs UFOs: keep as is, but mark UFOs inactive
   - UFO bullets vs player: keep as is

6. Update the collision methods to handle `active` flags instead of immediate removal.

7. Test performance:
   - Create a test with 50+ bullets and 20+ asteroids
   - Measure FPS before and after
   - Ensure no collision misses

**Expected Outcome**: Collision detection uses optimized Pygame functions, better performance with many objects.

## Task 3: Implement UI Text Caching
**File**: `game.py`  
**Description**: Cache rendered text surfaces to avoid re-rendering every frame.

**Steps**:
1. Add cache dictionary to `Game.__init__()`:
   ```python
   self.ui_text_cache = {}
   ```

2. Create helper method for cached text:
   ```python
   def _get_cached_text(self, key: str, text: str, color: tuple) -> pygame.Surface:
       cache_key = f"{key}_{text}_{color}"
       if cache_key not in self.ui_text_cache or self.ui_text_cache[cache_key][0] != text:
           surface = self.font.render(text, True, color)
           self.ui_text_cache[cache_key] = (text, surface)
       return self.ui_text_cache[cache_key][1]
   ```

3. Update `draw_game()` to use cached text:
   ```python
   score_text = self._get_cached_text("score", f"Score: {self.score}", WHITE)
   lives_text = self._get_cached_text("lives", f"Lives: {self.lives}", WHITE)
   level_text = self._get_cached_text("level", f"Level: {self.level}", WHITE)

   self.screen.blit(score_text, (UI_SCORE_X, UI_SCORE_Y))
   self.screen.blit(lives_text, (UI_LIVES_X, UI_LIVES_Y))
   self.screen.blit(level_text, (UI_LEVEL_X, UI_LEVEL_Y))

   if self.game_over:
       game_over_text = self._get_cached_text("game_over", "GAME OVER - Press R to restart, M for menu", RED)
       self.screen.blit(game_over_text, (self.screen_width // 2 - UI_GAME_OVER_X_OFFSET, UI_GAME_OVER_Y))
   ```

4. Update other draw methods similarly:
   - `draw_menu()`: cache "ASTEROIDS", "Press ENTER to Start", "Press H for High Scores"
   - `draw_highscores()`: cache title and back text
   - `draw_enter_name()`: cache prompt
   - `draw_pause_overlay()`: cache all pause texts

5. Clear cache when needed (e.g., on state change or score change).

6. Test:
   - UI renders correctly
   - Text updates when values change
   - Performance improvement in FPS (small but measurable)

**Expected Outcome**: UI text surfaces cached, reduced CPU usage for text rendering.

## Task 4: Implement Real Alpha for Particles
**File**: `particle.py`  
**Description**: Replace size-based fade with proper alpha blending for particles.

**Steps**:
1. Modify `Particle.__init__()` to remove size fade logic (keep alpha calculation).

2. Update `Particle.update()`:
   ```python
   def update(self, dt: float, screen_width: int, screen_height: int):
       self.lifetime -= dt
       if self.lifetime <= 0:
           self.active = False
       self.position += self.velocity * dt
       # Optional: fade velocity or wrap
   ```

3. Update `Particle.draw()` to use alpha surface:
   ```python
   def draw(self, screen: pygame.Surface):
       if self.lifetime <= 0:
           return

       size = 5  # Fixed size
       alpha = int(255 * (self.lifetime / PARTICLE_LIFETIME))

       # Create surface with alpha
       particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
       pygame.draw.circle(particle_surf, (*self.color, alpha), (size, size), size)

       # Blit to screen
       screen.blit(particle_surf, self.position - pygame.Vector2(size, size))
   ```

4. Test particle effects:
   - Explosion particles fade properly
   - Thrust particles look good
   - Performance: ensure not too many surfaces created per frame

**Expected Outcome**: Particles use real alpha blending instead of size fade, better visual quality.

## Testing and Validation
- Performance benchmarks: measure FPS with various object counts
- Collision accuracy: ensure no missed collisions
- Visual quality: check particle fading and UI rendering
- Memory usage: monitor for leaks with many particles
- Edge cases: test with maximum objects on screen

## Completion Criteria
- All object management migrated to Sprite Groups
- Collision detection optimized with Pygame functions
- UI text cached and rendering efficient
- Particles use alpha blending
- No performance regressions, ideally improvements