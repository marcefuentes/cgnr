""" Creates dummy data for histograms. """

import numpy as np
from common_modules.get_config import get_config


def lims():
    """Sets the limits of the axes."""

    x_lim = [-2, get_config("bins") + 1]
    y_lim = [0, 0.25]
    return x_lim, y_lim


def data(update_args):
    """Creates dummy data for histograms"""

    x = np.arange(get_config("bins"))
    y = np.zeros(
        (
            len(update_args["alphas"]),
            len(update_args["logess"]),
            len(x),
        )
    )
    return x, y
