import unittest
from pipeline import *

class TestPipeline(unittest.TestCase):

    def setUp(self):
        pass
    
    def testMatrix(self):
        #filename = 'tmp/test_matrix.png'
        filename = 'tmp/tmp.jpg'
        out = handle_matrix(filename)['arith']
        print out
        self.assertEquals(out, [['1', '12', '3', '52', '54'], ['4', '5', '62', '9', '3'], ['7', '81', '9', '2', '98'], ['6', '3', '24', '1', '2'], ['4', '2', '76', '3', '43'], ['2', '33', '54', '23', '123']])
    
    """
    def testSimple(self):
        filename = 'tmp/test_simple.png'
        out = handle_simple(filename)['arith']
        self.assertEquals(out, ['10y+1=101', '3x+2y=10'])
    """

if __name__ == '__main__':
    unittest.main()
