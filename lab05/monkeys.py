from __future__ import annotations
from typing import Set, Tuple
from copy import deepcopy

from game import GameState, EnumAction, Game, solve


class MonkeysState(GameState):
    def __init__(
        self,
        L: int,
        x1: int,
        x2: int,
        banana: int,
        step: int,
        step_limit: int,
        player_turn: int,
    ):
        super().__init__(player_turn)
        self.L = L
        self.xs = [x1, x2]
        self.banana = banana
        self.monkey_up = [False, True if x1 == x2 else False]
        self.grab = False
        self.step = step
        self.step_limit = step_limit

    def is_goal(self) -> bool:
        return self.grab or self.step == self.step_limit

    def available_actions(self) -> Set[MonkeysAction]:
        return set(
            [
                MonkeysAction.LEFT,
                MonkeysAction.RIGHT,
                MonkeysAction.GRAB,
                MonkeysAction.NOTHING,
            ]
        )

    def result(self, action: MonkeysAction) -> MonkeysState:
        new_state = deepcopy(self)
        new_state.step += 1
        new_state.player_turn = 1 - self.player_turn

        player = self.player_turn

        # NOTHING action
        if action == MonkeysAction.NOTHING:
            return new_state

        # GRAB action
        if action == MonkeysAction.GRAB:
            # Case 1: The agent is not under the banana
            if self.xs[player] != self.banana:
                return new_state
            else:
                if self.monkey_up[player]:
                    new_state.grab = True
                return new_state

        # LEFT action
        if action == MonkeysAction.LEFT:
            # Monkey is on the left:
            if self.xs[player] == 0:
                return new_state

            # Monkey is below the other: no change
            if self.monkey_up[1 - player]:
                return new_state

            new_state.xs[player] -= 1

            if self.monkey_up[player]:
                # Monkey was up, goes down
                new_state.monkey_up[player] = False

            if new_state.xs[0] == new_state.xs[1]:
                new_state.monkey_up[player] = True

        # RIGHT action
        if action == MonkeysAction.RIGHT:
            # Monkey is on the right:
            if self.xs[player] == self.L - 1:
                return new_state

            # Monkey is below the other: no change
            if self.monkey_up[1 - player]:
                return new_state

            new_state.xs[player] += 1

            if self.monkey_up[player]:
                # Monkey was up, goes down
                new_state.monkey_up[player] = False

            if new_state.xs[0] == new_state.xs[1]:
                new_state.monkey_up[player] = True
        return new_state

    def utilities(self) -> Tuple[int]:
        if self.grab:
            return (1, 1)

        return (0, 0)


class MonkeysAction(EnumAction):
    LEFT = 1
    RIGHT = 2
    GRAB = 3
    NOTHING = 4


class MonkeysGame(Game):
    def __init__(
        self, L: int, x1_init: int, x2_init: int, banana: int, step_limit: int
    ):
        super().__init__(MonkeysState(L, x1_init, x2_init, banana, 0, step_limit, 0))

    def perform_action(self, action: MonkeysAction):
        self.state = self.state.result(action)
        if self.state.is_goal():
            self.done = True
            if self.state.grab:
                print(
                    f"== Player {1 - self.state.player_turn + 1} grabbed the banana! =="
                )
            else:
                print("== The monkeys could not grab the banana in time :( ==")


game = MonkeysGame(L=10, x1_init=0, x2_init=5, banana=3, step_limit=8)
while not game.done:
    a = solve(game.state)
    print(f"Player {game.state.player_turn + 1}'s action: {a}")
    game.perform_action(a)
print("Utilities:", game.state.utilities())
