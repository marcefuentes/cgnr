""" Initialize artists for plotting. """

import numpy as np

import modules.settings as ss


def init_imshow_artists(axs, nr, nc):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    nrows, ncols = axs.shape
    artists = np.empty_like(axs)
    dummy_zmatrix = np.zeros((nr, nc))

    for r in range(nrows):
        for c in range(ncols):
            artists[r, c] = axs[r, c].imshow(
                dummy_zmatrix, cmap=ss.COLOR_MAP, vmin=-1, vmax=1
            )
    return artists


def init_plot_artists(axs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, ncols, nr, nc = axs.shape
    artists = np.empty_like(axs)
    x = np.arange(ss.N_X_VALUES)
    dummy_y = np.zeros_like(x)

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                for e in range(nc):
                    (artists[r, c, a, e],) = axs[r, c, a, e].plot(
                        x, dummy_y, c="black", lw=ss.LINE_WIDTH * 2
                    )
    return artists
