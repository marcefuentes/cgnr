""" Initialize artists for plotting. """

from numpy import empty
from matplotlib.collections import LineCollection


def get_artists(axs, x, y, ic):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, _, nr, nc = axs.shape
    budgets = empty((nrows, 1, nr, nc), dtype=object)
    icurves = empty((nrows, 1, nr, nc), dtype=object)
    icurves_grey = empty((nrows, 1, nr, nc, ic.shape[2]), dtype=object)
    landscapes = empty((nrows, 1, nr, nc), dtype=object)

    for i in range(nrows):
        for k in range(nr):
            for m in range(nc):
                for n in range(ic.shape[2]):
                    icurves_grey[i, 0, k, m, n] = axs[i, 0, k, m].plot(x, ic[k, m, n])[
                        0
                    ]
                budgets[i, 0, k, m] = axs[i, 0, k, m].plot(x, y)[0]
                icurves[i, 0, k, m] = axs[i, 0, k, m].plot(x, y)[0]
                landscapes[i, 0, k, m] = LineCollection([])
                axs[i, 1, k, m].add_collection(landscapes[i, 0, k, m])

    return budgets, icurves, icurves_grey, landscapes
