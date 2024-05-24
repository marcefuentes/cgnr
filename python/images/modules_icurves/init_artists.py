""" Initialize artists for plotting. """

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

from modules.get_setting import get_setting as get


def init_artists_line2d(axs, x, y, ic):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nr, nc = axs.shape[2:4]
    budgets = np.empty((nr, nc), dtype=object)
    icurves = np.empty((nr, nc), dtype=object)
    landscapes = np.empty((nr, nc), dtype=object)

    lw = get("COMMON", "line_width") * get("COMMON", "plot_size") * 12 / nc

    for i in range(nr):
        for j in range(nc):
            for k in range(ic.shape[2]):
                axs[0, 0, i, j].plot(
                    x,
                    ic[i, j, k],
                    c="0.850",
                    lw=lw / 2,
                )
            budgets[i, j] = Line2D(
                x,
                y,
                c="0.300",
                lw=lw,
                alpha=0.6,
            )
            axs[0, 0, i, j].add_line(budgets[i, j])

            icurves[i, j] = Line2D(
                x,
                y,
                lw=lw,
                alpha=0.8,
            )
            axs[0, 0, i, j].add_line(icurves[i, j])

            landscapes[i, j] = LineCollection(
                [],
                lw=lw,
            )
            axs[0, 1, i, j].add_collection(landscapes[i, j])

    return budgets, icurves, landscapes
