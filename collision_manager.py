import pygame
import random
from constants import SOUND_EXPLODE, UFO_SCORE, POWERUP_SPAWN_CHANCE, POWERUP_TYPES, PARTICLE_COUNT_EXPLODE
from powerup import PowerUp
from particle import Particle
from highscores import is_highscore

class CollisionManager:
    def __init__(self, game):
        self.game = game

    def check_collisions(self):
        self.lives_lost_this_frame = 0
        self._check_bullet_asteroid_collisions()
        self._check_bullet_ufo_collisions()
        self._check_powerup_collection()
        self._check_player_asteroid_collisions()
        self._check_player_ufo_collisions()
        self._check_ufo_bullet_player_collisions()

    def _check_bullet_asteroid_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.bullets, self.game.asteroids, False, False, collided=lambda bullet, asteroid: bullet.position.distance_to(asteroid.position) < bullet.radius + asteroid.radius)

        for bullet, asteroids in hits.items():
            for asteroid in asteroids:
                bullet.active = False
                if hasattr(asteroid, 'hitpoints'):
                    asteroid.hitpoints -= 1
                    if asteroid.hitpoints > 0:
                        continue
                asteroid.active = False
                self.game.score += asteroid.score_value
                if SOUND_EXPLODE:
                    SOUND_EXPLODE.play()
                new_asteroids = asteroid.split()
                self.game.asteroids.add(*new_asteroids)
                if random.random() < POWERUP_SPAWN_CHANCE:
                    powerup_type = random.choice(POWERUP_TYPES)
                    powerup = PowerUp(asteroid.position, powerup_type)
                    self.game.powerups.add(powerup)
                for _ in range(PARTICLE_COUNT_EXPLODE):
                    particle = Particle(asteroid.position)
                    self.game.explosion_particles.add(particle)

        self.game.bullets = pygame.sprite.Group(b for b in self.game.bullets if b.active)
        self.game.asteroids = pygame.sprite.Group(a for a in self.game.asteroids if a.active)

    def _check_bullet_ufo_collisions(self):
        hits = pygame.sprite.groupcollide(self.game.bullets, self.game.ufos, False, False, collided=lambda bullet, ufo: bullet.position.distance_to(ufo.position) < bullet.radius + ufo.radius)

        for bullet, ufos in hits.items():
            for ufo in ufos:
                bullet.active = False
                ufo.active = False
                self.game.score += UFO_SCORE
                if SOUND_EXPLODE:
                    SOUND_EXPLODE.play()
                for _ in range(PARTICLE_COUNT_EXPLODE):
                    particle = Particle(ufo.position)
                    self.game.explosion_particles.add(particle)

        self.game.bullets = pygame.sprite.Group(b for b in self.game.bullets if b.active)
        self.game.ufos = pygame.sprite.Group(u for u in self.game.ufos if u.active)

    def _check_powerup_collection(self):
        hits = pygame.sprite.spritecollide(self.game.player, self.game.powerups, False, collided=lambda player, powerup: player.position.distance_to(powerup.position) < player.radius + powerup.radius)
        for powerup in hits:
            powerup.active = False
            self.game.apply_powerup(powerup.type)

        self.game.powerups = pygame.sprite.Group(p for p in self.game.powerups if p.active)

    def _check_player_asteroid_collisions(self):
        for asteroid in self.game.asteroids.sprites():
            if self.game.player.position.distance_to(asteroid.position) < self.game.player.radius + asteroid.radius:
                if self.game.player.shielded:
                    self.game.player.shielded = False
                    asteroid.active = False
                    self.game.score += asteroid.score_value
                    new_asteroids = asteroid.split()
                    self.game.asteroids.add(*new_asteroids)
                else:
                    if self.lives_lost_this_frame == 0:
                        self.game.lives -= 1
                        self.lives_lost_this_frame += 1
                if self.game.lives <= 0:
                    self.game.game_over = True
                    if is_highscore(self.game.score):
                        self.game.state = 'enter_name'
                    else:
                        self.game.state = 'game_over'
                else:
                    self.game._reset_player_position()
                break

        self.game.asteroids = pygame.sprite.Group(a for a in self.game.asteroids if a.active)

    def _check_player_ufo_collisions(self):
        for ufo in self.game.ufos.sprites():
            if self.game.player.position.distance_to(ufo.position) < self.game.player.radius + ufo.radius:
                if self.lives_lost_this_frame == 0:
                    self.game.lives -= 1
                    self.lives_lost_this_frame += 1
                if self.game.lives <= 0:
                    self.game.game_over = True
                    if is_highscore(self.game.score):
                        self.game.state = 'enter_name'
                    else:
                        self.game.state = 'game_over'
                else:
                    self.game._reset_player_position()
                break

    def _check_ufo_bullet_player_collisions(self):
        for bullet in self.game.ufo_bullets.sprites():
            if bullet.position.distance_to(self.game.player.position) < bullet.radius + self.game.player.radius:
                if self.lives_lost_this_frame == 0:
                    self.game.lives -= 1
                    self.lives_lost_this_frame += 1
                if self.game.lives <= 0:
                    self.game.game_over = True
                    if is_highscore(self.game.score):
                        self.game.state = 'enter_name'
                    else:
                        self.game.state = 'game_over'
                else:
                    self.game._reset_player_position()
                bullet.active = False
                break

        self.game.ufo_bullets = pygame.sprite.Group(b for b in self.game.ufo_bullets if b.active)