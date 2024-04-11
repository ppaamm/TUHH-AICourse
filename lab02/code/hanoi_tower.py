from typing import Optional, List, Set
from copy import deepcopy
from collections import deque


class HanoiTowerState:
    """
    Tower of Hanoi with three pegs and `N` discs.
    """

    def __init__(self, N: int, pegs: Optional[List[List]] = None):
        self.N = N
        self.pegs: list[list] = [list(range(N, 0, -1)), [], []] if not pegs else pegs

    def pegs_representation(self):
        return (tuple(self.pegs[0]), tuple(self.pegs[1]), tuple(self.pegs[2]))

    def visualize(self):
        base = "  ".join(["=" * 2 * self.N] * 3)
        rev_lines = [base]
        for r in range(self.N):
            line = []
            for p in range(3):
                i = self.pegs[p][r] if len(self.pegs[p]) > r else 0
                tmp = self.N - i
                line.append(tmp * " " + i * 2 * "-" + tmp * " ")
            rev_lines.append("  ".join(line))
        print("\n".join(rev_lines[::-1]))

    def move(self, p1: int, p2: int):
        """
        Move the top disk from pole `p1` to the top of pole `p2`.
        """
        if not self.pegs[p1] or (
            self.pegs[p2] and self.pegs[p2][-1] < self.pegs[p1][-1]
        ):
            return False
        a = self.pegs[p1].pop()
        self.pegs[p2].append(a)
        return True

    def get_neighbors(self):
        """
        Returns a list of neighbors in the state graph, that is,
        all possible configurations that can be reached via a
        single `move` call.
        """
        nbs = []
        for a in range(3):
            for b in range(3):
                if a == b:
                    continue
                if self.move(a, b):
                    nbs.append(deepcopy(self))
                    self.move(b, a)
        return nbs


def is_goal(state: HanoiTowerState):
    return state.pegs[1] == list(range(state.N, 0, -1)) or state.pegs[2] == list(
        range(state.N, 0, -1)
    )


def bfs(start: HanoiTowerState):
    q = deque([start])
    seen = [start.pegs]

    parent = {start: None}
    while q:
        v = q.pop()
        # check if we are done
        if is_goal(v):
            steps = []
            while v:
                steps.append(v)
                v = parent[v]
            
            # Visualize the resulting path
            for i, s in enumerate(steps[::-1]):
                print(f"Step {i}:")
                s.visualize()
            return
        for w in v.get_neighbors():
            if w.pegs in seen:
                continue
            seen.append(w.pegs)
            q.appendleft(w)
            parent[w] = v


class DLSNode:
    def __init__(self, state, parent, depth):
        self.state = state
        self.parent = parent
        self.depth = depth


def is_cycle(node: DLSNode) -> bool:
    st = node.state
    while node.parent != None:
        if st.pegs == node.parent.state.pegs:
            return True
        node = node.parent
    return False


def dls(start: HanoiTowerState, depth_limit: int, verbose: bool = False):
    S = [DLSNode(start, None, 0)]
    while S:
        node = S.pop()
        if verbose: node.state.visualize()
        if is_goal(node.state):
            steps = []
            while node:
                steps.append(node.state)
                node = node.parent
            for i, s in enumerate(steps[::-1]):
                print(f"Step {i}:")
                s.visualize()
            return
        if node.depth >= depth_limit:
            continue
        elif not is_cycle(node):
            for w in node.state.get_neighbors():
                S.append(DLSNode(w, node, node.depth + 1))



N = 5
state = HanoiTowerState(N)
bfs(state)
