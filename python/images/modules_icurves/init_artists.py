""" Initialize artists for plotting. """

import numpy as np

from modules.get_setting import get_setting as get


def init_plot_artists(axs, file_name, update_args):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    update_args["budgets"] = np.empty(
        (get(file_name, "nc"), get(file_name, "nc")), dtype=object
    )
    update_args["icurves"] = np.empty_like(update_args["budgets"])
    update_args["landscapes"] = np.empty_like(update_args["budgets"])
    dummy_budgety = np.full_like(update_args["icx"], -1.0)
    dummy_icy = np.zeros_like(update_args["icx"])
    dummy_segments = [[[x, y] for x, y in zip(update_args["icx"], dummy_icy)]]

    for i in range(get(file_name, "nc")):
        for j in range(get(file_name, "nc")):
            for m in range(get(file_name, "n_ic")):
                axs[0, 0, i, j].plot(
                    update_args["icx"],
                    update_args["isoclines"][i, j, m],
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
            update_args["landscapes"][i, j] = axs[0, 1, i, j]

    return update_args
