#!/usr/bin/env python

""" Plot indifference curves and budget lines, and fitness landscapes"""

import os
import time

from modules.prettify_axes import prettify_axes_plot
from modules.init_fig import init_fig

from modules_theory.get_data import get_data
from modules_theory.init_artists import init_plot_artists
from modules_theory.make_movie import make_movie
from modules_theory.make_image import make_image, close_plt
from modules_theory.parse_args import parse_args

# Add data to figure


def main(args):
    """Main function"""

    start_time = time.perf_counter()

    givens, update_args = get_data()

    axes_args = {
        "x_values": update_args["logess"],
        "y_values": update_args["alphas"],
        "column_titles": ["", ""],
        "row_titles": [""],
        "x_lim": [0, 1],
        "y_lim": [0, 1],
    }

    update_args["movie"] = args.movie

    fig_args = {
        "nrows": 1,
        "ncols": 2,
        "nr": len(update_args["alphas"]),
        "nc": len(update_args["logess"]),
        "nested": True,
        "bar_width": 21,
    }

    fig, axes_args["axs"], axes_args["divider"] = init_fig(fig_args)
    prettify_axes_plot(axes_args)

    update_args["budgets"], update_args["icurves"], update_args["landscapes"] = (
        init_plot_artists(axes_args["axs"], update_args)
    )

    file_name = os.path.basename(__file__).split(".")[0]
    if args.movie:
        make_movie(fig, givens, update_args, file_name)
    else:
        make_image(givens, update_args, file_name)

    close_plt(fig)

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
