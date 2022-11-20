import numpy as np
import math
from matplotlib import pyplot as plt
from scipy import integrate
from constants import MU_0

def langevin(x: float) -> float:
    return 1 / np.tanh(x) - 1 / x

# Finds value of y for a given x using step size h
# and initial value y0 at x0.
def runge_kutta(f, x0, y0, x, h, args):
    # Count number of iterations using step size or
    # step height h
    n = (int)((x - x0)/h)
    # Iterate for number of iterations
    y = y0
    for i in range(1, n + 1):
        k1 = h * f(x0, y, *args)
        k2 = h * f(x0 + 0.5 * h, y + 0.5 * k1, *args)
        k3 = h * f(x0 + 0.5 * h, y + 0.5 * k2, *args)
        k4 = h * f(x0 + h, y + k3, *args)
 
        # Update next value of y
        y = y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4)
 
        # Update next value of x
        x0 = x0 + h
    return y

class IsotropicCoefficients:
    def __init__(self, a: float, alpha: float, ms: float, k: float, c: float) -> None:
        self.a = a
        self.alpha = alpha
        self.ms = ms
        self.k = k
        if c < 0 or c > 1:
            raise Exception("Invalid value of c")
        self.c = c


class AnisotropicCoefficients:
    def __init__(self, kan: float, psi: float, t: float) -> None:
        self.kan = kan
        self.psi = psi
        if t < 0 or t > 1:
            raise Exception("Invalid value of t")
        self.t = t

class JilesAthertonFormulas:
    def get_h_e(h: float, alpha: float, m: float) -> float:
        return h + alpha * m

    def get_m_an(h_e: float, isotropic: IsotropicCoefficients, anisotropic: AnisotropicCoefficients) -> float:
        if isotropic is None:
            raise Exception("Isotropic coefficients must be non-null")
        m_an_iso = m_an_aniso = t = 0
        if anisotropic is not None:
            t = anisotropic.t
            m_an_aniso = JilesAthertonFormulas.get_m_an_aniso(isotropic, anisotropic)
        m_an_iso = JilesAthertonFormulas.get_m_an_iso(h_e, isotropic)
        return (1 - t) * m_an_iso + t * m_an_aniso

    # def get_m(h: float, m_an: float, initial_h: float, delta: int, isotropic: IsotropicCoefficients, dm_an_dh: float) -> float:
    #     args = [m_an, delta, isotropic, dm_an_dh]
    #     return runge_kutta(JilesAthertonFormulas.get_dm_dh, initial_h, 0, h, 10, args)

    def get_m(dh: float, m: float, m_an: float, d_m_an: float, delta: int, isotropic: IsotropicCoefficients) -> float:
        dm = m_an - m
        return m + 1 / (1 + isotropic.c) * (dm / (isotropic.k * delta - isotropic.alpha * dm))\
                * dh + (isotropic.c / (isotropic.c + 1)) * d_m_an

    def get_m_an_iso(h_e: float, isotropic: IsotropicCoefficients) -> float:
        if h_e == 0:
            return 0
        return isotropic.ms * langevin(h_e / isotropic.a)

    def get_m_an_aniso(h_e: float, isotropic: IsotropicCoefficients, anisotropic: AnisotropicCoefficients) -> float:
        args = [h_e, isotropic, anisotropic]
        return isotropic.ms * integrate.quadrature(JilesAthertonFormulas.get_e_1, 0, np.pi, args) / integrate.quadrature(JilesAthertonFormulas.get_e_2, 0, np.pi, args)

    def get_e_1(x: float, h_e: float, isotropic: IsotropicCoefficients, anisotropic: AnisotropicCoefficients) -> float:
        return h_e / math.cos(x) - anisotropic.kan / (isotropic.ms * MU_0 * isotropic.a) * (math.sin(anisotropic.psi - x)) ** 2

    def get_e_2(x: float, h_e: float, isotropic: IsotropicCoefficients, anisotropic: AnisotropicCoefficients) -> float:
        return h_e / math.cos(x) - anisotropic.kan / (isotropic.ms * MU_0 * isotropic.a) * (math.sin(anisotropic.psi + x)) ** 2

    def get_dm_dh(h: float, m: float, m_an: float, delta: int, isotropic: IsotropicCoefficients, dm_an_dh: float) -> float:
        return 1 / (1 + isotropic.c) * (m_an - m) / (delta * isotropic.k - isotropic.alpha *(m_an - m)) \
            + isotropic.c / (1 + isotropic.c) * dm_an_dh

class JilesAthertonModel: 
    def __init__(self, delta_h: float = 20, initial_position: int = 125) -> None:
        self.initial_position = initial_position
        self.plotting_steps = initial_position * 5
        self.isotropic = self.anisotropic = None
        self.fill_h(delta_h, initial_position, initial_position * 2)

    def fill_h(self, delta_h: float, initial_position: int, hysteresis_peak: int) -> None:
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
        m = [0]

        for i in range(self.plotting_steps):
            h_e = JilesAthertonFormulas.get_h_e(self.h[i + 1], self.isotropic.alpha, m[i])
            m_an = JilesAthertonFormulas.get_m_an(h_e, self.isotropic, self.anisotropic)
            Man.append(m_an)
            dman = Man[i + 1] - Man[i]
            dh = self.h[i + 1] - self.h[i]
            m_cur = JilesAthertonFormulas.get_m(dh, m[i], Man[i + 1], dman, delta[i + 1], self.isotropic)
            # m_cur = JilesAthertonFormulas.get_m(self.h[i + 1], m_an, self.initial_position, delta[i + 1], self.isotropic, dman_dh)
            m.append(m_cur)

        B = [MU_0 * i for i in m]

        plt.plot(self.h, B)
        plt.show()



a = 470 # A/m
alpha = 9.38e-4
c = 0.0889
k = 483 # A/m
ms = 1.48e6 # A/m


model = JilesAthertonModel()
coefs = IsotropicCoefficients(a, alpha, ms, k, c)
model.set_isotropic(coefs)
model.plot()


