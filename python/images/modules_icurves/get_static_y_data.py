""" Calculates static fitness isoclines. """

import numpy as np

from modules.get_setting import get_setting as get
from modules.theory import indifference


def get_static_y_data(update_args):
    """Calculates static fitness isoclines."""

    n_ic = get(update_args["file_name"], "n_ic")

    ws = np.linspace(
        1.0 / (n_ic + 1),
        n_ic / (n_ic + 1),
        num=n_ic,
    )

    isoclines = np.zeros(
        (
            len(update_args["alphas"]),
            len(update_args["rhos"]),
            n_ic,
            len(update_args["x_values"]),
        )
    )

    for i, alpha in enumerate(update_args["alphas"]):
        for j, rho in enumerate(update_args["rhos"]):
            for k, w in enumerate(ws):
                isoclines[i, j, k] = indifference(
                    update_args["x_values"], w, alpha, rho
                )

    return isoclines
