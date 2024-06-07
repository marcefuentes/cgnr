#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

import os
import time

from matplotlib import colormaps
from modules.fix_positions import create_divider
from modules.create_fig import create_fig
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.format_lines import format_lines
from modules.save_file import save_file
from modules.save_image import close_plt

from modules_icurves.get_data import get_data
from modules_icurves.get_sm import get_sm
from modules_icurves.get_static_data import get_static_data
from modules_icurves.init_artists import init_artists_line2d
from modules_icurves.parse_args import parse_args
from modules_icurves.update_artists import update_artists
from settings_icurves.data_constants import data_constants
from settings_icurves.image import (
    image,
    image_budgets,
    image_icurves,
    image_icurves_grey,
    image_landscapes,
)


def main(options):
    """Main function"""

    start_time = time.perf_counter()

    dynamic_data = get_data(data_constants)

    fig_layout = {
        "nc": len(dynamic_data["logess"]),
        "ncols": 2,
        "nr": len(dynamic_data["alphas"]),
        "nrows": 1,
    }

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image, get_sm(image["color_map"]))
    dynamic_data["text"] = fig.texts[2]
    dynamic_data["x_values"], y, ic = get_static_data(
        dynamic_data["alphas"], dynamic_data["rhos"]
    )
    update_args = {
        "cmap": colormaps.get_cmap(image["color_map"]),
        "file_name": os.path.basename(__file__).split(".")[0],
        "function": update_artists,
    }

    (
        update_args["budgets"],
        update_args["icurves"],
        update_args["icurves_grey"],
        update_args["landscapes"],
    ) = init_artists_line2d(axs, dynamic_data["x_values"], y, ic)

    format_lines(update_args["budgets"], image_budgets)
    format_lines(update_args["icurves"], image_icurves)
    format_lines(update_args["icurves_grey"], image_icurves_grey)
    format_lines(update_args["landscapes"], image_landscapes)

    axes_args = {
        "axs": axs,
        "c_labels": dynamic_data["logess"],
        "column_titles": [""],
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "nc": fig_layout["nc"],
        "nr": fig_layout["nr"],
        "r_labels": dynamic_data["alphas"],
        "row_titles": [""],
        "x_lim": [0, 1],
        "y_lim": [0, 1],
    }

    format_axes(axes_args, image)

    save_file(fig, update_args, options, dynamic_data)

    # pylint: disable=duplicate-code
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
