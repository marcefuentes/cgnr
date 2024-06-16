""" Initialize artists for plotting. """

import numpy as np


def init_artists(axs, x, y):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    artists = np.empty_like(axs, dtype=object)

    if x is None:
        for idx in np.ndindex(axs.shape):
            artists[idx] = axs[idx].imshow(y[idx])
        return artists

    for idx in np.ndindex(axs.shape):
        artists[idx] = axs[idx].fill_between(x, 0, y[idx])

    return artists
