""" Data constants for icurves. """

import numpy as np


def get_data(options, layout):
    """Gets data from layout."""

    data = {
        "alphas": np.linspace(**layout["alphas"]),
        "frames": [0.0],
        "givens": layout["given_rows"],
        "logess": np.linspace(**layout["logess"]),
        "n_ic": layout["n_indifference_curves"],
    }

    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    if options["movie"]:
        data["frames"] = np.concatenate([np.linspace(**layout["movie_frames"]), [0.0]])

    return data
