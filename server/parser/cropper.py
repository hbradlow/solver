import cv2
from scipy import ndimage
from skimage.filter import threshold_otsu, threshold_adaptive
import numpy as np

def crop(f, bbs):
    img = cv2.imread(f)[0::5,0::5]

    block_size = img.shape[0]/7.
    binary_adaptive = np.invert(threshold_adaptive(img, block_size, offset=40))
    img = binary_adaptive > binary_adaptive.mean()
    print img.shape
    new = np.zeros(img.shape)
    for (x,y,z), value in np.ndenumerate(img):
        if value:
            new[x,y,:] = 0
        else:
            new[x,y,:] = 255
    img = new

    i = 0
    buffer = 3
    files = []
    for box in bbs:
        cv2.imwrite("tmp"+str(i)+".png", ndimage.rotate(img[box.x1-buffer:box.x2+buffer, box.y1-buffer:box.y2+buffer],-90))
        files.append("tmp"+str(i)+".png")
        i += 1
    return files

