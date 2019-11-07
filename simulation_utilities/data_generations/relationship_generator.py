import sympy as sy

from other_utilities.dictionary_creator import MyDictionary


def multiple_data(formula, **kwargs):
    print(len(kwargs))
    print(formula)


def formula_generator(formula, **kwargs):
    expr = sy.sympify(formula)
    # return expr.evalf(subs=kwargs)
    print(expr.evalf(subs=kwargs))


data_dictionary = MyDictionary()
data_dictionary.add('p1',1)
data_dictionary.add('p2',1)

print(data_dictionary)
"""
x = [2, 3, 4]

for x in range(0,9):
    setattr(x, 'string%s' % x, 'Hello')
"""

multiple_data(data_dictionary, formula='p1+p2')
