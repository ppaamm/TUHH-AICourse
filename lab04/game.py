from enum import Enum
from abc import ABC, abstractmethod
from typing import Union, Set


class Player(Enum):
    MAX = 0  # Player 1
    MIN = 1  # Player 2


class GameState(ABC):
    def __init__(self, turn: Player):
        self.turn = turn


class EnumAction(Enum):
    pass


class OtherAction(ABC):
    pass


Action = Union[OtherAction, OtherAction]


class Game(ABC):
    def __init__(self, state):
        self.state = state
        self.done = False

    @abstractmethod
    def perform_action(self, action: Action):
        pass
