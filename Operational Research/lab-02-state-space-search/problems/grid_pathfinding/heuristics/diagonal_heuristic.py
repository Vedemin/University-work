from base import Heuristic
from problems.grid_pathfinding.grid_pathfinding import GridPathfinding
from problems.grid_pathfinding.grid import GridCoord


class GridDiagonalHeuristic(Heuristic[GridCoord]):
 
    def __init__(self, problem: GridPathfinding):
        self.problem = problem

    def __call__(self, state: GridCoord) -> float:
        # TODO:
        # Calculate a diagonal distance:
        # - 'state' is the current state 
        # - 'self.problem.goal' is the goal state
        # - 'self.problem.diagonal_weight' is cost of making a diagonal move
        xDist = abs(state.x - self.problem.goal.x)
        yDist = abs(state.y - self.problem.goal.y)
        diagonal = 0
        if xDist < yDist:
            diagonal = xDist
        else:
            diagonal = yDist
        xDist -= diagonal
        yDist -= diagonal
        return xDist + yDist + diagonal * self.problem.diagonal_weight
