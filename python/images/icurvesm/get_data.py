""" Data constants for icurves. """

import numpy as np


def get_data(data):
    """Gets data from data."""

    data["alphas"] = np.linspace(**data["alphas_params"])
    data["frames"] = [0.0]
    data["logess"] = np.linspace(**data["logess_params"])
    data["n_ic"] = data["n_indifference_curves"]
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    if data["movie"]:
        data["frames"] = np.concatenate([np.linspace(**data["frames_params"]), [0.0]])

    return data
