""" Calculates static fitness isoclines. """

import os

import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting
from modules.theory import fitness, qbeq
from modules_results.trait_sets_config import GIVEN_FOLDER


def dummy_y(update_args, x):
    """Returns a dummy y array."""

    y = np.zeros(
        (
            len(update_args["alphas"]),
            len(update_args["logess"]),
            len(x),
        )
    )
    return y


def get_lims(fitness_limits):
    """Sets the limits of the axes."""

    if fitness_limits:
        x_lim = [0, 1]
        y_lim = [0, 1]
        return x_lim, y_lim

    x_lim = [-2, get_config("bins") + 1]
    y_lim = [0, 0.25]
    return x_lim, y_lim


def get_static_data(update_args):
    """Calculates static fitness isoclines."""

    if update_args["fitness"]:
        x = np.linspace(0.001, 0.999, num=get_setting("results", "n_x_values"))
        y = fitness_curve(update_args, x)
        return x, y

    x = np.arange(get_config("bins"))
    y = dummy_y(update_args, x)
    return x, y


def fitness_curve(update_args, x):
    """Calculates static fitness curves."""

    if update_args["single_folder"] and update_args["single_trait"]:
        given_folder = os.path.basename(os.getcwd())
    else:
        given_folder = GIVEN_FOLDER
    given = float(given_folder)

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
