""" Calculates fitness isoclines. """

import numpy as np
from modules.theory import calculate_trps, qbeq


def get_curves(num, traits, givens, alphas, rhos):
    """Calculates fitness curves."""

    x = np.linspace(0.001, 0.999, num=num)
    y = np.zeros((len(givens), len(givens[0]), len(alphas), len(rhos), len(x)))

    for i in range(y.shape[0]):
        for j in range(y.shape[1]):
            for k in range(y.shape[2]):
                for m in range(y.shape[3]):
                    y[i, j, k, m] = process_plot(
                        x, traits[i][j], float(givens[i][j]), alphas[k], rhos[m]
                    )

    mask = y <= 0
    y[mask] = np.nan

    return x, y


def process_plot(x, trait, given, alpha, rho):
    """Difference in fitness between reciprocators and non-reciprocators."""

    increment = 0.001
    tt, rr, pp, ss = calculate_trps(x + increment, x, given, alpha, rho)
    if trait == "MimicGrain":
        y = pp - ss
        # y = (pp - ss) / (64 * rr - ss + 2 * pp - tt - 64 * pp)
    else:
        y = rr - pp  # Partner choice

    y *= 500
    mask = (x + increment < qbeq(given, alpha, rho)) | (x > qbeq(0.0, alpha, rho))
    y[mask] = None

    return y
