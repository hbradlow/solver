from parser import pipeline
from solver import solver
import unittest

class TestAll(unittest.TestCase):

    def setUp(self):
        self.solver = solver.Solver()
        self.pipe = pipeline.Pipeline()

    def test_simple(self):
        filename = 'parser/images/1+2+3.png'
        self.assertEquals(self.solver._simple(self.pipe.handle(filename)['arith'][0]),"6")

        filename = 'parser/images/5*2+7.png'
        self.assertEquals(self.solver._simple(self.pipe.handle(filename)['arith'][0]),"17")

        filename = 'parser/images/6+10+11+4:2+10.png'
        self.assertEquals(self.solver._simple(self.pipe.handle(filename)['arith'][0]),"39")

if __name__ == '__main__':
    unittest.main()
