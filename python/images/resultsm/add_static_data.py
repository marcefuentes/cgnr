""" Add static data. """

import numpy as np
from settings.project import project
from resultsm.add_theoretical_data import add_theoretical_data


def add_static_data(data, image):
    """Add limits to x axis and y axis."""

    layout = (data["layout_i"], data["layout_j"], data["layout_k"], data["layout_m"])

    if data["layout"] == "curves":
        data["x"] = np.linspace(0.001, 0.999, num=image["n_x_values"])
        data["y"] = np.zeros((*layout, image["n_x_values"]))
        image["lim_x"] = [0, 1]
        image["lim_y"] = [0, 1]
        image["margin_top"] *= 0.5
    elif data["histogram"]:
        data["x"] = np.arange(project["bins"])
        data["y"] = np.zeros((*layout, project["bins"]))
        image["lim_x"] = [-2, len(data["x"]) + 1]
        image["lim_y"] = [0, 0.25]
    else:
        data["x"] = None
        data["y"] = np.zeros((*layout, len(data["alphas"]), len(data["rhos"])))
        image["lim_x"] = [None, None]
        image["lim_y"] = [None, None]

    if data["layout"] == "curves" or data["layout"] == "theory":
        add_theoretical_data(data)
