import sympy

class Solver:
    def __init__(self):
        pass
    def solve_simple(self,s):
        return sympy.sympify(s)
    def solve(self,s):
        return self.solve_simple(s)
