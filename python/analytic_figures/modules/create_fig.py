""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt

from modules.add_colorbar import add_colorbar
from modules.fix_positions import create_divider
from modules.prettify_fig import create_measurements, prettify_fig


def create_fig(layout):
    """Create figure with subplots based on the layout dictionary."""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    nrows = layout["nrows"]
    ncols = layout["ncols"]
    nr = layout.get("nr", 1)
    nc = layout.get("nc", 1)

    measurements = create_measurements(nrows, ncols)
    width = measurements["width"]
    height = measurements["height"]

    if nr == 1:
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

    prettify_fig(fig, measurements)
    add_colorbar(fig, measurements, layout["color_bar_nc"])
    divider = create_divider(fig, measurements, layout)

    return fig, axs, divider
