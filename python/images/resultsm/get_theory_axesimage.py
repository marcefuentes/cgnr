""" Calculates theoretical values for AxesImage. """

import numpy as np
from modules.theory import calculate_fitness, qbeq


def get_theory_axesimage(traits, givens, alphas, rhos):
    """Calculates theoretical values for AxesImage."""

    x = None
    y = np.zeros((len(givens), len(givens[0]), 1, 1, len(alphas), len(rhos)))

    for i, givens_row in enumerate(givens):
        for k, alpha in enumerate(alphas):
            for m, rho in enumerate(rhos):
                y[i, 0, 0, 0, k, m] = process_plot(
                    traits[i][1], float(givens_row[1]), alpha, rho
                )

    return x, y


def process_plot(trait, given, alpha, rho):
    """Processes the plot."""

    qb = qbeq(given, alpha, rho)
    if trait == "qBSeenmean":
        return qb
    return calculate_fitness(qb, qb, given, alpha, rho)
