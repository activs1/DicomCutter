import pydicom as pd
import numpy as np
import matplotlib.pyplot as plt


class DicomCutter:

    def __init__(self):
        self.original_3d_image = None
        self.cut_orientation = None
        self.cut_3d_image = None

    def set_original_image(self, image: np.array):
        pass

    def cut(self, points):
        x1, y1 = points[0]
        x2, y2 = points[1]

        img = self.original_3d_image[y1:y2, x1:x2, :]
        return img

        plt.imshow(img[:, :, 2])
        plt.show()

