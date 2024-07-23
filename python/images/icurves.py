#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

import time

from matplotlib import colormaps

from modules.add_ax_labels import add_ax_labels
from modules.add_colorbar import add_colorbar
from modules.add_letters import add_letters_line2d
from modules.add_ticks import ticks_ax_line2d, ticks_line2d
from modules.create_fig import create_fig
from modules.create_divider import create_divider
from modules.format_artists import format_artists
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.get_layout import get_layout
from modules.save_file import save_file
from modules.save_image import close_plt

from icurvesm.get_data import get_data
from icurvesm.get_sm import get_sm
from icurvesm.init_artists import init_artists
from icurvesm.parse_args import parse_args
from icurvesm.update_artists import update_artists

from icurvess import layouts
from icurvess.image import image_common, image_unit


def main(data):
    """Main function"""

    start_time = time.perf_counter()

    get_layout(data, layouts)
    get_data(data)

    mr = len(data["alphas"])
    mc = len(data["rhos"])

    if data["layout"] == "m01":
        image = image_unit
    else:
        image = image_common

    image["fig_layout"] = {
        "nc": mc,
        "ncols": 2,
        "nr": mr,
        "nrows": len(data["givens"]),
    }

    image["fig"], image["axs"] = create_fig(image["fig_layout"])
    get_distances(image)
    format_fig(image)
    add_colorbar(image, get_sm(image["color_map"]))
    create_divider(image)

    data["text"] = image["fig"].texts[2]
    data["cmap"] = colormaps.get_cmap(image["color_map"])
    data["file_name"] = "output"
    data["function"] = update_artists

    image["letter_position"] = (0.0, 1.0 + image["padding_letter"] * image["fig_layout"]["nr"])
    image["nc"] = mc
    image["nr"] = mr
    image["ticklabels_x"] = [
        f"{data["rhos"][0]:.0f}",
        f"{data["rhos"][mc // 2]:.0f}",
        f"{data["rhos"][-1]:.2f}",
    ]
    image["ticklabels_y"] = [
        f"{data["alphas"][0]:.1f}",
        f"{data["alphas"][mr // 2]:.1f}",
        f"{data["alphas"][-1]:.1f}",
    ]
    image["titles_columns"] = [""] * image["fig_layout"]["ncols"]
    image["titles_rows"] = [""] * image["fig_layout"]["nrows"]
    image["lim_x"] = [0, 1]
    image["lim_y"] = [0, 1]

    (
        data["budgets"],
        data["icurves"],
        data["icurves_grey"],
        data["landscapes"],
    ) = init_artists(image["axs"], data["x_values"], data["y"], data["ic"])

    format_axes(image)
    if data["layout"] == "m01":
        add_ax_labels(
            image["axs"][0, 0, 0, 0],
            image["label_x_0"],
            image["label_y_0"],
            image["titles_columns_params"]["fontsize"],
            image["labelpad"],
        )
        add_ax_labels(
            image["axs"][0, 1, 0, 0],
            image["label_x_1"],
            image["label_y_1"],
            image["titles_columns_params"]["fontsize"],
            image["labelpad"],
        )
        image["ticklabels_x"] = [0.0, 0.5, 1.0]
        image["ticklabels_y"] = [0.0, 0.5, 1.0]
        ticks_ax_line2d(
            image["axs"][0, 0, 0, 0],
            image["ticklabels_y"],
            image["ticklabels_x"],
            image["ticks"],
        )
        ticks_ax_line2d(
            image["axs"][0, 1, 0, 0],
            image["ticklabels_y"],
            image["ticklabels_x"],
            image["ticks"],
        )
    else:
        ticks_line2d(image)
    add_letters_line2d(image["axs"], image["letter_position"], image["letters"])

    for artist in ["budgets", "icurves", "icurves_grey", "landscapes"]:
        image[artist]["linewidth"] /= pow(image["fig_layout"]["nr"], 0.5)
        format_artists(data[artist], image[artist])

    save_file(image["fig"], data)
    close_plt(image["fig"])

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
