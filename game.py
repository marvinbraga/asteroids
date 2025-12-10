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
from game_renderer import GameRenderer
from game_logic import GameLogic
from state_machine import StateMachine
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
    """Main game class managing the Asteroids game loop, state, and components.

    Handles initialization, game loop, input processing, updating, rendering,
    and manages all game entities through sprite groups and state machine.
    """
    def __init__(self) -> None:
        """Initialize the game with all necessary components."""
        self._setup_pygame()
        self._setup_audio()
        self._setup_ui()
        self._load_config()
        self._setup_sprite_groups()
        self._setup_game_state()
        self._setup_state_machine()
        self._setup_managers()

    def _setup_pygame(self) -> None:
        """Initialize Pygame and basic display settings."""
        try:
            pygame.init()
        except pygame.error as e:
            raise RuntimeError(f"Failed to initialize Pygame: {e}")

        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Warning: Failed to initialize Pygame mixer: {e}. Audio will be disabled.")

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.fps = FPS

    def _setup_audio(self) -> None:
        """Load and initialize audio components."""
        global SOUND_SHOOT, SOUND_EXPLODE, SOUND_THRUST
        SOUND_SHOOT, SOUND_EXPLODE, SOUND_THRUST = load_sounds()
        init_channels()
        if os.path.exists(MUSIC_BACKGROUND):
            pygame.mixer.music.load(MUSIC_BACKGROUND)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)

    def _setup_ui(self) -> None:
        """Initialize UI components and caching."""
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.difficulty = 'normal'
        self.input_name = ""
        self.ui_text_cache = {}
        self.dirty_rects = []
        self.use_dirty_rects = True  # Enable optimized rendering

    def _load_config(self) -> None:
        """Load game configuration from JSON file."""
        config_path = 'config.json'
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            self.config = {}  # Fallback empty config

    def _setup_sprite_groups(self) -> None:
        """Initialize all sprite groups for game entities."""
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.explosion_particles = pygame.sprite.Group()

    def _setup_game_state(self) -> None:
        """Initialize game state variables."""
        self.apply_difficulty()
        self.score = 0
        self.lives = self.initial_lives
        self.level = INITIAL_LEVEL
        self.game_over = False
        self.player = None
        self.running = True
        self.start_time = pygame.time.get_ticks()
        self.logic = GameLogic(self)
        self.logic.reset_game()

    def _setup_state_machine(self) -> None:
        """Initialize the state machine with all game states."""
        self.state_machine = StateMachine(self)
        self.state_machine.add_state('menu', MenuState)
        self.state_machine.add_state('playing', PlayingState)
        self.state_machine.add_state('game_over', GameOverState)
        self.state_machine.add_state('highscores', HighscoresState)
        self.state_machine.add_state('enter_name', EnterNameState)
        self.state_machine.change_state('menu')

    def _setup_managers(self) -> None:
        """Initialize collision and rendering managers."""
        self.collision_manager = CollisionManager(self)
        self.renderer = GameRenderer(self)

    @property
    def states(self):
        """Property for backward compatibility."""
        return self.state_machine.states

    @property
    def current_state(self):
        """Property for backward compatibility."""
        return self.state_machine.current_state

    @property
    def state_name(self):
        """Property for backward compatibility."""
        return self.state_machine.state_name

    def change_state(self, new_state_name):
        self.state_machine.change_state(new_state_name)

    def update(self, dt: float) -> None:
        """Update game logic with delta time."""
        self.logic.update(dt)

    def handle_input(self, events, keys) -> None:
        """Process input events and key states."""
        self.state_machine.handle_input(events, keys)

    def draw(self) -> None:
        """Render the current game state to the screen."""
        self.renderer.draw(self.screen)

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

    def _get_cached_text(self, key: str, text: str, color: tuple[int, int, int]) -> pygame.Surface:
        cache_key = f"{key}_{text}_{color}"
        cached = self.ui_text_cache.get(cache_key)
        if cached is None or cached[0] != text:
            surface = self.font.render(text, True, color)
            self.ui_text_cache[cache_key] = (text, surface)
        return self.ui_text_cache[cache_key][1]

    def get_highscores(self):
        return get_highscores()

    def add_highscore(self, name, score):
        return add_highscore(name, score)

    def _reset_player_position(self) -> None:
        self.player.position = pygame.Vector2(self.screen_width // 2, self.screen_height // 2)
        self.player.velocity = pygame.Vector2(0, 0)
        self.player.rotation = 0
        self.player.invincible_timer = 2.0  # 2 seconds of invincibility

    def run(self) -> None:
        """Main game loop handling events, updates, and rendering."""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input(events, keys)

            if self.state_name == 'playing' and not self.game_over:
                self.update(dt)

            if self.state_name == 'playing' and self.game_over:
                if is_highscore(self.score):
                    self.change_state('enter_name')

            self.draw()

        pygame.quit()