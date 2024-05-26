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

from modules_results.get_sm import get_sm
import modules_results.get_static_fitness as static_fitness
import modules_results.get_static_hist as static_hist
from modules_results.get_update_args import get_update_args, get_rows, get_columns
from modules_results.init_artists import (
    init_imshow,
    init_line2d,
)
from modules_results.parse_args import parse_args
from modules_results.settings import SETTINGS as settings
from modules_results.update_artists import update_artists


def main(args):
    """Main function"""

    start_time = time.perf_counter()

    update_args = {
        "alphas": [],
        "artists": [],
        "columns": get_columns(args.single_trait, args.trait_set, args.single_folder),
        "fitness": args.fitness,
        "df_none": [],
        "df_social": [],
        "dfs": [],
        "file_name": os.path.basename(__file__).split(".")[0],
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

    update_args = get_update_args(update_args, args.clean)

    fig_layout = {
        "nc": 1,
        "ncols": len(update_args["columns"]),
        "nr": 1,
        "nrows": len(update_args["rows"]),
    }

    if args.fitness or args.histogram:
        fig_layout["nc"] = len(update_args["logess"])
        fig_layout["nr"] = len(update_args["alphas"])

    fig, axs = create_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"])
    format_fig(fig, fig_distances, settings, get_sm())
    update_args["text"] = fig.texts[2]

    if args.fitness:
        update_args["artists"] = init_line2d(axs, *static_fitness.data(update_args))
    elif args.histogram:
        update_args["artists"] = init_line2d(axs, *static_hist.data(update_args))
    else:
        update_args["artists"] = init_imshow(
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

    if args.fitness:
        axes_args["x_lim"], axes_args["y_lim"] = static_fitness.lims()
        update_args["file_name"] += "_fitness"
    elif args.histogram:
        axes_args["x_lim"], axes_args["y_lim"] = static_hist.lims()
        update_args["file_name"] += "_histogram"

    format_axes(axes_args)

    if args.trait_set == "all_traits":
        for trait in settings["all_traits"]:
            update_args["trait_set"] = trait
            update_args["file_name"] += f"_{trait}"
            save_file(fig, update_args)
    else:
        update_args["file_name"] += f"_{args.trait_set}"
        save_file(fig, update_args)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
