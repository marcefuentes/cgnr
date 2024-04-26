""" Initialize artists for plotting. """

import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get


def init_imshow_artists(axs, nr, nc):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    nrows, ncols = axs.shape
    artists = np.empty_like(axs)
    dummy_zmatrix = np.zeros((nr, nc))

    for r in range(nrows):
        for c in range(ncols):
            artists[r, c] = axs[r, c].imshow(
                dummy_zmatrix, cmap=get("COMMON", "color_map"), vmin=-1, vmax=1
            )
    return artists


def init_plot_artists(axs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, ncols, nr, nc = axs.shape
    artists = np.empty_like(axs)
    x = np.arange(get_config("bins"))
    dummy_y = np.zeros_like(x)

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                for e in range(nc):
                    (artists[r, c, a, e],) = axs[r, c, a, e].plot(
                        x, dummy_y, c="black", lw=get("COMMON", "line_width") * get("COMMON", "plot_size")
                    )
    return artists
