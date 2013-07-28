import unittest

from parser.lines import Box,cluster,Cluster
from parser.lines import cluster
from parser.lines import cluster

class TestClusters(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple(self):
        boxes = [
                    Box(50,50),
                    Box(150,52),
                    Box(250,48),
                    Box(350,43),

                    Box(50,150),
                    Box(150,152),
                    Box(250,148),
                    Box(350,143),
                ]
        expected_clusters = [
                    Cluster([
                        Box(50,50),
                        Box(150,52),
                        Box(250,48),
                        Box(350,43),
                    ]),
                    Cluster([
                        Box(50,150),
                        Box(150,152),
                        Box(250,148),
                        Box(350,143),
                    ])
                ]
        clusters = cluster(boxes)
        self.assertEquals(clusters,expected_clusters)


if __name__ == '__main__':
    unittest.main()
