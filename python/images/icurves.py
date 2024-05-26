#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

import os
import time

from modules.fix_positions import create_divider
from modules.create_fig import create_fig
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.save_file import save_file
from modules.save_image import close_plt

from modules_icurves.get_sm import get_sm
from modules_icurves.get_static_data import get_static_data
from modules_icurves.get_update_args import get_update_args
from modules_icurves.init_artists import init_artists_line2d
from modules_icurves.parse_args import parse_args
from modules_icurves.settings import SETTINGS as settings
from modules_icurves.update_artists import update_artists


def main(args):
    """Main function"""

    start_time = time.perf_counter()

    update_args = {
        "alphas": [],
        "budgets": [],
        "file_name": os.path.basename(__file__).split(".")[0],
        "frames": [],
        "icurves": [],
        "landscapes": [],
        "logess": [],
        "movie": args.movie,
        "rhos": [],
        "update_function": update_artists,
        "x_values": [],
    }

    update_args = get_update_args(update_args)

    fig_layout = {
        "nc": len(update_args["logess"]),
        "ncols": 2,
        "nr": len(update_args["alphas"]),
        "nrows": 1,
    }

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"])
    format_fig(fig, fig_distances, settings, get_sm())
    update_args["text"] = fig.texts[2]
    update_args["x_values"], y, ic = get_static_data(
        update_args["alphas"], update_args["rhos"]
    )
    update_args["budgets"], update_args["icurves"], update_args["landscapes"] = (
        init_artists_line2d(axs, update_args["x_values"], y, ic)
    )

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

    format_axes(axes_args)

    save_file(fig, update_args)

    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
