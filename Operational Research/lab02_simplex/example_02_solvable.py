import logging
from saport.simplex.model import Model 

def create_model() -> Model:
    model = Model(__file__)

    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * minimize the objective (so the solver would have to normalize it)
    # * make some ">=" constraints (GE)
    # * the model still has to be solvable by the basix simplex withour artificial var
    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(x1 >= -50)
    model.add_constraint(x2 <= 100)
    model.add_constraint(x1 + x2 <= 350)
    model.minimize(x1 - 2 * x2)

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
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)
    assert (solution.assignment(model) == [200.0, 150.0]), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
