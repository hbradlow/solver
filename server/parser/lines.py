import Tkinter as tk 
from scipy.cluster.vq import kmeans
import numpy as np
from gui import Visualizer, Point2D, Line2D, Box2D, add_line

class Cluster:
    def __init__(self,boxes=None):
        self.boxes = []
        if boxes:
            self.boxes = boxes
        self.error = 0
    def mid_y(self):
        return self.bounding_box().mid_y()
    def bounding_box(self):
        x1 = min([b.x1 for b in self.boxes])
        x2 = max([b.x2 for b in self.boxes])
        y1 = min([b.y1 for b in self.boxes])
        y2 = max([b.y2 for b in self.boxes])
        return Box(x1,y1,x2,y2)
    def __eq__(self,other):
        if len(self.boxes)!=len(other.boxes):
            return False
        for box in self.boxes:
            if box not in other.boxes:
                return False
        return True
    def __repr__(self):
        return "Cluster:" + str(len(self.boxes))+"," + str(self.bounding_box())+"\n"

def display_boxes(boxes):
    root = tk.Tk()
    vis = Visualizer(root,1000,600)

    for b in boxes:
        box = Box2D((b.x1,b.y1),size=b.size_t())
        vis.add_drawable(box)

    vis.run()
    root.mainloop()

class Box:
    def __init__(self,x1,y1,x2=None,y2=None):
        if not x2:
            x2 = x1+20
        if not y2:
            y2 = y1+20
            
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color="red"
    def overlaps_x(self,other):
        return not (self.x1>other.x2 or self.x2<other.x1)
    def overlaps_y(self,other):
        return not (self.y1>other.y2 or self.y2<other.y1)
    def __eq__(self,other):
        return [self.x1,self.x2,self.y1,self.y2] == [other.x1,other.x2,other.y1,other.y2]
    def y_size(self):
        return abs(self.y2-self.y1)
    def size_t(self):
        return (abs(self.x2-self.x1),abs(self.y2-self.y1))
    def size(self):
        return abs(self.y2-self.y1) + abs(self.x2-self.x1)
    def mid_y(self):
        return (self.y1+self.y2)/2.
    def mid_x(self):
        return (self.x1+self.x2)/2.
    def pos(self):
        return np.array([self.mid_x(),self.mid_y()])
    def __repr__(self):
        return "Box[" + str(self.mid_x()) + ", " + str(self.mid_y()) + ":" + str(self.size()) + "]"

def classify(ys,means):
    out = []
    for y in ys:
        out.append(min(range(means[0].shape[0]),key=lambda i: np.linalg.norm(means[0][i]-y)))
    return out

def x_cluster(xs,num_clusters=3):
    return kmeans(xs,num_clusters,iter=200)

def y_cluster(ys,num_clusters=3):
    return kmeans(ys,num_clusters,iter=200)

def accept_outliers(data, m=2):
    return data[abs(data[:,1] - np.mean(data[:,1])) > m * np.std(data[:,1])]

def reject_outliers(data, m=1):
    return data[abs(data[:,1] - np.mean(data[:,1])) < m * np.std(data[:,1])]

def cluster_boxes(boxes,num_clusters=3):
    ys = np.array([np.array([b.mid_y()]) for b in boxes])

    means = y_cluster(ys,num_clusters)
    classification = classify(ys,means)
    clusters = [Cluster() for i in range(means[0].shape[0])]
    for i,b in enumerate(boxes):
        clusters[classification[i]].boxes.append(b)

    return clusters,means[1]

def matrix_cluster(boxes):
    sizes = np.array([[b,b.y_size()] for b in boxes])
    normal = reject_outliers(sizes)[:,0]
    return cluster(list(normal))

def cluster(boxes):
    clusters = []
    while boxes:
        cluster = Cluster()
        b = boxes.pop()
        cluster.boxes.append(b)

        tmp = []
        for other in boxes:
            print cluster
            if cluster.bounding_box().overlaps_y(other):
                cluster.boxes.append(other)
            else:
                tmp.append(other)
            #print cluster.bounding_box()
        boxes = tmp

        #if len(cluster.boxes)<5 and cluster.bounding_box().size()>10:
        clusters.append(cluster)

    """
    root = tk.Tk()
    vis = Visualizer(root,1000,600)

    #return the clusters of boxes
    for cluster in clusters:
        for b in cluster.boxes:
            box = Box2D((b.x1,b.y1),size=b.size_t())
            vis.add_drawable(box)
        box = Box2D((cluster.bounding_box().x1,cluster.bounding_box().y1),
                    size=cluster.bounding_box().size_t())
        box.fill = None
        vis.add_drawable(box)
    vis.run()
    root.mainloop()
    """

    return sorted(clusters,key = lambda c:c.mid_y())

def cluster2(boxes):
    sizes = np.array([[b,b.y_size()] for b in boxes])
    #remove boxes whos size is an outlier
    #abnormal = accept_outliers(sizes)[:,0]
    #normal = reject_outliers(sizes)[:,0]
    normal = []
    for b in boxes:
        if b.size()>100:
            normal.append(b)
    normal = boxes
    """
    clusters = []
    for box in boxes:
        clusters.append(Cluster([box]))
    return clusters
    """


    root = tk.Tk()
    #vis = Visualizer(root,1000,600)

    #scan over values of k and pick the best one
    cluster = None
    first = -1
    """
    for i in range(100):
        clusters,error = cluster_boxes(normal,num_clusters=i+1)
        if first!=-1 and error/(first-error)<.15:
            break
        first = error
    """
    clusters,error = cluster_boxes(normal,num_clusters=6)

    #return the clusters of boxes
    for cluster in clusters:
        for b in cluster.boxes:
            box = Box2D((b.x1,b.y1),size=b.size_t())
            #vis.add_drawable(box)
        box = Box2D((cluster.bounding_box().x1,cluster.bounding_box().y1),
                    size=cluster.bounding_box().size_t())
        box.fill = None
        vis.add_drawable(box)
    vis.run()
    root.mainloop()

    return clusters

def find_matricies(boxes):
    pass

if __name__=="__main__":
    dist = 200

    boxes = [
                Box(5,5,20,400),
                
                Box(50,50),
                Box(150,52),
                Box(250,48),
                Box(350,43),

                Box(50,150),
                Box(150,152),
                Box(250,148),
                Box(350,143),

                Box(50,250),
                Box(150,252),
                Box(250,248),
                Box(350,243),

                Box(50,350),
                Box(150,352),
                Box(250,348),
                Box(350,343),

                Box(400,5,420,400),
            ]
    colors = ['red','blue','green','yellow']

    sizes = np.array([[b,b.y_size()] for b in boxes])
    abnormal = accept_outliers(sizes)[:,0]
    normal = reject_outliers(sizes)[:,0]

    first = -1
    num = 0
    for i in range(100):
        num = i+1
        clusters,error = cluster_boxes(normal,num_clusters=i+1)
        if first!=-1 and error/(first-error)<.15:
            break
        first = error
    colors *= len(clusters)/len(colors)
    root = tk.Tk()
    #vis = Visualizer(root,1000,600)

    for cluster,color in zip(clusters,colors):
        for b in cluster.boxes:
            box = Box2D((b.x1,b.y1),size=b.size_t())
            box.fill = color
            #vis.add_drawable(box)
        box = Box2D((cluster.bounding_box().x1,cluster.bounding_box().y1),
                    size=cluster.bounding_box().size_t())
        box.fill = None
        #vis.add_drawable(box)


    #vis.run()
    root.mainloop()
