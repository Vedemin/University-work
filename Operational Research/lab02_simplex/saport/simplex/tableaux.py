from __future__ import annotations
from typing import List
from numpy.typing import ArrayLike
import numpy as np
from . import model as ssmod

"""
eps is used to avoid numerical errors, e.g.
- for float equality checks use math.isclose https://docs.python.org/3/library/math.html#math.isclose
- for inequality checks, instead of >= 0 you may just write >= -eps
"""
eps = 1e-09


class Tableaux:
    """
    A class to represent a tableaux to linear programming problem.

    Attributes
    ----------
    model : Model
        model corresponding to the tableaux
    table : numpy.Array
        2d-array with the tableaux

    Methods
    -------
    __init__(model: Model, table: array) -> Tableaux:
        constructs a new tableaux for the specified model and initial table
    objective_coefficients() -> numpy.Array:
        returns a vector containing coefficients in the objective row
    objective_value() -> float:
        returns the objective value of solution represented in tableaux
    is_optimal() -> bool:
        checks whether the current solution is optimal
    choose_entering_variable() -> int:
        finds index of the variable, that should enter the basis next
    is_unbounded(col: int) -> bool:
        checks whether the problem is unbounded
    choose_leaving_variable(col: int) -> int:
        finds index of the variable, that should leave the basis next
    pivot(col: int, row: int):
        updates tableaux using pivot operation with given entering and leaving variables
    extract_assignment() -> List[float]:
        returns assignment corresponding to the tableaux
    extract_basis() -> List[int]
        returns list of indexes corresponding to the variables belonging to the basis
    """

    model: ssmod.Model
    table: ArrayLike

    def __init__(self, model: ssmod.Model, table: ArrayLike):
        self.model = model
        self.table = table

    def objective_coefficients(self) -> ArrayLike:
        return self.table[0, :-1]

    def objective(self) -> float:
        return self.table[0, -1]

    def is_optimal(self) -> bool:
        # TODO:
        # if all coefficients in the objective row are >= 0
        # tip. check the eps constant at the top of this file
        rows_n, cols_n = self.table.shape
        arr = []
        for i in range(cols_n - 1): # we need to exclude the last column of the objective row
            arr.append(float(self.table[0][i]))
        for val in arr:
            if val < -eps:
                return False
        return True

    def choose_entering_variable(self) -> int:
        # TODO:
        # return column index with the smallest coefficient in the objective row
        smallest = 0
        rows_n, cols_n = self.table.shape
        arr = []
        for i in range (cols_n - 1):
            arr.append(float(self.table[0][i]))
        for coefficient in arr:
            if smallest != 0 and coefficient < smallest:
                smallest = coefficient
            elif smallest == 0:
                smallest = coefficient
        return arr.index(smallest)

    def is_unbounded(self, col: int) -> bool:
        # TODO:
        # if all coefficients in the specified column are <= 0
        col = int(col)
        result = True
        for row in self.table:
            if row[col] > eps:
                result = False
        return result

    def choose_leaving_variable(self, col: int) -> int:
        # TODO:
        # return row index associated with the leaving variable - czyli numer wiersza, nie sam wiersz
        # to choose the row, divide bound column (last column) by the specified column - mamy index kolumny, musimy wziąć teraz index wiersza
        # then choose a row index associated with the smallest positive value in the result
        # patrzymy gdzie wyjdzie najmniej, możemy zrobić sobie array z wynikami, największy index arraya będzie indexem wiersza
        # tip: take care to not divide by 0 :)
        col = int(col) # The type of col was actually float instead of int
        values = []
        for row in self.table:
            if row[col] != 0:
                values.append(row[len(row) - 1] / row[col])
            else:
                values.append(0)
        if values.index(max(x for x in values if x >= 0)) != 0:
            return values.index(min(x for x in values if x > 0))
        else:
            return 0

    def pivot(self, row: int, col: int):
        # TODO:
        # Pivot operation should transform the tableaux to a form, where pivot column ('col')
        # contains only 0's with the exception of 1 in the pivot row ('row'), i.e.
        #
        #              col
        #       _ _ _ _ 0 _
        #       _ _ _ _ 0 _
        #  row  _ _ _ _ 1 _
        #       _ _ _ _ 0 _
        #
        # To achieve this goal, one has to transform tableaux in a way preserving the set of solutions
        # (remember, that tableaux represents a set of linear equations, we don't want to break them!).
        # Therefore one can only use following operations taught in the secondary school:
        # - multiple the row (coefficients in the equation) by scalar, e.g.
        #       4x + 5y = 4 | * 1/5 -> 4/5x + y = 4/5
        # - add one equation (optionally multiplied by scalar) to another, e.g.
        #       4x - 3y = 7
        #       2x - 1y = 3
        #       ___________ -2*
        #       0x - 5y = 1
        #
        # In other words, one can only multiple the rows of the tableaux by a scalar (numpy rows
        # can be easily multiplied), or add one row (possibly multiplied by scalar) to another
        # (again, numpy supports this out of the box). There exists a fixed set of such operations
        # leading to the correct pivot.
        # workingCopy = self.table
        # Generally speaking the self.table contains columns which contain rows
        row = int(row)
        col = int(col)
        rows_n, cols_n = self.table.shape
        print("Pivoting at row: ", row, " col: ", col, " pivot value: ", self.table[row][col])
        print("Before pivot: \n", self.table)
        if self.table[row][col] != 1:
            scalar = self.table[row][col]
            for colIndex in range(cols_n):
                self.table[row][colIndex] = self.table[row][colIndex] / scalar
            print("After scalar: \n", self.table)

        for rowIndex in range(rows_n):
            if rowIndex == row or self.table[rowIndex][col] == 0:
                continue
            scalar = self.table[rowIndex][col]
            print("Subtracting from row: ", rowIndex, ", scalar: ", scalar)
            for colIndex in range(cols_n):
                self.table[rowIndex][colIndex] = self.table[rowIndex][colIndex] - self.table[row][colIndex] * scalar
        print("After pivot: \n", self.table)

    def extract_assignment(self) -> List[float]:
        rows_n, cols_n = self.table.shape
        assignment = [0.0 for _ in range(cols_n - 1)]
        basis = self.extract_basis()
        for r in range(1, rows_n):
            var_index = basis[r - 1]
            assignment[var_index] = self.table[r, -1]

        return assignment

    def extract_basis(self) -> List[int]:
        rows_n, cols_n = self.table.shape
        basis = [-1 for _ in range(rows_n - 1)]
        for c in range(cols_n - 1):
            column = self.table[:, c]
            belongs_to_basis = column.min() == 0.0 and column.max() == 1.0 and column.sum() == 1.0
            if belongs_to_basis:
                row = np.where(column == 1.0)[0][0]
                # [row-1] because we ignore the objective variable in the basis
                basis[row - 1] = c
        return basis

    def __str__(self) -> str:
        def cell(x: float, w: int) -> str:
            return "{0: >{1}}".format(x, w)

        objective_name = self.model.objective.name()
        basis = self.extract_basis()
        header = ["basis", objective_name] + [var.name for var in self.model.variables] + ["b"]
        longest_col = max([len(h) for h in header])

        rows = [[objective_name]] + [[self.model.variables[i].name] for i in basis]

        for i, r in enumerate(rows):
            objective_coefficient = 0.0 if i > 0 else 1.0
            r += ["{:.3f}".format(v) for v in [objective_coefficient] + list(self.table[i])]
            longest_col = max(longest_col, max([len(v) for v in r]))

        header = [cell(h, longest_col) for h in header]
        rows = [[cell(v, longest_col) for v in row] for row in rows]

        cell_sep = " | "

        result = cell_sep.join(header) + "\n"
        for row in rows:
            result += cell_sep.join(row) + "\n"
        return result
