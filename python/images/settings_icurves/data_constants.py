""" Data constants for icurves. """

import numpy as np


def data_constants():
    """Data common to all subplots."""

    given_params = {
        "start": 0.0,
        "stop": 1.0,
        "num": 11,
    }

    alpha_params = {
        "start": 0.1,
        "stop": 0.9,
        "num": 3,
    }

    loges_params = {
        "start": -2.0,
        "stop": 2.0,
        "num": 3,
    }

    data = {
        "alphas": np.linspace(**alpha_params),
        "givens": [1.0, 0.99, 0.5, 0.0],
        "logess": np.linspace(**loges_params),
        "n_ic": 5,
        "n_x_values": 64,
    }

    data["frames"] = np.linspace(**given_params)
    data["frames"] = np.append(data["frames"], 0.0)

    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    return data
