""" Add theoretical data. """

import numpy as np
from modules.theory import get_fitness, get_trps, get_qbeq


def add_theoretical_data(data):
    """Add theoretical data to the plot."""

    trait = data["traits"][0][1]

    for i in range(data["layout_i"]):
        given = data["givens"][i][0]
        for k, alpha in enumerate(data["alphas"]):
            for m, rho in enumerate(data["rhos"]):
                if data["layout"] == "curves":
                    data["y"][i, 0, k, m] = get_curve(
                        data["x"], trait, given, alpha, rho
                    )
                else:
                    data["y"][i, 0, 0, 0, k, m] = get_eq(trait, given, alpha, rho)


def get_curve(x, trait, given, alpha, rho):
    """Difference in fitness between reciprocators and non-reciprocators."""

    inc = 0.001
    tt, rr, pp, ss = get_trps(x + inc, x, given, alpha, rho)

    _ = tt  # To avoid unused variable warning.

    if trait == "MimicGrainmean":
        y = pp - ss
        y *= 1000
    else:
        y = rr - pp  # Partner choice
        y *= 1000
    mask = (
        (x + inc < get_qbeq(given, alpha, rho))
        | (x + inc > get_qbeq(0.0, alpha, rho))
        | (y < 0)
    )
    y[mask] = np.nan

    return y


def get_eq(trait, given, alpha, rho):
    """Processes the plot."""

    qb = get_qbeq(given, alpha, rho)
    if trait == "qBSeenmean":
        return qb
    return get_fitness(qb, qb, given, alpha, rho)
