import cv2
import numpy as np
import sys

def components(img):
    seen = np.zeros(img.shape)
    def neighbors(x,y):
        for i in [-1,1]:
            for j in [-1,1]:
                # if its in bounds and black and unseen
                if x+i < img.shape[0] and y+j < img.shape[1] and x+i >= 0 and y+j >= 0 and img[x+i, y+j] == 0 and seen[x+i, y+j] == 0: 
                    yield (x+i, y+j)
    def find():
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                # if we haven't seen it and its black
                if img[i,j] == 0 and seen[i,j] == 0:
                    print "found unseen black pixel"
                    return (i,j)
        return false
    components = []
    pixel = find() #find a black pixel we haven't seen
    while ( pixel ): # while such a pixel exists
        cc = [] # new connected comp
        stack = [pixel] # stack of pixels to process
        while ( stack ):
            (px, py) = stack.pop() # get a pix
            print "processing pixel: " + str((px, py))
            cc.append((px,py)) # add to connected comp
            seen[px,py] = 1 # mark it as seen
            for (nx, ny) in neighbors(px, py): # add its neighbors to the stack
                stack.append((nx,ny))
        print "collected a component"
        components.append(cc)
        pixel = find()
    return components

if __name__ == "__main__":
    win = cv2.namedWindow('win')
    im = cv2.imread(sys.argv[1])
    
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    im = cv2.threshold(im, 150, 255, cv2.THRESH_BINARY)[1]
    
    cv2.imshow('win', im)
   
    print len(components(im))

    cv2.waitKey()
