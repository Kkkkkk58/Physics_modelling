from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DiscreteDomainFiniteSquareWell import DiscreteDomainFiniteSquareWell


class Plotter:
    def __init__(self, frame, well_width, well_depth):
        self.frame = frame
        self.finite_well = DiscreteDomainFiniteSquareWell(well_width, well_depth)
        self.x = self.finite_well.get_x()
        self.eigen_values = self.finite_well.get_eigen_values()
        # self.fig = plt.figure(figsize=(12, 12), facecolor="#2f2e30")
        self.fig, (ax, ax2) = plt.subplots(1, 2)
        self.fig.set_figwidth(8)
        self.fig.set_figheight(8)
        self.fig.set_facecolor("#2b2b2b")
        # ax.set_ylim(0, 2E-5)
        left_outside_x = self.finite_well.left_x
        right_outside_x = self.finite_well.right_x
        print(self.x)
        print(self.eigen_values)
        offset_delta = self.eigen_values[0]
        y_offset = 0
        for n in range(len(self.eigen_values)):
            y_offset += self.eigen_values[n]
            print(n)
            wave_function_vals = self.finite_well.get_nth_state_eigen_function_vals(n)
            print(wave_function_vals)

            left_vals = self.finite_well.get_outside_left_nth_state_eigen_function_vals(n)
            right_vals = self.finite_well.get_outside_right_nth_state_eigen_function_vals(n)
            # ax2.plot(left_outside_x, left_vals ** 2, linewidth=2)
            ax.plot(self.x, (wave_function_vals ** 2 * 1E4 + y_offset), linewidth=2, label=f'{n} Энергетический уровень, {self.eigen_values[n]} В')
            ax2.plot(self.x, wave_function_vals ** 2 * 1E4, linewidth=2)
            # ax2.plot(right_outside_x, (right_vals ** 2 + y_offset), linewidth=2)

        self.set_colors(ax)
        ax.grid(color='black')

        # ax.set_xlabel('X, m')
        # ax.set_ylabel('Y, m')
        # ax2 = plt.subplot(1, 2, 2)
        # ax2.plot(self.x, ?, linewidth=1)
        self.set_colors(ax2)
        ax2.grid(color='black')
        # ax2.set_xlabel('x, m')
        # ax2.set_ylabel('alpha, deg')
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
