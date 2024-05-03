#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

import os
import time

from modules.fix_positions import create_divider
from modules.init_fig import init_fig
from modules.prettify_axes import prettify_axes
from modules.prettify_fig import get_distances, prettify_fig
from modules.save_file import save_file
from modules.save_image import close_plt

from modules_icurves.get_sm import get_sm
from modules_icurves.get_static_y_data import get_static_y_data
from modules_icurves.get_update_args import get_update_args
from modules_icurves.init_artists import init_plot_artists
from modules_icurves.parse_args import parse_args
from modules_icurves.update_artists import update_artists


def main(args):
    """Main function"""

    start_time = time.perf_counter()

    update_args = {
        "file_name": os.path.basename(__file__).split(".")[0],
        "movie": args.movie,
        "update_function": update_artists,
        "frames": None,
        "alphas": None,
        "rhos": None,
        "logess": None,
        "x_values": None,
        "budgets": None,
        "icurves": None,
        "landscapes": None,
    }

    update_args = get_update_args(update_args)

    fig_layout = {
        "nc": len(update_args["logess"]),
        "ncols": 2,
        "nr": len(update_args["alphas"]),
        "nrows": 1,
    }

    fig, axs = init_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"])
    prettify_fig(fig, fig_distances, update_args["file_name"], get_sm())
    update_args["text"] = fig.texts[2]
    update_args = init_plot_artists(axs, update_args, get_static_y_data(update_args))

    axes_args = {
        "axs": axs,
        "column_titles": [""],
        "divider": create_divider(fig, fig_layout, fig_distances),
        "row_titles": [""],
        "x_lim": [0, 1],
        "c_values": update_args["logess"],
        "y_lim": [0, 1],
        "r_values": update_args["alphas"],
    }
    prettify_axes(axes_args)

    save_file(fig, update_args)

    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
