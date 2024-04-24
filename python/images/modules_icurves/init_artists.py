""" Initialize artists for plotting. """

import numpy as np

from modules.get_setting import get_setting as get


def init_plot_artists(axs, file_name, kwargs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    kwargs["budgets"] = np.empty(
        (get(file_name, "nc"), get(file_name, "nc")), dtype=object
    )
    kwargs["icurves"] = np.empty_like(kwargs["budgets"])
    kwargs["landscapes"] = np.empty_like(kwargs["budgets"])
    dummy_budgety = np.full_like(kwargs["icx"], -1.0)
    dummy_icy = np.zeros_like(kwargs["icx"])

    for k in range(get(file_name, "nc")):
        for m in range(get(file_name, "nc")):
            for c in range(get(file_name, "n_ic")):
                axs[0, 0, k, m].plot(
                    kwargs["icx"],
                    kwargs["isoclines"][k, m, c],
                    c="0.850",
                    lw=get("COMMON", "line_width") * 8,
                )
            (kwargs["budgets"][k, m],) = axs[0, 0, k, m].plot(
                kwargs["icx"],
                dummy_budgety,
                c="0.300",
                lw=get("COMMON", "line_width") * 20,
                alpha=0.8,
            )
            (kwargs["icurves"][k, m],) = axs[0, 0, k, m].plot(
                kwargs["icx"], dummy_icy, lw=get("COMMON", "line_width") * 20, alpha=0.8
            )
            (kwargs["landscapes"][k, m],) = axs[0, 1, k, m].plot(
                kwargs["icx"], dummy_icy, lw=get("COMMON", "line_width") * 20, alpha=0.8
            )

    return kwargs
