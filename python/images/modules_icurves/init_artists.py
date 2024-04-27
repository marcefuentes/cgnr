""" Initialize artists for plotting. """

import numpy as np

from modules.get_setting import get_setting as get
from matplotlib.collections import LineCollection


def init_plot_artists(axs, update_args):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    _, _, nr, nc = axs.shape
    _, _, n_ic, _ = update_args["isoclines"].shape
    update_args["budgets"] = np.empty((nr, nc), dtype=object)
    update_args["icurves"] = np.empty_like(update_args["budgets"])
    update_args["landscapes"] = np.empty_like(update_args["budgets"])
    dummy_budgety = np.full_like(update_args["icx"], -1.0)
    dummy_icy = np.zeros_like(update_args["icx"])

    for i in range(nr):
        for j in range(nc):
            for k in range(n_ic):
                axs[0, 0, i, j].plot(
                    update_args["icx"],
                    update_args["isoclines"][i, j, k],
                    c="0.850",
                    lw=get("COMMON", "line_width") * get("COMMON", "plot_size") * 2,
                )
            (update_args["budgets"][i, j],) = axs[0, 0, i, j].plot(
                update_args["icx"],
                dummy_budgety,
                c="0.300",
                lw=get("COMMON", "line_width") * get("COMMON", "plot_size") * 4,
                alpha=0.8,
            )
            (update_args["icurves"][i, j],) = axs[0, 0, i, j].plot(
                update_args["icx"],
                dummy_icy,
                lw=get("COMMON", "line_width") * get("COMMON", "plot_size") * 5,
                alpha=0.8,
            )
            update_args["landscapes"][i, j] = LineCollection(
                    [],
                    cmap=get("COMMON", "color_map"),
                    lw=get("COMMON", "line_width") * get("COMMON", "plot_size") * 6
                )
            axs[0, 1, i, j].add_collection(update_args["landscapes"][i, j])

    return update_args
