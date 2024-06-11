""" Data constants for icurves. """

import numpy as np


def data_constants():
    """Data common to all subplots."""

    data = {
        "alpha_min": 0.1,
        "alpha_max": 0.9,
        "loges_min": -2.0,
        "loges_max": 2.0,
        "n_ic": 5,
        "n_x_values": 256,
        "nc": 3,
        "nr": 3,
    }

    data["frames"] = np.linspace(0.0, 1.0, num=11)
    data["frames"] = np.append(data["frames"], 0.0)

    data["givens"] = [0.99, 0.5, 0.0]
    data["alphas"] = np.linspace(
        data["alpha_max"],
        data["alpha_min"],
        num=data["nr"],
    )
    data["logess"] = np.linspace(
        data["loges_min"],
        data["loges_max"],
        num=data["nc"],
    )
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    return data
