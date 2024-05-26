""" Creates dummy data for histograms. """

import numpy as np
from common_modules.settings import SETTINGS as settings


def lims():
    """Sets the limits of the axes."""

    x_lim = [-2, settings["bins"] + 1]
    y_lim = [0, 0.25]
    return x_lim, y_lim


def data(update_args):
    """Creates dummy data for histograms"""

    x = np.arange(settings["bins"])
    y = np.zeros(
        (
            len(update_args["alphas"]),
            len(update_args["logess"]),
            len(x),
        )
    )
    return x, y
