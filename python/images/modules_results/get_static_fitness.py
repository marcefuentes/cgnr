""" Calculates fitness isoclines. """

import os
import numpy as np
from modules.theory import fitness, qbeq


def fitness_curve(x, given, alphas, rhos):
    """Calculates fitness curves."""

    reciprocator = np.zeros((len(alphas), len(rhos), len(x)))
    non_reciprocator = np.zeros_like(reciprocator)

    increment = 0.001
    for i, alpha in enumerate(alphas):
        for j, rho in enumerate(rhos):
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


def data(data_dict, data_constants):
    """Main function."""

    x = np.linspace(0.001, 0.999, num=data_constants["n_x_values"])

    if data_dict["single_folder"] and data_dict["single_trait"]:
        given = float(os.path.basename(os.getcwd()))
    else:
        given = float(data_constants["given_folder"])

    alphas = data_dict["alphas"]
    rhos = data_dict["rhos"]

    y = fitness_curve(x, given, alphas, rhos)

    return x, y
