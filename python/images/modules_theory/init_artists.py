""" Initialize artists for plotting. """

import numpy as np

import modules_theory.settings as ss
from modules.settings import PLOT_SIZE


def init_plot_artists(axs, kwargs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    kwargs["budgets"] = np.empty((ss.NC, ss.NC), dtype=object)
    kwargs["icurves"] = np.empty_like(kwargs["budgets"])
    kwargs["landscapes"] = np.empty_like(kwargs["budgets"])
    dummy_budgety = np.full_like(kwargs["icx"], -1.0)
    dummy_icy = np.zeros_like(kwargs["icx"])

    for k in range(ss.NC):
        for m in range(ss.NC):
            for c in range(ss.N_IC):
                axs[0, 0, k, m].plot(
                    kwargs["icx"],
                    kwargs["isoclines"][k, m, c],
                    c="0.850",
                    lw=ss.LINE_WIDTH * PLOT_SIZE / 4,
                )
            (kwargs["budgets"][k, m],) = axs[0, 0, k, m].plot(
                kwargs["icx"],
                dummy_budgety,
                c="0.300",
                lw=ss.LINE_WIDTH * PLOT_SIZE,
                alpha=0.8,
            )
            (kwargs["icurves"][k, m],) = axs[0, 0, k, m].plot(
                kwargs["icx"], dummy_icy, lw=ss.LINE_WIDTH * PLOT_SIZE, alpha=0.8
            )
            (kwargs["landscapes"][k, m],) = axs[0, 1, k, m].plot(
                kwargs["icx"], dummy_icy, lw=ss.LINE_WIDTH * PLOT_SIZE, alpha=0.8
            )

    return kwargs
