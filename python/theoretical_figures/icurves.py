#!/usr/bin/env python

""" Creates plots. """

import os
import time

from analytic_figures.modules.create_fig import create_fig
from modules.init_artists import init_plot_artists
from modules.prettify_axes import prettify_plot_axes
from analytic_figures.modules.process_plt import process_plt
from modules.get_data import get_data
import modules.settings as ss


def main():
    """Create the figure."""

    start_time = time.perf_counter()

    update_args = get_data()
    update_args["movie"] = False

    axes_args = {
        "y_values": update_args["alphas"],
        "x_values": update_args["logess"],
    }

    layout = {
        "nrows": 1,
        "ncols": 2,
        "nr": len(update_args["alphas"]),
        "nc": len(update_args["logess"]),
        "nested": True,
    }

    fig, axes_args["axs"], axes_args["divider"] = create_fig(layout)


    file_name = os.path.basename(__file__).split(".")[0]
    prettify_plot_axes(axes_args)
    update_args["artists"] = init_plot_artists(axes_args["axs"])

    process_plt(fig, ss.GIVENS, update_args, file_name)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    main()
