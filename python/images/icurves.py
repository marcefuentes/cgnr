#!/usr/bin/env python

""" Plots indifference curves and budget lines, and fitness landscapes"""

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

from icurvesm.add_artists import add_artists
from icurvesm.add_data import add_data
from icurvesm.artists_update import artists_update
from icurvesm.get_sm import get_sm
from icurvesm.m01_reformat import m01_reformat
from icurvesm.parse_args import parse_args


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
    if data["layout"] == "m01":
        m01_reformat(image)
    else:
        axes_ticks(data["ax_type"], image)
    axes_letters(data["ax_type"], image["axs"], image["letters"])

    data["file_name"] = "output"
    data["function"] = artists_update
    data["text"] = image["fig"].texts[2]
    save_file(image["fig"], data)

    close_plt(image["fig"])

    print(f"\nTime elapsed: {(perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    main(*parse_args())
