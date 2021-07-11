import pydicom as pd
import os
import numpy as np
from tkinter.filedialog import askdirectory
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000
from imagecodecs import jpeg2k_encode
from pydicom.uid import ExplicitVRLittleEndian


class DicomIO:
    """

    """

    def __init__(self):
        self.dicoms = []
        self.series = []
        self.number_of_series = 0
        self.current_series = None
        self.current_3D = None
        self.cut3D = None

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
        print("Series: ", self.number_of_series)

    def save_cut3D(self):
        pass

    def load_series(self):
        series_dicoms = []
        for dcm in self.dicoms:
            try:
                if dcm.SeriesInstanceUID == self.current_series:
                    series_dicoms.append(dcm)
                    rows, columns = dcm.Rows, dcm.Columns
                    print(rows, columns)
            except Exception:
                pass
        img = np.zeros((rows, columns, len(series_dicoms)))

        for index, dcm in enumerate(series_dicoms):
            img[:, :, index] = dcm.pixel_array
        self.current_3D = img
        print(self.current_3D.shape)

    def get_2d_image(self, slice_: int):
        return self.current_3D[:, :, slice_]

    def save_cut3D(self):
        dir = askdirectory()
        series_dicoms = []
        for dcm in self.dicoms:
            try:
                if dcm.SeriesInstanceUID == self.current_series:
                    series_dicoms.append(dcm)
            except Exception:
                pass

        for index, series in enumerate(series_dicoms):
            series.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
            series.PixelData = self.cut3D[:, :, index].reshape(-1).astype(np.uint16).tostring()
            series.Rows = self.cut3D.shape[0]
            series.Columns = self.cut3D.shape[1]
            series.SamplesPerPixel = 1
            series.save_as(os.path.join(dir, str(index) + "_cut.dcm"))

    def hounsfield2grayscale(self):
        pass

# class DicomSeries:
#
#     def __init__(self, dicom):
#         self.SeriesInstanceUID = dicom.SeriesInstanceUID
#         self.StudyDescription
