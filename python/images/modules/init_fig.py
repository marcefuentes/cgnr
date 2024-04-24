""" Create figure with subplots. """

import numpy as np
import matplotlib.pyplot as plt

from modules.fix_positions import create_divider
from modules.prettify_fig import create_measurements, prettify_fig


def init_fig(kwargs, axes_args, update_args):
    """Create figure with subplots based on the kwargs dictionary."""

    new_args = create_measurements(kwargs["nrows"], kwargs["ncols"])

    if kwargs["nested"]:
        fig = plt.figure(figsize=(new_args["width"], new_args["height"]))
        outergrid = fig.add_gridspec(nrows=kwargs["nrows"], ncols=kwargs["ncols"])
        axes_args["axs"] = np.empty(
            (kwargs["nrows"], kwargs["ncols"], kwargs["nr"], kwargs["nc"]), dtype=object
        )
        for r in range(kwargs["nrows"]):
            for c in range(kwargs["ncols"]):
                grid = outergrid[r, c].subgridspec(
                    nrows=kwargs["nr"], ncols=kwargs["nc"], hspace=0.0, wspace=0.0
                )
                axes_args["axs"][r, c] = grid.subplots()
    else:
        fig, axes_args["axs"] = plt.subplots(
            nrows=kwargs["nrows"],
            ncols=kwargs["ncols"],
            figsize=(new_args["width"], new_args["height"]),
        )

    axes_args["divider"] = create_divider(fig, new_args, kwargs)
    new_args["sm"] = kwargs["sm"]
    new_args["file_name"] = kwargs["file_name"]

    prettify_fig(fig, new_args)
    update_args["text"] = fig.texts[2]
    update_args = axes_args["init_function"](
        axes_args["axs"], axes_args["file_name"], update_args
    )
    axes_args["prettify_function"](axes_args)

    return fig, update_args
