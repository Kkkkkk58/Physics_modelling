import tkinter

from jiles_atherton import AnisotropicCoefficients, IsotropicCoefficients
import customtkinter
from tkinter import messagebox
from values import Values
from plot_preisach import PlotPreisach
from plot_jiles_atherton import PlotJilesAtherton

def is_float(element: any) -> bool:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    WIDTH = 1080
    HEIGHT = 720
    REQUESTS = { Values.NORMALIZATION_COEFFICIENT : "Введите нормализующий коэффициент A", 
        Values.COERCIVE_FORCE : "Введите коэрцитивную силу Hc",
        Values.SIGMA : "Введите среднеквадратичное отклонение сигма",
        Values.DOMAIN_WALLS_DENSITY: "Плотность доменной стенки", 
        Values.INTERDOMAIN_COUPLING: "Коэффициент междоменной связи", 
        Values.SATURATION_MAGNETIZATION: "Намагниченность насыщения",
        Values.AVG_ENERGY_TO_BREAK_PINNING_SITE: "Среднее значение энергии,\nтребуемой для покидания точки закрепления",
        Values.MAGNETIZATION_REVERSIBILITY: "Коэффициент обратимости намагниченности",
        Values.AVG_ANISOTROPY_ENERGY_DENSITY: "Плотность анизотропной энергии",
        Values.ANGLE: "Угол между вектором намагниченностью\nи осью анизотропии", 
        Values.ANISOTROPIC_PARTICIPATION: "Коэффициент присутствия\nанизотроной фазы в веществе" }
    LABELS = []
    ENTRIES = []

    def __init__(self):
        super().__init__()

        self.title("Hysteresis Loop Model by K. Sasan & A. Gogolev")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                width=180,
                                                corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_right ============
        self.init_right_frame_grid()
        # ============ frame_left ============
        self.init_left_frame_grid()


        self.atherton_button = customtkinter.CTkButton(master=self.frame_right, height=40, fg_color=None, text="Модель Атертона",
                                                      border_width=3, command=self.init_atherton)
        self.atherton_button.grid(row=1, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")
        self.preisach_button = customtkinter.CTkButton(master=self.frame_right, height=40, fg_color=None, text="Модель Прейзаха",
                                                      border_width=3, command=self.init_preisach)
        self.preisach_button.grid(row=2, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")


    def init_preisach(self):

        self.reset_frame()

        # ============ create two frames ============

        # Confirm Button
        self.init_confirm_button(self.confirm_event_preisach, 14)

        # ============ frame_right ============


        # ============ frame_right ============

        self.init_start_button(self.start_plotting_preisach)

        self.init_reset_button(self.reset_preisach)
        
        self.init_disabled_buttons()

        # ============ frame_left ============ #

        self.init_preisach_left_frame()
    
    def init_atherton(self):

        self.reset_frame()

        # ============ create two frames ============
        # Confirm Button
        self.init_confirm_button(self.confirm_event_atherton, 20)

        # ============ frame_right ============

        self.init_start_button(self.start_plotting_atherton)

        self.init_reset_button(self.reset_atherton)
        
        self.init_disabled_buttons()

        # ============ frame_left ============ #
        
        self.init_atherton_left_frame()

    def reset_frame(self):
        self.frame_left.grid_forget()

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                width=180,
                                                corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

    
    def init_confirm_button(self, handler_command, curr_row):
        self.confirm_button = customtkinter.CTkButton(master=self.frame_left, height=40, fg_color=None, text="Ввести данные",
                                                      border_width=3, command=handler_command)
        self.confirm_button.grid(row=curr_row, column=0, padx=10)
        self.left_frame_elements.append(self.confirm_button)

    def init_start_button(self, handler_command):
        self.start_button = customtkinter.CTkButton(master=self.frame_right,
                                                    height=50,
                                                    text="Пуск",
                                                    command=handler_command)
        self.start_button.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")
        self.right_frame_elements.append(self.start_button)

    def init_reset_button(self, reset_func):
        self.start_button.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")
        self.right_frame_elements.append(self.start_button)
        self.reset_button = customtkinter.CTkButton(master=self.frame_right,
                                                    height=50,
                                                    text="Сброс",
                                                    border_width=3,  # <- custom border_width
                                                    fg_color=None,  # <- no fg_color
                                                    command=reset_func)
        self.reset_button.grid(row=7, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")
        self.right_frame_elements.append(self.reset_button)

    def init_right_frame_grid(self):
        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(5, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)
        self.right_frame_elements = []
    
    def init_disabled_buttons(self):
        for elem in self.right_frame_elements:
            elem.configure(state=tkinter.DISABLED)
        self.parameters_pack = []
        self.plotter = None

    def init_left_frame_grid(self):
        # self.frame_left.grid_rowconfigure((0, 1, 2, 3), minsize=35)
        # self.frame_left.grid_rowconfigure(13, minsize=80)
        self.entries = []
        self.left_frame_elements = []

    def init_preisach_left_frame(self):
        # Input A_preisach
        self.label_normalize_preisach = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.NORMALIZATION_COEFFICIENT],
                                                    text_font=("Roboto Medium", -16))
        self.label_normalize_preisach.grid(row=4, column=0, pady=0, padx=10, sticky="sn")
        self.entry_normalize_preisach = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="1")
        self.entry_normalize_preisach.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="sn")
        self.entries.append(self.entry_normalize_preisach)
        self.left_frame_elements.append(self.entry_normalize_preisach)

        # Input coercive_preisach Hc
        self.label_coercive_preisach = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.COERCIVE_FORCE],
                                                text_font=("Roboto Medium", -16))
        self.label_coercive_preisach.grid(row=6, column=0, pady=0, padx=10, sticky="sn")
        self.entry_coercive_preisach = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="20 А/м")
        self.entry_coercive_preisach.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="sn")
        self.entries.append(self.entry_coercive_preisach)
        self.left_frame_elements.append(self.entry_coercive_preisach)

        # Input sigma_preisach
        self.label_sigma_preisach = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.SIGMA],
                                                    text_font=("Roboto Medium", -16))
        self.label_sigma_preisach.grid(row=8, column=0, pady=0, padx=10, sticky="sn")
        self.entry_sigma_preisach = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="60")
        self.entry_sigma_preisach.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky="sn")
        self.entries.append(self.entry_sigma_preisach)
        self.left_frame_elements.append(self.entry_sigma_preisach)

    def init_atherton_left_frame(self):
        self.atherton_labels = []
        self.atherton_entries = []
        count = 0
        curr_row = 1
        placeholder_text = [ "470", "0.000938", "1480000", "483", "0.0889", "0", "0", "0" ]

        for key in App.REQUESTS.keys():
            if count < 3:
                count += 1
                continue
            self.atherton_labels.append(customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[key],
                                                    text_font=("Roboto Medium", -16)))
            self.atherton_labels[-1].grid(row=curr_row, column=0, pady=0, padx=10, sticky="sn")
            curr_row += 1
            self.atherton_entries.append(customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text=placeholder_text[count - 3]))
            self.atherton_entries[-1].grid(row=curr_row, column=0, columnspan=2, pady=5, padx=10, sticky="sn")
            self.entries.append(self.atherton_entries[-1])
            self.left_frame_elements.append(self.atherton_entries[-1])
            curr_row += 1
            count += 1
            if key in (Values.ANGLE, Values.AVG_ANISOTROPY_ENERGY_DENSITY, Values.ANISOTROPIC_PARTICIPATION):
                self.atherton_entries[-1].configure(state=tkinter.DISABLED)

        self.is_isotropic = tkinter.BooleanVar()
        self.dj_eban = customtkinter.CTkCheckBox(master=self.frame_left, variable=self.is_isotropic,
                 onvalue=True, offvalue=False,
                 command=self.switch_anisotropic, text="Вещество анизотропно")
        self.dj_eban.toggle()
        self.dj_eban.toggle()
        self.dj_eban.grid(row=0, column=0, pady=0, padx=10, sticky="sn")


    def confirm_event_preisach(self):
        parameters_pack = [self.entry_normalize_preisach.get(), self.entry_coercive_preisach.get(),
                           self.entry_sigma_preisach.get()]
        if any([len(x) == 0 or is_float(x) and float(x) < 0 for x in parameters_pack]):
           messagebox.showerror(title="АХАХАХАХАХХА", message="ВЫ ВВЕЛИ КРИНЖ")

        else:
            def transform(x):
                return float(x)
            self.parameters_pack = [transform(x) for x in parameters_pack]
            for elem in self.left_frame_elements:
                elem.configure(state=tkinter.DISABLED)
            for elem in self.right_frame_elements:
                elem.configure(state=tkinter.NORMAL)
    
    def start_plotting_preisach(self):
        self.plotter = PlotPreisach(self.frame_right, *self.parameters_pack)
        if self.curr_page == 1:
            self.start_button.configure(text="Вперед")

            self.curr_page = 2
        else:
            self.curr_page = 1
            self.start_button.configure(text="Назад")
        self.plotter.display()

    def confirm_event_atherton(self):
        parameters_pack = [x.get() for x in self.atherton_entries]
        if any([len(x) == 0 or is_float(x) and float(x) < 0 for x in parameters_pack[:5]]):
           messagebox.showerror(title="АХАХАХАХАХХА", message="ВЫ ВВЕЛИ КРИНЖ")

        else:
            def transform(x):
                return float(x)
        isotropicCoefs = IsotropicCoefficients(*[transform(x) for x in parameters_pack[:5]])
        self.parameters_pack = [isotropicCoefs]
        if not self.is_isotropic:
            anisotropicCoefs = AnisotropicCoefficients(*[transform(x) for x in parameters_pack[-3:]])
            self.parameters_pack.append(anisotropicCoefs)

        for elem in self.left_frame_elements:
            elem.configure(state=tkinter.DISABLED)
        for elem in self.right_frame_elements:
            elem.configure(state=tkinter.NORMAL)

    def start_plotting_atherton(self):
        self.plotter = PlotJilesAtherton(self.frame_right, *self.parameters_pack)
        self.plotter.display()

    def switch_anisotropic(self):
        if self.is_isotropic.get():
            for elem in self.atherton_entries[-3:]:
                elem.configure(state=tkinter.DISABLED)
        else:
            for elem in self.atherton_entries:
                elem.configure(state=tkinter.NORMAL)

        
    def reset_preisach(self):
        self.reset(len(self.left_frame_elements))

    def reset_atherton(self):
        self.reset(6)

    def reset(self, n):
        self.start_button.configure(text="Пуск")
        self.curr_page = 1
        for elem in self.left_frame_elements[:n]:
            elem.configure(state=tkinter.NORMAL)
        for elem in self.right_frame_elements:
            elem.configure(state=tkinter.DISABLED)

    def on_closing(self):
        self.quit()

    def start(self):
        self.mainloop()