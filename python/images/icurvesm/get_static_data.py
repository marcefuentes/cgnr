""" Calculates static fitness isoclines. """

import numpy as np

from modules.theory import indifference
from icurvess.image import image_common


def get_static_data(alphas, rhos, n_ic):
    """Calculates static fitness isoclines."""

    x = np.linspace(0.001, 0.999, num=image_common["n_x_values"])
    y = np.zeros_like(x)

    ws = np.linspace(
        1.0 / (n_ic + 1),
        n_ic / (n_ic + 1),
        num=n_ic,
    )

    isoclines = np.zeros((len(alphas), len(rhos), n_ic, image_common["n_x_values"]))

    for i, alpha in enumerate(alphas):
        for j, rho in enumerate(rhos):
            for k, w in enumerate(ws):
                isoclines[i, j, k] = indifference(x, w, alpha, rho)

    return x, y, isoclines
