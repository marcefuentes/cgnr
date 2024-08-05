#!/usr/bin/env python

""" Plots results. """

from time import perf_counter

from modules.add_distances import add_distances
from modules.add_divider import add_divider
from modules.axes_format import axes_format
from modules.axes_letters import axes_letters
from modules.axes_ticks import axes_ticks
from modules.fig_colorbar import fig_colorbar
from modules.fig_format import fig_format
from modules.get_fig import get_fig
from modules.save_file import save_file
from modules.save_image import close_plt

from resultsm.add_artists import add_artists
from resultsm.add_data import add_data
from resultsm.artists_update import artists_update
from resultsm.artists_theory import artists_theory
from resultsm.axes_adjust import axes_adjust
from resultsm.get_sm import get_sm
from resultsm.parse_args import parse_args


def main(data, image):
    """Main function"""

    start_time = perf_counter()

    add_data(data, image)

    image["fig"], image["axs"] = get_fig(image["fig_layout"])
    add_distances(image)
    fig_format(image)
    fig_colorbar(image, get_sm(image["color_map"]))

    add_artists(data, image)

    add_divider(image)
    axes_format(image)
    axes_ticks(data["ax_type"], image)
    axes_adjust(data, image)
    axes_letters(data["ax_type"], image["axs"], image["letters"])

    if data["layout"] == "theory":
        artists_theory(data)
    data["file_name"] = "output"
    data["function"] = artists_update
    data["text"] = image["fig"].texts[2]
    save_file(image["fig"], data)

    close_plt(image["fig"])

    print(f"\nTime elapsed: {(perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    main(*parse_args())
