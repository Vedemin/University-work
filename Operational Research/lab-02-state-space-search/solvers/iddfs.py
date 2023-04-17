from typing import Tuple, Optional
from base.solver import P, Solver
from solvers.utils import PriorityQueue
from solvers.utils import LIFO
from tree import Node, Tree


class IDDFS(Solver):
    def __init__(self, problem: P):
        self.problem = problem
        self.start = problem.initial
        self.root = Node(self.start)
        self.tree = Tree(self.root)


    def solve(self) -> Optional[Node]:
        # TODO:
        # - if the root node is a goal, just return it
        if self.problem.is_goal(self.root):
            return self.root
        #   tip. use 'is_goal' method from Problem
        # - set depth to 1
        depth = 1
        while (depth < len(self.tree.expand())):
            # - run self._depth_limited search
            node = self._depth_limited_search(self.root, depth)
            #   * if it returned a node, return it!
            if node != None:
                return node
            else:
                depth += 1
        return None

        #   * if there is no nodes left, return None 
        #   * otherwise increment depth and repeat the limited search
    

    def _depth_limited_search(self, root: Node, max_depth: int) -> Tuple[Optional[Node], bool]:
        # TODO:
        # - do a DFS with depth limited by a given depth
        #   tip. base in on the Uninformed search you have already done by now
        # differences:
        # - you should store in the frontier a tuple (node, depth), so later you could easily access current depth
        # - if depth of child is bigger than the max_depth, do not expand this child and store info there are still nodes left
        # - this method return a tuple:
        #   * first element is the node if the method finds a goal state, otherwise it should be None
        #   * second element is a boolean telling whether there are any nodes left to be expanded
        raise NotImplementedError()

    # self.frontier.push(self.root)
    # while not self.frontier.is_empty():
    #     node = self.frontier.pop()
    #     if self.problem.is_goal(node.state):
    #         return node
    #     else:
    #         for child in self.tree.expand(self.problem, node):
    #             if child.state not in self.visited:
    #                 self.visited.add(child.state)
    #                 self.frontier.push(child)
    # return None


    def search_tree(self) -> Tree:
        return self.tree
        