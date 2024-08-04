#!/usr/bin/env python

""" Plots results. """

from time import perf_counter

from modules.add_divider import add_divider
from modules.add_layout import add_layout
from modules.artists_format import artists_format
from modules.axes_format import axes_format
from modules.axes_letters import axes_letters
from modules.axes_ticks import axes_ticks
from modules.fig_colorbar import fig_colorbar
from modules.fig_format import add_distances, fig_format
from modules.get_fig import get_fig
from modules.save_file import save_file
from modules.save_image import close_plt

from resultsm.add_data import add_data
from resultsm.artists_update import artists_update
from resultsm.artists_theory import artists_theory
from resultsm.axes_adjust import axes_adjust
from resultsm.get_artists import get_artists
from resultsm.get_sm import get_sm
from resultsm.parse_args import parse_args

from resultss import layouts
from resultss.image import image


def main(data):
    """Main function"""

    start_time = perf_counter()

    add_layout(data, layouts)
    add_data(data)

    if data["layout"] == "curves":
        image["margin_top"] *= 0.5

    image["fig_layout"] = {
        "nc": (1 if data["ax_type"] == "AxesImage" else data["layout_m"]),
        "ncols": data["layout_j"],
        "nr": (1 if data["ax_type"] == "AxesImage" else data["layout_k"]),
        "nrows": data["layout_i"],
    }

    image["fig"], image["axs"] = get_fig(image["fig_layout"])
    add_distances(image)
    fig_format(image)
    fig_colorbar(image, get_sm(image["color_map"]))

    data["color_map"] = image["color_map"]
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

    data["artists"] = get_artists(data["ax_type"], image["axs"], data["x"], data["y"])
    add_divider(image)
    axes_format(image)
    axes_ticks(data["ax_type"], image)
    axes_adjust(data, image)
    axes_letters(data["ax_type"], image["axs"], image["letters"])
    artists_format(data["artists"], image[data["ax_type"]])

    if data["layout"] == "theory":
        artists_theory(data)

    save_file(image["fig"], data)
    close_plt(image["fig"])

    print(f"\nTime elapsed: {(perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
