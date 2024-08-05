""" Calculates fitness curves. """

import numpy as np
from modules.theory import calculate_trps, qbeq


def add_static_data(data):
    """Calculates fitness curves."""

    layout = (data["layout_i"], data["layout_j"], data["layout_k"], data["layout_m"])

    data["y"] = np.zeros((*layout, len(data["x"])))

    for i in range(layout[0]):
        for j in range(layout[1]):
            process_grid(data, i, j)


def process_grid(data, i, j):
    """Processes a grid."""

    trait = data["traits"][i][j]
    given = float(data["givens"][i][j])

    for k, alpha in enumerate(data["alphas"]):
        for m, rho in enumerate(data["rhos"]):
            if j == 0:
                data["y"][i, j, k, m] = process_plot(
                    data["x"], trait, given, alpha, rho
                )


def process_plot(x, trait, given, alpha, rho):
    """Difference in fitness between reciprocators and non-reciprocators."""

    inc = 0.001
    tt, rr, pp, ss = calculate_trps(x + inc, x, given, alpha, rho)

    _ = tt  # To avoid unused variable warning.

    if trait == "MimicGrainmean":
        y = pp - ss
        y *= 1000
    else:
        y = rr - pp  # Partner choice
        y *= 1000
    mask = (
        (x + inc < qbeq(given, alpha, rho))
        | (x + inc > qbeq(0.0, alpha, rho))
        | (y < 0)
    )
    y[mask] = np.nan

    return y
