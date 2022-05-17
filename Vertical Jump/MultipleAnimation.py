from Ctk_graphics import *


def on_closing(event=0):
    Window.destroy()


Window = tkinter.Tk()
Window.title("Vertical Jump Model by K. Khasan & A. Gogolev")
Window.geometry(f"720x1080")


# create a figure with four subplots
GRAPH_COUNT = 4
fig, axs = plt.subplots(2, 2)
# fig.set_size_inches(8, 8)
canvas = FigureCanvasTkAgg(fig, master=Window)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, pady=60, padx=60, sticky="nswe")

# evaluate human object (parameteres should be pulled from gui

human = Human(72, 180, "M", 40, 52, 35)
evaluation = VerticalJumpEvaluation(human, 8)
terminal_time = evaluation.flight_time()
AXES_INFO = [
             [ {'xlabel': 'Time(s)', 'ylabel': 'Coordinate (m)', 'ylim': (0, 10), 'xlim' : (0, terminal_time), 'color': 'r'},
               {'xlabel': 'Time(s)', 'ylabel': 'Velocity (m/s)', 'ylim': (-10, 10), 'xlim' : (0, terminal_time), 'color': 'g'}],
             [ {'xlabel': 'Time(s)', 'ylabel': 'Total Energy (j)', 'ylim': (0, 5000), 'xlim' : (0, terminal_time), 'color': 'b'},
               {'xlabel': 'Time(s)', 'ylabel': 'Distance (m)', 'ylim': (0, 30), 'xlim' : (0, terminal_time), 'color': 'c'}]
            ]


# Initializing all the axes
for i in range(0, 2):
    for j in range(0, 2):
        axs[i][j].set_xlabel(AXES_INFO[i][j]['xlabel'])
        axs[i][j].set_ylabel(AXES_INFO[i][j]['ylabel'])
        axs[i][j].set_ylim(AXES_INFO[i][j]['ylim'])
        # axs[i][j].set_xlim(AXES_INFO[i][j]['xlim'])
        axs[i][j].set_xlim(0, terminal_time)
        axs[i][j].minorticks_on()
        # включаем основную сетку
        axs[i][j].grid(which='major')
        # включаем дополнительную сетку
        axs[i][j].grid(which='minor', linestyle=':')

plt.subplots_adjust(hspace=0.9, wspace=0.8, top=0.9)

# initializing all the lines
line1, = axs[0][0].plot([], [], lw=2, color=AXES_INFO[0][0]['color'])
line2, = axs[0][1].plot([], [], lw=2, color=AXES_INFO[0][1]['color'])
line3, = axs[1][0].plot([], [], lw=2, color=AXES_INFO[1][0]['color'])
line4, = axs[1][1].plot([], [], lw=2, color=AXES_INFO[1][1]['color'])
line = [line1, line2, line3, line4]


# coroutine to push data to matplotlib
def data_gen():
    t = data_gen.t
    cnt = 0
    # y = [0] * GRAPH_COUNT
    while t < terminal_time:
        t += 0.05
        y1 = evaluation.coordinate(t)
        y2 = evaluation.velocity(t)
        y3 = evaluation.full_energy(t)
        y4 = evaluation.distance(t)
        # adapted the data generator to yield both sin and cos
        yield t, y1, y2, y3, y4


data_gen.t = 0

# initialize the data arrays
xdata = []
ydata1 = []
ydata2 = []
ydata3 = []
ydata4 = []


def run(data):
    # update the data
    t, y1, y2, y3, y4 = data
    xdata.append(t)

    # appending data
    ydata1.append(y1)
    ydata2.append(y2)
    ydata3.append(y3)
    ydata4.append(y4)

    # update the data of all line objects
    line[0].set_data(xdata, ydata1)
    line[1].set_data(xdata, ydata2)
    line[2].set_data(xdata, ydata3)
    line[3].set_data(xdata, ydata4)

    return line


ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=100,
    repeat=False)

canvas.draw()


if __name__ == '__main__':
    Window.mainloop()
    Window.protocol("WM_DELETE_WINDOW", on_closing)  # call .on_closing() when app gets closed

