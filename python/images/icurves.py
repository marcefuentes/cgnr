#!/usr/bin/env python

""" Plot indifference curves and budget lines, and fitness landscapes"""

import os
import time

from modules.init_fig import init_fig
from modules.save_image import save_image, close_plt
from modules.save_movie import save_movie
from modules.prettify_axes import prettify_axes_plot

from modules_icurves.get_data import get_data
from modules_icurves.get_sm import get_sm
from modules_icurves.init_artists import init_plot_artists
from modules_icurves.parse_args import parse_args
from modules_icurves.update import update_artists


def main(args):
    """Main function"""

    start_time = time.perf_counter()
    file_name = os.path.basename(__file__).split(".")[0]

    update_args = {
        "alphas": None,
        "buget_0": None,
        "budgets": None,
        "icurves": None,
        "icx": None,
        "isoclines": None,
        "landscapes": None,
        "logess": None,
        "movie": args.movie,
        "rhos": None,
        "update_function": update_artists,
    }

    givens, update_args = get_data(file_name, update_args)

    axes_args = {
        "axs": None,
        "column_titles": [""],
        "divider": None,
        "file_name": file_name,
        "init_function": init_plot_artists,
        "prettify_function": prettify_axes_plot,
        "row_titles": [""],
        "x_lim": [0, 1],
        "x_values": update_args["logess"],
        "y_lim": [0, 1],
        "y_values": update_args["alphas"],
    }

    fig_args = {
        "file_name": file_name,
        "nc": len(update_args["logess"]),
        "ncols": 2,
        "nested": True,
        "nr": len(update_args["alphas"]),
        "nrows": 1,
        "sm": get_sm(),
    }

    fig, update_args = init_fig(fig_args, axes_args, update_args)

    if args.movie:
        save_movie(fig, givens, update_args, file_name)
    else:
        save_image(givens[-1], update_args, file_name)

    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
