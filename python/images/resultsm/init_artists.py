""" Initialize artists for plotting. """

import numpy as np


def init_artists(axs, x, y, ax_type):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    artists = np.empty_like(axs, dtype=object)

    for idx in np.ndindex(axs.shape):
        if ax_type == "AxesImage":
            artists[idx] = axs[idx].imshow(y[idx])
        elif ax_type == "Line2D":
            artists[idx] = axs[idx].plot(x, y[idx])[0]
        else:
            artists[idx] = axs[idx].fill_between(x, 0, y[idx])

    return artists
