""" Initialize artists for plotting. """

import numpy as np

import modules.settings as ss


def init_plot_artists(axs, update_args):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    budgets = np.empty((ss.NC, ss.NC), dtype=object)
    icurves = np.empty_like(budgets)
    landscapes = np.empty_like(budgets)
    dummy_budgety = np.full_like(update_args["icx"], -1.0)
    dummy_icy = np.zeros_like(update_args["icx"])

    for k, alpha in enumerate(update_args["alphas"]):
        for m, rho in enumerate(update_args["rhos"]):
            for c in range(ss.N_IC): 
                axs[0, k, m].plot(update_args["icx"], update_args["isoclines"][k, m, c], c="0.850")
            budgets[k, m], = axs[0, k, m].plot(update_args["icx"],
                dummy_budgety,
                c="0.300",
                linewidth=4,
                alpha=0.8)
            icurves[k, m], = axs[0, k, m].plot(update_args["icx"],
                dummy_icy,
                linewidth=4,
                alpha=0.8)
            landscapes[k, m], = axs[1, k, m].plot(update_args["icx"],
                dummy_icy,
                linewidth=4,
                alpha=0.8)

    return budgets, icurves, landscapes
