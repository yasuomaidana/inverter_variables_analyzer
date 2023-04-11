import math

import numpy as np
from numpy import linalg

# Here we calculate the POWER invariant transformation
clarke_matrix = np.sqrt(2 / 3) * np.array(
    [[1, -1 / 2, -1 / 2],
     [0, math.sqrt(3) / 2, -math.sqrt(3) / 2],
     1.0 / math.sqrt(2) * np.ones(3)])
inverse_clarke_matrix = linalg.inv(clarke_matrix)


def clark(input_signal: np.array) -> np.array:
    return np.matmul(clarke_matrix, input_signal)


def inv_clark(input_signal: np.array) -> np.array:
    return np.matmul(inverse_clarke_matrix, input_signal)
