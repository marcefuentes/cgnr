""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt


def fig_create(fig_layout):
    """Create figure with subplots based on the fig_layout dictionary."""

    fig = plt.figure()
    outer_grid = fig.add_gridspec(nrows=fig_layout["nrows"], ncols=fig_layout["ncols"])
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
            grid = outer_grid[i, j].subgridspec(
                nrows=fig_layout["nr"],
                ncols=fig_layout["nc"],
                hspace=0.0,
                wspace=0.0,
            )
            axs[i, j] = grid.subplots()

    return fig, axs
