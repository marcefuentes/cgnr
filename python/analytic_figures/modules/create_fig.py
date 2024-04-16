""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt

from modules.fix_positions import create_divider


def create_fig(measurements, nrows, ncols, nc=None, nr=None):
    """Create figure with subplots."""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    width = measurements["width"]
    height = measurements["height"]

    if nr is None:
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(width, height))
        divider = create_divider(fig, measurements, nrows, ncols)
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
        divider = create_divider(fig, measurements, nrows, ncols, nr=nr, nc=nc)

    return fig, axs, divider
