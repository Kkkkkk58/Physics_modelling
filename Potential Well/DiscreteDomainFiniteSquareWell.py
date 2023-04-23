import numpy
import numpy as np
from scipy.linalg import eigh_tridiagonal


class DiscreteDomainFiniteSquareWell:
    def __init__(self, a, num_of_discrete_x_vals, U0):
        self.num_of_discrete_x_vals = num_of_discrete_x_vals
        self.a = a
        self.discrete_x = numpy.linspace(-a, a, num_of_discrete_x_vals)
        self.dx = np.diff(self.discrete_x)[0]
        self.U0 = U0
        # Configuring hamiltonian tridiagonal matrix of n - 1 dimensions
        self.hamiltonian_main_diagonal = 2 * np.ones(self.num_of_discrete_x_vals) / self.dx ** 2 \
                                     - self.U0 * ((self.discrete_x >= -1) * (self.discrete_x <= 1)).astype(float)
        self.hamiltonian_off_diagonal = -np.ones(self.num_of_discrete_x_vals - 1) / self.dx ** 2
        self.__eigen_values = None
        self.__eigen_vectors = None

    def get_eigen_values_and_vectors(self):
        if self.__eigen_values is None:
            self.__eigen_values, self.__eigen_vectors = eigh_tridiagonal(self.hamiltonian_main_diagonal,
                                                                         self.hamiltonian_off_diagonal, select='v',
                                                                         select_range=(-np.min(self.U0, 0)))
        return self.__eigen_values, self.__eigen_vectors
