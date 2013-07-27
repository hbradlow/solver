import unittest

from solver import Solver

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.solver = Solver()

    def test_random(self):
        self.assertEquals(self.solver.solve("6*3"),"18")
        self.assertEquals(self.solver.solve("x-4=10"),"x = 14")

    def test_simple(self):
        self.assertEquals(self.solver._simple("1+6"),"7")

    def test_wolfram(self):
        self.assertEquals(self.solver._wolfram("3x+4=10"),"x = 2")

if __name__ == '__main__':
    unittest.main()
