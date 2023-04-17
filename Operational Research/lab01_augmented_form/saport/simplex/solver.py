from __future__ import annotations
from typing import Dict, List

from copy import deepcopy
from . import model as ssmod 
from .expressions import constraint as ssecon
from .expressions import expression as sseexp
from .expressions import objective as sseobj
from . import solution as sssol 
from . import tableaux as sstab
import numpy as np 

class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Tableaux:
            solves the given model and return the first solution
    """
    def solve(self, model: ssmod.Model) -> sssol.Solution:
        augmented_model = self._augment_model(model)
        tableaux = self._basic_initial_tableaux(augmented_model)
        solution = self._extract_solution(tableaux, model)
        return solution
        
    def _augment_model(self, original_model: ssmod.Model) -> ssmod.Model:
        """
            _augment_model(model: Model) -> Model:
                returns an augmented version of the given model 
        """
        # We don't want to modify the original model
        model = deepcopy(original_model)
        # Wa want to have simplified expressions 
        # (each variable) should occur only once in every expression
        model.simplify()

        # TODO:
        # 1. the augmented model is always a maximizing model
        # - if the objective is minimizing, we have to "invert" it
        #   tip. Objective class has an "invert" method just for this purpose
        # 2. all the bounds in the augmented model have to be positive
        # - every model with a negative bound has to be "inverted"
        #   tip. Constraint class has an "invert" method just for this purpose
        # 3. add slack/surplus variables
        # - every GE constraint needs a new surplus variable, that should be subtracted to its expression
        # - every LE constraint needs a new slack variable, that should be added to its expression
        # tip. '-' and '+' operators are overloaded for the expression type, so you can literally add/subtract variables
        # - all constraints in the augmented model should be of type EQ
        if model.objective.type == model.objective.type.MIN:
            model.objective.invert()

        for constraint in model.constraints:
            if constraint.bound < 0:
                constraint.invert()

        for constraint in model.constraints:
            print(constraint.expression)
            if constraint.type == constraint.type.LE:
                new_var = model.create_variable(f"s{constraint.index}")
                constraint.expression += new_var
            elif constraint.type == constraint.type.GE:
                new_var = model.create_variable(f"s{constraint.index}")
                constraint.expression -= new_var
            constraint.type = constraint.type.EQ

        for i in model.variables:
            print(i)
        return model

    def _basic_initial_tableaux(self, model: ssmod.Model) -> sstab.Tableaux:
        # TODO:
        # replace the 'None' below with a numpy array, where
        # 1) first row consists of the inverted coefficients of the objective expression 
        #    plus 0.0 in the last column
        # 2) every other row consists of the coefficitients in the corresponding constraints, 
        #    don't forget to put the constraint bound in the last column
        # tips.
        # - to invert coefficients in the expression, one can multiply it by "-1"
        # - to get coefficients one can use the coefficients method in the expression object
        first_row = [x * (-1) for x in model.objective.expression.coefficients(model)]
        first_row = np.append(first_row, 0)
        table = np.array(first_row)

        for constraint in model.constraints:
            new_row = constraint.expression.coefficients(model)
            new_row = np.append(new_row, constraint.bound)
            table = np.vstack((table, new_row))


        return sstab.Tableaux(model, table)

    def _extract_solution(self, tableaux: sstab.Tableaux, model: ssmod.Model) -> sssol.Solution:
        return sssol.Solution(model, tableaux)