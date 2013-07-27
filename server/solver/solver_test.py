import unittest

from solver import Solver

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.solver = Solver()

    def test_add(self):
        self.assertTrue(self.solver.solve("1+6") == 7)

if __name__ == '__main__':
    unittest.main()
