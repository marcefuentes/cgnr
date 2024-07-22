""" Data constants for icurves. """

import numpy as np

from icurvesm.get_static_data import get_static_data


def get_data(data):
    """Gets data from data."""

    data["alphas"] = np.linspace(**data["alphas_params"])
    data["logess"] = np.linspace(**data["logess_params"])
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])
    data["x_values"], data["y"], data["ic"] = get_static_data(
        data["alphas"], data["rhos"], data["n_ic"]
    )
    data["frames"] = [0.0]
    if data["movie"]:
        data["frames"] = np.concatenate([np.linspace(**data["frames_params"]), [0.0]])
