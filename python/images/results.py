#!/usr/bin/env python

""" Plots results. """

import os
import time

from modules.fix_positions import create_divider
from modules.create_fig import create_fig
from modules.format_axes import format_axes
from modules.format_fig import get_distances, format_fig
from modules.get_titles import get_titles
from modules.save_file import save_file
from modules.save_image import close_plt

from modules_results.get_data import get_data, get_rows, get_columns
from modules_results.get_sm import get_sm
import modules_results.get_static_fitness as static_fitness
import modules_results.get_static_hist as static_hist
from modules_results.init_artists import init_imshow, init_line2d
from modules_results.parse_args import parse_args
from modules_results.update_artists import update_artists

from settings_results.data_constants import data_constants
from settings_results.image import image
from settings_results.titles import titles


def main(config_data):
    """Main function"""

    start_time = time.perf_counter()

    config_data["rows"] = get_rows(config_data)
    config_data["columns"] = get_columns(config_data)

    dynamic_data = {
        "alphas": [],
        "df_none": [],
        "df_social": [],
        "dfs": [],
        "frames": [],
        "logess": [],
        "text": "",
    }

    dynamic_data = get_data(config_data, dynamic_data)
    mr = len(dynamic_data["alphas"])
    mc = len(dynamic_data["logess"])

    fig_layout = {
        "nc": 1,
        "ncols": len(config_data["columns"]),
        "nr": 1,
        "nrows": len(config_data["rows"]),
    }

    if config_data["fitness"] or config_data["histogram"]:
        fig_layout["nc"] = mc
        fig_layout["nr"] = mr

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image, get_sm(image["color_map"]))
    dynamic_data["text"] = fig.texts[2]

    update_args = {
        "artists": [],
        "file_name": os.path.basename(__file__).split(".")[0],
        "function": update_artists,
    }

    if config_data["fitness"]:
        update_args["artists"] = init_line2d(
            axs, *static_fitness.data(config_data, dynamic_data, data_constants)
        )
    elif config_data["histogram"]:
        update_args["artists"] = init_line2d(axs, *static_hist.data(mr, mc))
    else:
        update_args["artists"] = init_imshow(axs, mr, mc)

    axes_args = {
        "axs": axs,
        "c_labels": [
            dynamic_data["logess"][0],
            dynamic_data["logess"][mc // 2],
            dynamic_data["logess"][-1],
        ],
        "column_titles": get_titles(config_data["columns"], titles),
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "nc": mc,
        "nr": mr,
        "r_labels": [
            dynamic_data["alphas"][0],
            dynamic_data["alphas"][mr // 2],
            dynamic_data["alphas"][-1],
        ],
        "row_titles": get_titles(config_data["rows"], titles),
        "x_lim": [None, None],
        "y_lim": [None, None],
    }

    if config_data["fitness"]:
        axes_args["x_lim"], axes_args["y_lim"] = static_fitness.lims()
        update_args["file_name"] += "_fitness"
    elif config_data["histogram"]:
        axes_args["x_lim"], axes_args["y_lim"] = static_hist.lims()
        update_args["file_name"] += "_histogram"

    format_axes(axes_args, image)

    if config_data["trait_set"] == "all_traits":
        for trait in data_constants["all_traits"]:
            config_data["trait_set"] = trait
            update_args["file_name"] += f"_{trait}"
            save_file(fig, update_args, config_data, dynamic_data)
    else:
        update_args["file_name"] += f"_{config_data['trait_set']}"
        save_file(fig, update_args, config_data, dynamic_data)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(vars(parsed_args))
