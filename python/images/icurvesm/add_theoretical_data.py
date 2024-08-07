""" Add theoretical data. """

import numpy as np
from modules.theory import get_icurves


def add_theoretical_data(data):
    """Calculates theoretical data."""
        
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
                data["ic"][i, j, k] = get_icurves(data["x"], w, alpha, rho)
