from matplotlib import pyplot as plt
from jiles_atherton import JilesAthertonModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotJilesAtherton:
    def __init__(self, frame, isotropic, anisotropic = None):
        self.frame = frame
        self.jiles_atherton = JilesAthertonModel()
        self.jiles_atherton.set_isotropic(isotropic)
        self.jiles_atherton.set_anisotropic(anisotropic)
        self.fig, self.ax = self.jiles_atherton.get_plot_data()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, pady=0, padx=0, ipadx=0, sticky="nswe")

    def display(self):
        self.canvas.draw()
    
    def reset(self):
        self.canvas.flush_events()
        self.canvas.delete("all")
