""" Initialize artists for plotting. """

import numpy as np


def add_artists(data, image):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    axs = image["axs"]
    artists = np.empty_like(axs, dtype=object)

    for idx in np.ndindex(axs.shape):
        if data["ax_type"] == "AxesImage":
            artists[idx] = axs[idx].imshow(data["y"], **image["AxesImage"])
        elif data["ax_type"] == "Line2D":
            artists[idx] = axs[idx].plot(data["x"], data["y"], **image["Line2D"])[0]
        else:
            artists[idx] = axs[idx].fill_between(
                data["x"], 0, data["y"][idx], **image["PolyCollection"]
            )

    data["artists"] = artists
