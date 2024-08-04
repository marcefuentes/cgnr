""" Initialize artists for plotting. """

import numpy as np


def get_artists(ax_type, axs, x, y):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    artists = np.empty_like(axs, dtype=object)

    for idx in np.ndindex(axs.shape):
        if ax_type == "AxesImage":
            artists[idx] = axs[idx].imshow(y)
        elif ax_type == "Line2D":
            artists[idx] = axs[idx].plot(x, y)[0]
        else:
            artists[idx] = axs[idx].fill_between(x, 0, y[idx])

    return artists
