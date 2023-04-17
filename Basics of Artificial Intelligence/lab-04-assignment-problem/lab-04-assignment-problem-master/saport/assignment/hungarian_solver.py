import numpy as np
from .model import Assignment, AssignmentProblem, NormalizedAssignmentProblem
from typing import List, Dict, Tuple, Set
from numpy.typing import ArrayLike

class Solver:
    '''
    A hungarian solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    extract_mins(costs: ArrayLike):
        substracts from columns and rows in the matrix to create 0s in the matrix
    find_max_assignment(costs: ArrayLike) -> Dict[int,int]:
        finds the biggest possible assinments given 0s in the cost matrix
        result is a dictionary, where index is a worker index, value is the task index
    add_zero_by_crossing_out(costs: ArrayLike, partial_assignment: Dict[int,int])
        creates another zero(s) in the cost matrix by crossing out lines (rows/cols) with zeros in the cost matrix,
        then substracting/adding the smallest not crossed out value
    create_assignment(raw_assignment: Dict[int, int]) -> Assignment:
        creates an assignment instance based on the given dictionary assignment
    '''
    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        costs = np.array(self.problem.costs)

        while True:
            self.extracts_mins(costs)
            max_assignment = self.find_max_assignment(costs)
            if len(max_assignment) == self.problem.size():
                return self.create_assignment(max_assignment)
            self.add_zero_by_crossing_out(costs, max_assignment)

    def extracts_mins(self, costs: ArrayLike):
        #TODO: substract minimal values from each row and column
        # ALERT: There is a possibility of having negative numbers in a column if something is wrong.
        # In that case, all this might collapse when going through columns
        # print(costs)
        row_n = 0
        col_n = 0
        # This is a really bad implementation of it. Too bad!
        for row_idx, row in enumerate(costs):
            minimalInRow = row[0]
            col_n = 0
            for col in row:
                if col < minimalInRow:
                    minimalInRow = col
                col_n += 1
            # print(minimalInRow)
            for col_idx in range(len(row)):
                costs[row_idx, col_idx] -= minimalInRow
            row_n += 1
        # Each row has been scanned for its lowest value. Now each column will be to generate more zeroes.
        # print(costs)
        for col in range(0, col_n):
            minimalInCol = costs[0][col]
            for row in range(0, row_n):
                if costs[row][col] < minimalInCol:
                    minimalInCol = costs[row][col]
            for row in range(0, row_n):
                costs[row][col] -= minimalInCol
        # Now every single row and column should have at least one 0


    def add_zero_by_crossing_out(self, costs: ArrayLike, partial_assignment: Dict[int,int]):
        # print(">>>Adding zero by crossing out!<<<")
        usedRows = []

        def get_row_with_least_zeroes(costs: ArrayLike, excludedColumns: list):
            # print("\tGetting row with least zeroes, costs as given to method:")
            # print(costs)
            print("\tExcluded columns: ", excludedColumns, " Excluded rows: ", usedRows)
            cZeroes_n = dict()
            for i_c in range(0, len(costs[0])):
                zeroesInColumn = 0
                for i_r in range(0, len(costs)):
                    if i_c not in excludedColumns and i_r not in usedRows and costs[i_r][i_c] == 0:
                        zeroesInColumn += 1
                        print("Zero on R: ", i_r, " C: ", i_c)
                cZeroes_n[i_c] = zeroesInColumn
            print("Columns by zeroes: ", cZeroes_n)
            # We can now make a 2d array out of it
            cZArr = []
            for key in cZeroes_n:
                cZArr.append([key, cZeroes_n[key]])
            cZArr = sorted(cZArr, key=lambda x: x[
                1])  # This is an array sorted by values, each value here is the amount of 0s, each key is the index
            rZeroes_n = []
            i = 0
            col_i = 0
            for row in costs:
                col_i = 0
                rZeroes_n.append(0)
                # We initiate a value of zeroes which will later on be increased for every zero in a non-excluded column
                for col in row:
                    # print("Checking for exclusion column: ", col_i)
                    isExcluded = False
                    for exclusion in excludedColumns:
                        if col_i == exclusion:
                            isExcluded = True
                            # print("Excluded column: ", col_i)
                    # Now it has been checked if the column in question is excluded
                    if isExcluded == False and col == 0 and i not in usedRows:
                        rZeroes_n[i] += 1
                    col_i += 1
                i += 1
            leastZeroes = col_i + 2  # The most zeroes a row may have is the number of columns
            indexWithLeastZeroes = 0
            j = 0
            zeroFound = False
            # print("\tZeroes by row: ", rZeroes_n)
            for row in rZeroes_n:
                if row < leastZeroes and row > 0:
                    leastZeroes = row
                    indexWithLeastZeroes = j
                    zeroFound = True
                j += 1
            # For loop above finds the index of a row that has at least one zero AND has the least zeroes of any row
            chosenColumn = -1
            k = 0
            zeroIndexes = []
            for col in costs[indexWithLeastZeroes]:
                isExcluded = False
                for exclusion in excludedColumns:
                    if k == exclusion:
                        isExcluded = True
                if col == 0 and isExcluded == False:
                    zeroIndexes.append(k)
                k += 1
            # Now we have zeroIndexes filled with indexes containing a zero
            for column in cZArr:
                if column[0] in zeroIndexes and chosenColumn == -1:
                    chosenColumn = column[0]
            # This code finds the first zero to occur in the row with least zeroes in a non-excluded column
            if zeroFound == False:
                indexWithLeastZeroes = -1
                chosenColumn = -1
            print("\tRow with least zeroes: ", indexWithLeastZeroes, " -|- First zero on index: ", chosenColumn)
            return indexWithLeastZeroes, chosenColumn
        #TODO:
        # 1) "mark" columns and rows according to the instructions given by teacher
        # 2) cross out marked columns and not marked rows
        # 3) find minimal uncrossed value and subtract it from the cost matrix
        # 4) add the same value to all crossed out columns and rows
        # Algorithm be like:
        # 1. Find usable zeroes, mark them with a square and exclude other zeroes
        # 2. Find rows without squares and mark them with an arrow
        # 3. In each row without an arrow, place an arrow on a column containing a 0
        print(costs)
        excludedColumns = []
        squares = []
        isFinished = False
        # print("Going to find zeroes now")
        while isFinished == False:
            sqRow, sqCol = get_row_with_least_zeroes(costs, excludedColumns)
            if sqRow > -1 and sqCol > -1:
                excludedColumns.append(sqCol)
                usedRows.append(sqRow)
                squares.append([sqRow, sqCol])
            else:
                isFinished = True
        # print("Found all zeroes, going next")
        sortedSquares = sorted(squares, key=lambda x: x[0])
        amountOfRows = len(costs)
        arRows = [] # This means a row where we place an arrow, also name is funny
        squareR = []
        squareC = []
        for square in sortedSquares:
            squareR.append(square[0])
            squareC.append(square[1])
        for index in range(0, amountOfRows): # We have to find rows that don't have squares and place an arrow there
            if index not in squareR:
                arRows.append(index)

        # We have placed arrows in each row without a square, let's get on to columns
        arCols = [] # This means a column where we place an arrow
        isSame = False
        # print("Entered hell")
        while isSame == False:
            isSame = True # PROBLEM TUTAJ
            for row in arRows:
                col_i = 0
                for col in costs[row]:
                    if col == 0 and col_i not in arCols:
                        arCols.append(col_i)
                        isSame = False
                    col_i += 1
            arCols = list(dict.fromkeys(arCols))
            # We removed duplicates so in every row where there is no square, there is an arrow at 0s
            # Now we need to find rows in the specified column that also contain a square
            for colIndex in arCols:
                for rowIndex in squareR:
                    if [rowIndex, colIndex] in sortedSquares:
                        arRows.append(rowIndex)
        # print("Squares: ", sortedSquares)
        # print("Arrowed columns: ", arCols)
        crossedRows = []
        crossedCols = []
        for row_i in range(0, len(costs)):
            if row_i not in arRows:
                crossedRows.append(row_i)
        for col_i in range(0, len(costs[0])):
            if col_i in arCols:
                crossedCols.append(col_i)
        # Now we have crossed rows and columns
        minimalValueRemaining = 0
        # print("Crossed rows: ", crossedRows)
        # print("Crossed columns: ", crossedCols)
        for row_i in range(0, len(costs)):
            if row_i not in crossedRows:
                for col_i in range(0, len(costs[row_i])):
                    if col_i not in crossedCols:
                        if minimalValueRemaining == 0:
                            minimalValueRemaining = costs[row_i][col_i]
                        elif costs[row_i][col_i] < minimalValueRemaining:
                            minimalValueRemaining = costs[row_i][col_i]
                            # print("\tNew minimal value: ", minimalValueRemaining)
        # Now that we have the minimal value, let's subtract it from the entire costs array
        newCosts = []
        counter = 0
        for row in costs:
            newRow = []
            # print("\tScan row ", counter, row, minimalValueRemaining)
            for col in row:
                print(col, col - minimalValueRemaining)
                newRow.append(col - minimalValueRemaining)
            newCosts.append(newRow)
            counter += 1
        print(newCosts)
        # Now we have the cost array with negative values. What is needed to do now is to reverse the damage
        for cRow in crossedRows:
            for column in range(0, len(newCosts[cRow])):
                newCosts[cRow][column] += minimalValueRemaining
        for cCol in crossedCols:
            for row in range(0, len(newCosts)):
                newCosts[row][cCol] += 1
        # Now the table is fixed
        # print("--------------------------------New costs--------------------------------")
        # print(hex(id(costs)))
        # costs = np.array(newCosts)

        for row_i in range(0, len(costs)):
            for col_i in range(0, len(costs[row_i])):
                costs[row_i][col_i] = newCosts[row_i][col_i]
        # print(hex(id(costs)))
        # print(costs)
        # print("----------------Send it brother!----------------")
        # Now the method ends after creating a new zero


    def find_max_assignment(self, costs) -> Dict[int,int]:
        # print(">>>Finding max assignment<<<")
        usedRows = []
        print(costs)
        def get_row_with_least_zeroes(costs: ArrayLike, excludedColumns: list):
            # print("\tGetting row with least zeroes, costs as given to method:")
            # print(costs)
            print("\tExcluded columns: ", excludedColumns, " Excluded rows: ", usedRows)
            cZeroes_n = dict()
            for i_c in range(0, len(costs[0])):
                zeroesInColumn = 0
                for i_r in range(0, len(costs)):
                    if i_c not in excludedColumns and i_r not in usedRows and costs[i_r][i_c] == 0:
                        zeroesInColumn += 1
                        print("Zero on R: ", i_r, " C: ", i_c)
                cZeroes_n[i_c] = zeroesInColumn
            print("Columns by zeroes: ", cZeroes_n)
            # We can now make a 2d array out of it
            cZArr = []
            for key in cZeroes_n:
                cZArr.append([key, cZeroes_n[key]])
            cZArr = sorted(cZArr, key=lambda x: x[1]) # This is an array sorted by values, each value here is the amount of 0s, each key is the index
            rZeroes_n = []
            i = 0
            col_i = 0
            for row in costs:
                col_i = 0
                rZeroes_n.append(0)
                # We initiate a value of zeroes which will later on be increased for every zero in a non-excluded column
                for col in row:
                    # print("Checking for exclusion column: ", col_i)
                    isExcluded = False
                    for exclusion in excludedColumns:
                        if col_i == exclusion:
                            isExcluded = True
                            # print("Excluded column: ", col_i)
                    # Now it has been checked if the column in question is excluded
                    if isExcluded == False and col == 0 and i not in usedRows:
                        rZeroes_n[i] += 1
                    col_i += 1
                i += 1
            leastZeroes = col_i + 2  # The most zeroes a row may have is the number of columns
            indexWithLeastZeroes = 0
            j = 0
            zeroFound = False
            # print("\tZeroes by row: ", rZeroes_n)
            for row in rZeroes_n:
                if row < leastZeroes and row > 0:
                    leastZeroes = row
                    indexWithLeastZeroes = j
                    zeroFound = True
                j += 1
            # For loop above finds the index of a row that has at least one zero AND has the least zeroes of any row
            chosenColumn = -1
            k = 0
            zeroIndexes = []
            for col in costs[indexWithLeastZeroes]:
                isExcluded = False
                for exclusion in excludedColumns:
                    if k == exclusion:
                        isExcluded = True
                if col == 0 and isExcluded == False:
                    zeroIndexes.append(k)
                k += 1
            # Now we have zeroIndexes filled with indexes containing a zero
            for column in cZArr:
                if column[0] in zeroIndexes and chosenColumn == -1:
                    chosenColumn = column[0]
            # This code finds the first zero to occur in the row with least zeroes in a non-excluded column
            if zeroFound == False:
                indexWithLeastZeroes = -1
                chosenColumn = -1
            print("\tRow with least zeroes: ", indexWithLeastZeroes, " -|- First zero on index: ", chosenColumn)
            return indexWithLeastZeroes, chosenColumn
        partial_assignment = dict()
         #TODO: find the biggest assignment in the cost matrix
        # 1) always try first the row with the least amount of 0s
        # 2) then use column with the least amount of 0s
        # TIP: remember, rows and cols can't repeat in the assignment
        #      partial_assignment[1] = 2 means that the worker with index 1
        #                                has been assigned to task with index 2
        excludedColumns = []
        squares = []
        isFinished = False
        while isFinished == False:
            sqRow, sqCol = get_row_with_least_zeroes(costs, excludedColumns)
            usedRows.append(sqRow)
            if sqRow > -1 and sqCol > -1:
                excludedColumns.append(sqCol)
                squares.append([sqRow, sqCol])
            else:
                isFinished = True
        sortedSquares = sorted(squares, key=lambda x: x[0])
        # result = []
        # for counter in range(0, len(costs)):
        #     result.append(-1)
        # for square in sortedSquares:
        #     result[square[0]] = square[1]
        # partial_assignment = result
        for square in sortedSquares:
            partial_assignment[square[0]] = square[1]
        print("Workers are indexes, values are assignments: ", partial_assignment)
        return partial_assignment

    def create_assignment(self, raw_assignment: Dict[int,int]) -> Assignment:
        #TODO: create an assignment instance based on the dictionary
        # tips:
        # 1) use self.problem.original_problem.costs to calculate the cost
        # 2) in case the original cost matrix (self.problem.original_problem.costs wasn't square)
        #    and there is more workers than task, you should assign -1 to workers with no task
        total_cost = 0
        assignment = []
        # for i in range(self.problem.costs.shape[0]):
        #     if raw_assignment[i] > -1:
        #         total_cost += self.problem.costs[i][raw_assignment[i]]
        for worker in raw_assignment:
            if raw_assignment[worker] > self.problem.original_problem.costs.shape[1] - 1:
                raw_assignment[worker] = -1
            if raw_assignment[worker] > -1 and worker < len(self.problem.original_problem.costs):
                print("INDEX: ", worker, "/", len(self.problem.original_problem.costs), " VALUE: ", raw_assignment[worker], "/", len(self.problem.original_problem.costs[0]))
                total_cost += self.problem.original_problem.costs[worker][raw_assignment[worker]]
        for worker in range(0, len(raw_assignment)):
            if worker < self.problem.original_problem.costs.shape[0]:
                assignment.append(raw_assignment[worker])
        print(total_cost)
        print(raw_assignment)
        print(" ================================= CREATE_ASSIGNMENT ================================= ")
        print(assignment)
        return Assignment(assignment, total_cost)