from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from typing import Union, Tuple, Collection


class EnumAction(Enum):
    pass


class OtherAction(ABC):
    pass


Action = Union[EnumAction, OtherAction, int]


class GameState(ABC):
    def __init__(self, player_turn: int):
        self.player_turn = player_turn

    @abstractmethod
    def is_goal(self) -> bool:
        pass

    @abstractmethod
    def available_actions(self) -> Collection[Action]:
        pass

    @abstractmethod
    def result(self, action: Action) -> GameState:
        pass

    @abstractmethod
    def utilities(self) -> Tuple[int]:
        pass


class Game(ABC):
    def __init__(self, state: GameState):
        self.state = state
        self.done = False

    @abstractmethod
    def perform_action(self, action: Action):
        pass


def solve(state: GameState) -> int:
    # TODO: Question 8 => The method returns the optimal action for the current player
    pass
