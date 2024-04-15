
""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import gridspec

from modules.add_colorbar import add_colorbar
from modules.fix_positions import create_divider
from modules.prettify_fig import prettify_fig
import modules.settings as ss

def create_measurements(nrows, ncols):
    """ Create measurements for figure. """

    inner_height = ss.PLOT_SIZE*nrows + ss.SPACING*(nrows - 1)
    inner_width = ss.PLOT_SIZE*ncols + ss.SPACING*(ncols - 1)
    width = inner_width + ss.LEFT_MARGIN + ss.RIGHT_MARGIN
    height = inner_height + ss.TOP_MARGIN + ss.BOTTOM_MARGIN
    measurements = {
        "width": width,
        "height": height,
        "inner_width": inner_width,
        "inner_height": inner_height
    }

    return measurements

def create_fig(nrows, ncols, nc, nr=None):
    """ Create figure with subplots. """

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    measurements = create_measurements(nrows, ncols)
    width = measurements["width"]
    height = measurements["height"]

    if nr is None:
        fig, axs = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(width, height)
        )
        divider = create_divider(fig, measurements, nrows, ncols)
    else:
        fig = plt.figure(figsize=(width, height))

        outergrid = fig.add_gridspec(nrows=nrows, ncols=ncols)
        axs = np.empty((nrows, ncols, nr, nc), dtype=object)
        for r in range(nrows):
            for c in range(ncols):
                grid = outergrid[r, c].subgridspec(
                    nrows=nr,
                    ncols=nc,
                    hspace=0.0,
                    wspace=0.0
                )
                axs[r, c] = grid.subplots()
        divider = create_divider(fig, measurements, nrows, ncols, nr=nr, nc=nc)

    prettify_fig(fig, measurements)
    add_colorbar(fig, measurements, nc)

    return fig, axs, divider
