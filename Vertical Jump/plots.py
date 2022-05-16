from enum import IntEnum
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from PIL import Image, ImageTk
from VerticalJumpEvaluation import VerticalJumpEvaluation
from Human import *


class Values(IntEnum):
    IN_WEIGHT = 0
    IN_HEIGHT = 1
    IN_LEG_GIRTH = 2
    IN_BODY_SIZE = 3
    IN_SEX = 4
    IN_SQUAT = 5



def plot(data):
    human = Human(data[Values.IN_WEIGHT], data[Values.IN_HEIGHT], data[Values.IN_SEX], data[Values.IN_LEG_GIRTH],
                  data[Values.IN_LEG_GIRTH], data[Values.IN_SQUAT])
    evaluation = VerticalJumpEvaluation(human, 12) 
    terminal_time = evaluation.flight_time()
    t = np.linspace(0, terminal_time, 300)

    fig, ax = plt.subplots()
    print(evaluation.takeoff_time(), evaluation.max_height())
    #  Создаем функцию, генерирующую картинки
    #  для последующей "склейки":
    def animate(i):
        ax.clear()
        line = ax.plot(t, evaluation.coordinate(t))
        return line

    #  Создаем объект анимации:
    sin_animation = animation.FuncAnimation(fig, 
                                        animate, 
                                        frames=np.linspace(2, 4, 30),
                                        interval = 10,
                                        repeat = True)
    plt.show()
    #evaluate = VerticalJumpEvaluation(human, )
    #time = np.array([_ for _ in range(0, )])