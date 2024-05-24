""" Initialize artists for plotting. """

import numpy as np

from modules.get_setting import get_setting as get


def init_artists_imshow(axs, mr, mc):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    artists = np.empty_like(axs, dtype=object)
    dummy_zmatrix = np.zeros((mr, mc))
    plot_params = {
        "cmap": get("COMMON", "color_map"),
        "vmin": -1,
        "vmax": 1,
    }

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            for k in range(axs.shape[2]):
                for m in range(axs.shape[3]):
                    artists[i, j, k, m] = axs[i, j, k, m].imshow(
                        dummy_zmatrix,
                        **plot_params,
                    )
    return artists


def init_artists_line2d(axs, x, y):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    artists = np.empty_like(axs, dtype=object)
    plot_params = {
        "c": "black",
        "lw": get("COMMON", "line_width") * get("COMMON", "plot_size"),
    }

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            for k in range(axs.shape[2]):
                for m in range(axs.shape[3]):
                    (artists[i, j, k, m],) = axs[i, j, k, m].plot(
                        x,
                        y[k, m],
                        **plot_params,
                    )
    return artists
