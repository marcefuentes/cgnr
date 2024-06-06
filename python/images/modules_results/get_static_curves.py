""" Calculates fitness isoclines. """

import os
import numpy as np
from modules.theory import calculate_trps, qbeq


def lims():
    """Sets the limits of the axes."""

    x_lim = [0, 1]
    y_lim = [0, 1]
    return x_lim, y_lim


def data(num, traits, givens, alphas, rhos):
    """Calculates fitness curves."""

    x = np.linspace(0.001, 0.999, num=num)
    y = np.zeros((len(givens), len(givens[0]), len(alphas), len(rhos), len(x)))

    for i, givens_row in enumerate(givens):
        for j, given in enumerate(givens_row):
            for k, alpha in enumerate(alphas):
                for m, rho in enumerate(rhos):
                    y[i, j, k, m] = process_plot(x, traits[i][j], float(given), alpha, rho)

    mask = y <= 0
    y[mask] = None

    return x, y


def process_plot(x, trait, given, alpha, rho):
    """Difference in fitness between reciprocators and non-reciprocators."""

    increment = 0.001
    tt, rr, pp, ss = calculate_trps(x + increment, x, given, alpha, rho)
    if trait == "MimicGrain":
        y = pp - ss
        # y = (pp - ss) / (64 * rr - ss + 2 * pp - tt - 64 * pp)
    else:
        y = rr - pp # Partner choice

    y *= 500
    mask = (x + increment < qbeq(given, alpha, rho)) | (x > qbeq(0.0, alpha, rho))
    y[mask] = None

    return y
