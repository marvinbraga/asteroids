import pygame
import random
import os
from player import Player
from asteroid import Asteroid
from bullet import Bullet
from particle import Particle
from powerup import PowerUp
from ufo import UFO
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, FONT_SIZE,
    INITIAL_LIVES, INITIAL_LEVEL, BASE_ASTEROIDS, LEVEL_ASTEROID_INCREASE,
    ASTEROID_SPAWN_DISTANCE, SPEED_INCREASE_PER_LEVEL,
    POWERUP_SPAWN_CHANCE, POWERUP_TYPES, POWERUP_DURATION,
    UFO_SPAWN_LEVEL, UFO_SPAWN_CHANCE, UFO_SCORE,
    PARTICLE_COUNT_EXPLODE,
    load_sounds, init_channels, MUSIC_BACKGROUND, MUSIC_VOLUME, SOUND_EXPLODE
)
from highscores import get_highscores, add_highscore, is_highscore
from highscores import add_highscore, get_highscores, is_highscore


class Game:
    def __init__(self):
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

        load_sounds()
        init_channels()
        if os.path.exists(MUSIC_BACKGROUND):
            pygame.mixer.music.load(MUSIC_BACKGROUND)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)

        self.apply_difficulty()
        self.reset_game()

    def apply_difficulty(self):
        if self.difficulty == 'easy':
            self.initial_lives = 5
            self.ufo_spawn_chance = 0.02
        elif self.difficulty == 'hard':
            self.initial_lives = 2
            self.ufo_spawn_chance = 0.08
        else:  # normal
            self.initial_lives = 3
            self.ufo_spawn_chance = 0.05

    def reset_game(self):
        self.player = Player(pygame.Vector2(self.screen_width // 2, self.screen_height // 2))
        self.asteroids = []
        self.bullets = []
        self.powerups = []
        self.ufos = []
        self.ufo_bullets = []
        self.explosion_particles = []
        self.explosion_particles = []
        self.score = 0
        self.lives = self.initial_lives
        self.level = INITIAL_LEVEL
        self.game_over = False
        self.spawn_asteroids()

    def spawn_asteroids(self):
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
            self.asteroids.append(asteroid)

    def check_collisions(self):
        # Bullet vs Asteroid
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
                            # Don't destroy yet
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

        # Power-up collection
        powerups_to_remove = []
        for powerup in self.powerups:
            if self.player.position.distance_to(powerup.position) < self.player.radius + powerup.radius:
                powerups_to_remove.append(powerup)
                self.apply_powerup(powerup.type)

        for powerup in powerups_to_remove:
            self.powerups.remove(powerup)

        # Player vs Asteroid
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

        # Bullet vs UFO
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

        # UFO bullet vs Player
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

        # Player vs UFO (similar to asteroid)
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

    def apply_powerup(self, type_: str):
        self.player.powerup_timer = POWERUP_DURATION
        if type_ == 'shield':
            self.player.shielded = True
        elif type_ == 'speed':
            self.player.speed_boost = 1.5
        elif type_ == 'multishot':
            self.player.multishot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Update player
        self.player.update(dt, keys, self.screen_width, self.screen_height)

        # Shoot
        if keys[pygame.K_SPACE]:
            bullets = self.player.shoot()
            self.bullets.extend(bullets)

        # Update bullets
        self.bullets = [b for b in self.bullets if b.active]
        for bullet in self.bullets:
            bullet.update(dt, self.screen_width, self.screen_height)

        # Update asteroids
        for asteroid in self.asteroids:
            asteroid.update(dt, self.screen_width, self.screen_height)

        # Update power-ups
        self.powerups = [p for p in self.powerups if p.active]
        for powerup in self.powerups:
            powerup.update(dt, self.screen_width, self.screen_height)

        # Spawn UFOs
        if self.level >= UFO_SPAWN_LEVEL and len(self.ufos) < 2 and random.random() < UFO_SPAWN_CHANCE:
            # Spawn at top or bottom
            y = 0 if random.random() > 0.5 else self.screen_height
            x = random.randint(0, self.screen_width)
            ufo = UFO(pygame.Vector2(x, y), self.screen_width)
            self.ufos.append(ufo)

        # Update UFOs
        for ufo in self.ufos:
            ufo.update(dt, self.screen_width, self.screen_height, self.player.position)
            bullet = ufo.shoot(self.player.position)
            if bullet:
                self.ufo_bullets.append(bullet)

        self.ufo_bullets = [b for b in self.ufo_bullets if b.active]
        for bullet in self.ufo_bullets:
            bullet.update(dt, self.screen_width, self.screen_height)

        # Check collisions
        self.check_collisions()

        # Update explosion particles
        self.explosion_particles = [p for p in self.explosion_particles if p.active]
        for particle in self.explosion_particles:
            particle.update(dt, self.screen_width, self.screen_height)

        # Check level complete
        if not self.asteroids and not self.game_over:
            self.level += 1
            # Automatic upgrade every 5 levels
            if self.level % 5 == 0:
                self.lives += 1
            self.spawn_asteroids()

    def draw(self):
        self.screen.fill(BLACK)

        if self.state in ('playing', 'game_over'):
            self.draw_game()
        elif self.state == 'menu':
            self.draw_menu()
        elif self.state == 'highscores':
            self.draw_highscores()
        elif self.state == 'enter_name':
            self.draw_enter_name()

        pygame.display.flip()

    def draw_game(self):
        # Existing game draw code
        self.player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        for ufo in self.ufos:
            ufo.draw(self.screen)
        for bullet in self.ufo_bullets:
            bullet.draw(self.screen)
        for particle in self.explosion_particles:
            particle.draw(self.screen)
        # for ufo in self.ufos:
        #     ufo.draw(self.screen)  # Commented out since ufos not implemented

        # UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(level_text, (10, 90))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to restart, M for menu", True, RED)
            self.screen.blit(game_over_text, (self.screen_width // 2 - 200, self.screen_height // 2))

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

        self.screen.blit(pause_text, (self.screen_width // 2 - 50, self.screen_height // 2 - 100))
        self.screen.blit(resume_text, (self.screen_width // 2 - 60, self.screen_height // 2 - 50))
        self.screen.blit(restart_text, (self.screen_width // 2 - 60, self.screen_height // 2))
        self.screen.blit(menu_text, (self.screen_width // 2 - 70, self.screen_height // 2 + 50))

    def draw_menu(self):
        title = self.font.render("ASTEROIDS", True, WHITE)
        start = self.font.render("Press ENTER to Start", True, WHITE)
        highscores = self.font.render("Press H for High Scores", True, WHITE)

        self.screen.blit(title, (self.screen_width // 2 - 50, self.screen_height // 2 - 100))
        self.screen.blit(start, (self.screen_width // 2 - 100, self.screen_height // 2 - 50))
        self.screen.blit(highscores, (self.screen_width // 2 - 120, self.screen_height // 2))

    def draw_highscores(self):
        # From highscores task
        title = self.font.render("HIGH SCORES", True, WHITE)
        self.screen.blit(title, (self.screen_width // 2 - 70, 50))
        scores = get_highscores()
        for i, entry in enumerate(scores):
            text = self.font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, WHITE)
            self.screen.blit(text, (self.screen_width // 2 - 100, 100 + i * 40))
        back = self.font.render("Press ESC to go back", True, WHITE)
        self.screen.blit(back, (self.screen_width // 2 - 100, self.screen_height - 50))

    def draw_enter_name(self):
        # From highscores task
        prompt = self.font.render("Enter your name:", True, WHITE)
        name_text = self.font.render(self.input_name, True, WHITE)
        self.screen.blit(prompt, (self.screen_width // 2 - 80, self.screen_height // 2 - 50))
        self.screen.blit(name_text, (self.screen_width // 2 - len(self.input_name)*5, self.screen_height // 2))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == 'menu':
                        if event.key == pygame.K_RETURN or event.key == pygame.K_1:
                            self.state = 'playing'
                            self.reset_game()
                        elif event.key == pygame.K_h or event.key == pygame.K_2:
                            self.state = 'highscores'
                        elif event.key == pygame.K_4:
                            difficulties = ['easy', 'normal', 'hard']
                            current_index = difficulties.index(self.difficulty)
                            self.difficulty = difficulties[(current_index + 1) % len(difficulties)]
                            self.apply_difficulty()
                        elif event.key == pygame.K_q or event.key == pygame.K_3:
                            running = False
                    elif self.state == 'highscores':
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'menu'
                    elif self.state == 'game_over':
                        if event.key == pygame.K_r:
                            self.state = 'playing'
                            self.reset_game()
                        elif event.key == pygame.K_m:
                            self.state = 'menu'
                    elif self.state == 'enter_name':
                        if event.key == pygame.K_RETURN and self.input_name:
                            add_highscore(self.input_name, self.score)
                            self.input_name = ""
                            self.state = 'highscores'
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_name = self.input_name[:-1]
                        else:
                            if len(self.input_name) < 5:  # Limit name length to 5
                                self.input_name += event.unicode.upper()

            if self.state == 'playing' and not self.game_over:
                self.update(dt)

            if self.state == 'playing' and self.game_over:
                if is_highscore(self.score):
                    self.state = 'enter_name'

            self.draw()

        pygame.quit()