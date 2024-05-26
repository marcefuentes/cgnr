""" Calculates fitness isoclines. """

import os

import numpy as np

from modules_results.settings import SETTINGS as settings
from modules.theory import fitness, qbeq


def fitness_curve(update_args, x):
    """Calculates static fitness curves."""

    if update_args["single_folder"] and update_args["single_trait"]:
        given = float(os.path.basename(os.getcwd()))
    else:
        given = float(settings["given_folder"])

    reciprocator = np.zeros(
        (
            len(update_args["alphas"]),
            len(update_args["rhos"]),
            len(x),
        )
    )
    non_reciprocator = np.zeros_like(reciprocator)

    increment = 0.001
    for i, alpha in enumerate(update_args["alphas"]):
        for j, rho in enumerate(update_args["rhos"]):
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


def data(update_args):
    """Calculates static fitness isoclines."""

    x = np.linspace(0.001, 0.999, num=settings["n_x_values"])
    y = fitness_curve(update_args, x)
    return x, y
