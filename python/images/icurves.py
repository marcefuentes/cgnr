#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

import os
import time

from matplotlib import colormaps

from modules.add_ax_titles import add_ax_titles
from modules.create_fig import create_fig
from modules.fix_positions import create_divider
from modules.format_artists import format_artists
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.add_ticks import ticks_ax_line2d, ticks_line2d
from modules.get_layout import get_layout
from modules.save_file import save_file
from modules.save_image import close_plt

from icurvesm.get_data import get_data
from icurvesm.get_sm import get_sm
from icurvesm.get_static_data import get_static_data
from icurvesm.init_artists import init_artists
from icurvesm.parse_args import parse_args
from icurvesm.update_artists import update_artists

from icurvess import layouts
from icurvess.image import image_common, image_unit


def main(options):
    """Main function"""

    start_time = time.perf_counter()

    layout = get_layout(options, layouts)
    data = get_data(options, layout)

    options["budget_line"] = layout["budget_line"]

    fig_layout = {
        "nc": len(data["logess"]),
        "ncols": 2,
        "nr": len(data["alphas"]),
        "nrows": len(data["givens"]),
    }

    fig, axs = create_fig(fig_layout)

    if options["layout"] == "unit":
        image = image_unit
    else:
        image = image_common
    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image, get_sm(image["color_map"]))
    data["text"] = fig.texts[2]
    data["x_values"], y, ic = get_static_data(image["n_x_values"], data)
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
    ) = init_artists(axs, data["x_values"], y, ic)

    axes_args = {
        "axs": axs,
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "lim_x": [0, 1],
        "lim_y": [0, 1],
        "nc": fig_layout["nc"],
        "nr": fig_layout["nr"],
        "ticklabels_x": [
            data["logess"][0],
            data["logess"][fig_layout["nc"] // 2],
            data["logess"][-1],
        ],
        "ticklabels_y": [
            data["alphas"][0],
            data["alphas"][fig_layout["nr"] // 2],
            data["alphas"][-1],
        ],
        "titles_columns": [""] * fig_layout["ncols"],
        "titles_rows": [""] * fig_layout["nrows"],
    }

    format_axes(axes_args, image)
    if options["layout"] == "unit":
        add_ax_titles(
            axs[0, 0, 0, 0],
            image["title_x_0"],
            image["title_y_0"],
            image["titles_columns"]["fontsize"],
            image["labelpad"],
        )
        add_ax_titles(
            axs[0, 1, 0, 0],
            image["title_x_1"],
            image["title_y_1"],
            image["titles_columns"]["fontsize"],
            image["labelpad"],
        )
        axes_args["ticklabels_x"] = [0.0, 0.5, 1.0]
        axes_args["ticklabels_y"] = [0.0, 0.5, 1.0]
        ticks_ax_line2d(axs[0, 0, 0, 0], axes_args, image["ticks"])
        ticks_ax_line2d(axs[0, 1, 0, 0], axes_args, image["ticks"])
    else:
        ticks_line2d(axes_args, image["ticks"])

    for artist in ["budgets", "icurves", "icurves_grey", "landscapes"]:
        image[artist]["linewidth"] /= pow(fig_layout["nr"], 0.5)
        format_artists(update_args[artist], image[artist])

    update_args["file_name"] += f"_{options['layout']}"
    save_file(fig, update_args, options, data)

    # pylint: disable=duplicate-code
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
