import pygame
import random
from player import Player
from asteroid import Asteroid
from bullet import Bullet
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, FONT_SIZE,
    INITIAL_LIVES, INITIAL_LEVEL, BASE_ASTEROIDS, LEVEL_ASTEROID_INCREASE,
    ASTEROID_SPAWN_DISTANCE, SPEED_INCREASE_PER_LEVEL
)


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.font = pygame.font.Font(None, FONT_SIZE)

        self.reset_game()

    def reset_game(self):
        self.player = Player(pygame.Vector2(self.screen_width // 2, self.screen_height // 2))
        self.asteroids = []
        self.bullets = []
        self.score = 0
        self.lives = INITIAL_LIVES
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
                    asteroids_to_remove.append(asteroid)
                    self.score += asteroid.score_value
                    new_asteroids.extend(asteroid.split())
                    break

        # Remove collided objects
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        for asteroid in asteroids_to_remove:
            if asteroid in self.asteroids:
                self.asteroids.remove(asteroid)

        self.asteroids.extend(new_asteroids)

        # Player vs Asteroid
        for asteroid in self.asteroids:
            if self.player.position.distance_to(asteroid.position) < self.player.radius + asteroid.radius:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    # Reset player position
                    self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
                    self.player.velocity = pygame.Vector2(0, 0)
                break

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Update player
        self.player.update(dt, keys, self.screen_width, self.screen_height)

        # Shoot
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.append(bullet)

        # Update bullets
        self.bullets = [b for b in self.bullets if b.active]
        for bullet in self.bullets:
            bullet.update(dt, self.screen_width, self.screen_height)

        # Update asteroids
        for asteroid in self.asteroids:
            asteroid.update(dt, self.screen_width, self.screen_height)

        # Check collisions
        self.check_collisions()

        # Check level complete
        if not self.asteroids and not self.game_over:
            self.level += 1
            self.spawn_asteroids()

    def draw(self):
        self.screen.fill(BLACK)

        self.player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)

        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(level_text, (10, 90))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to restart", True, RED)
            self.screen.blit(game_over_text, (self.screen_width // 2 - 150, self.screen_height // 2))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            if not self.game_over:
                self.update(dt)
            self.draw()

        pygame.quit()