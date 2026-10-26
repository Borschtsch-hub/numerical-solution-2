import numpy as np

from Methods.fitness import fitness

class Method:
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

    def chord():
        pass

    def midpoint(self, left:float, right:float)->float:
        return (left+right)/2
