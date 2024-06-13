""" Data constants for icurves. """

import numpy as np


def layouts():
    """Data common to all subplots."""

    given = {
        "start": 0.0,
        "stop": 1.0,
        "num": 11,
    }

    alpha = {
        "start": 0.1,
        "stop": 0.9,
        "num": 3,
    }

    loges = {
        "start": -2.0,
        "stop": 2.0,
        "num": 3,
    }

    data = {
        "alphas": np.linspace(**alpha),
        "frames": np.concatenate([np.linspace(**given), [0.0]]),
        "givens": [1.0, 0.99, 0.5, 0.0],
        "logess": np.linspace(**loges),
        "n_ic": 5,
    }

    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    return data
