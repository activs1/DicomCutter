import pydicom as pd
import os
import numpy as np


class DicomIO:
    """

    """

    def __init__(self):
        self.dicoms = []
        self.series = []
        self.number_of_series = 0
        self.current_series = None
        self.current_3D = None

    def read_dicom_folder(self, path: str):
        """

        :param path: Path to the directory containing DICOM files
        :return: -
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                fname = os.path.join(root, file)

                try:
                    dcm = pd.dcmread(fname)
                    self.dicoms.append(dcm)
                    print(f"Loaded {fname}")
                except Exception:
                    print(f"Couldn't load {fname}")

        descriptions = []
        for dcm in self.dicoms:
            try:
                descriptions.append(dcm.SeriesInstanceUID)
            except Exception:
                pass

        self.series = list(set(descriptions))
        self.number_of_series = len(set(descriptions))

    def load_series(self):
        series_dicoms = []
        for dcm in self.dicoms:
            try:
                if dcm.SeriesInstanceUID == self.current_series:
                    series_dicoms.append(dcm)
                    rows, columns = dcm.Rows, dcm.Columns
            except Exception:
                pass
        img = np.zeros((rows, columns, len(series_dicoms)))

        for index, dcm in enumerate(series_dicoms):
            img[:, :, index] = dcm.pixel_array
        self.current_3D = img
        print(self.current_3D.shape)

    def get_2d_image(self, slice_: int):
        return self.current_3D[:, :, slice_]

    def hounsfield2grayscale(self):
        pass