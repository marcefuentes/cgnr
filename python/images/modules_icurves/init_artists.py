""" Initialize artists for plotting. """

import numpy as np
from matplotlib.collections import LineCollection


def init_artists_line2d(axs, x, y, ic):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nr, nc = axs.shape[2:4]
    budgets = np.empty((nr, nc), dtype=object)
    icurves = np.empty((nr, nc), dtype=object)
    icurves_grey = np.empty((nr, nc, ic.shape[2]), dtype=object)
    landscapes = np.empty((nr, nc), dtype=object)

    for i in range(nr):
        for j in range(nc):
            for k in range(ic.shape[2]):
                icurves_grey[i, j, k] = axs[0, 0, i, j].plot(x, ic[i, j, k])[0]
            budgets[i, j] = axs[0, 0, i, j].plot(x, y)[0]
            icurves[i, j] = axs[0, 0, i, j].plot(x, y)[0]
            landscapes[i, j] = LineCollection([])
            axs[0, 1, i, j].add_collection(landscapes[i, j])

    return budgets, icurves, icurves_grey, landscapes
