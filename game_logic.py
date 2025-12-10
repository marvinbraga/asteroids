import pygame
import random
from typing import TYPE_CHECKING
from player import Player
from asteroid import Asteroid
from ufo import UFO
from constants import (
    INITIAL_LIVES, INITIAL_LEVEL, BASE_ASTEROIDS, LEVEL_ASTEROID_INCREASE,
    ASTEROID_SPAWN_DISTANCE, SPEED_INCREASE_PER_LEVEL, UFO_SPAWN_LEVEL, UFO_SPAWN_CHANCE
)

if TYPE_CHECKING:
    from game import Game

class GameLogic:
    def __init__(self, game: 'Game') -> None:
        self.game = game

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        # Update player
        self.game.player.update(dt, keys, self.game.screen_width, self.game.screen_height)

        # Shoot
        if keys[pygame.K_SPACE]:
            bullets = self.game.player.shoot()
            self.game.bullets.add(*bullets)

        # Update groups
        self.game.bullets.update(dt, self.game.screen_width, self.game.screen_height)
        self.game.asteroids.update(dt, self.game.screen_width, self.game.screen_height)
        self.game.powerups.update(dt, self.game.screen_width, self.game.screen_height)

        # Spawn UFOs
        if self.game.level >= UFO_SPAWN_LEVEL and len(self.game.ufos.sprites()) < 2 and random.random() < self.game.ufo_spawn_chance:
            # Spawn at top or bottom
            y = 0 if random.random() > 0.5 else self.game.screen_height
            x = random.randint(0, self.game.screen_width)
            ufo = UFO(pygame.Vector2(x, y), self.game.screen_width)
            self.game.ufos.add(ufo)

        # Update UFOs
        for ufo in self.game.ufos:
            ufo.update(dt, self.game.screen_width, self.game.screen_height, self.game.player.position)
            bullet = ufo.shoot(self.game.player.position)
            if bullet:
                self.game.ufo_bullets.add(bullet)

        self.game.ufos.update(dt, self.game.screen_width, self.game.screen_height)
        self.game.ufo_bullets.update(dt, self.game.screen_width, self.game.screen_height)

        # Check collisions
        self.game.collision_manager.check_collisions()

        # Update particles
        self.game.explosion_particles.update(dt, self.game.screen_width, self.game.screen_height)
        self.game.player.thrust_particles.update(dt, self.game.screen_width, self.game.screen_height)

        # Check level complete
        if not self.game.asteroids and not self.game.game_over:
            self.game.level += 1
            # Automatic upgrade every 5 levels
            if self.game.level % 5 == 0:
                self.game.lives += 1
            self.spawn_asteroids()

    def spawn_asteroids(self) -> None:
        num_asteroids = BASE_ASTEROIDS + self.game.level * LEVEL_ASTEROID_INCREASE
        for _ in range(num_asteroids):
            # Spawn away from player
            while True:
                pos = pygame.Vector2(random.randint(0, self.game.screen_width), random.randint(0, self.game.screen_height))
                if pos.distance_to(self.game.player.position) > ASTEROID_SPAWN_DISTANCE:
                    break
            asteroid = Asteroid(pos, 'large')
            # Increase speed with level
            asteroid.velocity *= 1.0 + (self.game.level - 1) * SPEED_INCREASE_PER_LEVEL
            self.game.asteroids.add(asteroid)

    def apply_powerup(self, type_: str) -> None:
        self.game.player.powerup_timer = self.game.constants.POWERUP_DURATION
        if type_ == 'shield':
            self.game.player.shielded = True
        elif type_ == 'speed':
            self.game.player.speed_boost = 1.5
        elif type_ == 'multishot':
            self.game.player.multishot = True

    def reset_game(self) -> None:
        self.game.player = Player(pygame.Vector2(self.game.screen_width // 2, self.game.screen_height // 2))
        self.game.asteroids.empty()
        self.game.bullets.empty()
        self.game.powerups.empty()
        self.game.ufos.empty()
        self.game.ufo_bullets.empty()
        self.game.explosion_particles.empty()
        self.game.player.thrust_particles.empty()
        self.game.score = 0
        self.game.lives = self.game.initial_lives
        self.game.level = INITIAL_LEVEL
        self.game.game_over = False
        self.spawn_asteroids()