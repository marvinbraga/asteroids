from typing import TYPE_CHECKING, Dict, Type

if TYPE_CHECKING:
    from game import Game
    from game_states import GameState

class StateMachine:
    def __init__(self, game: 'Game') -> None:
        self.game = game
        self.states: Dict[str, 'GameState'] = {}
        self.current_state: 'GameState' = None
        self.state_name: str = ''

    def add_state(self, name: str, state_class: Type['GameState']) -> None:
        self.states[name] = state_class(self.game)

    def change_state(self, new_state_name: str) -> None:
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[new_state_name]
        self.state_name = new_state_name
        self.current_state.enter()

    def handle_input(self, events, keys) -> None:
        if self.current_state:
            self.current_state.handle_input(events, keys)

    def update(self, dt: float) -> None:
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, screen) -> None:
        if self.current_state:
            self.current_state.draw(screen)