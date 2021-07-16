import numpy as np


class DicomCutter:

    def __init__(self):
        self.original_3d_image = None
        self.cut_orientation = None
        self.cut_3d_image = None
        self.cut_plane = 'AX'
        self.orig_canvas_size = ()
        
    def set_original_image(self, image: np.array):
        pass

    def cut(self, points):
        x1, y1 = points[0]
        x2, y2 = points[1]
        print("dcm cutter shape: ", self.original_3d_image.shape)
        if self.cut_plane == 'AX':
            x1 = x1 - int((self.orig_canvas_size[0] / 2) - (self.original_3d_image.shape[0] / 2))
            x2 = x2 - int((self.orig_canvas_size[0] / 2) - (self.original_3d_image.shape[0] / 2))

            y1 = y1 - int((self.orig_canvas_size[1] / 2) - (self.original_3d_image.shape[1] / 2))
            y2 = y2 - int((self.orig_canvas_size[1] / 2) - (self.original_3d_image.shape[1] / 2))

            img = self.original_3d_image[y1:y2, x1:x2, :]
        elif self.cut_plane == 'SAG':
            x1 = x1 - int((self.orig_canvas_size[0] / 2) - (self.original_3d_image.shape[1] / 2))
            x2 = x2 - int((self.orig_canvas_size[0] / 2) - (self.original_3d_image.shape[1] / 2))

            y1 = y1 - int((self.orig_canvas_size[1] / 2) - (self.original_3d_image.shape[2] / 2))
            y2 = y2 - int((self.orig_canvas_size[1] / 2) - (self.original_3d_image.shape[2] / 2))

            img = self.original_3d_image[:, x1:x2, y1:y2]
        elif self.cut_plane == 'COR':
            x1 = x1 - int((self.orig_canvas_size[0] / 2) - (self.original_3d_image.shape[0] / 2))
            x2 = x2 - int((self.orig_canvas_size[0] / 2) - (self.original_3d_image.shape[0] / 2))

            y1 = y1 - int((self.orig_canvas_size[1] / 2) - (self.original_3d_image.shape[2] / 2))
            y2 = y2 - int((self.orig_canvas_size[1] / 2) - (self.original_3d_image.shape[2] / 2))

            print(self.original_3d_image.shape)
            img = self.original_3d_image[x1:x2, :, y1:y2]
            print(img.shape)
        return img


