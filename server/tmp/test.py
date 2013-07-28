from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import mahotas
from skimage.filter import threshold_otsu, threshold_adaptive
image = mahotas.imread('photo.jpg')[0::20,0::20]


block_size = 50
binary_adaptive = threshold_adaptive(image, block_size, offset=30)
for row in binary_adaptive:
    print row

mask = binary_adaptive > binary_adaptive.mean()
label_im, n_labels = ndimage.label(binary_adaptive)#mask)

print n_labels, 'labels'

plt.imshow(label_im)
sizes = ndimage.sum(mask, label_im, range(n_labels+1))
mean_vals = ndimage.sum(binary_adaptive, label_im, range(1, n_labels + 1))

mask_size = sizes < 1000
remove_pixel = mask_size[label_im]
print 'shape', remove_pixel.shape
label_im[remove_pixel] = 0
plt.imshow(label_im)
labels = np.unique(label_im)
label_im = np.searchsorted(labels, label_im)

plt.show()
