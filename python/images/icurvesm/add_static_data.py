""" Add static data. """

import numpy as np
from icurvesm.add_theoretical_data import add_theoretical_data


def add_static_data(data, image):
    """Calculates static fitness isoclines."""

    data["x"] = np.linspace(0.001, 0.999, num=image["n_x_values"])
    data["y"] = np.zeros_like(data["x"])
    image["lim_x"] = [0, 1]
    image["lim_y"] = [0, 1]
    add_theoretical_data(data)
