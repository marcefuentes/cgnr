""" Calculates static fitness isoclines. """

import os

import numpy as np

from modules_results.trait_sets_config import GIVEN_FOLDER
from modules.theory import fitness, qbeq


def get_static_y_data(update_args):
    """Calculates static fitness isoclines."""

    x_values = update_args["x_values"]

    if update_args["single_folder"] and update_args["single_trait"]:
        given_folder = os.path.basename(os.getcwd())
    else:
        given_folder = GIVEN_FOLDER
    given = float(given_folder[-3:])/100

    reciprocator = np.zeros(
        (
            len(update_args["alphas"]),
            len(update_args["rhos"]),
            len(update_args["x_values"]),
        )
    )
    non_reciprocator = np.zeros_like(reciprocator)

    increment = 0.001
    for i, alpha in enumerate(update_args["alphas"]):
        for j, rho in enumerate(update_args["rhos"]):
            qb_social = qbeq(0.0, alpha, rho)
            qb_private = qbeq(given, alpha, rho)
            reciprocator[i, j] = fitness(x_values, x_values, given, alpha, rho)
            non_reciprocator[i, j] = fitness(x_values, x_values + increment, given, alpha, rho)
            mask = x_values + increment > qb_social
            reciprocator[i, j][mask] = None

    y = (reciprocator - non_reciprocator) * 1000
    mask = y <= 0
    y[mask] = None
  
    return y
