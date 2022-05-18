from enum import IntEnum
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from PIL import Image, ImageTk
from VerticalJumpEvaluation import VerticalJumpEvaluation
from Human import *
import MultipleAnimation

class Values(IntEnum):
    IN_WEIGHT = 0
    IN_HEIGHT = 1
    IN_LEG_GIRTH = 2
    IN_BODY_SIZE = 3
    IN_SEX = 4
    IN_SQUAT = 5


class Plotter:
    def __init__(self, frame, data):
        self.human = Human(data[Values.IN_WEIGHT], data[Values.IN_HEIGHT], data[Values.IN_SEX], data[Values.IN_LEG_GIRTH],
                      data[Values.IN_LEG_GIRTH], data[Values.IN_SQUAT])
        self.plot_animation = MultipleAnimation.PlotAnimation(frame, self.human)

    def plot(self):
        self.plot_animation.display()

    def reset(self):
        self.plot_animation.clear()
