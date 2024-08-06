""" Add static data. """

import numpy as np

from settings.project import project
from modules.theory import calculate_fitness, calculate_trps, qbeq


def add_static_data(data, image):
    """Add limits to x axis and y axis."""

    layout = (data["layout_i"], data["layout_j"], data["layout_k"], data["layout_m"])

    if data["layout"] == "curves":
        data["x"] = np.linspace(0.001, 0.999, num=image["n_x_values"])
        data["y"] = np.zeros((*layout, image["n_x_values"]))
        image["lim_x"] = [0, 1]
        image["lim_y"] = [0, 1]
        image["margin_top"] *= 0.5
        curves_data(data)
    elif data["histogram"]:
        data["x"] = np.arange(project["bins"])
        data["y"] = np.zeros((*layout, project["bins"]))
        image["lim_x"] = [-2, len(data["x"]) + 1]
        image["lim_y"] = [0, 0.25]
    else:
        data["x"] = None
        data["y"] = np.zeros((*layout, len(data["alphas"]), len(data["rhos"])))
        image["lim_x"] = [None, None]
        image["lim_y"] = [None, None]
        if data["layout"] == "theory":
            eq_data(data)


def curves_data(data):
    """Calculates fitness curves."""

    layout = (data["layout_i"], data["layout_j"])

    for i, j in np.ndindex(layout):
        trait = data["traits"][i][j]
        given = float(data["givens"][i][j])

        for k, alpha in enumerate(data["alphas"]):
            for m, rho in enumerate(data["rhos"]):
                if j == 0:
                    data["y"][i, j, k, m] = get_curves_data_plot(
                        data["x"], trait, given, alpha, rho
                    )


def get_curves_data_plot(x, trait, given, alpha, rho):
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


def eq_data(data):
    """Calculates theoretical values for AxesImage."""

    trait = data["traits"][0][1]

    for i, givens_row in enumerate(data["givens"]):
        given = float(givens_row[1])
        for k, alpha in enumerate(data["alphas"]):
            for m, rho in enumerate(data["rhos"]):
                data["y"][i, 0, 0, 0, k, m] = get_eq_data_pixel(
                    trait, given, alpha, rho
                )


def get_eq_data_pixel(trait, given, alpha, rho):
    """Processes the plot."""

    qb = qbeq(given, alpha, rho)
    if trait == "qBSeenmean":
        return qb
    return calculate_fitness(qb, qb, given, alpha, rho)
