from ..abstractsolver import AbstractSolver
from ..model import Solution
from numpy.typing import ArrayLike
import numpy as np
from typing import Tuple


class DynamicSolver(AbstractSolver):
    """
    A naive dynamic programming solver for the knapsack problem.
    """

    def create_table(self) -> ArrayLike:
        # TODO: fill the table!
        # tip 1. init table using np.zeros function
        # tip 2. remember to handle timeout (refer to the dfs solver for an example)
        #        - just return the current state of the table
        col_a = len(self.problem.items) + 1
        row_a = self.problem.capacity + 1
        table = np.zeros((row_a, col_a))
        for row in range(0, row_a):
            if self.timeout():
                return table
            for col in range(1, col_a):
                if row > 0:
                    # print(col)
                    if row < self.problem.items[col - 1].weight:
                        table[row][col] = table[row][col - 1]
                    elif row >= self.problem.items[col - 1].weight:
                        table[row][col] = max(table[row][col - 1], table[row - self.problem.items[col - 1].weight][col - 1] + self.problem.items[col - 1].value)
        return table

    def extract_solution(self, table: ArrayLike) -> Solution:
        used_items = []
        optimal = table[-1, -1] > 0

        # TODO: extract taken items from the table!
        #self.extract_solution(table)
        # print('extract_solution', used_items, optimal, Solution.from_items(used_items, optimal))
        # print(table.shape)

        row = table.shape[0] - 1
        col = table.shape[1] - 1
        while row > 0:
            # if self.timeout():
            #     returnItems = []
            #     for used in used_items:
            #         returnItems.append(self.problem.items[used - 1])
            #     return Solution.from_items(returnItems, optimal)
            if table[row][col] > table[row][col - 1] and col not in used_items and col > 0:
                used_items.append(col)
                row = row - self.problem.items[col - 1].weight
            elif col < 1:
                row -= 1
            else:
                col -= 1
        # print(used_items)
        returnItems = []
        for used in used_items:
            returnItems.append(self.problem.items[used - 1])
        return Solution.from_items(returnItems, optimal)

    def solve(self) -> Tuple[Solution, float]:
        self.interrupted = False
        self.start_timer()

        table = self.create_table()
        solution = self.extract_solution(table) if table is not None else Solution.empty()

        self.stop_timer()
        return solution
