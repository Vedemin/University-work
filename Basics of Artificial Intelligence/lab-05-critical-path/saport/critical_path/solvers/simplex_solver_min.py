from ..model import Project
from ..project_network import ProjectNetwork
from ...simplex.model import Model
from ...simplex.expressions.expression import Expression
from ..solution import BasicSolution


class Solver:
    '''
    Simplex based solver looking for the critical path in the project.
    Uses linear model minimizing total duration of the project.

    Attributes:
    ----------
    project_network: ProjectNetwork
        a project network related to the given project
    model: simplex.model.Model
        a linear model looking for the quickest way to finish the project
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
        self.model = self.create_model()

    def create_model(self) -> Model:
        #TODO:
        # 0) we need as many variables as there is nodes in the project network
        # 1) for each arc in the network, difference between times at its ends has to be
        # greater or equal duration of the task
        # 2) we have to minimize difference between time of the goal node and the start node
        model = Model("critical path (min)")
        variableBox = []
        nodes = self.project_network.nodes()
        for node in nodes:
            varname = "t" + str(node.index)
            variableBox.append([model.create_variable(varname), node])
        # All variables are created, time to
        objective = Expression()
        objective += variableBox[len(variableBox) - 1][0]
        objective -= variableBox[0][0] # tn-t1
        print("Objective (min): ", objective)
        # Objective has been created, time to read nodes connecting to each one
        for variable in variableBox:
            predecessors = self.project_network.predecessors(variable[1])
            for predecessor in predecessors:
                deltaTime = self.project_network.arc_duration(predecessor, variable[1])
                print("Adding constraint: ", variable[0], " - ", variableBox[predecessor.index - 1][0], " >= ", deltaTime)
                model.add_constraint(variable[0] - variableBox[predecessor.index - 1][0] >= deltaTime)

        model.minimize(objective)
        return model

    def solve(self) -> BasicSolution:
        solution = self.model.solve()
        print("MIN: solution.objective_value(): ", solution.objective_value())
        return BasicSolution(int(solution.objective_value()))
