""" Initialize artists for plotting. """

import numpy as np


def init_imshow(axs, mr, mc, cmap):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    artists = np.empty_like(axs, dtype=object)
    dummy_zmatrix = np.zeros((mr, mc))
    params = {
        "cmap": cmap,
        "vmin": -1,
        "vmax": 1,
    }

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            for k in range(axs.shape[2]):
                for m in range(axs.shape[3]):
                    artists[i, j, k, m] = axs[i, j, k, m].imshow(
                        dummy_zmatrix,
                        **params,
                    )
    return artists


def init_line2d(axs, x, y):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    artists = np.empty_like(axs, dtype=object)

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            for k in range(axs.shape[2]):
                for m in range(axs.shape[3]):
                    (artists[i, j, k, m],) = axs[i, j, k, m].plot(
                        x,
                        y[i, j, k, m],
                    )
    return artists
