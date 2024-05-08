""" Initialize artists for plotting. """

import numpy as np
from matplotlib.collections import LineCollection

from modules.get_setting import get_setting as get


def init_artists_2dline(axs, update_args, static_y_data):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    _, _, nr, nc = axs.shape
    _, _, n_ic, _ = static_y_data.shape
    update_args["budgets"] = np.empty((nr, nc), dtype=object)
    update_args["icurves"] = np.empty((nr, nc), dtype=object)
    update_args["landscapes"] = np.empty((nr, nc), dtype=object)
    dummy_y = np.zeros_like(update_args["x_values"])
    plot_size = get("COMMON", "plot_size")

    for i in range(nr):
        for j in range(nc):
            for k in range(n_ic):
                axs[0, 0, i, j].plot(
                    update_args["x_values"],
                    static_y_data[i, j, k],
                    c="0.850",
                    lw=get("COMMON", "line_width") * plot_size * 6 / nc,
                )
            (update_args["budgets"][i, j],) = axs[0, 0, i, j].plot(
                update_args["x_values"],
                dummy_y,
                c="0.300",
                lw=get("COMMON", "line_width") * plot_size * 12 / nc,
                alpha=0.6,
            )

            (update_args["icurves"][i, j],) = axs[0, 0, i, j].plot(
                update_args["x_values"],
                dummy_y,
                lw=get("COMMON", "line_width") * plot_size * 12 / nc,
                alpha=0.8,
            )

            update_args["landscapes"][i, j] = LineCollection(
                [],
                lw=get("COMMON", "line_width") * plot_size * 12 / nc,
            )
            axs[0, 1, i, j].add_collection(update_args["landscapes"][i, j])

    return update_args
