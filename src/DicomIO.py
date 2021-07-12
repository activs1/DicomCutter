import pydicom as pd
import os
import numpy as np
from tkinter.filedialog import askdirectory
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000
from imagecodecs import jpeg2k_encode
from pydicom.uid import ExplicitVRLittleEndian
from copy import copy

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
        
        if self.ORIENTATION == 'AX':
            for i in range(0, self.cut3D.shape[2]):
                series = basic_series[i]
                series.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
                series.SeriesInstanceUID = series.SeriesInstanceUID if ".170798" in series.SeriesInstanceUID else series.SeriesInstanceUID + ".170798"
                series.PixelData = self.cut3D[:, :, i].reshape(-1).astype(np.uint16).tostring()
                series.Rows = self.cut3D.shape[0]
                series.Columns = self.cut3D.shape[1]
                series.SamplesPerPixel = 1
                series.save_as(os.path.join(dir, str(i) + "_cut.dcm"))
                
        elif self.ORIENTATION == 'SAG':
            for i in range(0, self.cut3D.shape[0]):
                series = basic_series[i]
                series.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
                series.SeriesInstanceUID = series.SeriesInstanceUID if ".170798" in series.SeriesInstanceUID else series.SeriesInstanceUID + ".170798"
                series.PixelData = self.cut3D[i, :, :].reshape(-1).astype(np.uint16).tostring()
                series.Rows = self.cut3D.shape[1]
                series.Columns = self.cut3D.shape[2]
                print(self.cut3D.shape)
                series.SamplesPerPixel = 1
                series.save_as(os.path.join(dir, str(i) + "_cut.dcm"))
                
        elif self.ORIENTATION == 'COR':
            for i in range(0, self.cut3D.shape[1]):
                series = basic_series[i]
                series.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
                series.SeriesInstanceUID = series.SeriesInstanceUID if ".170798" in series.SeriesInstanceUID else series.SeriesInstanceUID + ".170798"
            
                series.PixelData = self.cut3D[:, i, :].reshape(-1).astype(np.uint16).tostring()
                series.Rows = self.cut3D.shape[0]
                series.Columns = self.cut3D.shape[2]
                print(self.cut3D.shape)
                series.SamplesPerPixel = 1
                series.save_as(os.path.join(dir, str(i) + "_cut.dcm"))


    def hounsfield2grayscale(self):
        pass

# class DicomSeries:
#
#     def __init__(self, dicom):
#         self.SeriesInstanceUID = dicom.SeriesInstanceUID
#         self.StudyDescription
