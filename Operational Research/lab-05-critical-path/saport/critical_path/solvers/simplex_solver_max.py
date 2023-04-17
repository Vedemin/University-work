from ..model import Project
from ..project_network import ProjectNetwork
from ...simplex.model import Model
from ...simplex.expressions.expression import Expression
from ..solution import BasicSolution


class Solver:
    '''
    Simplex based solver looking for the critical path in the project.
    Uses linear model maximizing length of the path in the project network. 

    Attributes:
    ----------
    project_network: ProjectNetwork
        a project network related to the given project
    model: simplex.model.Model
        a linear model looking for the maximal path in the project network
    Methods:
    --------
    __init__(problem: Project)
        create a solver for the given project
    create_simplex_model() -> simplex.model.Model
        builds a linear model of the problem
    solve() -> BasicSolution
        finds the duration of the critical (longest) path in the project network
    '''
    def __init__(self, problem: Project):
        self.project_network = ProjectNetwork(problem)
        self.model = self.create_simplex_model()

    def create_simplex_model(self) -> Model:
        #TODO:
        # 0) we need as many variables as there is edges in the project network
        # 1) every variable has to be <= 1
        # 2) sum of the variables starting at the initial state has to be equal 1
        # 3) sum of the variables ending at the goal state has to be equal 1
        # 4) for every other node, total flow going trough it has to be equal 0
        #    i.e. sum of incoming arcs minus sum of the outgoing arcs = 0
        # 5) we have to maximize length of the path
        #    (sum of variables weighted by the durations of the corresponding tasks)
        model = Model("critical path (max)")
        edges = self.project_network.edges()
        variableBox = []
        objective = Expression()
        for edge in edges:
            variableName = "x" + str(edge[0].index) + str(edge[1].index)
            variableBox.append([model.create_variable(variableName), edge])

        for variable in variableBox:
            objective += variable[0] * variable[1][2].duration

        print("Objective (max): ", objective)

        # Now that we have the final constraint and all variables added, it's time to add middle constraints
        constraintBox = [Expression()] * (self.project_network.goal_node.index)
        for variable in variableBox:
            sourceNode = variable[1][0].index
            destNode = variable[1][1].index
            # print("N: ", name, " SN: ", sourceNode, " DN: ", destNode)
            if sourceNode == self.project_network.start_node.index:
                # print("IT IS THE START NODE")
                constraintBox[sourceNode - 1] += variable[0]
            else:
                constraintBox[sourceNode - 1] -= variable[0]
            constraintBox[destNode - 1] += variable[0]
        const_i = 0
        for constraint in constraintBox:
            if const_i == 0 or const_i == len(constraintBox) - 1:
                model.add_constraint(constraint == 1)
            else:
                model.add_constraint(constraint == 0)
            const_i += 1

        model.maximize(objective)
        return model

    def solve(self) -> BasicSolution:
        solution = self.model.solve()
        print("MAX: solution.objective_value(): ", solution.objective_value())
        return BasicSolution(int(solution.objective_value()))
