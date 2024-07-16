#!/usr/bin/env python

""" Plots results. """

import os
import time

import numpy as np
from matplotlib import colormaps

from modules.add_colorbar import add_colorbar
from modules.add_letters import add_letters_imshow, add_letters_line2d
from modules.add_ticks import ticks_imshow, ticks_line2d
from modules.create_fig import create_fig
from modules.fix_positions import create_divider
from modules.format_artists import format_artists
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.get_layout import get_layout
from modules.save_file import save_file
from modules.save_image import close_plt

from resultsm.adjust import adjust
from resultsm.get_data import get_data
from resultsm.get_sm import get_sm
from resultsm.get_static_data import get_static_data
from resultsm.get_theory_imshow import get_theory_imshow
from resultsm.init_artists import init_artists
from resultsm.parse_args import parse_args
from resultsm.update_artists import update_artists

from resultss import layouts
from resultss.image import image
from settings.project import project


def main(options):
    """Main function"""

    start_time = time.perf_counter()

    options = get_layout(options, layouts)
    try:
        data = get_data(
            options,
            *project["output_file_extensions"],
        )
    except ValueError as error:
        print(error)
        return

    mr = len(data["alphas"])
    mc = len(data["rhos"])

    fig_layout = {
        "nc": 1,
        "ncols": len(options["variants"][0]),
        "nr": 1,
        "nrows": len(options["variants"]),
    }

    if options["layout"] == "curves" or options["histogram"]:
        fig_layout["nc"] = mc
        fig_layout["nr"] = mr

    fig, axs = create_fig(fig_layout)

    if options["layout"] == "curves":
        image["margin_top"] *= 0.5
    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image)
    add_colorbar(fig, fig_distances, image, get_sm(image["color_map"]))
    data["text"] = fig.texts[2]

    if options["layout"] == "curves":
        x, y = get_static_data(
            image["n_x_values"],
            options["traits"],
            options["givens"],
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
            options["traits"], options["givens"], data["alphas"], data["rhos"]
        )
    else:
        x = None
        y = np.zeros((fig_layout["nrows"], fig_layout["ncols"], 1, 1, mr, mc))

    data["artists"] = init_artists(axs, x, y, options["ax_type"])
    data["cmap"] = colormaps.get_cmap(image["color_map"])
    data["file_name"] = os.path.basename(__file__).split(".")[0]
    data["function"] = update_artists

    axes_args = {
        "axs": axs,
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "lim_x": [None, None],
        "lim_y": [None, None],
        "nc": mc,
        "nr": mr,
        "ticklabels_x": [
            f"{data["rhos"][0]:.0f}",
            f"{data["rhos"][mc // 2]:.0f}",
            f"{data["rhos"][-1]:.2f}",
        ],
        "ticklabels_y": [
            f"{data["alphas"][0]:.1f}",
            f"{data["alphas"][mr // 2]:.1f}",
            f"{data["alphas"][-1]:.1f}",
        ],
        "titles_columns": options["titles_columns"],
        "titles_rows": options["titles_rows"],
    }

    if options["layout"] == "curves":
        axes_args["lim_x"] = [0, 1]
        axes_args["lim_y"] = [0, 1]
    if options["histogram"]:
        axes_args["lim_x"] = [-2, project["bins"] + 1]
        axes_args["lim_y"] = [0, 0.25]

    format_axes(axes_args, image)
    if options["layout"] == "curves" or options["histogram"]:
        format_artists(data["artists"], image["lines"])
        ticks_line2d(axes_args, image["ticks"])
    else:
        format_artists(data["artists"], image["show"])
        ticks_imshow(axes_args, image["ticks"])

    adjust(
        axs,
        options,
        fig_distances,
        image,
        axes_args["ticklabels_x"],
        axes_args["ticklabels_y"],
    )

    if options["layout"] == "curves" or options["histogram"]:
        add_letters_line2d(
            axs,
            (0, 1.0 + image["padding_letter"] * fig_layout["nr"]),
            image["letters"],
        )
    else:
        add_letters_imshow(
            axs,
            (0, 1.0 + image["padding_letter"] * fig_layout["nr"]),
            image["letters"],
        )
    save_file(fig, data, options)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
