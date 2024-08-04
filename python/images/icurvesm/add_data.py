""" Data constants for icurves. """

import numpy as np

from icurvesm.get_static_data import get_static_data


def add_data(data):
    """Gets data from data."""

    data["alphas"] = np.linspace(**data["alphas_params"])
    data["logess"] = np.linspace(**data["logess_params"])
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])
    data["layout_k"] = len(data["alphas"])
    data["layout_m"] = len(data["rhos"])
    data["ticklabels_x"] = [
        f"{data["rhos"][0]:.0f}",
        f"{data["rhos"][data['layout_m'] // 2]:.0f}",
        f"{data["rhos"][-1]:.2f}",
    ]
    data["ticklabels_y"] = [
        f"{data["alphas"][0]:.1f}",
        f"{data["alphas"][data['layout_k'] // 2]:.1f}",
        f"{data["alphas"][-1]:.1f}",
    ]
    data["x_values"], data["y"], data["ic"] = get_static_data(
        data["alphas"], data["rhos"], data["n_ic"]
    )
    data["frames"] = [0.0]
    if data["movie"]:
        data["frames"] = np.concatenate([np.linspace(**data["frames_params"]), [0.0]])
