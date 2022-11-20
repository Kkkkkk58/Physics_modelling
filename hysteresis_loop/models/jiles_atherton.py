import numpy as np
from matplotlib import pyplot as plt
from hysteresis_loop.core.constants import MU0

def langevin(x: float) -> float:
    return 1 / np.tanh(x) - 1 / x

class IsotropicCoefficients:
    def __init__(self, a: float, alpha: float, Ms: float, k: float, c: float) -> None:
        self.a = a
        self.alpha = alpha
        self.Ms = Ms
        self.k = k
        self.c = c

class AnisotropicCoefficients:
    def __init__(self, Kan: float, psi: float, t: float) -> None:
        self.Kan = Kan
        self.psi = psi
        self.t = t

class JilesAthertonModel: 
    def __init__(self, delta_h: float = 20, initial_position: float = 125) -> None:
        self.plotting_steps = initial_position * 3.0
        self.isotropic = self.anisotropic = None
        self.fill_h(delta_h, initial_position, initial_position * 2.0)

    def fill_h(self, delta_h: float, initial_position: float, hysteresis_peak: float):
        self.h = [0]
        for i in range(initial_position):
            self.h.append(self.h[i] + delta_h)

        for i in range(hysteresis_peak):
            self.h.append(self.h[-1] - delta_h)

        for i in range(hysteresis_peak):
            self.h.append(self.h[-1] + delta_h)
        

    def set_isotropic(self, coefficients: IsotropicCoefficients) -> None:
        self.isotropic = coefficients

    def set_anisotropic(self, coefficients: AnisotropicCoefficients) -> None:
        self.anisotropic = coefficients

    def plot(self) -> None:
        delta = [0]
        for i in range(len(self.h) - 1):
            if self.h[i + 1] > self.h[i]:
                delta.append(1)
            else:
                delta.append(-1)

        Man = [0]
        dMirrdH = [0]
        Mirr = [0]
        M = [0]

        for i in range(self.plotting_steps):

            Man.append(self.isotropic.Ms * langevin((self.h[i + 1] + self.isotropic.alpha * M[i]) / self.isotropic.a))
            dMirrdH.append((Man[i+1] - M[i]) / (self.isotropic.k * delta[i+1] - self.isotropic.alpha * (Man[i + 1] - M[i])))
            Mirr.append(Mirr[i] + dMirrdH[i + 1] * (self.h[i+1] - self.h[i]))
            M.append(self.isotropic.c * Man[i + 1] + (1 - self.isotropic.c) * Mirr[i + 1])

        B = [MU0 * i for i in M]

        plt.plot(self.h, B)
        plt.show()



a = 1070 # A/m
alpha = 9.38e-4
c = 0.0889
k = 483 # A/m
Ms = 1.48e6 # A/m


model = JilesAthertonModel()
coefs = IsotropicCoefficients(a, alpha, Ms, k, c)
model.set_isotropic(coefs)
model.plot()


