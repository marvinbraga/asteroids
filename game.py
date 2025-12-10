import pygame
import random
import os
import json
from typing import List, Optional
from player import Player
from asteroid import Asteroid
from bullet import Bullet
from particle import Particle
from powerup import PowerUp
from ufo import UFO
from game_states import MenuState, PlayingState, GameOverState, HighscoresState, EnterNameState
from collision_manager import CollisionManager
from event_manager import EventManager
from factories import AsteroidFactory, PowerUpFactory, UFOFactory, ParticleFactory
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, FONT_SIZE,
    INITIAL_LIVES, INITIAL_LEVEL, BASE_ASTEROIDS, LEVEL_ASTEROID_INCREASE,
    ASTEROID_SPAWN_DISTANCE, SPEED_INCREASE_PER_LEVEL,
    POWERUP_SPAWN_CHANCE, POWERUP_TYPES, POWERUP_DURATION,
    UFO_SPAWN_LEVEL, UFO_SPAWN_CHANCE, UFO_SCORE,
    PARTICLE_COUNT_EXPLODE,
    load_sounds, init_channels, MUSIC_BACKGROUND, MUSIC_VOLUME, SOUND_EXPLODE,
    UI_SCORE_X, UI_SCORE_Y, UI_LIVES_X, UI_LIVES_Y, UI_LEVEL_X, UI_LEVEL_Y,
    UI_GAME_OVER_X_OFFSET, UI_GAME_OVER_Y, UI_TITLE_X, UI_TITLE_Y,
    UI_START_X, UI_START_Y, UI_HIGHSCORES_X, UI_HIGHSCORES_Y,
    UI_BACK_X, UI_BACK_Y, UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y,
    UI_ENTER_NAME_TEXT_Y, UI_PAUSE_TITLE_X, UI_PAUSE_TITLE_Y,
    UI_RESUME_X, UI_RESUME_Y, UI_RESTART_X, UI_RESTART_Y,
    UI_MENU_X, UI_MENU_Y
)
from highscores import get_highscores, add_highscore, is_highscore


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.difficulty = 'normal'
        self.state = 'menu'
        self.input_name = ""
        self.ui_text_cache = {}
        self.dirty_rects = []
        self.use_dirty_rects = False  # Set to True to enable

        load_sounds()
        init_channels()
        if os.path.exists(MUSIC_BACKGROUND):
            pygame.mixer.music.load(MUSIC_BACKGROUND)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)

        # Load config
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        # Initialize sprite groups first
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.explosion_particles = pygame.sprite.Group()

        self.apply_difficulty()
        self.reset_game()

        # Initialize states
        self.states = {
            'menu': MenuState(self),
            'playing': PlayingState(self),
            'game_over': GameOverState(self),
            'highscores': HighscoresState(self),
            'enter_name': EnterNameState(self)
        }
        self.current_state = self.states['menu']
        self.state_name = 'menu'

        # Initialize managers
        self.collision_manager = CollisionManager(self)

    def change_state(self, new_state_name):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[new_state_name]
        self.state_name = new_state_name
        self.current_state.enter()

    def apply_difficulty(self) -> None:
        if self.difficulty == 'easy':
            self.initial_lives = 5
            self.ufo_spawn_chance = 0.02
        elif self.difficulty == 'hard':
            self.initial_lives = 2
            self.ufo_spawn_chance = 0.08
        else:  # normal
            self.initial_lives = 3
            self.ufo_spawn_chance = 0.05

    def reset_game(self) -> None:
        self.player = Player(pygame.Vector2(self.screen_width // 2, self.screen_height // 2))
        self.asteroids.empty()
        self.bullets.empty()
        self.powerups.empty()
        self.ufos.empty()
        self.ufo_bullets.empty()
        self.explosion_particles.empty()
        self.player.thrust_particles.empty()
        self.score = 0
        self.lives = self.initial_lives
        self.level = INITIAL_LEVEL
        self.game_over = False
        self.spawn_asteroids()

    def spawn_asteroids(self) -> None:
        num_asteroids = BASE_ASTEROIDS + self.level * LEVEL_ASTEROID_INCREASE
        for _ in range(num_asteroids):
            # Spawn away from player
            while True:
                pos = pygame.Vector2(random.randint(0, self.screen_width), random.randint(0, self.screen_height))
                if pos.distance_to(self.player.position) > ASTEROID_SPAWN_DISTANCE:
                    break
            asteroid = Asteroid(pos, 'large')
            # Increase speed with level
            asteroid.velocity *= 1.0 + (self.level - 1) * SPEED_INCREASE_PER_LEVEL
            self.asteroids.add(asteroid)

    def check_collisions(self) -> None:
        self._check_bullet_asteroid_collisions()
        self._check_bullet_ufo_collisions()
        self._check_powerup_collection()
        self._check_player_asteroid_collisions()
        self._check_player_ufo_collisions()
        self._check_ufo_bullet_player_collisions()

    def apply_powerup(self, type_: str):
        self.player.powerup_timer = POWERUP_DURATION
        if type_ == 'shield':
            self.player.shielded = True
        elif type_ == 'speed':
            self.player.speed_boost = 1.5
        elif type_ == 'multishot':
            self.player.multishot = True

    def _reset_player_position(self):
        self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
        self.player.velocity = pygame.Vector2(0, 0)

    def _get_cached_text(self, key: str, text: str, color: tuple) -> pygame.Surface:
        cache_key = f"{key}_{text}_{color}"
        if cache_key not in self.ui_text_cache or self.ui_text_cache[cache_key][0] != text:
            surface = self.font.render(text, True, color)
            self.ui_text_cache[cache_key] = (text, surface)
        return self.ui_text_cache[cache_key][1]

    def _check_bullet_asteroid_collisions(self):
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

    def _check_powerup_collection(self):
        hits = pygame.sprite.spritecollide(self.player, self.powerups, False, collided=lambda player, powerup: player.position.distance_to(powerup.position) < player.radius + powerup.radius)
        for powerup in hits:
            powerup.active = False
            self.apply_powerup(powerup.type)

        self.powerups = pygame.sprite.Group(p for p in self.powerups if p.active)

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
                        self.asteroids.add(*new_asteroids)
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
                    self._reset_player_position()
                break

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
                    self._reset_player_position()
                break

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
                    self._reset_player_position()
                ufo_bullets_to_remove.append(bullet)
                break

        for bullet in ufo_bullets_to_remove:
            if bullet in self.ufo_bullets:
                self.ufo_bullets.remove(bullet)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Update player
        self.player.update(dt, keys, self.screen_width, self.screen_height)

        # Shoot
        if keys[pygame.K_SPACE]:
            bullets = self.player.shoot()
            self.bullets.add(*bullets)

        # Update groups
        self.bullets.update(dt, self.screen_width, self.screen_height)
        self.asteroids.update(dt, self.screen_width, self.screen_height)
        self.powerups.update(dt, self.screen_width, self.screen_height)

        # Spawn UFOs
        if self.level >= UFO_SPAWN_LEVEL and len(self.ufos.sprites()) < 2 and random.random() < UFO_SPAWN_CHANCE:
            # Spawn at top or bottom
            y = 0 if random.random() > 0.5 else self.screen_height
            x = random.randint(0, self.screen_width)
            ufo = UFO(pygame.Vector2(x, y), self.screen_width)
            self.ufos.add(ufo)

        # Update UFOs
        for ufo in self.ufos:
            ufo.update(dt, self.screen_width, self.screen_height, self.player.position)
            bullet = ufo.shoot(self.player.position)
            if bullet:
                self.ufo_bullets.add(bullet)

        self.ufos.update(dt, self.screen_width, self.screen_height)
        self.ufo_bullets.update(dt, self.screen_width, self.screen_height)

        # Check collisions
        self.check_collisions()

        # Update particles
        self.explosion_particles.update(dt, self.screen_width, self.screen_height)
        self.player.thrust_particles.update(dt, self.screen_width, self.screen_height)

        # Check level complete
        if not self.asteroids and not self.game_over:
            self.level += 1
            # Automatic upgrade every 5 levels
            if self.level % 5 == 0:
                self.lives += 1
            self.spawn_asteroids()

    def draw(self):
        self.screen.fill(BLACK)
        self.current_state.draw(self.screen)
        pygame.display.flip()

    def handle_input(self, events, keys):
        self.current_state.handle_input(events, keys)

    def draw_game(self):
        # Draw sprite groups manually since we have custom draw methods
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        for ufo in self.ufos:
            ufo.draw(self.screen)
        for bullet in self.ufo_bullets:
            bullet.draw(self.screen)
        for particle in self.explosion_particles:
            particle.draw(self.screen)
        self.player.draw(self.screen)  # Player last

        # UI
        score_text = self._get_cached_text("score", f"Score: {self.score}", WHITE)
        lives_text = self._get_cached_text("lives", f"Lives: {self.lives}", WHITE)
        level_text = self._get_cached_text("level", f"Level: {self.level}", WHITE)
        self.screen.blit(score_text, (UI_SCORE_X, UI_SCORE_Y))
        self.screen.blit(lives_text, (UI_LIVES_X, UI_LIVES_Y))
        self.screen.blit(level_text, (UI_LEVEL_X, UI_LEVEL_Y))

    def draw_pause_overlay(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font.render("PAUSED", True, WHITE)
        resume_text = self.font.render("R: Resume", True, WHITE)
        restart_text = self.font.render("S: Restart", True, WHITE)
        menu_text = self.font.render("M: Main Menu", True, WHITE)

        self.screen.blit(pause_text, (UI_PAUSE_TITLE_X, UI_PAUSE_TITLE_Y))
        self.screen.blit(resume_text, (UI_RESUME_X, UI_RESUME_Y))
        self.screen.blit(restart_text, (UI_RESTART_X, UI_RESTART_Y))
        self.screen.blit(menu_text, (UI_MENU_X, UI_MENU_Y))

    def draw_menu(self):
        title = self.font.render("ASTEROIDS", True, WHITE)
        start = self.font.render("Press ENTER to Start", True, WHITE)
        highscores = self.font.render("Press H for High Scores", True, WHITE)

        self.screen.blit(title, (UI_TITLE_X, UI_TITLE_Y))
        self.screen.blit(start, (UI_START_X, UI_START_Y))
        self.screen.blit(highscores, (UI_HIGHSCORES_X, UI_HIGHSCORES_Y))

    def draw_highscores(self):
        # From highscores task
        title = self.font.render("HIGH SCORES", True, WHITE)
        self.screen.blit(title, (self.screen_width // 2 - 70, 50))
        scores = get_highscores()
        for i, entry in enumerate(scores):
            text = self.font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, WHITE)
            self.screen.blit(text, (self.screen_width // 2 - 100, 100 + i * 40))
        back = self.font.render("Press ESC to go back", True, WHITE)
        self.screen.blit(back, (UI_BACK_X, UI_BACK_Y))

    def draw_enter_name(self):
        # From highscores task
        prompt = self.font.render("Enter your name:", True, WHITE)
        name_text = self.font.render(self.input_name, True, WHITE)
        self.screen.blit(prompt, (UI_ENTER_NAME_PROMPT_X, UI_ENTER_NAME_PROMPT_Y))
        self.screen.blit(name_text, (self.screen_width // 2 - len(self.input_name)*5, UI_ENTER_NAME_TEXT_Y))

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
                if is_highscore(self.score):
                    self.change_state('enter_name')

            self.draw()

        pygame.quit()