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

        self.image_frame = None
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
                                     command=self.load_button_on_click)
        self.load_button.grid(column=1, row=0)

        self.loaded_series_label = tk.Label(self.window, text=cfg.APP_CONTENTS_CONFIG["LOADED_SERIES_LABEL_DEFAULT"],
                                            font=FONT)
        self.loaded_series_label.grid(column=2, row=0)

        #####
        self.image_frame = tk.Frame(self.window)
        self.canvas = tk.Canvas(self.image_frame, width='512', height='512', background='gray')
        self.default_image_path = r'../resources/dicom-not-loaded.png'
        self.image = ImageTk.PhotoImage(Image.open(self.default_image_path))
        self.imageID = self.canvas.create_image(256, 256, image=self.image)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.update()

        self.slice_slider = tk.Scale(self.image_frame, from_=100, to=0, orient=tk.VERTICAL, length=400,
                                     command=self.slider_value_changed)
        self.slice_slider.pack(side=tk.LEFT)
        self.image_frame.grid(column=0, row=1)
        #####

    def run(self):

        self.window.mainloop()

    def load_button_on_click(self):
        self.current_folder = filedialog.askdirectory()
        print(self.current_folder)

        self.dcmIO.read_dicom_folder(self.current_folder)
        self.loaded_folder_label.configure(text=cfg.APP_CONTENTS_CONFIG["LOADED_FOLDER_LABEL_LOADED"] + self.current_folder)

        self.dcmIO.current_series = self.dcmIO.series[2]
        self.dcmIO.load_series()
        self.slice_slider.configure(from_=self.dcmIO.current_3D.shape[2]-1, to=0)

    def update_canvas_image(self, img: np.ndarray):
        img = Image.fromarray(img)
        self.image = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.imageID, image=self.image)

    def slider_value_changed(self, val):
        self.update_canvas_image(self.dcmIO.get_2d_image(self.slice_slider.get()))
