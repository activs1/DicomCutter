import tkinter.filedialog
from tkinter import *
import numpy as np
from PIL import Image, ImageTk
import pydicom as pd
import config as cfg

from os.path import dirname, join
from pprint import pprint

import pydicom
from pydicom.data import get_testdata_files
from pydicom.filereader import read_dicomdir

FONT = cfg.APP_FONT_CONFIG["FONT"]

def run_app():
    window = create_window()

    loaded_folder_label = Label(window, text=cfg.APP_CONTENTS_CONFIG["LOADED_FOLDER_LABEL_DEFAULT"],
                                font=FONT)
    loaded_folder_label.grid(column=0, row=0)

    load_folder_button = Button(window, text=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON"],
                                font=FONT, bg=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON_BG"],
                                command=get_dicom_folder)
    load_folder_button.grid(column=1, row=0)

    loaded_series_label = Label(window, text=cfg.APP_CONTENTS_CONFIG["LOADED_SERIES_LABEL_DEFAULT"],
                                 font=FONT)
    loaded_series_label.grid(column=2, row=0)

    img = Image.fromarray(np.random.rand(400, 400)*255)
    img_tk = ImageTk.PhotoImage(image=img)
    print(img.__array__().shape)
    canvas = Canvas(window, width='400', height='400', background='gray')
    canvas.grid(column=0, row=1)
    canvas.create_image(100, 100, image=img_tk)
    canvas.update()


    window.mainloop()


def create_window():
    """
    Creates basic window, sets properties of the window
    :return:
    """
    window = Tk()

    window.title(cfg.BASIC_WINDOW_CONFIG["TITLE"])
    #window.geometry(cfg.BASIC_WINDOW_CONFIG["GEOMETRY"])

    return window


def get_dicom_folder():
    dir = tkinter.filedialog.askopenfilename()
    print(dir)
    load_dicom_folder(dir)

def load_dicom_folder(dir):
    dicom_dir = pd.dcmread(dir)
    print('loaded')
    base_dir = dirname(dir)
    for patient_record in dicom_dir.patient_records:
        if (hasattr(patient_record, 'PatientID') and
                hasattr(patient_record, 'PatientsName')):
            print("Patient: {}: {}".format(patient_record.PatientID,
                                           patient_record.PatientsName))
        studies = patient_record.children
        for study in studies:
            series = study.children
            for serie in series:
                if 'SeriesDescription' not in serie:
                    serie.SeriesDescription = "N/A"
                print(serie.SeriesDescription)



if __name__ == '__main__':
    run_app()
