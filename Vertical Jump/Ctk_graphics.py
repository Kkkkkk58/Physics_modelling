import tkinter
from plots import *
import customtkinter
from tkinter import messagebox

is_adv_digit = lambda x: x.isdigit() if x[:1] != '-' else x[1:].isdigit()

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

        self.frame_left.grid_rowconfigure(13, minsize=75)
        self.entries = []
        self.left_frame_elements = []
        # Input weight
        self.label_weight = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_WEIGHT],
                                                   text_font=("Roboto Medium", -16))
        self.label_weight.grid(row=0, column=0, pady=10, padx=10)
        self.entry_weight = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="72 кг")
        self.entry_weight.grid(row=1, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_weight)
        self.left_frame_elements.append(self.entry_weight)

        # Input height
        self.label_height = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_HEIGHT],
                                                   text_font=("Roboto Medium", -16))
        self.label_height.grid(row=2, column=0, pady=10, padx=10)
        self.entry_height = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="178 см")
        self.entry_height.grid(row=3, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_height)
        self.left_frame_elements.append(self.entry_height)

        # Input leg girth
        self.label_leg_girth = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_LEG_GIRTH],
                                                      text_font=("Roboto Medium", -16))
        self.label_leg_girth.grid(row=4, column=0, pady=10, padx=10)
        self.entry_leg_girth = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="38 см")
        self.entry_leg_girth.grid(row=5, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_leg_girth)
        self.left_frame_elements.append(self.entry_leg_girth)

        # Input body size
        self.label_body_size = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_BODY_SIZE],
                                                      text_font=("Roboto Medium", -16))
        self.label_body_size.grid(row=6, column=0, pady=10, padx=10)

        self.entry_body_size = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="52 см")
        self.entry_body_size.grid(row=7, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_body_size)
        self.left_frame_elements.append(self.entry_body_size)

        # Input sex
        self.sex_var = tkinter.StringVar(value="F")
        self.label_sex = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_SEX],
                                                text_font=("Roboto Medium", -16))
        self.label_sex.grid(row=8, column=0, pady=10, padx=20, sticky="nswe")

        self.radio_button_m = customtkinter.CTkRadioButton(master=self.frame_left, text="Мужской",
                                                           variable=self.sex_var,
                                                           value="M")
        self.radio_button_m.grid(row=9, column=0, pady=0, padx=20)
        self.radio_button_f = customtkinter.CTkRadioButton(master=self.frame_left, text="Женский",
                                                           variable=self.sex_var,
                                                           value="F")
        self.radio_button_f.grid(row=10, column=0, pady=10, padx=20)
        self.left_frame_elements.append(self.radio_button_f)
        self.left_frame_elements.append(self.radio_button_m)

        # Input Squat
        self.squat_var = tkinter.IntVar(value=0)
        self.label_squat = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.IN_SQUAT],
                                                  text_font=("Roboto Medium", -16))
        self.label_squat.grid(row=11, column=0, pady=10, padx=10, sticky="nswe")
        self.slider_squat = tkinter.Scale(master=self.frame_left, variable=self.squat_var, from_=0, to=60,
                                          orient="horizontal", background="#e3e3e3",
                                          borderwidth=3, width=20, length=200)
        # self.slider_squat = tkinter.TkSlider(master=self.frame_left, from_=0, to=60)
        self.slider_squat.grid(row=12, column=0, columnspan=2, padx=10)
        self.left_frame_elements.append(self.slider_squat)

        # Confirm Button

        self.confirm_button = customtkinter.CTkButton(master=self.frame_left, height=40, text="Ввести данные",
                                                      border_width=3,
                                                      fg_color=None, command=self.confirm_event)
        self.confirm_button.grid(row=14, column=0, padx=10)
        self.left_frame_elements.append(self.confirm_button)

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(5, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)
        self.right_frame_elements = []

        # ============ frame_right ============

        self.curr_page = 1
        self.start_button = customtkinter.CTkButton(master=self.frame_right,
                                                    height=40,
                                                    text="Пуск",
                                                    command=self.start_plotting)
        self.start_button.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")
        self.right_frame_elements.append(self.start_button)
        self.reset_button = customtkinter.CTkButton(master=self.frame_right,
                                                    height=40,
                                                    text="Сброс",
                                                    border_width=3,  # <- custom border_width
                                                    fg_color=None,  # <- no fg_color
                                                    command=self.reset)
        self.reset_button.grid(row=7, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")
        self.right_frame_elements.append(self.reset_button)

        self.velocity_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=120,
                                                     placeholder_text="Введите скорость прыжка в метрах в секунду")
        self.velocity_entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        self.right_frame_elements.append(self.velocity_entry)
        #
        # self.velocity_confirm_button = customtkinter.CTkButton(master=self.frame_right,
        #                                                        text="Подтвердить")
        # self.velocity_confirm_button.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")
        # self.right_frame_elements.append(self.velocity_confirm_button)

        # set default values
        for elem in self.right_frame_elements:
            elem.configure(state=tkinter.DISABLED)
        self.parameters_pack = []
        self.plotter = None

    def confirm_event(self):
        parameters_pack = [self.entry_weight.get(), self.entry_height.get(),
                           self.entry_leg_girth.get(), self.entry_body_size.get(),
                           self.sex_var.get(), self.squat_var.get()]
        #DEBUG_DELETED
        if any([len(str(x)) == 0 or is_adv_digit(str(x)) and int(x) < 0 for x in parameters_pack]):
           messagebox.showerror(title="АХАХАХАХАХХА", message="ВЫ ВВЕЛИ КРИНЖ")

        else:
            def transform(x):
                return int(str(x)) if str(x) not in "MF" else str(x)
            self.parameters_pack = [transform(x) for x in parameters_pack]
            for elem in self.left_frame_elements:
                elem.configure(state=tkinter.DISABLED)
            for elem in self.right_frame_elements:
                elem.configure(state=tkinter.NORMAL)

    def start_plotting(self):
        speed = self.velocity_entry.get()
        if len(str(speed)) == 0 or is_adv_digit(str(speed)) and int(speed) < 0:
            messagebox.showerror(title="АХАХАХАХАХХА", message="ВЫ ВВЕЛИ КРИНЖ")
            return
        else:
            self.velocity_entry.configure(state=tkinter.DISABLED)
        self.plotter = Plotter(self.frame_right, self.parameters_pack, int(str(speed)), self.curr_page)
        if self.curr_page == 1:
            self.start_button.configure(text="Вперед")

            self.curr_page = 2
        else:
            self.curr_page = 1
            self.start_button.configure(text="Назад")
        self.plotter.plot()

    def reset(self):
        self.start_button.configure(text="Пуск")
        self.curr_page = 1
        for elem in self.left_frame_elements:
            elem.configure(state=tkinter.NORMAL)
        for elem in self.right_frame_elements:
            elem.configure(state=tkinter.DISABLED)
        if self.plotter is not None:
            self.plotter.reset()

    def on_closing(self):
        self.quit()

    def start(self):
        self.mainloop()
