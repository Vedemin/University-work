from saport.simplex.model import Model


def assignment_1():
    model = Model("Assignment 1")

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    expr1 = x1 + x2 + x3
    expr2 = x1 + 2 * x2 + x3
    expr3 = 2 * x2 + x3
    expr4 = 2 * x1 + x2 + 3 * x3

    model.add_constraint(expr1 <= 30)
    model.add_constraint(expr2 >= 10)
    model.add_constraint(expr3 <= 20)

    model.maximize(expr4)

    print("Before solving:")
    print(model.objective)

    solution = model.solve()
    print("Solution: ")
    print(solution)
    return model


def assignment_2():
    model = Model("Assignment 2")

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")
    x4 = model.create_variable("x4")

    expr1 = 0.8 * x1 + 2.4 * x2 + 0.9 * x3 + 0.4 * x4
    expr2 = 0.6 * x1 + 0.6 * x2 + 0.3 * x3 + 0.3 * x4
    expr3 = 9.6 * x1 + 14.4 * x2 + 10.8 * x3 + 7.2 * x4

    model.add_constraint(expr1 >= 1200)
    model.add_constraint(expr2 >= 600)

    model.minimize(expr3)

    print("Before solving:")
    print(model)
    solution = model.solve()
    print("Solution: ")
    print(solution)
    return model


def assignment_3():
    model = Model("Assignment 3")

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    expr1 = 5 * x1 + 15 * x2
    expr2 = 20 * x1 + 5 * x2
    expr3 = 15 * x1 + 2 * x2
    expr4 = 8 * x1 + 4 * x2

    model.add_constraint(expr1 >= 50)
    model.add_constraint(expr2 >= 40)
    model.add_constraint(expr3 <= 60)

    model.minimize(expr4)

    print("Before solving:")
    print(model)
    solution = model.solve()
    print("Solution: ")
    print(solution)
    return model


def assignment_4():
    model = Model("Assignment 4")

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")
    x4 = model.create_variable("x4")
    x5 = model.create_variable("x5")
    x6 = model.create_variable("x6")
    x7 = model.create_variable("x7")
    x8 = model.create_variable("x8")
    x9 = model.create_variable("x9")
    x10 = model.create_variable("x10")
    x11 = model.create_variable("x11")
    x12 = model.create_variable("x12")
    x13 = model.create_variable("x13")
    x14 = model.create_variable("x14")
    x15 = model.create_variable("x15")

    expr1 = x1 + x2 + x3 + x4
    expr2 = x2 + x5 + 2*x6 + 2*x7 + x8 + x9 + x10
    expr3 = x3 + 2*x4 + x7 + x8 + 2*x9 + 3*x10 + x11 + 2*x12 + 3*x13 + 4*x14 + 5*x15

    expr4 = 95*x1 + 20*x2 + 60*x3 + 25*x4 + 125*x5 + 50*x6 + 15*x7 + 90*x8 + 55*x9 + 20*x10 + 165*x11 + 130*x12 + 95*x13 + 50*x14 + 25*x15
    model.add_constraint(expr1 >= 150)
    model.add_constraint(expr2 >= 200)
    model.add_constraint(expr3 >= 150)

    model.minimize(expr4)
    print("Before solving:")
    print(model)
    solution = model.solve()
    print("Solution: ")
    print(solution)
    return model

assignment_1()
assignment_2()
assignment_3()
assignment_4()