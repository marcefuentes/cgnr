""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt

from modules.fix_positions import create_divider


def create_fig(measurements, layout):
    """Create figure with subplots based on the layout dictionary."""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    width = measurements["width"]
    height = measurements["height"]

    nrows = layout["nrows"]
    ncols = layout["ncols"]
    nr = layout.get("nr", 1)
    nc = layout.get("nc", 1)

    if nr == 1 and nc == 1:
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(width, height))
    else:
        fig = plt.figure(figsize=(width, height))
        outergrid = fig.add_gridspec(nrows=nrows, ncols=ncols)
        axs = np.empty((nrows, ncols, nr, nc), dtype=object)
        for r in range(nrows):
            for c in range(ncols):
                grid = outergrid[r, c].subgridspec(
                    nrows=nr, ncols=nc, hspace=0.0, wspace=0.0
                )
                axs[r, c] = grid.subplots()

    divider = create_divider(fig, measurements, layout)

    return fig, axs, divider
