import math

import numpy
import numpy as np
import scipy.constants as constants
from PotentialWell import PotentialWell
from scipy.special import hermite, factorial
import numpy.polynomial.hermite as Herm


class QuantumHarmonicOscillator(PotentialWell):
    def __init__(self, a, omega, m, num_of_discrete_x_vals=10000):
       
        self.a = a
        self.m = m
        self.omega = omega
        self.num_of_discrete_x_vals = num_of_discrete_x_vals
        self.discrete_x = numpy.linspace(-a, a, num_of_discrete_x_vals)

    def get_eigen_values(self, n=4):
        return constants.hbar * self.omega * (np.arange(n + 1) + 0.5)

    def get_nth_wave_function(self, n):
        nth_hermite = hermite(n)
        return lambda x: 1 / np.sqrt(2**n * factorial(n)) \
               + pow(self.m * self.omega / (constants.pi * constants.hbar), 1/4) \
               * nth_hermite(np.sqrt(self.m * self.omega / constants.hbar) * x) \
               * np.exp(-self.m * self.omega * x ** 2 / constants.hbar)

    def hermite(self, x, n):
        xi = numpy.sqrt(self.m * self.omega / constants.hbar) * x
        herm_coeffs = numpy.zeros(n + 1)
        herm_coeffs[n] = 1
        return Herm.hermval(xi, herm_coeffs)

    # def get_nth_state_eigen_function_vals(self, n):
    #     nth_hermite = hermite(n)
    #     x = self.discrete_x
    #     return (1. / math.sqrt((2. ** n) * factorial(n))) * ((self.m * self.omega) / (constants.pi * constants.hbar)) ** (1. / 4) * self.hermite(x, n) * np.exp((-self.m * self.omega * (x ** 2)) / (2 * constants.hbar))

    def get_nth_state_eigen_function_vals(self, n):
        hbar = 1e-34
        x = numpy.arange(-self.a, self.a, 2 * self.a / self.num_of_discrete_x_vals)
        xi = numpy.sqrt(self.m * self.omega / hbar) * x
        prefactor = 1. / math.sqrt(2. ** n * math.factorial(n)) * (self.m * self.omega / (numpy.pi * hbar)) ** (0.25)
        psi = prefactor * numpy.exp(- xi ** 2 / 2) * self.hermite(x, n)
        return psi

    def get_potential_well_vals(self):
        return self.m * (self.omega ** 2) * (self.discrete_x ** 2) / 2.

    def get_x(self):
        return self.discrete_x

    def get_constants(self):
        return 1, 1e36
