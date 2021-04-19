import sympy as sy

import Config as Config


def sample_system(data_point):
    dictionary_data_point = creating_dictionary(data_point)
    object_point = float(formula_generator(**dictionary_data_point))
    return object_point


def formula_generator(**kwargs):
    formula = Config.FUNCTION
    expr = sy.sympify(formula)
    return expr.evalf(subs=kwargs)


def creating_dictionary(x_data):
    dictionary = {}
    count = 0

    if type(x_data) is not tuple and type(x_data) is not list:
        list_create = [x_data]
        x_data = list_create

    for i in range(Config.NUMBER_OF_PARAMETERS):
        dictionary["p{0}".format(i + 1)] = x_data[count]
        count += 1

    for j in range(Config.NUMBER_OF_FEATURES):
        dictionary["f{0}".format(j + 1)] = x_data[count]
        count += 1

    return dictionary
