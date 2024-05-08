""" Initialize artists for plotting. """

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

from modules.get_setting import get_setting as get


def init_artists_line2d(axs, update_args, x, y, ic):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nr, nc = axs.shape[2:4]
    n_ic = ic.shape[2]
    update_args["budgets"] = np.empty((nr, nc), dtype=object)
    update_args["icurves"] = np.empty((nr, nc), dtype=object)
    update_args["landscapes"] = np.empty((nr, nc), dtype=object)
    plot_size = get("COMMON", "plot_size")
    lw = get("COMMON", "line_width") * plot_size * 12 / nc

    for i in range(nr):
        for j in range(nc):
            for k in range(n_ic):
                axs[0, 0, i, j].plot(
                    x,
                    ic[i, j, k],
                    c="0.850",
                    lw=lw / 2,
                )
            update_args["budgets"][i, j] = Line2D(
                x,
                y,
                c="0.300",
                lw=lw,
                alpha=0.6,
            )
            axs[0, 0, i, j].add_line(update_args["budgets"][i, j])

            update_args["icurves"][i, j] = Line2D(
                x,
                y,
                lw=lw,
                alpha=0.8,
            )
            axs[0, 0, i, j].add_line(update_args["icurves"][i, j])

            update_args["landscapes"][i, j] = LineCollection(
                [],
                lw=lw,
            )
            axs[0, 1, i, j].add_collection(update_args["landscapes"][i, j])

    return update_args
