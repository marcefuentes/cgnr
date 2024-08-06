""" Add static data. """

import numpy as np

from settings.project import project
from modules.theory import calculate_trps, qbeq


def add_static_data(data, image):
    """Add limits to x axis and y axis."""

    if data["layout"] == "curves":
        data["x"] = np.linspace(0.001, 0.999, num=image["n_x_values"])
        image["lim_x"] = [0, 1]
        image["lim_y"] = [0, 1]
        image["margin_top"] *= 0.5
        add_curves_data(data)
    elif data["histogram"]:
        data["x"] = np.arange(project["bins"])
        data["y"] = np.zeros_like(data["x"])
        image["lim_x"] = [-2, len(data["x"]) + 1]
        image["lim_y"] = [0, 0.25]
    else:
        data["x"] = None
        data["y"] = np.zeros((data["layout_k"], data["layout_m"]))
        image["lim_x"] = [None, None]
        image["lim_y"] = [None, None]


def add_curves_data(data):
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
