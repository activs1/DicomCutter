import numpy as np


def hu_to_grayscale(volume):
    mxval = np.max(volume)
    mnval = np.min(volume)
    im_volume = (volume - mnval)/max(mxval - mnval, 1e-3)

    im_volume = 255*im_volume
    return im_volume
