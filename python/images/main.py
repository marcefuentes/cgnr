#!/usr/bin/env python

""" Plots. """

from time import perf_counter
from importlib import import_module

from modules.add_data import add_data
from modules.add_distances import add_distances
from modules.axes_format import axes_format
from modules.axes_letters import axes_letters
from modules.axes_place import axes_place
from modules.axes_ticks import axes_ticks
from modules.fig_colorbar import fig_colorbar
from modules.fig_format import fig_format
from modules.get_fig import get_fig
from modules.parse_args import parse_args
from modules.save_file import save_file


def main(data, image):
    """Main function"""

    start_time = perf_counter()

    mm = data["modules"]
    import_module(f"{mm}.add_simulation_data").add_simulation_data(data)
    add_data(data, image)
    import_module(f"{mm}.add_static_data").add_static_data(data, image)

    image["fig"], image["axs"] = get_fig(image["fig_layout"])
    add_distances(image)
    fig_format(image)
    fig_colorbar(image, import_module(f"{mm}.get_sm").get_sm(image["color_map"]))

    import_module(f"{mm}.add_artists").add_artists(data, image)

    axes_place(image)
    axes_format(image)
    axes_ticks(data["ax_type"], image)
    import_module(f"{mm}.axes_adjust").axes_adjust(data, image)
    axes_letters(data["ax_type"], image["axs"], image["letters"])

    data["file_name"] = "output"
    data["function"] = import_module(f"{mm}.artists_update").artists_update
    data["text"] = image["fig"].texts[2]
    save_file(image["fig"], data)

    print(f"\nTime elapsed: {(perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    main(*parse_args())
