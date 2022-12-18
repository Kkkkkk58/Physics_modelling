from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mirage import Mirage

class Plotter:
    def __init__(self, frame, n0, alpha0, gamma):
        self.frame = frame
        self.mirage = Mirage(n0, alpha0, gamma)
        self.fig, self.ax1, self.ax2 = self.mirage.get_plot_data()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, pady=0, padx=0, ipadx=0, sticky="nswe")

    def plot(self):
        self.canvas.draw()

    def reset(self):
        self.canvas.flush_events()