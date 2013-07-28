import unittest
from pipeline import *

p = Pipeline()


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = Pipeline()
    
    def testSimple(self):
        filename = 'tmp/tmp.jpg'
        out = self.pipeline.handle(filename)['arith']
        m = []
        for i in out:
            i = i.replace(" ","")
            m.append([int(a) for a in list(i)])
        print m
        print "OUTPUT::::",out
        self.assertEquals(out, "1+2+3")

if __name__ == '__main__':
    unittest.main()
