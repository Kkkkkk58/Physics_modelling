import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections
from matplotlib import gridspec
from scipy.interpolate import LinearNDInterpolator
from typing import Tuple, Callable, List
import copy


def analyticalPreisachFunction1(a: float, b: float, c: float, d: float, n: float, p: float, q: float, beta: np.ndarray,
                                alpha: np.ndarray) -> np.ndarray:
#     """
#     Function based on Paper IEEE TRANSACTIONS ON MAGNETICS, VOL. 39, NO. 3, MAY 2003 'Analytical  Approximation  of  Preisach
#     Distribution Functions' by Janos Fuezi
#     """
    hm = (alpha + beta) / 2
    hc = (alpha - beta) / 2
    nom1 = c
    den1 = (1 + np.square(a) * np.square(alpha + b)) * (1 + np.square(a) * np.square(beta - b))
    nom2 = d
    den2 = np.exp(n * np.square(hm)) * np.exp(p * np.square(hc + q))
    preisach = nom1 / den1 + nom2 / den2
    # set lower right diagonal to zero
    for i in range(preisach.shape[0]):
        preisach[i, (-i - 1):] = 0
    return preisach


def analyticalPreisachFunction2(A: float, Hc: float, sigma: float, beta: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """
    Function based on Paper 'Removing numerical instabilities in the Preisach model identification
    using genetic algorithms' by G. Consolo G. Finocchio, M. Carpentieri, B. Azzerboni.
    """
    nom1 = 1
    den1 = 1 + ((beta - Hc) * sigma / Hc) ** 2
    nom2 = 1
    den2 = 1 + ((alpha + Hc) * sigma / Hc) ** 2
    preisach = A * (nom1 / den1) * (nom2 / den2)
    # set lower right diagonal to zero
    for i in range(preisach.shape[0]):
        preisach[i, (-i - 1):] = 0
    return preisach


def initPreisachWithOnes(gridX: np.ndarray) -> np.ndarray:
    """
    Initialize the Preisach distribution function with ones over the entire Preisach-plane
    """
    preisach = np.ones_like(gridX)
    # set lower right diagonal to zero
    for i in range(preisach.shape[0]):
        preisach[i, (-i - 1):] = 0
    return preisach


def removeInBetween(arr: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Function for removing in between points of an array
    """
    whipeout_indexes = np.empty(len(arr), dtype=bool)
    if len(arr) < 3:
        whipeout_indexes[:] = True
        return arr, whipeout_indexes
    else:
        range_list = list(range(1, len(arr) - 1))
        whipeout_indexes[0] = True
        whipeout_indexes[-1] = True
        for i in range_list:
            if arr[i] == arr[i - 1] == arr[i + 1]:
                whipeout_indexes[i] = False
            else:
                whipeout_indexes[i] = True
        return arr[whipeout_indexes], whipeout_indexes


def removeRedundantPoints(pointsX: np.ndarray, pointsY: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Function for removing redundant points inside vertices and horizontal lines of staircase polylines
    """
    pointsX, whipeout_indices = removeInBetween(pointsX)
    pointsY = pointsY[whipeout_indices]
    pointsY, whipeout_indices = removeInBetween(pointsY)
    pointsX = pointsX[whipeout_indices]
    return pointsX, pointsY


def preisachIntegration(w: float, Z: np.ndarray) -> np.ndarray:
    """
    Perform 2D- integration of the Preisach distribution function.
    """
    flipped = np.fliplr(np.flipud(w * Z))
    flipped_integral = np.cumsum(np.cumsum(flipped, axis=0), axis=1)
    return np.fliplr(np.flipud(flipped_integral))


class PreisachModel:
    """
    Efficient implementation of the scalar Preisach model
    """

    def __init__(self, n: int, alpha0: float) -> None:
        self.n = n
        self.alpha0 = alpha0
        self.beta0 = alpha0
        x = np.linspace(-self.beta0, self.beta0, n - 1)
        y = np.linspace(-self.alpha0, self.alpha0, n - 1)
        self.width = 2 * alpha0 / (n - 1)
        self.gridX, self.gridY = np.meshgrid(x, y)
        # flip  gridY to be compatible with definiton of preisach plane
        self.gridY = np.flipud(self.gridY)
        self.pointsX = np.array([-self.beta0], dtype=np.float64)
        self.pointsY = np.array([-self.alpha0], dtype=np.float64)
        self.interfaceX = np.array([-self.beta0, -self.beta0], dtype=np.float64)
        self.interfaceY = np.array([-self.alpha0, -self.alpha0], dtype=np.float64)
        self.historyInterfaceX: List[float] = []
        self.historyInterfaceY: List[float] = []
        self.historyU = - self.alpha0 * np.ones(1, dtype=np.float64)
        self.historyOut = np.zeros(0, dtype=np.float64)
        self.state = 'ascending'
        self.stateOld = 'ascending'
        self.stateChanged = False
        self.everett: Callable[[float, float], float]

    def __call__(self, *args, **kwargs) -> float:
        """
        Call model with input value given as argument
        """
        self.pointsX = self.interfaceX[:-1]
        self.pointsY = self.interfaceY[:-1]
        u = args[0]
        if u > self.historyU[-1]:
            self.state = 'ascending'
        elif u < self.historyU[-1]:
            self.state = 'descending'
        if self.state != self.stateOld:
            self.stateChanged = True
        else:
            self.stateChanged = False

        if self.stateChanged:
            # reached boundary
            self.pointsX = np.append(self.pointsX, self.historyU[-1])
            self.pointsY = np.append(self.pointsY, self.historyU[-1])

        if self.state == 'ascending':
            self.pointsY[self.pointsY <= u] = u
            self.pointsY[-1] = u

        elif self.state == 'descending':
            self.pointsX[self.pointsX >= u] = u
            self.pointsX[-1] = u

        self.interfaceX = np.append(self.pointsX, u)
        self.interfaceY = np.append(self.pointsY, u)

        self.interfaceX, self.interfaceY = removeRedundantPoints(self.interfaceX, self.interfaceY)

        self.stateOld = self.state
        self.historyInterfaceX.append(copy.deepcopy(self.interfaceX))
        self.historyInterfaceY.append(copy.deepcopy(self.interfaceY))
        self.historyU = np.append(self.historyU, copy.deepcopy(u))
        output = self.calculateOutput()
        self.historyOut = np.append(self.historyOut, copy.deepcopy(output))
        return output

    def setNegSatState(self) -> None:
        """
        Set the interface to negative saturation.
        """
        self.pointsX = np.array([-self.beta0], dtype=np.float64)
        self.pointsY = np.array([-self.alpha0], dtype=np.float64)
        self.interfaceX = np.array([-self.beta0, -self.beta0], dtype=np.float64)
        self.interfaceY = np.array([-self.alpha0, -self.alpha0], dtype=np.float64)
        self.resetHistory()

    def resetHistory(self) -> None:
        """
        Reset all model history parameters.
        """
        self.historyInterfaceX = []
        self.historyInterfaceY = []
        self.historyU = - self.alpha0 * np.ones(1, dtype=np.float64)
        self.historyOut = np.zeros(0, dtype=np.float64)
        self.state = 'ascending'
        self.stateOld = 'ascending'
        self.stateChanged = False

    def setDemagState(self, n: int = -1) -> None:
        """
        Function for setting the interface so that the output of the model will
        be zero initially (demagnetized state).
        Parameters
        ----------
        n : int
            Demagnetization step granularity
        """
        if n == -1:
            n = 150

        self.setNegSatState()
        excitation = np.linspace(1, 0, n)
        excitation[1::2] = - excitation[1::2]
        for i in excitation:
            self(i)

        self.resetHistory()

    def invert(self) -> 'PreisachModel':
        """
        Return inverse Preisachmodel by constructing the inverse Everett
        function from the non inverted model using first order reversal curves (FODs).
        Grid points of the inverse Everett function are defined by the response values
        of the non inverse model. Inverse Everett function values on these grid points are directly
        defined by the dominant input extrema of the non inverted model. Inverse Everett function
        on irregular grid is interpolated using irregular grid interpolation.
        For a description of Preisach model inversion also see the following paper:
        'Identification and Inversion of Magnetic Hysteresis for Sinusoidal Magnetization' by Martin Kozek and
        Bernhard Gross
        """
        invModel = PreisachModel(self.n, self.alpha0)

        # Construct set of first order reversal curves (FODs) for identification of the inverse everett map
        # number of FODs correspond to the number of Hystereon elements n in Preisach plane
        FODs = np.zeros((self.n * self.n // 2 + self.n // 2 + 1, 2), dtype=np.float64)
        Mk = np.zeros(FODs.shape[0], dtype=np.float64)
        mk = np.zeros(FODs.shape[0], dtype=np.float64)
        invEverettVals = np.zeros(FODs.shape[0], dtype=np.float64)
        cnt = 0
        print('Inverting Model...')
        for valAlpha in np.linspace(-self.alpha0, self.alpha0, self.n - 1):
            for valBeta in np.linspace(-self.beta0, valAlpha, int((valAlpha - (-self.alpha0)) // self.width)):
                FODs[cnt, 0] = valAlpha
                FODs[cnt, 1] = valBeta
                # Reset and excite non inverted model with the FODs to get the grid Points of the inverse model
                # by dominant output extrema of the non inverted model
                self.setNegSatState()
                invEverettVals[cnt] = (1 / 2) * (valAlpha - valBeta)
                Mk[cnt] = self(valAlpha)
                mk[cnt] = self(valBeta)
                cnt += 1

        points = np.zeros((len(Mk), 2), dtype=np.float64)
        points[:, 1] = np.concatenate([Mk])
        points[:, 0] = np.concatenate([mk])
        Z = np.concatenate([invEverettVals])
        # Fit interpolator function on irregular grid using linear interpolation
        invEverettInterp = LinearNDInterpolator(points, Z, fill_value=0)

        # Set interpolator as everett function of the inverse model
        invModel.setEverettFunction(invEverettInterp)

        # return inverse model
        print('Model inversion succesfull !!!')
        return invModel

    def calculateOutput(self, **kwargs) -> float:
        """
        Calculate the output of the model with the current interface.
        Negative beta0 required, because beta0 was defined to be positive,
        however in the book 'mathematical models of hysteresis' from Mayergoyz, -
        (alpha0, beta0) is defined as the left top corner of the preisach triangle.
        Therefore beta0 has to be inverted to give the correct value
        Also the parameter order was defined different E(x,y)
        """
        if kwargs.get('mode'):
            mode = kwargs['mode'].lower()
        else:
            mode = 'default'

        if mode == 'default':
            sum = 0.0
            for i in range(1, len(self.interfaceX)):
                Mk = self.interfaceY[i]
                mk = self.interfaceX[i]
                mkOld = self.interfaceX[i - 1]
                sum = sum + (self.everett(mkOld, Mk) - self.everett(mk, Mk))
            output = -self.everett(-self.beta0, self.alpha0) + 2 * sum

        else:
            # alternative output calculation
            pass

        return output

    def setEverettFunction(self, everett: Callable[[float, float], float]) -> None:
        """
        Set everett function to given interpolator function.
        Parameters
        ----------
        everett : callable python method
            Interpolator for Everett function
        """
        if not isinstance(everett, collections.abc.Callable):
            raise ValueError('Given Parameter must be a callable function')
        self.everett = everett

    def animateHysteresis(self) -> animation.FuncAnimation:
        # @Todo vector length of u and out must be same
        self.historyU = self.historyU[1:]

        def update_line(num, self, line1, line2, line3):
            line1.set_xdata(num)
            line1.set_ydata(self.historyU[num])
            line2.set_xdata(self.historyInterfaceX[num])
            line2.set_ydata(self.historyInterfaceY[num])
            line3.set_xdata(self.historyU[num])
            line3.set_ydata(self.historyOut[num])
            return line1, line2, line3

        frames = len(self.historyInterfaceX)

        gs = gridspec.GridSpec(1, 3, height_ratios=[1], width_ratios=[1, 1, 1])
        facecolor = "#5a595b"
        fig1 = plt.figure(figsize=(20, 10), facecolor="#2f2e30")
        ax1 = plt.subplot(gs[0, 0])
        ax1.set_facecolor(facecolor)
        ax2 = plt.subplot(gs[0, 1])
        ax2.set_facecolor(facecolor)
        ax3 = plt.subplot(gs[0, 2])
        ax3.set_facecolor(facecolor)

        # create plot of input
        ax1.plot(self.historyU, linewidth=1)
        ax1.set_xlim([0, len(self.historyU)])
        ax1.set_ylim([-self.alpha0 * 1.1, self.alpha0 * 1.1])
        ax1.set_xlabel('samples')
        ax1.set_ylabel('input')

        line1, = ax1.plot([0.0], [0.0], '.', markersize=15)

        # create plot of preisach plane
        ax2.plot(np.array([-self.beta0, self.beta0, -self.beta0, -self.beta0]),
                 np.array([-self.alpha0, self.alpha0, self.alpha0, -self.alpha0]), linewidth=3)
        line2, = ax2.plot([], [], 'r', linewidth=2)
        ax2.set_xlim(-self.beta0 * 1.1, self.beta0 * 1.1)
        ax2.set_ylim(-self.alpha0 * 1.1, self.alpha0 * 1.1)
        ax2.set_xlabel('Beta coefficients')
        ax2.set_ylabel('Alpha coefficients')
        ax2.legend(['Preisach plane', 'Interface'], loc='lower right')

        # create plot of hysteresis
        ax3.plot(self.historyU, self.historyOut)
        line3, = ax3.plot([0.0], [0.0], '.', markersize=15)

        simulation = animation.FuncAnimation(fig1, update_line, frames,
                                             fargs=(self, line1, line2, line3), interval=25,
                                             blit=True, repeat=False)

        return (simulation, fig1, ax1, ax2, ax3)

    # Use that for initializing the hysteresis model state using analytic 1
    def configureModelState1(self, A, B, C, D, N, P, Q):
        self.preisach = initPreisachWithOnes(self.gridX)
        self.preisach = analyticalPreisachFunction1(A, B, C, D, N, P, Q, self.gridX, self.gridY)
        self.initializeModelEverett()

    # Use that for initializing the hysteresis model state using analytic 2
    def configureModelState2(self, A : int, Hc : float, sigma : float):
        self.preisach = analyticalPreisachFunction2(A, Hc, sigma, self.gridX, self.gridY)
        self.initializeModelEverett()

    def initializeModelEverett(self):

        # Calculate Everett function from preisach function
        everett = preisachIntegration(self.width, self.preisach)

        # Scale Everett function to a maximum value of 1
        everett = everett / np.max(everett)

        # Calculate linear Interpolator for Everett function
        points = np.zeros((everett.size, 2), dtype=np.float64)
        points[:, 0] = self.gridX.flatten()
        points[:, 1] = self.gridY.flatten()
        values = everett.flatten()
        everettInterp = LinearNDInterpolator(points, values)
        self.setEverettFunction(everettInterp)

    def printHysteresis(self):
        # calculate inverse model
        self.invModel = self.invert()

        self.createSignal()
        return self.animateHysteresis()

    # Create excitation signal
    def createSignal(self):
        nSamps = 2500
        phi = np.linspace(0, 2 * np.pi + np.pi / 2, nSamps)

        sawtooth = np.zeros(nSamps, dtype=np.float64)
        sawtooth[phi < np.pi / 2] = 0.7 * 2 / np.pi * phi[phi < np.pi / 2]
        sawtooth[np.logical_and(phi < 3 * np.pi / 2, phi > np.pi / 2)] = -0.7 * 2 / np.pi * (
                phi[np.logical_and(phi < 3 * np.pi / 2, phi > np.pi / 2)] - np.pi)
        sawtooth[phi > 3 * np.pi / 2] = 0.7 * 2 / np.pi * (phi[phi > 3 * np.pi / 2] - 2 * np.pi)

        input = 0.15 * np.sin(30 * phi) + sawtooth
        output = np.zeros_like(input, dtype=np.float64)
        middle = np.zeros_like(input, dtype=np.float64)

        self.setDemagState(80)
        self.invModel.setDemagState(80)

        # Apply input to inverse model and then apply it to non inverse model
        for i in range(len(input)):
            middle[i] = self(input[i])
            output[i] = self.invModel(middle[i])

# Basic example of Preisach model usage
def exampleHysteresis():

    model = PreisachModel(200, 1)
    A = 1
    Hc = 0.01
    sigma = 0.03
    model.configureModelState2(A, Hc, sigma)
    model.printHysteresis()

######## init with ones #########
# preisach = initPreisachWithOnes()
# ####### analytic 1 #############
# A = 71
# B = -0.018
# C = 0.013
# D = 0.068
# N = 15
# P = 2500
# Q = 0.04
# preisach = analyticalPreisachFunction1(A, B, C, D, N, P, Q, gridX, gridY)
# ######## analytic 2 #############
# A = 1
# Hc = 0.01
# sigma = 0.03