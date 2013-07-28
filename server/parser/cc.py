from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import mahotas
from parser.lines import *
from skimage.filter import threshold_otsu, threshold_adaptive


image = mahotas.imread('photo.jpg')[0::20,0::20]


block_size = 50
binary_adaptive = np.invert(threshold_adaptive(image, block_size, offset=30))

mask = binary_adaptive > binary_adaptive.mean()
label_im, n_labels = ndimage.label(binary_adaptive)#mask)

print n_labels
plt.figure(figsize=(9,3))

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
print extrema

boxes = []
for label,coords in extrema.items():
    b = Box(coords[0][0], coords[0][1], coords[1][0], coords[1][1])
    boxes.append(b)
display_boxes(boxes)


plt.subplot(131)
plt.imshow(binary_adaptive)
plt.axis('off')
plt.subplot(132)
plt.imshow(mask, cmap=plt.cm.gray)
plt.axis('off')
plt.subplot(133)
plt.imshow(label_im, cmap=plt.cm.spectral)
plt.axis('off')

plt.subplots_adjust(wspace=0.02, hspace=0.02, top=1, bottom=0, left=0, right=1)
plt.show()
