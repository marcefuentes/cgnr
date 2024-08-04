#!/usr/bin/env python

""" Plots results. """

import time

from matplotlib import colormaps

from modules.artists_format import artists_format
from modules.axes_format import axes_format
from modules.axes_letters import axes_letters
from modules.axes_ticks import axes_ticks
from modules.fig_colorbar import fig_colorbar
from modules.fig_create import fig_create
from modules.fig_format import get_distances, fig_format
from modules.get_divider import get_divider
from modules.get_layout import get_layout
from modules.save_file import save_file
from modules.save_image import close_plt

from resultsm.artists_init import artists_init
from resultsm.artists_update import artists_update
from resultsm.axes_adjust import axes_adjust
from resultsm.get_data import get_data
from resultsm.get_sm import get_sm
from resultsm.parse_args import parse_args

from resultss import layouts
from resultss.image import image


def main(data):
    """Main function"""

    start_time = time.perf_counter()

    get_layout(data, layouts)
    get_data(data)

    if data["layout"] == "curves":
        image["margin_top"] *= 0.5

    image["fig_layout"] = {
        "nc": (1 if data["ax_type"] == "AxesImage" else data["layout_m"]),
        "ncols": data["layout_j"],
        "nr": (1 if data["ax_type"] == "AxesImage" else data["layout_k"]),
        "nrows": data["layout_i"],
    }

    image["fig"], image["axs"] = fig_create(image["fig_layout"])
    get_distances(image)
    fig_format(image)
    fig_colorbar(image, get_sm(image["color_map"]))

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

    if data["layout"] == "curves":
        image["lim_x"] = [0, 1]
        image["lim_y"] = [0, 1]
    elif data["histogram"]:
        image["lim_x"] = [-2, len(data["x"]) + 1]
        image["lim_y"] = [0, 0.25]
    else:
        image["lim_x"] = [None, None]
        image["lim_y"] = [None, None]

    data["artists"] = artists_init(data["ax_type"], image["axs"], data["x"], data["y"])
    get_divider(image)
    axes_format(image)
    axes_ticks(data["ax_type"], image)
    axes_adjust(data, image)
    axes_letters(data["ax_type"], image["axs"], image["letters"])
    artists_format(data["artists"], image[data["ax_type"]])

    save_file(image["fig"], data)
    close_plt(image["fig"])

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
