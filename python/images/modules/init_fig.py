""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt


def init_fig(fig_layout):
    """Create figure with subplots based on the fig_layout dictionary."""

    if fig_layout["nested"]:
        fig = plt.figure()
        outergrid = fig.add_gridspec(
            nrows=fig_layout["nrows"], ncols=fig_layout["ncols"]
        )
        axs = np.empty(
            (
                fig_layout["nrows"],
                fig_layout["ncols"],
                fig_layout["nr"],
                fig_layout["nc"],
            ),
            dtype=object,
        )
        for i in range(fig_layout["nrows"]):
            for j in range(fig_layout["ncols"]):
                grid = outergrid[i, j].subgridspec(
                    nrows=fig_layout["nr"],
                    ncols=fig_layout["nc"],
                    hspace=0.0,
                    wspace=0.0,
                )
                axs[i, j] = grid.subplots()
    else:
        fig, axs = plt.subplots(
            nrows=fig_layout["nrows"],
            ncols=fig_layout["ncols"],
        )

    return fig, axs
