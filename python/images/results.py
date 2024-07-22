#!/usr/bin/env python

""" Plots results. """

import time

from matplotlib import colormaps

from modules.add_colorbar import add_colorbar
from modules.add_letters import add_letters_axesimage, add_letters_line2d
from modules.add_ticks import ticks_axesimage, ticks_line2d
from modules.create_fig import create_fig
from modules.create_divider import create_divider
from modules.format_artists import format_artists
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.get_layout import get_layout
from modules.save_file import save_file
from modules.save_image import close_plt

from resultsm.adjust import adjust
from resultsm.get_data import get_data
from resultsm.get_sm import get_sm
from resultsm.init_artists import init_artists
from resultsm.parse_args import parse_args
from resultsm.update_artists import update_artists

from resultss import layouts
from resultss.image import image


def main(data):
    """Main function"""

    start_time = time.perf_counter()

    get_layout(data, layouts)
    get_data(data)

    mr = len(data["alphas"])
    mc = len(data["rhos"])

    if data["layout"] == "curves":
        image["margin_top"] *= 0.5

    fig_layout = {
        "nc": mc if data["ax_type"] == "Line2D" else 1,
        "ncols": len(data["variants"][0]),
        "nr": mr if data["ax_type"] == "Line2D" else 1,
        "nrows": len(data["variants"]),
    }

    image["fig"], image["axs"] = create_fig(fig_layout)
    get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(image)
    add_colorbar(image, get_sm(image["color_map"]))
    create_divider(fig_layout, image)

    data["text"] = image["fig"].texts[2]
    data["cmap"] = colormaps.get_cmap(image["color_map"])
    data["file_name"] = "output"
    data["function"] = update_artists

    image["letter_position"] = (0.0, 1.0 + image["padding_letter"] * fig_layout["nr"])
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

    data["artists"] = init_artists(image["axs"], data["x"], data["y"], data["ax_type"])
    format_axes(image)
    if data["ax_type"] == "Line2D":
        format_artists(data["artists"], image["lines2d"])
        ticks_line2d(image)
        add_letters_line2d(image["axs"], image["letter_position"], image["letters"])
    else:
        format_artists(data["artists"], image["axesimage"])
        ticks_axesimage(image)
        adjust(data, image)
        add_letters_axesimage(image["axs"], image["letter_position"], image["letters"])

    save_file(image["fig"], data)
    close_plt(image["fig"])

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
