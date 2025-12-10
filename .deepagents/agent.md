# Asteroids Game

A classic Asteroids arcade game implemented in Python using Pygame, featuring player-controlled spaceship, destructible asteroids, progressive difficulty, score tracking, and a lives system.

## Project Type
- **Primary language(s)**: Python
- **Framework(s) used**: None (utilizes Pygame library for game development)
- **Package manager**: uv/pip
- **Monorepo**: Not applicable (single-project structure)

## Architecture Overview
This project implements a simple arcade game using object-oriented programming in Python. Key components include a main game loop in `game.py`, game object classes (e.g., `GameObject`, `Player`, `Asteroid`, `Bullet`) for entities, and a `main.py` entry point that initializes and runs the game via Pygame.

## Directory Structure
- `__pycache__/`: Directory containing compiled Python bytecode files (generated automatically, can be ignored or deleted).
- Root directory: Contains all source files, configuration, and documentation for the game.

## Key Files
- `main.py`: Entry point of the application; initializes and starts the game.
- `game.py`: Contains the main `Game` class with the game loop, event handling, updates, and rendering.
- `player.py`: Defines the `Player` class for the spaceship, including movement and shooting.
- `asteroid.py`: Defines the `Asteroid` class for asteroids, including splitting behavior.
- `bullet.py`: Defines the `Bullet` class for projectiles fired by the player.
- `game_object.py`: Base class for game entities, providing common attributes like position and velocity.
- `constants.py`: Contains game constants such as screen dimensions, speeds, and colors.
- `pyproject.toml`: Project configuration file with dependencies and metadata.
- `uv.lock`: Lock file for dependency management via uv.
- `README.md`: Documentation with features, controls, and setup instructions.

## Development Commands
- **Install dependencies**: `pip install pygame` (or use uv if preferred, based on `uv.lock`).
- **Run the project**: `python main.py`.
- **Test the project**: `pytest` (assumes tests are set up, but no test files are visible in the structure).
- **Build the project**: Not specified (no build script detected; project runs directly with Python).
- **Lint the project**: Not specified (no linting configuration detected).

## Coding Conventions
- Uses standard Python naming conventions (e.g., classes in CamelCase, functions/methods in snake_case).
- Employs object-oriented design with inheritance (e.g., `GameObject` as a base class).
- Code style appears informal and game-focused, with no explicit style guide mentioned (e.g., no PEP 8 enforcement or formatter like Black detected).
- Best practices: Modular classes for game entities, separation of concerns (e.g., constants in a dedicated file), and use of Pygame's event-driven structure.

## Important Notes
- Requires Python 3.13+ and Pygame 2.6.1+ (as per `pyproject.toml` and README).
- Controls: Arrow keys/WASD for movement/rotation, Space to shoot, R to restart on game over.
- No automated testing or linting setup is evident; developers may need to add these (e.g., via pytest or flake8) for better practices.
- Project is lightweight and self-contained, suitable for rapid prototyping or learning Pygame.