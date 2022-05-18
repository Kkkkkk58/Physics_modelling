from plots import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class PlotAnimation:
    GRAPH_COUNT = 4

    def __init__(self, frame, human):

        self.frame = frame
        self.fig, self.axs = plt.subplots(2, 2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, pady=0, padx=0, ipadx=0, sticky="nswe")

        # evaluate human object (parameters should be pulled from gui)
        self.human = human
        self.evaluation = VerticalJumpEvaluation(self.human, 8)
        self.terminal_time = self.evaluation.flight_time()

        self.axes_info = [
            [{'xlabel': 'Time(s)', 'ylabel': 'Coordinate (m)', 'ylim': (0, 10), 'xlim': (0, self.terminal_time),
              'color': 'r'},
             {'xlabel': 'Time(s)', 'ylabel': 'Velocity (m/s)', 'ylim': (-10, 10), 'xlim': (0, self.terminal_time),
              'color': 'g'}],
            [{'xlabel': 'Time(s)', 'ylabel': 'Total Energy (j)', 'ylim': (0, 5000), 'xlim': (0, self.terminal_time),
              'color': 'b'},
             {'xlabel': 'Time(s)', 'ylabel': 'Distance (m)', 'ylim': (0, 30), 'xlim': (0, self.terminal_time),
              'color': 'c'}]
        ]

        # Initializing all the axes
        for i in range(0, 2):
            for j in range(0, 2):
                self.axs[i][j].set_xlabel(self.axes_info[i][j]['xlabel'])
                self.axs[i][j].set_ylabel(self.axes_info[i][j]['ylabel'])
                self.axs[i][j].set_ylim(self.axes_info[i][j]['ylim'])
                # axs[i][j].set_xlim(AXES_INFO[i][j]['xlim'])
                self.axs[i][j].set_xlim(0, self.terminal_time)
                self.axs[i][j].minorticks_on()
                # включаем основную сетку
                self.axs[i][j].grid(which='major')
                # включаем дополнительную сетку
                self.axs[i][j].grid(which='minor', linestyle=':')

        plt.subplots_adjust(hspace=0.9, wspace=0.8, top=0.9)

        # initializing all the lines
        line1, = self.axs[0][0].plot([], [], lw=2, color=self.axes_info[0][0]['color'])
        line2, = self.axs[0][1].plot([], [], lw=2, color=self.axes_info[0][1]['color'])
        line3, = self.axs[1][0].plot([], [], lw=2, color=self.axes_info[1][0]['color'])
        line4, = self.axs[1][1].plot([], [], lw=2, color=self.axes_info[1][1]['color'])
        self.line = [line1, line2, line3, line4]

        self.xdata = []
        self.ydata1 = []
        self.ydata2 = []
        self.ydata3 = []
        self.ydata4 = []

    # Function to be called when the start button is pressed
    def display(self):
        ani = animation.FuncAnimation(self.fig, self.run, self.data_gen, blit=True, interval=20,
                                      repeat=False)
        self.canvas.draw()

    # coroutine to push data to matplotlib
    def data_gen(self):
        t = 0
        # All the evaluations goes here
        while t < self.terminal_time:
            t += 0.01
            y1 = self.evaluation.coordinate(t)
            y2 = self.evaluation.velocity(t)
            y3 = self.evaluation.full_energy(t)
            y4 = self.evaluation.distance(t)
            # adapted the data generator to yield both sin and cos
            yield t, y1, y2, y3, y4

    def run(self, data):
        # update the data
        t, y1, y2, y3, y4 = data
        self.xdata.append(t)

        # appending data
        self.ydata1.append(y1)
        self.ydata2.append(y2)
        self.ydata3.append(y3)
        self.ydata4.append(y4)

        # update the data of all line objects
        self.line[0].set_data(self.xdata, self.ydata1)
        self.line[1].set_data(self.xdata, self.ydata2)
        self.line[2].set_data(self.xdata, self.ydata3)
        self.line[3].set_data(self.xdata, self.ydata4)

        return self.line

    def clear(self):
        for item in self.canvas.get_tk_widget().find_all():
            self.canvas.get_tk_widget().delete(item)
        self.canvas.flush_events()
