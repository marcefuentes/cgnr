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


def main(args):
    """Main function"""

    start_time = time.perf_counter()

    data_dict = {
        "alphas": [],
        "artists": [],
        "columns": get_columns(args.single_trait, args.trait_set, args.single_folder),
        "fitness": args.fitness,
        "df_none": [],
        "df_social": [],
        "dfs": [],
        "frames": [],
        "histogram": args.histogram,
        "logess": [],
        "movie": args.movie,
        "rows": get_rows(args.single_trait, args.trait_set, args.single_folder),
        "single_folder": args.single_folder,
        "single_trait": args.single_trait,
        "text": "",
        "trait_set": args.trait_set,
        "update_function": update_artists,
    }

    data_dict = get_data(data_dict, args.clean)
    mr = len(data_dict["alphas"])
    mc = len(data_dict["logess"])

    fig_layout = {
        "nc": 1,
        "ncols": len(data_dict["columns"]),
        "nr": 1,
        "nrows": len(data_dict["rows"]),
    }

    if args.fitness or args.histogram:
        fig_layout["nc"] = mc
        fig_layout["nr"] = mr

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"], image)
    format_fig(fig, fig_distances, image, get_sm())
    data_dict["text"] = fig.texts[2]

    if args.fitness:
        data_dict["artists"] = init_line2d(axs, *static_fitness.data(data_dict))
    elif args.histogram:
        data_dict["artists"] = init_line2d(axs, *static_hist.data(mr, mc))
    else:
        data_dict["artists"] = init_imshow(axs, mr, mc)

    axes_args = {
        "axs": axs,
        "c_labels": [
            data_dict["logess"][0],
            data_dict["logess"][mc // 2],
            data_dict["logess"][-1],
        ],
        "column_titles": get_titles(data_dict["columns"], titles),
        "divider": create_divider(fig, fig_layout, fig_distances, image),
        "nc": mc,
        "nr": mr,
        "r_labels": [
            data_dict["alphas"][0],
            data_dict["alphas"][mr // 2],
            data_dict["alphas"][-1],
        ],
        "row_titles": get_titles(data_dict["rows"], titles),
        "x_lim": [None, None],
        "y_lim": [None, None],
    }

    file_name = os.path.basename(__file__).split(".")[0]
    if args.fitness:
        axes_args["x_lim"], axes_args["y_lim"] = static_fitness.lims()
        file_name += "_fitness"
    elif args.histogram:
        axes_args["x_lim"], axes_args["y_lim"] = static_hist.lims()
        file_name += "_histogram"

    format_axes(axes_args, image)

    if args.trait_set == "all_traits":
        for trait in data_constants["all_traits"]:
            data_dict["trait_set"] = trait
            file_name += f"_{trait}"
            save_file(fig, data_dict, file_name)
    else:
        file_name += f"_{args.trait_set}"
        save_file(fig, data_dict, file_name)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
