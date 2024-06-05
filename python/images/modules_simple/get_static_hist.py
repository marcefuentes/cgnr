""" Creates dummy data for histograms. """

import numpy as np
from settings_project.project import project


def lims():
    """Sets the limits of the axes."""

    x_lim = [-2, project["bins"] + 1]
    y_lim = [0, 0.25]
    return x_lim, y_lim


def data(mr, mc):
    """Creates dummy data for histograms"""

    x = np.arange(project["bins"])
    y = np.zeros((mr, mc, len(x)))
    return x, y
