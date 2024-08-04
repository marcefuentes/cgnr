""" Initialize artists for plotting. """

import numpy as np


def add_artists(data, axs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    data["artists"] = np.empty_like(axs, dtype=object)

    for idx in np.ndindex(axs.shape):
        if data["ax_type"] == "AxesImage":
            data["artists"][idx] = axs[idx].imshow(data["y"])
        elif data["ax_type"] == "Line2D":
            data["artists"][idx] = axs[idx].plot(data["x"], data["y"])[0]
        else:
            data["artists"][idx] = axs[idx].fill_between(data["x"], 0, data["y"][idx])
