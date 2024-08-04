#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

import time

from matplotlib import colormaps

from modules.artists_format import artists_format
from modules.axes_format import axes_format
from modules.axes_letters import axes_letters
from modules.axes_ticks import axes_ticks
from modules.create_divider import create_divider
from modules.fig_colorbar import fig_colorbar
from modules.fig_create import fig_create
from modules.fig_format import get_distances, fig_format
from modules.get_layout import get_layout
from modules.save_file import save_file
from modules.save_image import close_plt

from icurvesm.artists_init import artists_init
from icurvesm.artists_update import artists_update
from icurvesm.get_data import get_data
from icurvesm.get_sm import get_sm
from icurvesm.m01_reformat import m01_reformat
from icurvesm.parse_args import parse_args

from icurvess import layouts
from icurvess.image import image_common, image_unit


def main(data):
    """Main function"""

    start_time = time.perf_counter()

    get_layout(data, layouts)
    get_data(data)

    image = image_unit if data["layout"] == "m01" else image_common

    image["fig_layout"] = {
        "nc": data["layout_m"],
        "ncols": 2,
        "nr": data["layout_k"],
        "nrows": len(data["givens"]),
    }

    image["fig"], image["axs"] = fig_create(image["fig_layout"])
    get_distances(image)
    fig_format(image)
    fig_colorbar(image, get_sm(image["color_map"]))
    create_divider(image)

    data["cmap"] = colormaps.get_cmap(image["color_map"])
    data["file_name"] = "output"
    data["function"] = artists_update
    data["text"] = image["fig"].texts[2]

    image["letters"]["x"] = 0.0
    image["letters"]["y"] = 1.0 + image["padding_letter"] * image["fig_layout"]["nr"]
    image["nc"] = data["layout_m"]
    image["nr"] = data["layout_k"]
    image["ticklabels_x"] = data["ticklabels_x"]
    image["ticklabels_y"] = data["ticklabels_y"]
    image["titles_columns"] = data["titles_columns"]
    image["titles_rows"] = data["titles_rows"]

    image["lim_x"] = [0, 1]
    image["lim_y"] = [0, 1]

    (
        data["budgets"],
        data["icurves"],
        data["icurves_grey"],
        data["landscapes"],
    ) = artists_init(image["axs"], data["x_values"], data["y"], data["ic"])

    axes_format(image)
    if data["layout"] == "m01":
        m01_reformat(image)
    else:
        axes_ticks("Line2D", image)
    axes_letters("Line2D", image["axs"], image["letters"])

    for artist in ["budgets", "icurves", "icurves_grey", "landscapes"]:
        image[artist]["linewidth"] /= pow(image["fig_layout"]["nr"], 0.5)
        artists_format(data[artist], image[artist])

    save_file(image["fig"], data)
    close_plt(image["fig"])

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
