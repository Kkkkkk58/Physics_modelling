from MultipleAnimation import PlotAnimation


class PlotFirstPage(PlotAnimation):
    def __init__(self, frame, human):
        super(PlotFirstPage, self).__init__(frame, human)

    def set_axes_info(self):
        return [
            [{'xlabel': 'Time (s)', 'ylabel': 'Coordinate (m)', 'ylim': (0, 2), 'xlim': (0, self.terminal_time),
              'color': 'r'},
             {'xlabel': 'Time (s)', 'ylabel': 'Velocity (m/s)', 'ylim': (-5, 5), 'xlim': (0, self.terminal_time),
              'color': 'g'}],
            [{'xlabel': 'Time (s)', 'ylabel': 'Total Energy (j)', 'ylim': (0, 2000), 'xlim': (0, self.terminal_time),
              'color': 'b'},
             {'xlabel': 'Time (s)', 'ylabel': 'Distance (m)', 'ylim': (0, 5), 'xlim': (0, self.terminal_time),
              'color': 'c'}]
        ]

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


class PlotSecondPage(PlotAnimation):
    def __init(self, frame, human):
        super(PlotSecondPage, self).__init__(frame, human)

    def set_axes_info(self):
        return [
            [{'xlabel': 'Time (s)', 'ylabel': 'Total Energy (j)', 'ylim': (0, 5000), 'xlim': (0, self.terminal_time),
              'color': 'r'},
             {'xlabel': 'Time (s)', 'ylabel': 'Kineteic Energy (j)', 'ylim': (0, 5000), 'xlim': (0, self.terminal_time),
              'color': 'g'}],
            [{'xlabel': 'Time (s)', 'ylabel': 'Potential Energy (j)', 'ylim': (0, 5000), 'xlim': (0, self.terminal_time),
              'color': 'b'},
             {'xlabel': 'Time (s)', 'ylabel': 'Support Reaction Work (j)', 'ylim': (0, 5000), 'xlim': (0, self.terminal_time),
              'color': 'c'}]
        ]

    def data_gen(self):
        t = 0
        # All the evaluations goes here
        while t < self.terminal_time:
            t += 0.01
            y1 = self.evaluation.full_energy(t)
            y2 = self.evaluation.kinetic_energy(t)
            y3 = self.evaluation.potential_energy(t)
            y4 = self.evaluation.support_reaction_work(t)
            # adapted the data generator to yield both sin and cos
            yield t, y1, y2, y3, y4

