import Tkinter as tk 
from scipy.cluster.vq import kmeans
import numpy as np
from gui import Visualizer, Point2D, Line2D, Box2D, add_line

class Box:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.color="red"
    def pos(self):
        return np.array([self.x,self.y])
    def __repr__(self):
        return "Box[" + str(self.x) + ", " + str(self.y) + "]"

def classify(ys,means):
    out = []
    print means[0].shape[0]
    for y in ys:
        out.append(min(range(means[0].shape[0]),key=lambda i: np.linalg.norm(means[0][i]-y)))
    return out

def y_cluster(ys):
    return kmeans(ys,3)

def cluster_boxes(boxes):
    ys = np.array([np.array([b.y]) for b in boxes])
    means = y_cluster(ys)
    classification = classify(ys,means)
    clusters = [[] for i in range(means[0].shape[0])]

    for i,b in enumerate(boxes):
        clusters[classification[i]].append(b)

    return clusters

if __name__=="__main__":

    boxes = [
                Box(50,50),
                Box(150,52),
                Box(250,48),
                Box(350,43),
                Box(150,158),
                Box(250,150),
                Box(350,151),
                Box(100,251),
                Box(333,230),
                Box(350,261),
            ]

    print  cluster_boxes(boxes)
    """
    root = tk.Tk()
    vis = Visualizer(root,800,600)

    for b in boxes:
        vis.add_drawable(Point2D(b.pos(),fill=b.color))

    vis.run()
    root.mainloop()
    """
