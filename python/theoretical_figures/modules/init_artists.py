""" Initialize artists for plotting. """

import numpy as np

import modules.settings as ss


def init_plot_artists(axs, update_args):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    budgets = np.empty_like(axs)
    icurves = np.empty_like(axs)
    dummy_budgety = np.full_like(update_args["icx"], -1.0)
    dummy_icy = np.zeros_like(update_args["icx"])

    for g in range(2):
        for a, alpha in enumerate(update_args["alphas"]):
            for r, rho in enumerate(update_args["rhos"]):
                if g == 0:
                    for c in range(ss.N_IC): 
                        axs[0, a, r].plot(update_args["icx"], update_args["isoclines"][a, r, c], c="0.850")
                budgets[g, a, r], = axs[g, a, r].plot(update_args["icx"],
                    dummy_budgety,
                    c="0.300",
                    linewidth=4,
                    alpha=0.8)
                icurves[g, a, r], = axs[g, a, r].plot(update_args["icx"],
                    dummy_icy,
                    linewidth=4,
                    alpha=0.8)

    return budgets, icurves
