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