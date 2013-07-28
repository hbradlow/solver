from scipy import ndimage
import numpy as np
import mahotas
from lines import *
from skimage.filter import threshold_otsu, threshold_adaptive
import Image

def get_bounding_boxes(filename):
    image = Image.open(filename)
    image = np.asarray(image)[0::1,0::1]

    block_size = image.shape[0]/7.
    binary_adaptive = np.invert(threshold_adaptive(image, block_size, offset=30))

    mask = binary_adaptive > binary_adaptive.mean()
    label_im, n_labels = ndimage.label(binary_adaptive)#mask)

    print n_labels, 'labels'

    extrema = {}
    for i in range(1, n_labels+1):
        extrema[i] = ((1000, 1000), (0, 0))

    # i: row
    # j: col
    for i,row in enumerate(label_im):
        for j, label in enumerate(row):
            if label[0] > 0:
                top, bottom  = extrema[label[0]]
                if i > bottom[0]:
                    bottom = (i, bottom[1])
                if j > bottom[1]:
                    bottom = (bottom[0], j)

                if i < top[0]:
                    top = (i, top[1])
                if j < top[1]:
                    top = (top[0], j)
                extrema[label[0]] = (top, bottom)

    boxes = []
    for label,coords in extrema.items():
        b = Box(coords[0][0], coords[0][1], coords[1][0], coords[1][1])
        boxes.append(b)
    #display_boxes(boxes)
    return boxes
