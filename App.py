import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import config as cfg
from DicomIO import DicomIO
import matplotlib.pyplot as plt
import numpy as np


FONT = cfg.APP_FONT_CONFIG["FONT"]


class App:
    """

    """

    def __init__(self):
        self.window = None
        self.dcmIO = DicomIO()

        self.loaded_folder_label = None
        self.loaded_series_label = None
        self.loaded_series = None
        self.loaded_series_listview = None

        self.load_button = None
        self.axial_orientation_checkbox = None
        self.saggital_orientation_checkbox = None
        self.coronal_orientation_checkbox = None
        self.current_folder = None

        self.canvas = None
        self.imageID = None
        self.image = None
        self.default_image_path = None
        self.slice_slider = None

        self.create_window()
        self.create_UI()
        self.run()

    def create_window(self):
        self.window = tk.Tk()
        self.window.title(cfg.BASIC_WINDOW_CONFIG["TITLE"])

    def create_UI(self):
        self.loaded_folder_label = tk.Label(self.window, text=cfg.APP_CONTENTS_CONFIG["LOADED_FOLDER_LABEL_DEFAULT"],
                                    font=FONT)
        self.loaded_folder_label.grid(column=0, row=0)

        self.load_button = tk.Button(self.window, text=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON"],
                                     font=FONT, bg=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON_BG"],
                                     command = self.load_button_on_click)
        self.load_button.grid(column=1, row=0)

        self.loaded_series_label = tk.Label(self.window, text=cfg.APP_CONTENTS_CONFIG["LOADED_SERIES_LABEL_DEFAULT"],
                                    font=FONT)
        self.loaded_series_label.grid(column=2, row=0)

        self.canvas = tk.Canvas(self.window, width='512', height='512', background='gray')
        self.default_image_path = r'resources/dicom-not-loaded.png'
        self.image = ImageTk.PhotoImage(Image.open(self.default_image_path))
        self.imageID = self.canvas.create_image(256, 256, image=self.image)
        self.canvas.grid(column=0, row=1)
        self.canvas.update()

        self.slice_slider = tk.Scale(self.window, from_=100, to=0, orient=tk.VERTICAL, length=400)
        self.slice_slider.grid(column=1, row=1, sticky=tk.NW)

    def run(self):

        self.window.mainloop()

    def load_button_on_click(self):
        self.current_folder = filedialog.askdirectory()
        print(self.current_folder)

        self.dcmIO.read_dicom_folder(self.current_folder)
        print("Series: ", self.dcmIO.number_of_series)

        self.dcmIO.current_series = self.dcmIO.series[2]
        self.dcmIO.load_series()
        img = self.dcmIO.get_2d_image(25)
        self.update_canvas_image(img)

    def update_canvas_image(self, img: np.ndarray):
        img = Image.fromarray(img)
        self.image = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.imageID, image=self.image)