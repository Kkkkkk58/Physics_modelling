import tkinter
import customtkinter
from tkinter import messagebox
from values import Values
from plotter import Plotter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

class App(customtkinter.CTk):

    WIDTH = 1920
    HEIGHT = 1080
    REQUESTS = {
        Values.INITIAL_REFRACTIVE_INDEX: "Показатель преломления\nна начальной высоте",
        Values.ANGLE: "Начальный угол падения",
        Values.REFRACTIVE_INDEX_COEFFICIENT: "Коэффициент убывания\nпоказателя преломления"
        }
    LABELS = []
    ENTRIES = []

    def __init__(self):
        super().__init__()

        self.title("Mirage Model by A.Gogolev & K.Khasan")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
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
        self.frame_right.grid(row=0, column=2, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============ #

        self.frame_left.grid_rowconfigure(13, minsize=75)
        self.entries = []
        self.left_frame_elements = []
        # Input weight
        self.label_n0 = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.INITIAL_REFRACTIVE_INDEX],
                                                   text_font=("Roboto Medium", -16))
        self.label_n0.grid(row=0, column=0, pady=10, padx=10)
        self.entry_n0 = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="1.0004")
        self.entry_n0.grid(row=1, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_n0)
        self.left_frame_elements.append(self.entry_n0)

        # Input height
        self.label_angle = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.ANGLE],
                                                   text_font=("Roboto Medium", -16))
        self.label_angle.grid(row=2, column=0, pady=10, padx=10)
        self.entry_angle = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="30")
        self.entry_angle.grid(row=3, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_angle)
        self.left_frame_elements.append(self.entry_angle)

        # Input leg girth
        self.label_gamma = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.REFRACTIVE_INDEX_COEFFICIENT],
                                                      text_font=("Roboto Medium", -16))
        self.label_gamma.grid(row=4, column=0, pady=10, padx=10)
        self.entry_gamma = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="0.00002")
        self.entry_gamma.grid(row=5, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_gamma)
        self.left_frame_elements.append(self.entry_gamma)
        # Confirm Button

        self.confirm_button = customtkinter.CTkButton(master=self.frame_left, height=40, text="Ввести данные",
                                                      border_width=3,
                                                      fg_color=None, command=self.confirm_event)
        self.confirm_button.grid(row=14, column=0, padx=10)
        self.left_frame_elements.append(self.confirm_button)

        # ============ frame_mid ============
        self.frame_mid = customtkinter.CTkFrame(master=self, width=720, corner_radius=20)
        self.frame_mid.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.init_mid_frame_grid()

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.init_right_frame_grid()

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

        for elem in self.right_frame_elements:
            elem.configure(state=tkinter.DISABLED)
        self.parameters_pack = []
        self.plotter = None
    
    def init_right_frame_grid(self):
        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(5, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)
        self.right_frame_elements = []

    def init_mid_frame_grid(self):
        self.frame_mid.rowconfigure(0, weight=1)
        self.frame_mid.rowconfigure(1, weight=2)
        self.frame_mid.rowconfigure(2, weight=1)

    def confirm_event(self):
        parameters_pack = [self.entry_n0.get(), self.entry_angle.get(), self.entry_gamma.get()]
        if any([len(str(x)) == 0 or not is_float(str(x)) for x in parameters_pack]):
           messagebox.showerror(title="АХАХАХАХАХХА", message="ВЫ ВВЕЛИ КРИНЖ")

        else:
            def transform(x):
                return float(str(x))
            self.parameters_pack = [transform(x) for x in parameters_pack]
            for elem in self.left_frame_elements:
                elem.configure(state=tkinter.DISABLED)
            for elem in self.right_frame_elements:
                elem.configure(state=tkinter.NORMAL)

    def start_plotting(self):
        self.plotter = Plotter(self.frame_mid, *self.parameters_pack)
        self.plotter.plot()

    def reset(self):
        self.plotter.reset()
        self.start_button.configure(text="Пуск")
        for elem in self.frame_mid.winfo_children():
            elem.destroy()
        for elem in self.left_frame_elements: 
            elem.configure(state=tkinter.NORMAL)
        for elem in self.right_frame_elements:
            elem.configure(state=tkinter.DISABLED)

    def on_closing(self):
        self.quit()

    def start(self):
        self.mainloop()
