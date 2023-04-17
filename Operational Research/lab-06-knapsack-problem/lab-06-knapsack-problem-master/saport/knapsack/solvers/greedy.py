from numpy.core.arrayprint import format_float_positional
from ..abstractsolver import AbstractSolver
from ..model import Solution, Item


class AbstractGreedySolver(AbstractSolver):
    """
    An abstract greedy solver for the knapsack problems.

    Methods:
    --------
    greedy_heuristic(item : Item) -> float:
        return a value representing how much the given items is valuable to the greedy algorithm
        bigger value > earlier to take in the backpack
    """

    def greedy_heuristic(self, item: Item) -> float:
        raise Exception("Greedy solver requires a heuristic!")

    def solve(self) -> Solution:
        solution = Solution.empty()
        self.start_timer()
        # leave the lines above as they are

        # TODO: implement the greedy solving strategy
        #      1) sort items in the problem by the self.greedy_heuristic
        #      2) take as many as you can
        #      3) remember to replace the line below :)
        # tip. don't implement sorting! Just use the "sorted" function
        greedySorted = sorted(self.problem.items, reverse=True, key=self.greedy_heuristic)
        # print(greedySorted)
        for item in greedySorted:
            cap = self.problem.capacity - solution.weight - item.weight
            print(cap)
            if cap >= 0:
                solution.weight += item.weight
                solution.value += item.value
                solution.items.append(item)
        # print(solution.items)
        # leave the lines below as they are
        self.stop_timer()
        return solution
