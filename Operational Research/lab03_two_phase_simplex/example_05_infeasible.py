import logging
from saport.simplex.model import Model 

from saport.simplex.model import Model

def create_model() -> Model:
    model = Model("example_05_infeasible")
    #TODO:
    # fill missing test based on the example_03_unbounded.py
    # to make the test a bit more interesting:
    # * make sure model is infeasible
    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    model.add_constraint(x1 - 3 * x2 + 2 * x3 >= 10)
    model.add_constraint(x1 + 5 * x2 - 1 * x3 <= -7)
    model.add_constraint(x1 - x2 >= 5)
    model.add_constraint(x2 - x3 >= 2)

    model.maximize(5 * x1 + 8 * x2)
    return model

def run():
    model = create_model()
    #TODO:
    # add a test "assert something" based on the example_01_solvable.py
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to find the correct solution
    try:
        solution = model.solve()
    except:
        raise AssertionError('Problem!')

    logging.info(solution)
    assert (solution.__str__() == 'There is no optimal solution, the model is infeasible'), 'This model has no optimal solution!'

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
