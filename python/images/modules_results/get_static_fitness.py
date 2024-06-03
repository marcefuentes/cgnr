""" Calculates fitness isoclines. """

import os
import numpy as np
from modules.theory import fitness, qbeq


def data(config_data, dynamic_data, data_constants):
    """Main function."""

    x = np.linspace(0.001, 0.999, num=data_constants["n_x_values"])

    if config_data["single_folder"] and config_data["single_trait"]:
        given = float(os.path.basename(os.getcwd()))
    else:
        given = float(data_constants["given_folder"])

    alphas = dynamic_data["alphas"]
    rhos = dynamic_data["rhos"]

    y = process_grid(x, given, alphas, rhos)

    return x, y


def lims():
    """Sets the limits of the axes."""

    x_lim = [0, 1]
    y_lim = [0, 1]
    return x_lim, y_lim


def process_grid(x, given, alphas, rhos):
    """Calculates fitness curves."""

    y = np.zeros((len(alphas), len(rhos), len(x)))

    for i, alpha in enumerate(alphas):
        for j, rho in enumerate(rhos):
            y[i, j] = process_plot(x, given, alpha, rho)

    mask = y <= 0
    y[mask] = None

    return y


def process_plot(x, given, alpha, rho):
    """Difference in fitness between reciprocators and non-reciprocators."""

    increment = 0.001
    reciprocator = fitness(x, x, given, alpha, rho)
    non_reciprocator = fitness(x, x + increment, given, alpha, rho)

    # reciprocator[i, j] = fitness(x + increment, x + increment, given, alpha, rho)
    # non_reciprocator[i, j] = fitness(x, x, given, alpha, rho)
    mask = x + increment > qbeq(0.0, alpha, rho)
    reciprocator[mask] = None

    return (reciprocator - non_reciprocator) * 500
