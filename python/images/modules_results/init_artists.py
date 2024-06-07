""" Initialize artists for plotting. """

import numpy as np


def init_imshow(axs, mr, mc):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    artists = np.empty_like(axs, dtype=object)
    dummy_zmatrix = np.zeros((mr, mc))

    for idx in np.ndindex(axs.shape):
        artists[idx] = axs[idx].imshow(dummy_zmatrix)

    return artists


def init_line2d(axs, x, y):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    artists = np.empty_like(axs, dtype=object)

    for idx in np.ndindex(axs.shape):
        artists[idx] = axs[idx].plot(x, y[idx])[0]

    return artists
