from parser import pipeline
from solver import solver

p = pipeline.Pipeline()
s = solver.Solver()
filename = 'parser/images/arith_1.png'
eqs = p.handle(filename)

for eq in eqs['arith']:
    print eq
    result = s.solve(eq)
    print result
