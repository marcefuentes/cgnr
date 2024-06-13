#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

import os
import time

from matplotlib import colormaps
from modules.fix_positions import create_divider
from modules.create_fig import create_fig
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.format_artists import format_artists
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
from icurvess.image import image


def main(options):
    """Main function"""

    start_time = time.perf_counter()

    layout = get_layout(options, layouts)
    data = get_data(options, layout)

    fig_layout = {
        "nc": len(data["logess"]),
        "ncols": 2,
        "nr": len(data["alphas"]),
        "nrows": len(data["givens"]),
    }

    fig, axs = create_fig(fig_layout)

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

    format_artists(update_args["budgets"], image["budgets"])
    format_artists(update_args["icurves"], image["icurves"])
    format_artists(update_args["icurves_grey"], image["icurves_grey"])
    format_artists(update_args["landscapes"], image["landscapes"])

    axes_args = {
        "axs": axs,
        "c_labels": [
            data["logess"][0],
            data["logess"][fig_layout["nc"] // 2],
            data["logess"][-1],
        ],
        "column_titles": [""] * fig_layout["ncols"],
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "nc": fig_layout["nc"],
        "nr": fig_layout["nr"],
        "r_labels": [
            data["alphas"][0],
            data["alphas"][fig_layout["nr"] // 2],
            data["alphas"][-1],
        ],
        "row_titles": [""] * fig_layout["nrows"],
        "x_lim": [0, 1],
        "y_lim": [0, 1],
    }

    format_axes(axes_args, image)

    update_args["file_name"] += f"_{options["layout"]}"
    save_file(fig, update_args, options, data)

    # pylint: disable=duplicate-code
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
