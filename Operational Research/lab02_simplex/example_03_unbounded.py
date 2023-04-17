import logging
from saport.simplex.model import Model 

def create_model() -> Model:
    model = Model(__file__)

    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make the model unbounded!

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    model.add_constraint(x1 - x2 <= 0)
    model.add_constraint(x3 <= 20)

    model.minimize(3*x1 - x2 + x3)
    return model 

def run():
    model = create_model()
    #TODO:
    # add a test "assert something" based on the example_01_solvable.py
    #
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to find the correct solution
    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)
    assert (solution.__str__() == "There is no optimal solution, the model is unbounded"), "This model don't have solution!"

    logging.info("Congratulations! This solution seems to be alright :)")
    #logging.info("This test is empty but it shouldn't be, fix it!")
    #raise AssertionError("Test is empty")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()