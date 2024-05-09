""" Calculates static fitness isoclines. """

import numpy as np

from modules.get_setting import get_setting as get
from modules.theory import indifference


def get_static_data(alphas, rhos):
    """Calculates static fitness isoclines."""

    x = np.linspace(0.001, 0.999, num=get("icurves", "n_x_values"))

    y = np.zeros_like(x)

    n_ic = get("icurves", "n_ic")

    ws = np.linspace(
        1.0 / (n_ic + 1),
        n_ic / (n_ic + 1),
        num=n_ic,
    )

    isoclines = np.zeros(
        (
            len(alphas),
            len(rhos),
            n_ic,
            len(x),
        )
    )

    for i, alpha in enumerate(alphas):
        for j, rho in enumerate(rhos):
            for k, w in enumerate(ws):
                isoclines[i, j, k] = indifference(x, w, alpha, rho)

    return x, y, isoclines
