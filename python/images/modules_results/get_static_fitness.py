""" Calculates fitness isoclines. """

import os

import numpy as np

from modules.theory import fitness, qbeq
from settings_results.data_constants import DATA_CONSTANTS as data_constants


def fitness_curve(data_dict, x):
    """Calculates static fitness curves."""

    if data_dict["single_folder"] and data_dict["single_trait"]:
        given = float(os.path.basename(os.getcwd()))
    else:
        given = float(data_constants["given_folder"])

    reciprocator = np.zeros(
        (
            len(data_dict["alphas"]),
            len(data_dict["rhos"]),
            len(x),
        )
    )
    non_reciprocator = np.zeros_like(reciprocator)

    increment = 0.001
    for i, alpha in enumerate(data_dict["alphas"]):
        for j, rho in enumerate(data_dict["rhos"]):
            qb_social = qbeq(0.0, alpha, rho)
            reciprocator[i, j] = fitness(x, x, given, alpha, rho)
            non_reciprocator[i, j] = fitness(x, x + increment, given, alpha, rho)
            mask = x + increment > qb_social
            reciprocator[i, j][mask] = None

    y = (reciprocator - non_reciprocator) * 1000
    mask = y <= 0
    y[mask] = None

    return y


def lims():
    """Sets the limits of the axes."""

    x_lim = [0, 1]
    y_lim = [0, 1]
    return x_lim, y_lim


def data(data_dict):
    """Calculates static fitness isoclines."""

    x = np.linspace(0.001, 0.999, num=data_constants["n_x_values"])
    y = fitness_curve(data_dict, x)
    return x, y
