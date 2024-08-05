""" Data constants for icurves. """

import numpy as np

from icurvesm.add_static_data import add_static_data


def add_data(data, image):
    """Gets data from data."""

    data["alphas"] = np.linspace(**data["alphas_params"])
    data["logess"] = np.linspace(**data["logess_params"])
    if data["movie"]:
        data["frames"] = np.concatenate([np.linspace(**data["frames_params"]), [0.0]])
    else:
        data["frames"] = [0.0]

    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    image["nr"] = data["layout_k"] = len(data["alphas"])
    image["nc"] = data["layout_m"] = len(data["rhos"])
    image["fig_layout"] = {
        "nc": data["layout_m"],
        "ncols": 2,
        "nr": data["layout_k"],
        "nrows": len(data["givens"]),
    }
    image["letters"]["y"] = 1.0 + image["padding_letter"] * image["fig_layout"]["nr"]
    image["titles_columns"] = data["titles_columns"]
    image["titles_rows"] = data["titles_rows"]
    image["ticklabels_x"] = [
        f"{data["rhos"][0]:.0f}",
        f"{data["rhos"][data['layout_m'] // 2]:.0f}",
        f"{data["rhos"][-1]:.2f}",
    ]
    image["ticklabels_y"] = [
        f"{data["alphas"][0]:.1f}",
        f"{data["alphas"][data['layout_k'] // 2]:.1f}",
        f"{data["alphas"][-1]:.1f}",
    ]
    data["x"] = np.linspace(0.001, 0.999, num=image["n_x_values"])
    data["y"] = np.zeros_like(data["x"])
    add_static_data(data)
    image["lim_x"] = [0, 1]
    image["lim_y"] = [0, 1]
    data["color_map"] = image["color_map"]
