#!/usr/bin/env python

""" Plots results. """

import os
import time

import numpy as np
from matplotlib import colormaps

from modules.create_fig import create_fig
from modules.fix_positions import create_divider
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.format_artists import format_artists
from modules.get_layout import get_layout
from modules.save_file import save_file
from modules.save_image import close_plt

from resultsm.get_data import get_data
from resultsm.get_sm import get_sm
from resultsm.get_static_data import get_static_data
from resultsm.get_theory_imshow import get_theory_imshow
from resultsm.init_artists import init_artists
from resultsm.parse_args import parse_args
from resultsm.update_artists import update_artists

from settings.project import project
from resultss import layouts
from resultss.image import image


def main(options):
    """Main function"""

    start_time = time.perf_counter()

    layout = get_layout(options, layouts)
    try:
        data = get_data(
            options,
            layout,
            *project["output_file_extensions"],
        )
    except ValueError as error:
        print(error)
        return

    mr = len(data["alphas"])
    mc = len(data["logess"])

    fig_layout = {
        "nc": 1,
        "ncols": len(layout["variants"][0]),
        "nr": 1,
        "nrows": len(layout["variants"]),
    }

    if options["layout"] == "curves" or options["histogram"]:
        fig_layout["nc"] = mc
        fig_layout["nr"] = mr

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image, get_sm(image["color_map"]))
    data["text"] = fig.texts[2]

    update_args = {
        "cmap": colormaps.get_cmap(image["color_map"]),
        "file_name": os.path.basename(__file__).split(".")[0],
        "function": update_artists,
    }

    if options["layout"] == "curves":
        x, y = get_static_data(
            image["n_x_values"],
            layout["traits"],
            layout["givens"],
            data["alphas"],
            data["rhos"],
        )
    elif options["histogram"]:
        x = np.arange(project["bins"])
        y = np.zeros(
            (fig_layout["nrows"], fig_layout["ncols"], mr, mc, project["bins"])
        )
    elif options["layout"] == "theory":
        x, y = get_theory_imshow(
            layout["traits"], layout["givens"], data["alphas"], data["rhos"]
        )
    else:
        x = None
        y = np.zeros((fig_layout["nrows"], fig_layout["ncols"], 1, 1, mr, mc))

    update_args["artists"] = init_artists(axs, x, y)

    if options["layout"] == "curves" or options["histogram"]:
        format_artists(update_args["artists"], image["lines"])
    else:
        format_artists(update_args["artists"], image["show"])

    axes_args = {
        "axs": axs,
        "c_labels": [
            data["logess"][0],
            data["logess"][mc // 2],
            data["logess"][-1],
        ],
        "column_titles": layout["column_titles"],
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "nc": mc,
        "nr": mr,
        "r_labels": [
            data["alphas"][0],
            data["alphas"][mr // 2],
            data["alphas"][-1],
        ],
        "row_titles": layout["row_titles"],
        "x_lim": [None, None],
        "y_lim": [None, None],
    }

    if options["layout"] == "curves":
        axes_args["x_lim"] = [0, 1]
        axes_args["y_lim"] = [0, 1]
    if options["histogram"]:
        axes_args["x_lim"] = [-2, project["bins"] + 1]
        axes_args["y_lim"] = [0, 0.25]
        update_args["file_name"] += "_histogram"

    format_axes(axes_args, image)

    update_args["file_name"] += f"_{options['layout']}_{options['trait']}"
    save_file(fig, update_args, options, data)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
