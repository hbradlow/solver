import cv2
import numpy as np
import sys

def components(img):
    seen = np.zeros(img.shape)
    def neighbors(x,y):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # if its in bounds and black and unseen
                if x+i < img.shape[0] and y+j < img.shape[1] and x+i >= 0 and y+j >= 0 and img[x+i, y+j] == 0 and seen[x+i, y+j] == 0 and i != 0 and j != 0: 
                    yield (x+i, y+j)
    def find():
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                # if we haven't seen it and its black
                if img[i,j] == 0 and seen[i,j] == 0:
                    #print "found unseen black pixel"
                    return (i,j)
        return False
    components = []
    pixel = find() #find a black pixel we haven't seen
    while ( pixel ): # while such a pixel exists
        cc = [] # new connected comp
        stack = [pixel] # stack of pixels to process
        while ( stack ):
            (px, py) = stack.pop() # get a pix
            seen[px,py] = 1
            cc.append((px,py)) # add to connected comp
            for (nx, ny) in neighbors(px, py): # add its neighbors to the stack
                if seen[nx,ny] == 1: print "FUCKING REPEAT"; continue
                stack.append((nx,ny))
        components.append(cc)
        print "Found Component"
        pixel = find()
    return components

def bounding_box(component):
    minx = float('inf')
    maxx = 0
    miny = float('inf')
    maxy = 0
    for (x,y) in component:
        if x < minx: minx = x
        if x > maxx: maxx = x
        if y < miny: miny = y
        if y > maxy: maxy = y
    return ((miny-10, minx-10), (maxy+10, maxx+10))


if __name__ == "__main__":
    win = cv2.namedWindow('win')
    im = cv2.imread(sys.argv[1])
    
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    im = cv2.threshold(im, 150, 255, cv2.THRESH_BINARY)[1]
    im = cv2.pyrDown(im)
    im = cv2.blur(im, (5,5))
    comps = components(im)
    print len(comps)
    for c in comps:
        (p2, p1) = bounding_box(c)
        cv2.rectangle(im, p1, p2, 0)
    cv2.imshow('win', im)
   

    cv2.waitKey()
