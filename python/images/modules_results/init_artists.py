""" Initialize artists for plotting. """

import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get


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


def init_artists_plot(axs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, ncols, nr, nc = axs.shape
    artists = np.empty_like(axs)
    x = np.arange(get_config("bins"))
    dummy_y = np.zeros_like(x)

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    (artists[i, j, k, m],) = axs[i, j, k, m].plot(
                        x,
                        dummy_y,
                        c="black",
                        lw=get("COMMON", "line_width") * get("COMMON", "plot_size"),
                    )
    return artists
