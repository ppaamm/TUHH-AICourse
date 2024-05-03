from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from typing import Union, Tuple, List
import math


class EnumAction(Enum):
    pass


class OtherAction(ABC):
    pass


Action = Union[OtherAction, OtherAction, int]


class GameState(ABC):
    def __init__(self, player_turn: int):
        self.player_turn = player_turn

    @abstractmethod
    def is_goal(self) -> bool:
        pass

    @abstractmethod
    def available_actions(self) -> List[Action]:
        pass

    @abstractmethod
    def result(self, action: Action) -> GameState:
        pass

    @abstractmethod
    def utilities(self) -> int:
        pass


class Game(ABC):
    def __init__(self, state):
        self.state = state
        self.done = False

    @abstractmethod
    def perform_action(self, action: Action):
        pass


def solve(state: GameState) -> int:
    # TODO: Question 8 => The method returns the optimal action for the current player
    return


