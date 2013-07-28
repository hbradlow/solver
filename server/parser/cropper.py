from scipy import ndimage
from skimage.filter import threshold_otsu, threshold_adaptive
from skimage.morphology import label, closing, square, reconstruction, erosion, dilation, square
import numpy as np
import Image

def crop(f, bbs):
    print 'filename', f
    img = Image.open(f)
    img_array = np.asarray(img)[0::1,0::1]
    
    print "SIZES"
    for b in bbs:
        print b.size_t()

    """
    block_size = img.shape[0]/7.
    binary_adaptive = np.invert(threshold_adaptive(img, block_size, offset=20))
    img = binary_adaptive > binary_adaptive.mean()
    print img.shape
    new = np.zeros(img.shape)
    for (x,y,z), value in np.ndenumerate(img):
        if value:
            new[x,y,:] = 0
        else:
            new[x,y,:] = 1
    img = new
    img = dilation(img[:,:,0],square(10))
    """

    i = 0
    buffer = 5
    files = []
    for box in bbs:
        name = "tmp"+str(i)+".png"
        print '+++++++++IMAGE_ARRAY', type(img_array)

        #img = img[box.x1*5-buffer:box.x2*5+buffer, box.y1*5-buffer:box.y2*5+buffer]
        coords = (box.x1*5-buffer, box.y1*5-buffer, box.x2*5+buffer, box.y2*5+buffer)
        img_array = img_array[coords[0]:coords[2], coords[1]:coords[3]]
        img = Image.fromarray(img_array)
        img.save(name)
        files.append("tmp"+str(i)+".png")
        i += 1
    return files

