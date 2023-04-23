import numpy
import numpy as np
import scipy.constants as constants
from scipy.special import hermite, factorial


class QuantumHarmonicOscillator:
    def __init__(self, m, omega, a, num_of_discrete_x_vals):
        self.a = a
        self.m = m
        self.omega = omega
        self.num_of_discrete_x_vals = num_of_discrete_x_vals
        self.discrete_x = numpy.linspace(-a, a, num_of_discrete_x_vals)

    def get_eigen_values_inclusively(self, n):
        return constants.hbar * self.omega * np.arange(n + 1)

    def get_nth_wave_function(self, n):
        nth_hermite = hermite(n)
        return lambda x: 1 / np.sqrt(2**n * factorial(n)) \
               + pow(self.m * self.omega / (constants.pi * constants.hbar), 1/4) \
               * nth_hermite(np.sqrt(self.m * self.omega / constants.hbar) * x) \
               * np.exp(-self.m * self.omega * x ** 2 / constants.hbar)

    def get_nth_wave_function_vals(self, n):
        nth_function = self.get_nth_wave_function(n)
        return nth_function(self.discrete_x)
