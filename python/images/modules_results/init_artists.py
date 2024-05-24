""" Initialize artists for plotting. """

import numpy as np

from modules.get_setting import get_setting as get


def init_artists_imshow(axs, mr, mc):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    nrows, ncols, nr, nc = axs.shape
    artists = np.empty((nrows, ncols, nr, nc), dtype=object)

    dummy_zmatrix = np.zeros((mr, mc))
    plot_params = {
        "cmap": get("COMMON", "color_map"),
        "vmin": -1,
        "vmax": 1,
    }

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    artists[i, j, k, m] = axs[i, j, k, m].imshow(
                        dummy_zmatrix,
                        **plot_params,
                    )
    return artists


def init_artists_line2d(axs, x, y):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, ncols, nr, nc = axs.shape
    artists = np.empty((nrows, ncols, nr, nc), dtype=object)

    plot_params = {
        "c": "black",
        "lw": get("COMMON", "line_width") * get("COMMON", "plot_size"),
    }

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    (artists[i, j, k, m],) = axs[i, j, k, m].plot(
                        x,
                        y[k, m],
                        **plot_params,
                    )
    return artists
