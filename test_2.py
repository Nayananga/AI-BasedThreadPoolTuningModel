import sympy as sy

dic = {'x':2, 'y':2, 'z':1}


def myformula(formula, **kwargs):
    expr = sy.sympify(formula)
    # return expr.evalf(subs=kwargs)
    lapply(X, FUN, ...)

#print(myformula(dic, formula="x+2*y/z"))
# 6.00000000000000

print(myformula(x=[2,2],y=2,z=1,formula="sin(x+y-z)"))
# 0.141120008059867
x= 2
y=2
z =2

formula = "(p1^2)/(f1)"

print(type(formula))

expr = sy.sympify(formula)
print(type(expr))

symbols = list(expr.free_symbols)
print(type(symbols))
print(symbols)
