""" Creates dummy data for histograms. """

import numpy as np


def lims(bins):
    """Sets the limits of the axes."""

    x_lim = [-2, bins + 1]
    y_lim = [0, 0.25]
    return x_lim, y_lim


def data(bins, mr, mc):
    """Creates dummy data for histograms"""

    x = np.arange(bins)
    y = np.zeros((mr, mc, len(x)))
    return x, y
