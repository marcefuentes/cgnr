""" Data constants for icurves. """

import numpy as np


def get_data(options):
    """Gets data from options."""

    data = {
        "alphas": np.linspace(**options["alphas"]),
        "frames": [0.0],
        "givens": options["given_rows"],
        "logess": np.linspace(**options["logess"]),
        "n_ic": options["n_indifference_curves"],
    }

    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    if options["movie"]:
        data["frames"] = np.concatenate([np.linspace(**options["movie_frames"]), [0.0]])

    return data
