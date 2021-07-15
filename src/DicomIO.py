import pydicom as pd
import os
import numpy as np
from tkinter.filedialog import askdirectory
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000
from imagecodecs import jpeg2k_encode
from pydicom.uid import ExplicitVRLittleEndian
from copy import copy
from src.interpolate import interpolate
from src.DicomSeries import DicomSeries
from collections import defaultdict

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
        self.ORIENTATION = 'AX'
        self.PixelSpacing = None
        self.SliceThickness = None

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

        series = defaultdict(list)
        for dcm in self.dicoms:
            try:
                series[dcm.SeriesInstanceUID].append(dcm)
            except Exception:
                pass

        self.create_series(series)
        self.number_of_series = len(self.series)
        print("Series: ", self.number_of_series)

    def create_series(self, series_dict):
        for key in series_dict:
            self.series.append(DicomSeries(series_dict[key]))


    def load_series(self):
        series_dicoms = []
        for dcm in self.dicoms:
            try:
                if dcm.SeriesInstanceUID == self.current_series:
                    series_dicoms.append(dcm)
                    rows, columns = dcm.Rows, dcm.Columns
                    print(rows, columns)
                    print(dcm.PixelSpacing)
                    print(dcm.SliceThickness)
                    self.SliceThickness = dcm.SliceThickness
                    self.PixelSpacing = dcm.PixelSpacing
            except Exception:
                pass
        img = np.zeros((rows, columns, len(series_dicoms)))

        for index, dcm in enumerate(series_dicoms):
            img[:, :, index] = dcm.pixel_array
        self.current_3D = interpolate(img, self.SliceThickness, self.PixelSpacing)
        print(self.current_3D.shape)

    def get_2d_image(self, slice_: int):
        if self.ORIENTATION == 'AX':
            return self.current_3D[:, :, slice_]
        elif self.ORIENTATION == 'SAG':
            return self.current_3D[slice_, :, :]
        elif self.ORIENTATION == 'COR':
            return self.current_3D[:, slice_, :]

    def save_cut3D(self):
        dir = askdirectory()
        basic_series = []
        for dcm in self.dicoms:
            try:
                if dcm.SeriesInstanceUID == self.current_series:
                    basic_series.append(dcm)
            except Exception:
                pass

        for i in range(0, self.cut3D.shape[2]):
            series = basic_series[i]
            series.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
            series.SeriesInstanceUID = series.SeriesInstanceUID if ".170798" in series.SeriesInstanceUID else series.SeriesInstanceUID + ".170798"
            series.PixelData = self.cut3D[:, :, i].reshape(-1).astype(np.uint16).tostring()
            series.Rows = self.cut3D.shape[0]
            series.Columns = self.cut3D.shape[1]
            series.PatientName = "DicomCutter Cut"
            series.SamplesPerPixel = 1
            series.save_as(os.path.join(dir, str(i) + "_cut.dcm"))



    def hounsfield2grayscale(self):
        pass

# class DicomSeries:
#
#     def __init__(self, dicom):
#         self.SeriesInstanceUID = dicom.SeriesInstanceUID
#         self.StudyDescription
