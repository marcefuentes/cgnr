""" Calculates fitness curves. """

import numpy as np
from modules.theory import calculate_trps, qbeq
from resultss.image import image


def get_static_data(traits, givens, alphas, rhos):
    """Calculates fitness curves."""

    x = np.linspace(0.001, 0.999, num=image["n_x_values"])
    y = np.zeros((len(givens), len(givens[0]), len(alphas), len(rhos), len(x)))

    for i, j, k, m in np.ndindex(y.shape[:-1]):
        y[i, j, k, m] = process_plot(
            x, traits[i][j], float(givens[i][j]), alphas[k], rhos[m]
        )

    y[y <= 0] = np.nan

    return x, y


def process_plot(x, trait, given, alpha, rho):
    """Difference in fitness between reciprocators and non-reciprocators."""

    inc = 0.001
    t_sup, r_sup, p_sup, s_sup = calculate_trps(x + inc, x, given, alpha, rho)
    t_inf, r_inf, p_inf, s_inf = calculate_trps(x - inc, x, given, alpha, rho)

    # tt, rr, pp, ss = calculate_trps(x + inc, x, given, alpha, rho)
    # _ = tt  # To avoid unused variable warning.

    if trait == "MimicGrainmean":
        # y = (pp - ss) / (64 * rr - ss + 2 * pp - tt - 64 * pp)
        y = p_sup - s_sup + r_inf - t_inf
    else:
        # y = rr - pp
        y = r_sup - p_sup  # Partner choice

    y *= 500
    mask = (x + inc < qbeq(given, alpha, rho)) | (x + inc > qbeq(0.0, alpha, rho))
    y[mask] = np.nan

    return y
