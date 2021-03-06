import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import src.config as cfg
from src.DicomIO import DicomIO
from src.DicomCutter import DicomCutter
import numpy as np


FONT = cfg.APP_FONT_CONFIG["FONT"]


class App:
    """

    """

    def __init__(self):
        self.ORIENTATION = 'AX'
        self.dicom_loaded = False

        self.window = None
        self.dcmIO = DicomIO()
        self.dicom_cutter = DicomCutter()
        self.dicom_cutter.orig_canvas_size = (512, 512)
        self.roi = ()

        self.loaded_folder_label = None
        self.loaded_series_label = None
        self.loaded_series = None
        self.loaded_series_listview = None

        self.load_button = None
        self.unload_button = None
        self.load_series_button = None
        self.unload_series_button = None
        self.axial_orientation_checkbox = None
        self.sagittal_orientation_checkbox = None
        self.coronal_orientation_checkbox = None
        self.current_folder = None

        self.cut_button = None

        self.image_frame = None
        self.canvas = None
        self.imageID = None
        self.region_of_interest = None
        self.image = None
        self.default_image_path = r'resources/dicom-not-loaded.png'
        self.slice_slider = None

        self.points = []

        self.create_window()
        self.create_UI()
        self.run()

    def create_window(self):
        self.window = tk.Tk()
        self.window.title(cfg.BASIC_WINDOW_CONFIG["TITLE"])

    def create_UI(self):
        self.load_button = tk.Button(self.window, text=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON"],
                                     font=FONT, bg=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON_BG"],
                                     command=self.load_button_on_click)
        self.load_button.grid(column=0, row=0)

        self.loaded_folder_label = tk.Label(self.window, text=cfg.APP_CONTENTS_CONFIG["LOADED_FOLDER_LABEL_DEFAULT"],
                                            font=FONT)
        self.loaded_folder_label.grid(column=0, row=1)

        self.loaded_series_listview = tk.Listbox(self.window, width='50', height='20')
        self.loaded_series_listview.grid(column=0, row=2)

        self.loading_series_buttons = tk.Frame(self.window)

        self.load_series_button = tk.Button(self.loading_series_buttons, text="Load selected series", font=FONT,
                                            bg=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON_BG"],
                                            command=self.load_series_button_on_click)

        self.unload_series_button = tk.Button(self.loading_series_buttons, text="Unload selected series", font=FONT,
                                              bg=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON_BG"],
                                              command=self.unload_series)

        self.load_series_button.pack(side=tk.TOP)
        self.unload_series_button.pack(side=tk.BOTTOM)
        self.loading_series_buttons.grid(column=0, row=3)

        self.cut_button = tk.Button(self.window, text="Confirm cut", font=FONT,
                                    bg=cfg.APP_CONTENTS_CONFIG["LOAD_FOLDER_BUTTON_BG"],
                                    command=self.confirm_cut_on_click)
        self.cut_button.grid(column=0, row=4)

        #####
        self.image_frame = tk.Frame(self.window)
        self.slice_slider = tk.Scale(self.image_frame, from_=100, to=0, orient=tk.VERTICAL, length=400,
                                     command=self.slider_value_changed)
        self.slice_slider.pack(side=tk.RIGHT)
        self.canvas = tk.Canvas(self.image_frame, width=512, height=512, background='gray')
        self.canvas.pack(side=tk.LEFT)
        self.canvas.update()
        self.canvas.bind('<Button>', self.mouse_click_canvas)
        self.set_default_canvas()
        self.image_frame.grid(column=1, row=1, rowspan=4, columnspan=3)

        self.axial_orientation_checkbox = tk.Checkbutton(self.window, text='Axial', 
                                                         state=tk.DISABLED,
                                                         command=self.axial_orientation_selected)
        self.axial_orientation_checkbox.grid(column=1, row=0)

        self.sagittal_orientation_checkbox = tk.Checkbutton(self.window, text='Sagittal', 
                                                            state=tk.DISABLED,
                                                            command=self.sagittal_orientation_selected)
        self.sagittal_orientation_checkbox.grid(column=2, row=0)

        self.coronal_orientation_checkbox = tk.Checkbutton(self.window, text='Coronal', 
                                                           state=tk.DISABLED,
                                                           command=self.coronal_orientation_selected)
        self.coronal_orientation_checkbox.grid(column=3, row=0)
        #####

    def mouse_click_canvas(self, event):
        if self.dicom_loaded:
            if len(self.points) < 2:
                self.points.append((event.x, event.y))
            if len(self.points) == 2:
                self.draw_rect_on_canvas()
                self.points = []

    def run(self):
        self.window.mainloop()

    def load_button_on_click(self):
        self.current_folder = filedialog.askdirectory()
        self.dcmIO.clear_loaded()
        self.dcmIO.read_dicom_folder(self.current_folder)
        self.loaded_folder_label.configure(text=cfg.APP_CONTENTS_CONFIG["LOADED_FOLDER_LABEL_LOADED"] + self.current_folder)

        self.update_listview()

    def set_default_canvas(self):
        self.image = ImageTk.PhotoImage(Image.open(self.default_image_path))
        self.imageID = self.canvas.create_image(256, 256, image=self.image)
        self.slice_slider.configure(state=tk.DISABLED)


    def update_canvas_image(self, img: np.ndarray):
        img = Image.fromarray(img)
        self.image = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.imageID, image=self.image)
        self.canvas.configure(width=img.shape[1], height=img.shape[0])
        self.dicom_cutter.orig_canvas_size = (self.canvas.width, self.canvas.height)
        self.canvas.update()

    def slider_value_changed(self, val):
        try:
            self.update_canvas_image(self.dcmIO.get_2d_image(self.slice_slider.get()))
        except Exception:
            pass
    
    def update_slider_values(self):
        if self.ORIENTATION == 'AX':
            self.slice_slider.configure(from_=self.dcmIO.current_3D.shape[2] - 1, to=0)
        elif self.ORIENTATION == 'SAG':
            self.slice_slider.configure(from_=self.dcmIO.current_3D.shape[0] - 1, to=0)
        elif self.ORIENTATION == 'COR':
            self.slice_slider.configure(from_=self.dcmIO.current_3D.shape[1] - 1, to=0)
    
    def load_series_button_on_click(self):
        selected = self.loaded_series_listview.curselection()[0]

        self.dcmIO.current_series = self.dcmIO.series[selected]
        self.dcmIO.load_series()
        self.dicom_cutter.original_3d_image = self.dcmIO.current_3D
        self.slice_slider.configure(state=tk.NORMAL)
        self.update_slider_values()
        self.slice_slider.set(0)
        self.slider_value_changed(0)
        self.dicom_loaded = True
        
        self.axial_orientation_checkbox.configure(state=tk.NORMAL)
        self.axial_orientation_checkbox.select()
        self.sagittal_orientation_checkbox.configure(state=tk.NORMAL)
        self.coronal_orientation_checkbox.configure(state=tk.NORMAL)

    def unload_series(self):
        self.dcmIO.current_series = None
        self.dcmIO.current_3D = None
        self.dcmIO.cut3D = None
        self.set_default_canvas()
        self.axial_orientation_checkbox.configure(state=tk.DISABLED)
        self.axial_orientation_checkbox.deselect()
        self.sagittal_orientation_checkbox.configure(state=tk.DISABLED)
        self.sagittal_orientation_checkbox.deselect()
        self.coronal_orientation_checkbox.configure(state=tk.DISABLED)
        self.coronal_orientation_checkbox.deselect()

    def update_listview(self):
        self.loaded_series_listview.delete(0, self.loaded_series_listview.size()-1)
        for index, series in enumerate(self.dcmIO.series):
            self.loaded_series_listview.insert(index, "Description: " + str(series.Description) + " " +
                                                str(series.PatientName) + ": Slices: " + str(series.Slices))

    def draw_rect_on_canvas(self):
        x1, y1 = self.points[0]
        x3, y3 = self.points[1]
        x2, y2 = x3, y1
        x4, y4 = x1, y3
        self.roi = self.points

        self.canvas.delete(self.region_of_interest)
        self.region_of_interest = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                                                             outline='red', fill="", width=3)

    def confirm_cut_on_click(self):
        if self.region_of_interest is not None:
            cut_image = self.dicom_cutter.cut(self.roi)
            self.dcmIO.cut3D = cut_image
            self.dcmIO.save_cut3D()

    def axial_orientation_selected(self):
        self.sagittal_orientation_checkbox.deselect()
        self.coronal_orientation_checkbox.deselect()
        self.ORIENTATION = 'AX'
        self.dicom_cutter.cut_plane = self.ORIENTATION
        self.dcmIO.ORIENTATION = self.ORIENTATION
        self.update_slider_values()
        self.slice_slider.set(0)
        self.slider_value_changed(0)

    def sagittal_orientation_selected(self):
        self.axial_orientation_checkbox.deselect()
        self.coronal_orientation_checkbox.deselect()
        self.ORIENTATION = 'SAG'
        self.dcmIO.ORIENTATION = self.ORIENTATION
        self.dicom_cutter.cut_plane = self.ORIENTATION
        self.update_slider_values()
        self.slice_slider.set(0)
        self.slider_value_changed(0)

    def coronal_orientation_selected(self):
        self.axial_orientation_checkbox.deselect()
        self.sagittal_orientation_checkbox.deselect()
        self.ORIENTATION = 'COR'
        self.dcmIO.ORIENTATION = self.ORIENTATION
        self.dicom_cutter.cut_plane = self.ORIENTATION
        self.update_slider_values()
        self.slice_slider.set(0)
        self.slider_value_changed(0)
        
