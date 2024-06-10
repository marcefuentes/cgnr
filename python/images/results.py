#!/usr/bin/env python

""" Plots results. """

import os
import time

import numpy as np
from matplotlib import colormaps

from modules.fix_positions import create_divider
from modules.create_fig import create_fig
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.format_artists import format_artists
from modules.save_file import save_file
from modules.save_image import close_plt

from modules_results.get_dynamic_data import get_dynamic_data
from modules_results.get_layout import get_layout
from modules_results.get_sm import get_sm
from modules_results.get_curves import get_curves
from modules_results.init_artists import init_imshow, init_line2d
from modules_results.parse_args import parse_args
from modules_results.update_artists import update_artists

from settings_project.project import project
from settings_results.image import image, image_lines, image_show


def main(options):
    """Main function"""

    start_time = time.perf_counter()

    data_layout = get_layout(options)
    try:
        dynamic_data = get_dynamic_data(
            data_layout,
            options,
            *project["output_file_extensions"],
        )
    except ValueError as error:
        print(error)
        return

    mr = len(dynamic_data["alphas"])
    mc = len(dynamic_data["logess"])

    fig_layout = {
        "nc": 1,
        "ncols": len(data_layout["variants"][0]),
        "nr": 1,
        "nrows": len(data_layout["variants"]),
    }

    if options["figure"] == "curves" or options["histogram"]:
        fig_layout["nc"] = mc
        fig_layout["nr"] = mr

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image, get_sm(image["color_map"]))
    dynamic_data["text"] = fig.texts[2]

    update_args = {
        "cmap": colormaps.get_cmap(image["color_map"]),
        "file_name": os.path.basename(__file__).split(".")[0],
        "function": update_artists,
    }

    if options["figure"] == "curves":
        x, y = get_curves(
            image["n_x_values"],
            data_layout["traits"],
            data_layout["givens"],
            dynamic_data["alphas"],
            dynamic_data["rhos"],
        )
    elif options["histogram"]:
        x = np.arange(project["bins"])
        y = np.zeros(
            (
                fig_layout["nrows"],
                fig_layout["ncols"],
                mr,
                mc,
                project["bins"],
            )
        )

    if options["figure"] == "curves" or options["histogram"]:
        update_args["artists"] = init_line2d(axs, x, y)
        format_artists(update_args["artists"], image_lines)
    else:
        update_args["artists"] = init_imshow(axs, mr, mc)
        format_artists(update_args["artists"], image_show)

    axes_args = {
        "axs": axs,
        "c_labels": [
            dynamic_data["logess"][0],
            dynamic_data["logess"][mc // 2],
            dynamic_data["logess"][-1],
        ],
        "column_titles": data_layout["column_titles"],
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "nc": mc,
        "nr": mr,
        "r_labels": [
            dynamic_data["alphas"][0],
            dynamic_data["alphas"][mr // 2],
            dynamic_data["alphas"][-1],
        ],
        "row_titles": data_layout["row_titles"],
        "x_lim": [None, None],
        "y_lim": [None, None],
    }

    if options["figure"] == "curves":
        axes_args["x_lim"] = [0, 1]
        axes_args["y_lim"] = [0, 1]
        update_args["file_name"] += "_curves"
    elif options["histogram"]:
        axes_args["x_lim"] = [-2, project["bins"] + 1]
        axes_args["y_lim"] = [0, 0.25]
        update_args["file_name"] += "_histogram"

    format_axes(axes_args, image)

    update_args["file_name"] += f"_{options['trait']}"
    save_file(fig, update_args, options, dynamic_data)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
