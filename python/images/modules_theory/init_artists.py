""" Initialize artists for plotting. """

import numpy as np

import modules_theory.settings as ss
from modules.settings import PLOT_SIZE, BORDER_COLOR


def init_plot_artists(axs, update_args):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    budgets = np.empty((ss.NC, ss.NC), dtype=object)
    icurves = np.empty_like(budgets)
    landscapes = np.empty_like(budgets)
    dummy_budgety = np.full_like(update_args["icx"], -1.0)
    dummy_icy = np.zeros_like(update_args["icx"])

    for k in range(ss.NC):
        for m in range(ss.NC):
            for c in range(ss.N_IC):
                axs[0, 0, k, m].plot(
                    update_args["icx"], update_args["isoclines"][k, m, c], c="0.850", lw=ss.LINE_WIDTH * PLOT_SIZE / 4
                )
            (budgets[k, m],) = axs[0, 0, k, m].plot(
                update_args["icx"], dummy_budgety, c="0.300", lw=ss.LINE_WIDTH * PLOT_SIZE, alpha=0.8
            )
            (icurves[k, m],) = axs[0, 0, k, m].plot(
                update_args["icx"], dummy_icy, lw=ss.LINE_WIDTH * PLOT_SIZE, alpha=0.8
            )
            (landscapes[k, m],) = axs[0, 1, k, m].plot(
                update_args["icx"], dummy_icy, lw=ss.LINE_WIDTH * PLOT_SIZE, alpha=0.8
            )

    return budgets, icurves, landscapes
