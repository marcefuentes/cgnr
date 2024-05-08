""" Initialize artists for plotting. """

import numpy as np

from modules.get_setting import get_setting as get
from modules_results.get_static_data import get_static_data


def init_artists_imshow(axs, mr, mc):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    nrows, ncols, nr, nc = axs.shape
    artists = np.empty_like(axs)
    dummy_zmatrix = np.zeros((mr, mc))

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    artists[i, j, k, m] = axs[i, j, k, m].imshow(
                        dummy_zmatrix, cmap=get("COMMON", "color_map"), vmin=-1, vmax=1
                    )
    return artists


def init_artists_2dline(axs, update_args):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, ncols, nr, nc = axs.shape
    artists = np.empty_like(axs)
    x, y = get_static_data(update_args)

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    (artists[i, j, k, m],) = axs[i, j, k, m].plot(
                        x,
                        y[k, m],
                        c="black",
                        lw=get("COMMON", "line_width") * get("COMMON", "plot_size"),
                    )
    return artists
