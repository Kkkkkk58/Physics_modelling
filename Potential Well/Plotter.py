from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DiscreteDomainFiniteSquareWell import DiscreteDomainFiniteSquareWell


class Plotter:
    def __init__(self, frame, potential_well):
        self.frame = frame
        self.finite_well = potential_well
        self.x = self.finite_well.get_x()
        self.eigen_values = self.finite_well.get_eigen_values()
        self.fig, (ax, ax2) = plt.subplots(1, 2)
        self.fig.set_figwidth(8)
        self.fig.set_figheight(8)
        self.fig.set_facecolor("#2b2b2b")
        print(self.x)
        print(self.eigen_values)
        y_offset = 0
        for n in range(len(self.eigen_values)):
            y_offset += self.eigen_values[n]
            print(n)
            wave_function_vals = self.finite_well.get_nth_state_eigen_function_vals(n)
            print(wave_function_vals)
            ax.plot(self.x, (wave_function_vals ** 2 * 1E4 + y_offset), linewidth=2, label=f'{n} Энергетический уровень, {self.eigen_values[n]} В')
            ax2.plot(self.x, wave_function_vals ** 2 * 1E4, linewidth=2)

        self.set_colors(ax)
        ax.grid(color='black')

        self.set_colors(ax2)
        ax2.grid(color='black')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, pady=0, padx=0, ipadx=0, sticky="nswe")

    def plot(self):
        self.canvas.draw()

    def reset(self):
        self.canvas.flush_events()

    def set_colors(self, ax):
        ax.grid(color='black')
        ax.set_facecolor("#b3b3b3")
        ax.spines['bottom'].set_color("#b3b3b3")
        ax.spines['left'].set_color("#b3b3b3")
        ax.spines['right'].set_color("#b3b3b3")
        ax.spines['top'].set_color("#b3b3b3")
        ax.xaxis.label.set_color("#b3b3b3")
        ax.yaxis.label.set_color("#b3b3b3")
        ax.tick_params(axis='x', colors="#b3b3b3")
        ax.tick_params(axis='y', colors="#b3b3b3")
