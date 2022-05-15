import tkinter
from enum import IntEnum
from tkinter import messagebox
from tkinter.tix import Tk
from plots import *
import customtkinter
import matplotlib


class Values(IntEnum):
    IN_WEIGHT = 0
    IN_HEIGHT = 1
    IN_LEG_GIRTH = 2
    IN_BODY_SIZE = 3
    IN_SEX = 4
    IN_SQUAT = 5

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 1080
    HEIGHT = 720
    REQUESTS = ["Введите массу человека", "Введите рост человека", "Введите обхват голени в сантиметрах",
                "Введите длину туловища в сантиметрах", "Введите пол", "Введите высоту приседа в сантиметрах"]
    LABELS = []
    ENTRIES = []

    def __init__(self):
        super().__init__()

        self.title("Vertical Jump Model by K. Khasan & A. Gogolev")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)
        self.iconbitmap("favicon.ico")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============ #

        self.frame_left.grid_rowconfigure(13, minsize=50)

        ## Input weight
        self.label_weight = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_WEIGHT],
                                                   text_font=("Roboto Medium", -16))
        self.label_weight.grid(row=0, column=0, pady=10, padx=10)
        self.entry_weight = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="72 кг")
        self.entry_weight.grid(row=1, column=0, columnspan=2, pady=0, padx=10)

        ## Input height
        self.label_height = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_HEIGHT],
                                                   text_font=("Roboto Medium", -16))
        self.label_height.grid(row=2, column=0, pady=10, padx=10)
        self.entry_height = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="178 см")
        self.entry_height.grid(row=3, column=0, columnspan=2, pady=0, padx=10)

        ## INput leg girth
        self.label_leg_girth = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_LEG_GIRTH],
                                                   text_font=("Roboto Medium", -16))
        self.label_leg_girth.grid(row=4, column=0, pady=10, padx=10)
        self.entry_leg_girth = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="38 см")
        self.entry_leg_girth.grid(row=5, column=0, columnspan=2, pady=0, padx=10)

        ## Input body size
        self.label_body_size = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_BODY_SIZE],
                                                      text_font=("Roboto Medium", -16))
        self.label_body_size.grid(row=6, column=0, pady=10, padx=10)

        self.entry_body_size = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="52 см")
        self.entry_body_size.grid(row=7, column=0, columnspan=2, pady=0, padx=10)

        ## Input sex
        self.radio_var = tkinter.StringVar(value="F")
        self.label_sex = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_SEX],
                                                text_font=("Roboto Medium", -16))
        self.label_sex.grid(row=8, column=0, pady=10, padx=20, sticky="nswe")

        self.radio_button_m = customtkinter.CTkRadioButton(master=self.frame_left, text="Мужской",
                                                           variable=self.radio_var,
                                                           value="M")
        self.radio_button_m.grid(row=9, column=0, pady=0, padx=20)
        self.radio_button_f = customtkinter.CTkRadioButton(master=self.frame_left, text="Женский",
                                                           variable=self.radio_var,
                                                           value="F")
        self.radio_button_f.grid(row=10, column=0, pady=10, padx=20)

        ## Input Squat
        self.label_squat = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_SQUAT],
                                                text_font=("Roboto Medium", -16))
        self.label_squat.grid(row=11, column=0, pady=10, padx=10, sticky="nswe")
        self.rofl = tkinter.Scale(master=self.frame_left, from_=0, to=60, orient="horizontal", background="#e3e3e3", borderwidth=3, width=20, length=200)
        self.entry_squat = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="40 см")
        # self.slider_squat = tkinter.TkSlider(master=self.frame_left, from_=0, to=60)
        self.rofl.grid(row=12, column=0, columnspan=2, padx=10)

        ## Confirm Button

        self.confirm_button = customtkinter.CTkButton(master=self.frame_left, height=40, text="Ввести данные",
                                                      border_width=3,
                                                      fg_color=None, command=self.button_event)
        self.confirm_button.grid(row=14, column=0, padx=10)

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="CTkLabel: Lorem ipsum dolor sit,\n" +
                                                        "amet consetetur sadipscing elitr,\n" +
                                                        "sed diam nonumy eirmod tempor" ,
                                                   height=100,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ frame_right ============

        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=1,
                                                number_of_steps=3,
                                                command=self.progressbar.set)
        self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
                                                command=self.progressbar.set)
        self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.slider_button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                       height=25,
                                                       text="CTkButton",
                                                       command=self.button_event)
        self.slider_button_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                       height=25,
                                                       text="CTkButton",
                                                       command=self.button_event)
        self.slider_button_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.checkbox_button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                         height=25,
                                                         text="CTkButton",
                                                         border_width=3,   # <- custom border_width
                                                         fg_color=None,   # <- no fg_color
                                                         command=self.button_event)
        self.checkbox_button_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="CTkCheckBox")
        self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="CTkCheckBox")
        self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="CTkEntry")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="CTkButton",
                                                command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.radio_button_1.select()
        # self.switch_2.select()
        self.slider_1.set(0.2)
        self.slider_2.set(0.7)
        self.progressbar.set(0.5)
        self.slider_button_1.configure(state=tkinter.DISABLED, text="Disabled Button")
        self.radio_button_3.configure(state=tkinter.DISABLED)
        self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        self.check_box_2.select()

    def button_event(self):
        print("Button pressed")

    # def change_mode(self):
    #     if self.switch_2.get() == 1:
    #         customtkinter.set_appearance_mode("dark")
    #     else:
    #         customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()