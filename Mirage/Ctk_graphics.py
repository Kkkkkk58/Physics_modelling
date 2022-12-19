import tkinter
import customtkinter
from tkinter import messagebox
from values import Values
from plotter import Plotter
from PIL import Image

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

        self.title("Mirage Model by K.Khasan & A.Gogolev")
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
        # Input initial refracrive index
        self.label_n0 = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.INITIAL_REFRACTIVE_INDEX])
        self.label_n0.grid(row=0, column=0, pady=10, padx=10)
        self.entry_n0 = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="1.0004")
        self.entry_n0.grid(row=1, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_n0)
        self.left_frame_elements.append(self.entry_n0)

        # Input initial angle
        self.label_angle = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.ANGLE])
        self.label_angle.grid(row=2, column=0, pady=10, padx=10)
        self.entry_angle = customtkinter.CTkEntry(master=self.frame_left, width=80, placeholder_text="30")
        self.entry_angle.grid(row=3, column=0, columnspan=2, pady=0, padx=10)
        self.entries.append(self.entry_angle)
        self.left_frame_elements.append(self.entry_angle)

        # Input gamma coeffecient 
        self.label_gamma = customtkinter.CTkLabel(master=self.frame_left, text=App.REQUESTS[Values.REFRACTIVE_INDEX_COEFFICIENT])
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
        self.help_button = customtkinter.CTkButton(master=self.frame_right,
                                                    height=40,
                                                    text="Справка",
                                                    command=self.display_help)
        self.help_button.grid(row=8, column=2, columnspan=1, pady=10, padx=20, sticky="nswe")


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

    def display_help(self):
        self.textbox = customtkinter.CTkTextbox(master=self.frame_mid, width=540, height=540)
        self.textbox.grid(row=0, column=0, columnspan=4, pady=10, padx=30, sticky="nswe")
        self.textbox.insert("0.0", """Я в своем познании настолько преисполнился, что я как будто бы уже
сто триллионов миллиардов лет проживаю на триллионах и
триллионах таких же планет, как эта Земля, мне этот мир абсолютно
понятен, и я здесь ищу только одного - покоя, умиротворения и
вот этой гармонии, от слияния с бесконечно вечным, от созерцания
великого фрактального подобия и от вот этого замечательного всеединства
существа, бесконечно вечного, куда ни посмотри, хоть вглубь - бесконечно
малое, хоть ввысь - бесконечное большое, понимаешь? А ты мне опять со
своим вот этим, иди суетись дальше, это твоё распределение, это
твой путь и твой горизонт познания и ощущения твоей природы, он
несоизмеримо мелок по сравнению с моим, понимаешь? Я как будто бы уже
давно глубокий старец, бессмертный, ну или там уже почти бессмертный,
который на этой планете от её самого зарождения, ещё когда только Солнце
только-только сформировалось как звезда, и вот это газопылевое облако,
вот, после взрыва, Солнца, когда оно вспыхнуло, как звезда, начало
формировать вот эти коацерваты, планеты, понимаешь, я на этой Земле уже
как будто почти пять миллиардов лет живу и знаю её вдоль и поперёк
этот весь мир, а ты мне какие-то... мне не важно на твои тачки, на твои
яхты, на твои квартиры, там, на твоё благо. Я был на этой
планете бесконечным множеством, и круче Цезаря, и круче Гитлера, и круче
всех великих, понимаешь, был, а где-то был конченым говном, ещё хуже,
чем здесь. Я множество этих состояний чувствую. Где-то я был больше
подобен растению, где-то я больше был подобен птице, там, червю, где-то
был просто сгусток камня, это всё есть душа, понимаешь? Она имеет грани
подобия совершенно многообразные, бесконечное множество. Но тебе этого
не понять, поэтому ты езжай себе , мы в этом мире как бы живем
разными ощущениями и разными стремлениями, соответственно, разное наше и 
место, разное и наше распределение. Тебе я желаю все самые крутые тачки
чтоб были у тебя, и все самые лучше самки, если мало идей, обращайся ко мне, я тебе на каждую твою идею предложу сотню триллионов, как всё делать. Ну а я всё, я иду как глубокий старец,узревший вечное, прикоснувшийся к Божественному, сам стал богоподобен и устремлен в это бесконечное, и который в умиротворении, покое, гармонии, благодати, в этом сокровенном блаженстве пребывает, вовлеченный во всё и во вся, понимаешь, вот и всё, в этом наша разница. Так что я иду любоваться мирозданием, а ты идёшь преисполняться в ГРАНЯХ каких-то, вот и вся разница, понимаешь, ты не зришь это вечное бесконечное, оно тебе не нужно. Ну зато ты, так сказать, более активен, как вот этот дятел долбящий, или муравей, который очень активен в своей стезе, поэтому давай, наши пути здесь, конечно, имеют грани подобия, потому что всё едино, но я-то тебя прекрасно понимаю, а вот ты меня - вряд ли, потому что я как бы тебя в себе содержу, всю твою природу, она составляет одну маленькую там песчиночку, от того что есть во мне, вот и всё, поэтому давай, ступай, езжай, а я пошел наслаждаться прекрасным осенним закатом на берегу теплой южной реки. Всё, ступай, и я пойду.
""")  # insert at line 0 character 0
        self.textbox.configure(state="disabled")  # configure textbox to be read-only
        
        

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
