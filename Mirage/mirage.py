import numpy as np
from matplotlib import pyplot as plt

class Mirage:
    def __init__(self, n0: float, alpha0: float, gamma: float) -> None:
        self.initial_refractive_index = n0
        self.angle = alpha0 * np.pi / 180
        self.gamma = gamma

    def get_y(self, x):
        return self.initial_refractive_index * (np.abs(np.sin(self.angle)) / np.tan(self.angle) - 1.) / (2. * self.gamma)\
            * np.exp((self.gamma * x) / (self.initial_refractive_index * np.abs(np.sin(self.angle))))\
            - self.initial_refractive_index * (np.abs(np.sin(self.angle)) / np.tan(self.angle) + 1.) / (2. * self.gamma)\
            * np.exp(- (self.gamma * x) / (self.initial_refractive_index * np.abs(np.sin(self.angle))))\
            + self.initial_refractive_index / self.gamma

    def get_derivative(self, x):
        return (np.abs(np.sin(self.angle)) / np.tan(self.angle) - 1.) / (2. * np.abs(np.sin(self.angle)))\
            * np.exp((self.gamma * x) / (self.initial_refractive_index * np.abs(np.sin(self.angle))))\
            + (np.abs(np.sin(self.angle)) / np.tan(self.angle) + 1.) / (2. * np.abs(np.sin(self.angle)))\
            * np.exp(- (self.gamma * x) / (self.initial_refractive_index * np.abs(np.sin(self.angle))))

    def get_alpha_y(self, x):
        return (np.pi / 2. - np.abs(np.arctan(self.get_derivative(x)))) * 180 / np.pi

    def get_plot_data(self):
        x = []
        y = []
        alpha = []
        k = 1000000000
        i = 0
        while i < k:
            x.append(i)
            y.append(self.get_y(i))
            alpha.append(self.get_alpha_y(i))
            if (y[-1] <= 0 and i != 0):
                y[-1] = 0
                alpha[-1] = alpha[-2]
                k = min(k, i + 100)
            i += 1
            
        fig = plt.figure(figsize=(9, 9), facecolor="#2f2e30")
        ax1 = plt.subplot(1, 2, 1)
        ax1.plot(x, y, linewidth=1)
        self.set_colors(ax1)
        ax1.grid(color='black')
        ax1.set_xlabel('X, m')
        ax1.set_ylabel('Y, m')
        ax2 = plt.subplot(1, 2, 2)
        ax2.plot(x, alpha, linewidth=1)
        self.set_colors(ax2)
        ax2.grid(color='black')
        ax2.set_xlabel('x, m')
        ax2.set_ylabel('alpha, deg')
        return (fig, ax1, ax2)

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