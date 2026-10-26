import numpy as np

from Methods.fitness import *
class Method:
    def __init__(self):
        self.fixed = None
        self.x = None

    @staticmethod
    def opposite_check(range: tuple):
        if fitness(range[0])*fitness(range[1]) > 0:
            raise ValueError("Not opposite endpoints: \n" + f"left={range[0]}\t" + f"right={range[1]}")
    
    def bisection(self, range: tuple) -> tuple:
        self.opposite_check(range)
        
        midpoint = self.midpoint(range[0], range[1])

        if fitness(midpoint) == 0:
            return (midpoint, midpoint)
        elif fitness(midpoint)*fitness(range[0]) < 0:
            return (range[0], midpoint)
        elif fitness(midpoint)*fitness(range[1]) < 0:
            return (midpoint, range[1])

    def secant(self, x_prev: float, x_curr: float) -> tuple:
        f_prev = fitness(x_prev)
        f_curr = fitness(x_curr)
        
        denominator = f_curr - f_prev
        if denominator == 0:
            raise ZeroDivisionError("Різниця значень функції дорівнює нулю (горизонтальна січна).")
        
        x_next = x_curr - f_curr * (x_curr - x_prev) / denominator
        return x_next, fitness(x_next)

    def regula_falsi(self, range: tuple) -> tuple:
        self.opposite_check(range)
        a, b = range
        fa = fitness(a)
        fb = fitness(b)
        
        x_n = a - fa * (b - a) / (fb - fa)
        fx_n = fitness(x_n)

        if fx_n == 0:
            return (x_n, x_n)
        elif fa * fx_n < 0:
            return (a, x_n)
        else:
            return (x_n, b)

    def newton(self, x: float) -> float:
        df = diff_1(x)
        if df == 0:
            raise ZeroDivisionError("Похідна дорівнює нулю (дотична паралельна осі X).")
        
        return x - fitness(x) / df        

    def midpoint(self, left:float, right:float)->float:
        return (left+right)/2
