""" Initialize artists for plotting. """

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D


def init_artists_line2d(axs, x, y, ic, image):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nr, nc = axs.shape[2:4]
    budgets = np.empty((nr, nc), dtype=object)
    icurves = np.empty((nr, nc), dtype=object)
    icurves_grey = np.empty((nr, nc, ic.shape[2]), dtype=object)
    landscapes = np.empty((nr, nc), dtype=object)

    lw = image["line_width"] * image["plot_size"] / nc

    for i in range(nr):
        for j in range(nc):
            for k in range(ic.shape[2]):
                icurves_grey[i, j, k] = Line2D(
                    x,
                    ic[i, j, k],
                )
                axs[0, 0, i, j].add_line(icurves_grey[i, j, k])
            budgets[i, j] = Line2D(
                x,
                y,
            )
            axs[0, 0, i, j].add_line(budgets[i, j])

            icurves[i, j] = Line2D(
                x,
                y,
            )
            axs[0, 0, i, j].add_line(icurves[i, j])

            landscapes[i, j] = LineCollection(
                [],
                lw=lw,
            )
            axs[0, 1, i, j].add_collection(landscapes[i, j])

    return budgets, icurves, icurves_grey, landscapes
