#!/usr/bin/env python

""" Plots results. """

import os
import time

from modules.fix_positions import create_divider
from modules.get_setting import get_titles
from modules.init_fig import init_fig
from modules.prettify_axes import prettify_axes
from modules.prettify_fig import get_distances, prettify_fig
from modules.save_file import save_file
from modules.save_image import close_plt

from modules_results.get_sm import get_sm
from modules_results.get_static_data import get_lims, get_static_data
from modules_results.get_update_args import get_update_args, get_rows, get_columns
from modules_results.init_artists import (
    init_artists_imshow,
    init_artists_line2d,
)
from modules_results.parse_args import parse_args
from modules_results.trait_sets_config import all_traits
from modules_results.update_artists import update_artists


def main(args):
    """Main function"""

    start_time = time.perf_counter()
    file_name = os.path.basename(__file__).split(".")[0]

    update_args = {
        "alphas": None,
        "artists": None,
        "columns": get_columns(args.single_trait, args.trait_set, args.single_folder),
        "curve": args.curve,
        "df_none": None,
        "df_social": None,
        "dfs": None,
        "file_name": file_name,
        "frames": None,
        "histogram": args.histogram,
        "logess": None,
        "movie": args.movie,
        "rows": get_rows(args.single_trait, args.trait_set, args.single_folder),
        "single_folder": args.single_folder,
        "single_trait": args.single_trait,
        "text": "",
        "trait_set": args.trait_set,
        "update_function": update_artists,
    }

    update_args = get_update_args(update_args, args.clean)

    fig_layout = {
        "nc": 1,
        "ncols": len(update_args["columns"]),
        "nr": 1,
        "nrows": len(update_args["rows"]),
    }

    if args.curve or args.histogram:
        fig_layout["nc"] = len(update_args["logess"])
        fig_layout["nr"] = len(update_args["alphas"])

    fig, axs = init_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"])
    prettify_fig(fig, fig_distances, update_args["file_name"], get_sm())
    update_args["text"] = fig.texts[2]
    if args.curve or args.histogram:
        update_args["artists"] = init_artists_line2d(axs, *get_static_data(update_args))
    else:
        update_args["artists"] = init_artists_imshow(
            axs, len(update_args["alphas"]), len(update_args["logess"])
        )

    axes_args = {
        "axs": axs,
        "column_titles": get_titles(update_args["columns"]),
        "divider": create_divider(fig, fig_layout, fig_distances),
        "row_titles": get_titles(update_args["rows"]),
        "x_lim": [None, None],
        "c_values": update_args["logess"],
        "y_lim": [None, None],
        "r_values": update_args["alphas"],
    }

    if args.curve or args.histogram:
        axes_args["x_lim"], axes_args["y_lim"] = get_lims(args.curve)

    prettify_axes(axes_args)

    if args.curve:
        file_name += "_curve"
    if args.histogram:
        file_name += "_histogram"

    if args.trait_set == "all_traits":
        for trait in all_traits:
            update_args["trait_set"] = trait
            update_args["file_name"] = f"{file_name}_{trait}"
            save_file(fig, update_args)
    else:
        update_args["file_name"] = f"{file_name}_{args.trait_set}"
        save_file(fig, update_args)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
