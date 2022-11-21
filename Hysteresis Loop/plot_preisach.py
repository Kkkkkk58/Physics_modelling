from matplotlib import pyplot as plt
from preisach import PreisachModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotPreisach:
    def __init__(self, frame, normalize_preisach, coercive_preisach, sigma_preisach):
        self.frame = frame
        self.preisach = PreisachModel(200, 1)
        self.preisach.configureModelState2(normalize_preisach, coercive_preisach, sigma_preisach)
        self.ani, self.fig, self.ax1, self.ax2, self.ax3 = self.preisach.printHysteresis()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, pady=0, padx=0, ipadx=0, sticky="nswe")
    def display(self):
        self.canvas.draw()
    
    def reset(self):
        self.ani.event_source.stop()
        self.canvas.flush_events()
        # self.canvas.delete("all")