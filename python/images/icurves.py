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

from modules_icurves.get_data import get_data
from modules_icurves.get_sm import get_sm
from modules_icurves.get_static_data import get_static_data
from modules_icurves.init_artists import init_artists_line2d
from modules_icurves.parse_args import parse_args
from modules_icurves.update_artists import update_artists
from settings_icurves.image import image


def main(args):
    """Main function"""

    start_time = time.perf_counter()

    data_dict = {
        "alphas": [],
        "budgets": [],
        "frames": [],
        "icurves": [],
        "landscapes": [],
        "logess": [],
        "movie": args.movie,
        "rhos": [],
        "update_function": update_artists,
        "x_values": [],
    }

    data_dict = get_data(data_dict)

    fig_layout = {
        "nc": len(data_dict["logess"]),
        "ncols": 2,
        "nr": len(data_dict["alphas"]),
        "nrows": 1,
    }

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image, get_sm(image["color_map"]))
    data_dict["text"] = fig.texts[2]
    data_dict["x_values"], y, ic = get_static_data(
        data_dict["alphas"], data_dict["rhos"]
    )
    data_dict["budgets"], data_dict["icurves"], data_dict["landscapes"] = (
        init_artists_line2d(axs, data_dict["x_values"], y, ic)
    )

    axes_args = {
        "axs": axs,
        "c_labels": data_dict["logess"],
        "column_titles": [""],
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "nc": fig_layout["nc"],
        "nr": fig_layout["nr"],
        "r_labels": data_dict["alphas"],
        "row_titles": [""],
        "x_lim": [0, 1],
        "y_lim": [0, 1],
    }

    format_axes(axes_args, image)

    file_name = os.path.basename(__file__).split(".")[0]
    save_file(fig, data_dict, file_name)

    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
