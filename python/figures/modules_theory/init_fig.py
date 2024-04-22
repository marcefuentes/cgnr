""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt

from modules.add_colorbar import add_colorbar
from modules.fix_positions import create_divider
from modules.prettify_fig import create_measurements, prettify_fig


def init_fig(kwargs):
    """Create figure with subplots based on the kwargs dictionary."""

    new_args = create_measurements(kwargs["nrows"], kwargs["ncols"])

    fig = plt.figure(figsize=(new_args["width"], new_args["height"]))
    outergrid = fig.add_gridspec(nrows=kwargs["nrows"], ncols=kwargs["ncols"])
    axs = np.empty(
        (kwargs["nrows"], kwargs["ncols"], kwargs["nr"], kwargs["nc"]), dtype=object
    )

    for j in range(2):
        grid = outergrid[j].subgridspec(
            nrows=kwargs["nr"], ncols=kwargs["nc"], hspace=0.0, wspace=0.0
        )
        axs[0, j] = grid.subplots()

    prettify_fig(fig, new_args)
    # add_colorbar(fig, new_args, kwargs["nc"])
    divider = create_divider(fig, new_args, kwargs)

    return fig, axs, divider
