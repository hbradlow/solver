#PIL
from PIL import Image

#numpy
import numpy as np

#scipy
import scipy
import scipy.signal
from scipy.ndimage.morphology import grey_opening

#IPython
import IPython

def rolling_window_lastaxis(a, window):
    """Directly taken from Erik Rigtorp's post to numpy-discussion.
    <http://www.mail-archive.com/numpy-discussion@scipy.org/msg29450.html>"""
    if window < 1:
       raise ValueError, "`window` must be at least 1."
    if window > a.shape[-1]:
       raise ValueError, "`window` is too long."
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def rolling_window(a, window):
    if not hasattr(window, '__iter__'):
        return rolling_window_lastaxis(a, window)
    for i, win in enumerate(window):
        if win > 1:
            a = a.swapaxes(i, -1)
            a = rolling_window_lastaxis(a, win)
            a = a.swapaxes(-2, i)
    return a

def entropy(X):
    probs = [np.mean(X == c) for c in set(X)]
    return np.sum(-p * np.log2(p) for p in probs)

def get_windows(data,stepsize=1,width=3):
    return np.hstack( data[i:1+i-width or None:stepsize] for i in range(0,width) )

def segment(filename):
    filtsize = (10, 2)

    img = Image.open(filename)
    data = np.asarray(img)[:,:,0]

    windows = rolling_window(data,filtsize)
    skip = 5.
    output = np.zeros((data.shape[0]/skip,data.shape[1]/skip))

    scipy.misc.imsave('outfile.jpg', data)

    num = windows.shape[0]
    index = 0
    print num/skip
    for i,row in enumerate(windows[0::skip]):
        print "ROW",index
        index += 1
        for j,col in enumerate(row[0::skip]):
            output[i,j] = entropy(col[:,1])

    scipy.misc.imsave('outfile.jpg', output)

if __name__=="__main__":
    segment("parser/images/adding.JPG")
