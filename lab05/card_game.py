from __future__ import annotations
from typing import List, Tuple, Set
from copy import deepcopy

from game import GameState, Game, EnumAction


class CardAction(EnumAction):
    PLAY = 0
    REFUSE = 1


class CardState(GameState):
    def __init__(
        self,
        player_turn: int,
        deck: List[int],
        alpha: int,
        choices: List[CardAction],
        cards: List[Set[int]],
    ):
        super().__init__(player_turn)
        assert alpha >= 0
        self.deck = deck
        self.alpha = alpha
        self.choices = choices
        self.cards = cards

    def available_actions(self) -> List[CardAction]:
        return [CardAction.PLAY, CardAction.REFUSE]

    def result(self, action: CardAction) -> CardState:
        new_choices = self.choices
        new_choices[self.player_turn] = action
        new_deck = deepcopy(self.deck)
        new_cards = deepcopy(self.cards)
        if (
            self.player_turn == 1 and action == CardAction.PLAY
        ):  # P2 can choose a card from the deck
            if len(new_deck) > 0:
                new_card = new_deck[0]
                new_deck = new_deck[1:]
                new_cards[1].add(new_card)

        return CardState(
            1 - self.player_turn, new_deck, self.alpha, new_choices, new_cards
        )

    def is_goal(self) -> bool:
        return not None in self.choices

    def utilities(self) -> Tuple[int]:
        if self.choices[0] == CardAction.REFUSE:
            return (-1, 1)
        if self.choices[1] == CardAction.REFUSE:
            return (1, -1)
        if self.choices[1] == CardAction.PLAY:
            maxs = [max(c) for c in self.cards]
            if maxs[0] > maxs[1]:
                return (self.alpha, -self.alpha)
            else:
                return (-self.alpha, self.alpha)


class CardGame(Game):
    def __init__(self, deck: List[int], k: int, alpha: int):
        assert len(deck) >= 2 * k
        cards = [deck[:k], deck[k : (2 * k)]]
        deck = deck[(2 * k) :]
        super().__init__(CardState(0, deck, alpha, [None, None], cards))

    def perform_action(self, action: CardAction):
        self.state = self.state.result(action)
