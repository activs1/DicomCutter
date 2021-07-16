import numpy as np
from scipy.ndimage.interpolation import map_coordinates


def interpolate(image3d, SliceThickness, PixelSpacing=(1, 1)):
    x = np.arange(0, image3d.shape[0], 1 / PixelSpacing[0])
    y = np.arange(0, image3d.shape[1], 1 / PixelSpacing[1])
    z = np.arange(0, image3d.shape[2], 1/ SliceThickness)

    xx, yy, zz = np.meshgrid(x, y, z)

    interpolated = map_coordinates(image3d, [yy, xx, zz])
    return interpolated


def hu_to_grayscale(volume):
    mxval = np.max(volume)
    mnval = np.min(volume)
    im_volume = (volume - mnval)/max(mxval - mnval, 1e-3)

    im_volume = 255*im_volume
    return im_volume


if __name__ == "__main__":
    img = np.random.rand(512, 512, 80)
    thickness = 2
    print("Interpoalting:")

    output = interpolate(img, thickness)
    print(img.shape)
    print(output.shape)
