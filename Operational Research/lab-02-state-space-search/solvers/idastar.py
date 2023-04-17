from typing import Tuple, Optional
from base.solver import H, P, HeuristicSolver
from solvers.utils import LIFO, PriorityQueue
from tree import Node, Tree


class IDAStar(HeuristicSolver):
    def __init__(self, problem: P, heuristic: H):
        super().__init__(problem, heuristic)
        self.start = problem.initial
        self.root = Node(self.start, cost=0)
        self.tree = Tree(self.root)

    
    def solve(self) -> Optional[Node]:
        # TODO:
        # - if the root node is a goal, just return it
        #   tip. use 'is_goal' method from Problem
        # - set bound to the heuristic of the start state
        # - run self._cost_limited search
        #   * if it returned a node, return it!
        #   * if returned cost equals bound, return None
        #   * otherwise update bound to cost and repeat the limited search
        raise NotImplementedError()

    
    def _cost_limited_search(self, root: Node, bound: float) -> Tuple[Optional[Node], float]:
        # TODO:
        # - do a DFS with depth limited by a given bound
        #   tip. base in on the BestFirstSearch you have already done by now
        # differences:
        # - sort children using A* fcost (cost + heuristic)
        # - if fcost of child is bigger than the bound, do not expand this child
        # - this method return a tuple:
        #   * first element is the node if the method finds a goal state, otherwise it should be None
        #   * second element is a new bound (the smallest fcost of a not expanded child)
        raise NotImplementedError()
                
    def search_tree(self) -> Tree:
        return self.tree
