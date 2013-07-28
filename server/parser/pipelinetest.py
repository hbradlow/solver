import unittest
from pipeline import *

p = Pipeline()


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = Pipeline()
    
    def testSimple(self):
        filename = 'images/1+2+3.png'
        self.assertEquals(self.pipeline.handle(filename)['arith'][0], "1+2+3")

        filename = 'images/5*2+7.png'
        self.assertEquals(self.pipeline.handle(filename)['arith'][0], "5*2+7")


if __name__ == '__main__':
    unittest.main()
