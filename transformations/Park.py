import numpy as np
from numpy import linalg

phi = np.pi * 2 / 3


def park_matrix(theta: float) -> np.array:
    return np.array([[np.cos(theta), np.sin(theta), 0],
                     [-np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]])


def inv_park_matrix(theta: float) -> np.array:
    return linalg.inv(park_matrix(theta))


def park(theta: float, alpha_beta_gamma: np.array) -> np.array:
    if not isinstance(theta, float):
        return np.array([np.matmul(park_matrix(theta_i), alpha_beta_gamma[:, i]) for i, theta_i in enumerate(theta)]) \
            .transpose()
    return np.matmul(park_matrix(theta), alpha_beta_gamma)


def inv_park(theta, dq):
    if not isinstance(theta, float):
        return np.array([np.matmul(inv_park_matrix(theta_i), dq) for i, theta_i in enumerate(theta)])
    return np.matmul(inv_park_matrix(theta), dq)
