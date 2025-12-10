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