import math

import numpy
import numpy as np
from scipy.linalg import eigh_tridiagonal


class DiscreteDomainFiniteSquareWell:
    def __init__(self, a, U0,  num_of_discrete_x_vals=10000):
        self.num_of_discrete_x_vals = num_of_discrete_x_vals
        self.a = a
        self.left_x = numpy.linspace(-2 * self.a, -self.a, 2 * self.num_of_discrete_x_vals)
        self.discrete_x = numpy.linspace(-a, a, num_of_discrete_x_vals)
        self.right_x = numpy.linspace(self.a, 2 * self.a, 2 * self.num_of_discrete_x_vals)

        self.dx = np.diff(self.discrete_x)[0]
        self.U0 = U0

        # Configuring hamiltonian tridiagonal matrix of n - 1 dimensions
        self.hamiltonian_main_diagonal = 2 * np.ones(self.num_of_discrete_x_vals) / self.dx ** 2 \
                                     - self.U0 * ((self.discrete_x >= -1) * (self.discrete_x <= 1)).astype(float)
        self.hamiltonian_off_diagonal = -np.ones(self.num_of_discrete_x_vals - 1) / self.dx ** 2
        self.__eigen_values = None
        self.__eigen_vectors = None

    def get_eigen_values(self):
        if self.__eigen_values is None:
            self.__eigen_values, self.__eigen_vectors = eigh_tridiagonal(self.hamiltonian_main_diagonal,
                                                                         self.hamiltonian_off_diagonal, select='v',
                                                                         select_range=(-self.U0, 0))
        return self.__eigen_values

    def get_nth_state_eigen_function_vals(self, n):
        if self.__eigen_vectors is None:
            self.__eigen_values, self.__eigen_vectors = eigh_tridiagonal(self.hamiltonian_main_diagonal,
                                                                         self.hamiltonian_off_diagonal, select='v',
                                                                         select_range=(-self.U0, 0))
        return self.__eigen_vectors.T[n]

    # Explanation
    # Psi_left_i = C * exp(a * x) + D * exp(-a * x)
    # for x -> -inf D * exp(-a * x) -> inf: D = 0
    # Psi_left_i = C * exp(a * x)
    # Psi_left_i(x = -a) = C * exp(-(a ** 2)) = Psi_i(x = -a) where Psi_i is Psi function for x in [-a, a]
    def get_outside_left_nth_state_eigen_function_vals(self, n):
        nth_left_inner_val = self.get_nth_state_eigen_function_vals(n)[0]
        C = nth_left_inner_val / math.exp(- (self.a ** 2))
        return C * np.exp(self.a * self.left_x)

    # Explanation
    # Psi_right_i = F * exp(a * x) + G * exp(-a * x)
    # for x -> inf F * exp(a * x) -> inf: F = 0
    # Psi_right_i = G * exp(-a * x)
    # Psi_right_i(x = a) = G * exp(-(a ** 2)) = Psi_i(x = a) where Psi_i is Psi function for x in [-a, a]
    def get_outside_right_nth_state_eigen_function_vals(self, n):
        nth_right_inner_val = self.get_nth_state_eigen_function_vals(n)[-1]
        G = nth_right_inner_val / math.exp(- (self.a ** 2))
        return G * np.exp(-self.a * self.right_x)

    def get_x(self):
        return self.discrete_x

    def get_left_outside_x(self):
        return self.left_x

    def get_right_outside_x(self):
        return self.right_x
