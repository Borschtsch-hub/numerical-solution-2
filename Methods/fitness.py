"""Defined equation for this solution"""

def fitness(x:float):
    return x**6-4*x**2+x+2.5

"""Here go derivatives"""

def diff_1(x: float):
    return 6*x**5-8*x+1

def diff_2(x: float):
    return 30*x**4-8

"""Single-point iteration func"""

def fitness_x(x:float):
    return -x**6+4*x**2-2.5

"""Single-point derivates"""

def diff_x_1(x:float):
    return -6*x**5+8*x