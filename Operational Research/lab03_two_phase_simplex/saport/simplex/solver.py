from __future__ import annotations
import sys
from typing import Dict, List

from copy import deepcopy
import saport.simplex.model as ssmod
import saport.simplex.expressions.objective as sseobj
import saport.simplex.expressions.constraint as ssecon
import saport.simplex.expressions.expression as sseexp
import saport.simplex.solution as sssol
import saport.simplex.tableaux as sstab
import numpy as np


class Solver:
    """
        A class to represent a simplex solver.

        Attributes:
        ______
        _slacks: Dict[Variable, Constraint]:
            contains mapping from slack variables to their corresponding constraints
        _surpluses: Dict[Variable, Constraint]:
            contains mapping from surplus variables to their corresponding constraints
        _artificial: Dict[Variable, Constraint]:
            contains mapping from artificial variables to their corresponding constraints

        Methods
        -------
        solve(model: Model) -> Tableaux:
            solves the given model and return the first solution
    """
    _slacks: Dict[sseexp.Variable, ssecon.Constraint]
    _surpluses: Dict[sseexp.Variable, ssecon.Constraint]
    _artificial: Dict[sseexp.Variable, ssecon.Constraint]

    def solve(self, model: ssmod.Model):
        print("| -|- | solver.solve - start")
        normal_model = self._augment_model(model)
        print("   |---> normal_model = self._augment_model(model)")
        if len(self._slacks) < len(normal_model.constraints):
            print("   |---> if len(self._slacks) < len(normal_model.constraints): TRUE")
            tableaux, success = self._presolve(normal_model)
            print("   |---> tableaux, success = self._presolve(normal_model)")
            if not success:
                print("   |---> if not success: NOT SUCCESS")
                return sssol.Solution.infeasible(model, tableaux, tableaux)
        else:
            print("   |---> if len(self._slacks) < len(normal_model.constraints): FALSE")
            tableaux = self._basic_initial_tableaux(normal_model)
            print("   |---> tableaux = self._basic_initial_tableaux(normal_model)")

        initial_tableaux = deepcopy(tableaux)
        if self._optimize(tableaux) == False:
            print(
                "| --- | solver.solve - end, if self._optimize(tableaux) == False:\nreturn sssol.Solution.unbounded(model, initial_tableaux, tableaux)")
            return sssol.Solution.unbounded(model, initial_tableaux, tableaux)

        assignment = tableaux.extract_assignment()
        print(
            "| --- | solver.solve - end, assignment = tableaux.extract_assignment()\nreturn self._create_solution(assignment, model, initial_tableaux, tableaux)")
        return self._create_solution(assignment, model, initial_tableaux, tableaux)

    def _optimize(self, tableaux: sstab.Tableaux):
        while not tableaux.is_optimal():
            pivot_col = tableaux.choose_entering_variable()
            if tableaux.is_unbounded(pivot_col):
                return False
            pivot_row = tableaux.choose_leaving_variable(pivot_col)

            tableaux.pivot(pivot_row, pivot_col)
        return True

    def _presolve(self, model: ssmod.Model):
        """
            _presolve(model: Model) -> Tableaux:
                returns an initial tableaux for the second phase of simplex
        """
        presolve_model = self._create_presolve_model(model)
        tableaux = self._presolve_initial_tableaux(presolve_model)

        self._optimize(tableaux)

        if self._artifical_variables_are_positive(tableaux):
            return (tableaux, False)

        tableaux = self._restore_initial_tableaux(tableaux, model)
        return (tableaux, True)

    def _augment_model(self, original_model: ssmod.Model):
        """
            _augment_model(model: Model) -> Model:
                returns an augmented version of the given model
        """
        model = deepcopy(original_model)
        model.simplify()
        self._change_objective_to_max(model)
        self._change_constraints_bounds_to_nonnegative(model)
        self._slacks = self._add_slack_variables(model)
        self._surpluses = self._add_surplus_variables(model)
        return model

    def _create_presolve_model(self, augmented_model: ssmod.Model):
        presolve_model = deepcopy(augmented_model)
        self._artificial = self._add_artificial_variables(presolve_model)
        return presolve_model

    def _change_objective_to_max(self, model: ssmod.Model):
        if model.objective.type == sseobj.ObjectiveType.MIN:
            model.objective.invert()

    def _change_constraints_bounds_to_nonnegative(self, model: ssmod.Model):
        for constraint in model.constraints:
            if constraint.bound < 0:
                constraint.invert()

    def _add_slack_variables(self, model: ssmod.Model) -> List[sseexp.Variable]:
        slacks: Dict[sseexp.Variable, ssecon.Constraint] = dict()

        for constraint in model.constraints:
            if constraint.type == ssecon.ConstraintType.LE:
                slack_var = model.create_variable(f"s{constraint.index}")
                slacks[slack_var] = constraint
                constraint.expression = constraint.expression + slack_var
                constraint.type = ssecon.ConstraintType.EQ

        return slacks

    def _add_surplus_variables(self, model: ssmod.Model) -> List[sseexp.Variable]:
        surpluses: Dict[sseexp.Variable, ssecon.Constraint] = dict()

        for constraint in model.constraints:
            if constraint.type == ssecon.ConstraintType.GE:
                surplus_var = model.create_variable(f"s{constraint.index}")
                surpluses[surplus_var] = constraint
                constraint.expression = constraint.expression - surplus_var
                constraint.type = ssecon.ConstraintType.EQ

        return surpluses

    def _add_artificial_variables(self, model: ssmod.Model):
        artificial_variables: Dict[sseexp.Variable, ssecon.Constraint] = dict()
        # TODO: add artificial variables to the model.
        #      tip 1. you may base your codes on _add_slack_variables/_add_surplus_variable
        #      tip 2. artificial variables have to be added only to the constraints without slacks
        #             use in self._slacks to find where were the slack added

        for constraint in model.constraints:
            if constraint.expression.__str__().split(' ')[-2] != '+':
                artificial_var = model.create_variable(f"R{constraint.index}")
                artificial_variables[artificial_var] = constraint
                constraint.expression = constraint.expression + artificial_var

        return artificial_variables

    def _basic_initial_tableaux(self, model: ssmod.Model):
        objective_row = np.array((-1 * model.objective.expression).coefficients(model) + [0.0])
        table = np.array([objective_row] + [c.expression.coefficients(model) + [c.bound] for c in model.constraints])
        print(table)
        return sstab.Tableaux(model, table)

    def _presolve_initial_tableaux(self, model: ssmod.Model):
        # TODO: create an initial tableaux for the artificial variables
        #       - cost row should contain 1.0 for every artificial variable
        #       - then fix the tableaux basis (tip. artificial variables should be basic) using simple transformations;
        #         like in the pivot: subtract rows / multiply by constant
        #       tip 1. you may look at the _basic_initial_tableaux on how to create a tableaux

        first_row = []
        for var in model.variables:
            if var.__str__().startswith('R'):
                first_row.append(1)
            else:
                first_row.append(0)

        objective_row = np.array(first_row + [0])
        table = np.array([objective_row] + [c.expression.coefficients(model) + [c.bound] for c in model.constraints])

        for const in model.constraints:
            print(const)
        print(sstab.Tableaux(model, table))
        return sstab.Tableaux(model, table)

    def _artifical_variables_are_positive(self, tableaux: sstab.Tableaux):
        # TODO: check whether any artificial variable in the table is positive
        #       tip. self._artificial contains info about artificial variables
        # print("Tableaux assignments:")
        # print(tableaux.extract_assignment())
        art_n = 1
        number = len(tableaux.extract_assignment())
        for key in self._artificial.keys():
            art_n += 1
        vars = tableaux.extract_assignment()
        vars.reverse()
        # print(vars)
        for artificial in range(0, art_n):
            # print(vars[artificial])
            if vars[artificial] > 0:
                return True
        return False

    def _restore_initial_tableaux(self, tableaux: sstab.Tableaux, model: ssmod.Model):
        # TODO: remove artificial variables from the tableaux and restore the objective
        #       1. remove corresponding columns from the tableaux (np.delete is a little helper here)
        #       2. restore the original objective row
        #       3. similarly to the way we have zeroed the artificial variables in _presolve_initial_tableaux,
        #          now we have to transform the tableaux to make the basic variables (basic = being part of the basis) 
        #          in the first phase tableaux also basic in the new tableaux
        new_table = None
        result = []
        colsToDel = 0
        for key in self._artificial.keys():
            colsToDel += 1
        # Now we have the amount of columns to take out of the table
        # print(tableaux.table)
        i = 0
        for row in tableaux.table:
            newRow = []
            last = 0
            for col in row:
                newRow.append(float(col))
                last = float(col)
            for done in range(0, colsToDel + 1):
                newRow.pop()

            newRow.append(last)
            if i == 0:
                newRow = (-1 * model.objective.expression).coefficients(model) + [0.0]
            result.append(newRow)
            i += 1
        new_table = np.array(result)
        print(new_table)
        return sstab.Tableaux(tableaux.model, new_table)

    def _create_solution(self, assignment: List[float], model: ssmod.Model, initial_tableaux: sstab.Tableaux,
                         tableaux: sstab.Tableaux):
        return sssol.Solution.with_assignment(model, assignment, initial_tableaux, tableaux)