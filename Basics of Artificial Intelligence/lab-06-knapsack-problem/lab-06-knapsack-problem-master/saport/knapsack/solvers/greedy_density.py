import math

from .greedy import AbstractGreedySolver
from ..model import Item


class GreedySolverDensity(AbstractGreedySolver):
    """
    A greedy solver for the knapsack problems. 
    Uses value/weight density as the greedy heuristic. 
    """
    def greedy_heuristic(self, item: Item) -> float:
        # TODO: replace line below with the correct value
        print("Density")
        # if item.weight <= 0:
        #     return float(math.inf)
        # else:
        #     return item.value / item.weight
        return item.value / item.weight