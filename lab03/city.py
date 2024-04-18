from typing import List
from enum import Enum


class TouristAction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class TouristState:
    def __init__(self, ave: int, street: str):
        self.ave: int = ave
        self.street: str = street

    def as_tuple(self):
        return (self.ave, self.street)

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __hash__(self):
        return self.as_tuple().__hash__()

    def __repr__(self):
        return self.as_tuple().__repr__()


initial_state = TouristState(1, "A")
stun_states = set([TouristState(2, "A"), TouristState(2, "C"), TouristState(4, "B")])
bad_restaurants = [
    ((2, "A"), (3, "A")),
    ((1, "B"), (1, "C")),
    ((4, "B"), (4, "C")),
]
good_restaurants = [
    ((4, "A"), (4, "B")),
    ((2, "C"), (3, "C")),
]
bad_restaurants += [(b, a) for (a, b) in bad_restaurants]
good_restaurants += [(b, a) for (a, b) in good_restaurants]


def available_actions(state: TouristState):
    return [
        x
        for x in [
            TouristAction.UP if state.street != "A" else None,
            TouristAction.DOWN if state.street != "C" else None,
            TouristAction.LEFT if state.ave != 1 else None,
            TouristAction.RIGHT if state.ave != 4 else None,
        ]
        if x is not None
    ]


def _move_deterministic(state: TouristState, action: TouristAction):
    if action == TouristAction.UP:
        new_street = chr(ord(state.street) - 1)
        return TouristState(state.ave, new_street)
    elif action == TouristAction.DOWN:
        new_street = chr(ord(state.street) + 1)
        return TouristState(state.ave, new_street)
    elif action == TouristAction.LEFT:
        return TouristState(state.ave - 1, state.street)
    elif action == TouristAction.RIGHT:
        return TouristState(state.ave + 1, state.street)


def resulting_states(state, action):
    assert action in available_actions(state), "Invalid action"

    results = set()
    if state in stun_states:
        for actions in available_actions(state):
            results.add(_move_deterministic(state, actions))
    else:
        results.add(_move_deterministic(state, action))

    return results


def or_search(state, path: List):
    if len(path) > 0:
        if (state.as_tuple(), path[0].as_tuple()) in good_restaurants:
            return []
        elif (state.as_tuple(), path[0].as_tuple()) in bad_restaurants:
            return None
    if state in path:
        return None
    for action in available_actions(state):
        plan = and_search(resulting_states(state, action), [state] + path)
        if plan:
            return [action, plan]
    return None


def and_search(states, path: List):
    # TODO: 
    # In case of success: Return a dictionary of plans, associating to each child state a plan reaching the end
    # Otherwise: return None
    plans = {}
    return plans


def and_or_search():
    return or_search(initial_state, [])


def print_plan(plan, depth=0):
    if plan == []:
        print(2 * depth * " " + "SUCCESS")
        return
    elif plan == None:
        print(2 * depth * " " + "FAILURE")
        return

    for a in plan:
        if isinstance(a, TouristAction):
            print(2 * depth * " " + a.name)
        else:
            for i, s in enumerate(a.keys()):
                pref = "el" if i > 0 else ""
                print(2 * depth * " " + pref + "if state == " + str(s.as_tuple()) + ":")
                print_plan(a[s], depth=depth + 1)


plan = and_or_search()
print_plan(plan)
