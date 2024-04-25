""" Initialize artists for plotting. """

from matplotlib.collections import LineCollection
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

    for k in range(get(file_name, "nc")):
        for m in range(get(file_name, "nc")):
            for c in range(get(file_name, "n_ic")):
                axs[0, 0, k, m].plot(
                    update_args["icx"],
                    update_args["isoclines"][k, m, c],
                    c="0.850",
                    lw=get("COMMON", "line_width") * 8,
                )
            (update_args["budgets"][k, m],) = axs[0, 0, k, m].plot(
                update_args["icx"],
                dummy_budgety,
                c="0.300",
                lw=get("COMMON", "line_width") * 20,
                alpha=0.8,
            )
            (update_args["icurves"][k, m],) = axs[0, 0, k, m].plot(
                update_args["icx"],
                dummy_icy,
                lw=get("COMMON", "line_width") * 20,
                alpha=0.8,
            )
            update_args["landscapes"][k, m] = axs[0, 1, k, m]

    return update_args
