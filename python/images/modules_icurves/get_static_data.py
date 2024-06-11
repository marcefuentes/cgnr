""" Calculates static fitness isoclines. """

import numpy as np

from modules.theory import indifference


def get_static_data(data):
    """Calculates static fitness isoclines."""

    x = np.linspace(0.001, 0.999, num=data["n_x_values"])
    y = np.zeros_like(x)

    n_ic = data["n_ic"]

    ws = np.linspace(
        1.0 / (n_ic + 1),
        n_ic / (n_ic + 1),
        num=n_ic,
    )

    isoclines = np.zeros(
        (
            data["nr"],
            data["nc"],
            n_ic,
            data["n_x_values"],
        )
    )

    for i, alpha in enumerate(data["alphas"]):
        for j, rho in enumerate(data["rhos"]):
            for k, w in enumerate(ws):
                isoclines[i, j, k] = indifference(x, w, alpha, rho)

    return x, y, isoclines
