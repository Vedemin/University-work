import numpy as np
from .model import AssignmentProblem, Assignment, NormalizedAssignmentProblem
from ..simplex.model import Model
from ..simplex.expressions.expression import Expression
from dataclasses import dataclass
from typing import List


class Solver:
    '''
    A simplex solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    '''

    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        model = Model("assignment")
        # TODO:
        # 1) creates variables, one for each cost in the cost matrix
        # 2) add constraint, that sum of every row has to be equal 1
        # 3) add constraint, that sum of every col has to be equal 1
        # 4) add constraint, that every variable has to be <= 1
        # 5) create an objective expression, involving all variables weighted by their cost
        # 6) add the objective to model (minimize it!)
        var_list = []
        i = 1
        for row in self.problem.costs:
            for val in row:
                var_list.append(model.create_variable(f"x{i}"))
                i += 1

        constraint_list = []
        j = 0
        for row in self.problem.original_problem.costs:
            expr = var_list[self.problem.original_problem.costs.shape[0] * j]
            for i in range(1, len(row)):
                expr += var_list[self.problem.original_problem.costs.shape[0] * j + i]
            j += 1
            model.add_constraint(expr == 1)

        for idx in range(self.problem.original_problem.costs.shape[1]):
            expr = var_list[idx]
            for idx_row in range(1, len(self.problem.original_problem.costs)):
                expr += var_list[idx + self.problem.original_problem.costs.shape[1] * idx_row]
            model.add_constraint(expr == 1)

        for var in var_list:
            model.add_constraint(var <= 1)

        expr = Expression()
        for idy, row in enumerate(self.problem.original_problem.costs):
            for idx, value in enumerate(row):
                expr += value * var_list[self.problem.original_problem.costs.shape[1] * idy + idx]

        print(expr)
        model.minimize(expr)

        # print(model.objective)
        solution = model.solve()
        # print(solution.assignment(model))
        # TODO:
        # 1) extract assignment for the original problem from the solution object
        # tips:
        # - remember that in the original problem n_workers() not alwyas equals n_tasks()
        solution.assignment(model)
        tasks = []
        k = 1
        for i in range(len(solution.assignment(model))):
            if i == self.problem.original_problem.costs.shape[1] * k:
                k += 1
            if i < self.problem.original_problem.costs.shape[1] * k:
                if solution.assignment(model)[i] == 1:
                    tasks.append(i % self.problem.original_problem.costs.shape[1])

        assigned_tasks = tasks
        org_objective = solution.objective_value()
        for con in model.constraints:
            print(con)
        print(org_objective)

        return Assignment(assigned_tasks, org_objective)



