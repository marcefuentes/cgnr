""" Initialize artists for plotting. """

import numpy as np
from matplotlib.collections import LineCollection


def init_artists(axs, x, y, ic):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, _, nr, nc = axs.shape
    budgets = np.empty((nrows, 1, nr, nc), dtype=object)
    icurves = np.empty((nrows, 1, nr, nc), dtype=object)
    icurves_grey = np.empty((nrows, 1, nr, nc, ic.shape[2]), dtype=object)
    landscapes = np.empty((nrows, 1, nr, nc), dtype=object)

    for i in range(nrows):
        for j in range(nr):
            for k in range(nc):
                for m in range(ic.shape[2]):
                    icurves_grey[i, 0, j, k, m] = axs[i, 0, j, k].plot(x, ic[j, k, m])[0]
                budgets[i, 0, j, k] = axs[i, 0, j, k].plot(x, y)[0]
                icurves[i, 0, j, k] = axs[i, 0, j, k].plot(x, y)[0]
                landscapes[i, 0, j, k] = LineCollection([])
                axs[i, 1, j, k].add_collection(landscapes[i, 0, j, k])

    return budgets, icurves, icurves_grey, landscapes
