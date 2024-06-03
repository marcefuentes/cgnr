""" Calculates fitness isoclines. """

import os
import numpy as np
from modules.theory import calculate_trps, qbeq


def data(options, dynamic_data, data_constants):
    """Main function."""

    x = np.linspace(0.001, 0.999, num=data_constants["n_x_values"])

    if options["single_folder"] and options["single_trait"]:
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
    tt, rr, pp, ss = calculate_trps(x + increment, x, given, alpha, rho)
    y = pp - ss # Reciprocity
    #y = (pp - ss) / (64 * rr - ss + 2 * pp - tt - 64 * pp)
    # y = rr - pp # Partner choice
    y *= 500
    mask = x + increment > qbeq(0.0, alpha, rho)
    y[mask] = None

    return y
