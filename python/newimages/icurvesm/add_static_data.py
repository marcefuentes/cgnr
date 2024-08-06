""" Calculates static fitness isoclines. """

import numpy as np
from modules.theory import indifference


def add_static_data(data, image):
    """Calculates static fitness isoclines."""

    data["x"] = np.linspace(0.001, 0.999, num=image["n_x_values"])
    data["y"] = np.zeros_like(data["x"])
    image["lim_x"] = [0, 1]
    image["lim_y"] = [0, 1]
    n_ic = data["n_ic"]

    ws = np.linspace(
        1.0 / (n_ic + 1),
        n_ic / (n_ic + 1),
        num=n_ic,
    )

    layout = (len(data["alphas"]), len(data["rhos"]), n_ic, len(data["x"]))

    data["ic"] = np.zeros(layout)

    for i, alpha in enumerate(data["alphas"]):
        for j, rho in enumerate(data["rhos"]):
            for k, w in enumerate(ws):
                data["ic"][i, j, k] = indifference(data["x"], w, alpha, rho)
