from scipy import ndimage
from skimage.filter import threshold_otsu, threshold_adaptive
from skimage.morphology import label, closing, square, reconstruction, erosion, dilation, square
import numpy as np
import Image

def crop(f, bbs,index=0):
    img = cv2.imread(f)[0::1,0::1]

    """
    block_size = img.shape[0]/7.
    binary_adaptive = np.invert(threshold_adaptive(img, block_size, offset=70))
    img = binary_adaptive > binary_adaptive.mean()
    new = np.zeros(img.shape)
    for (x,y,z), value in np.ndenumerate(img):
        if value:
            new[x,y,:] = 0
        else:
            new[x,y,:] = 1
    img = new
    #img = dilation(img[:,:,0],square(10))
    """

    i = index
    buffer = 5
    files = []
    for box in bbs:
        cv2.imwrite("tmp"+str(i)+".png", ndimage.rotate(img[box.x1-buffer:box.x2+buffer, box.y1-buffer:box.y2+buffer],0)[1:-1,1:-1])
        files.append("tmp"+str(i)+".png")
        i += 1
    return files,i

