#!/usr/bin/env python

""" Creates plots. """

import os
import time
import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get
from modules.init_fig import init_fig
from modules.save_image import save_image, close_plt
from modules.save_movie import save_movie
from modules.prettify_axes import prettify_axes_imshow, prettify_axes_plot

from modules_results.get_data import (
    get_data_single_trait,
    get_data_multitrait,
    get_rows_columns,
)
from modules_results.get_sm import get_sm
from modules_results.init_artists import init_imshow_artists, init_plot_artists
from modules_results.modes import all_traits
from modules_results.parse_args import parse_args
from modules_results.update import update_artists


def main(args):
    """Main function"""

    start_time = time.perf_counter()

    update_args = {
        "artists": None,
        "mode": args.mode,
        "mode_is_trait": args.mode_is_trait,
        "columns": None,
        "rows": None,
        "dfs": None,
        "df_none": None,
        "df_social": None,
        "dffrqs": None,
        "movie": args.movie,
        "nc": get_config("grid"),
        "nr": get_config("grid"),
        "text": "",
        "update_function": update_artists,
    }

    if args.mode_is_trait:
        (
            update_args["dfs"],
            update_args["df_none"],
            update_args["df_social"],
            update_args["dffrqs"],
            ts,
        ) = get_data_single_trait(args.mode, args.histogram, args.movie)
    else:
        (
            update_args["dfs"],
            update_args["df_none"],
            update_args["df_social"],
            update_args["dffrqs"],
            ts,
        ) = get_data_multitrait(args.mode, args.histogram, args.movie)

    file_name = os.path.basename(__file__).split(".")[0]

    axes_args = {
        "axs": None,
        "column_titles": [""],
        "divider": None,
        "file_name": file_name,
        "init_function": init_imshow_artists,
        "prettify_function": prettify_axes_imshow,
        "row_titles": [""],
        "x_lim": "None",
        "y_values": np.linspace(get_config("alpha_max"), get_config("alpha_min"), update_args["nr"]),
        "y_lim": "None",
        "x_values": np.linspace(get_config("loges_min"), get_config("loges_max"), update_args["nc"]),
    }

    if args.histogram:
        axes_args["init_function"] = init_plot_artists
        axes_args["prettify_function"] = prettify_axes_plot
        axes_args["x_lim"] = [-2, get(file_name, "bins") + 1]
        axes_args["y_lim"] = [0, 0.25]

    (
        update_args["rows"],
        axes_args["row_titles"],
        update_args["columns"],
        axes_args["column_titles"],
    ) = get_rows_columns(args.mode, args.mode_is_trait)

    fig_args = {
        "file_name": file_name,
        "nc": update_args["nc"],
        "ncols": len(update_args["columns"]),
        "nested": args.histogram,
        "nr": update_args["nr"],
        "nrows": len(update_args["rows"]),
        "sm": get_sm(),
    }

    fig, update_args = init_fig(fig_args, axes_args, update_args)

    if args.histogram:
        update_args["alphas"] = axes_args["y_values"]
        update_args["logess"] = axes_args["x_values"]
        file_name += "_histogram"

    if args.mode == "all_traits":
        for trait in all_traits:
            update_args["mode"] = trait
            save_image(ts[-1], update_args, f"{file_name}_{trait}")
    else:
        file_name += f"_{args.mode}"
        if args.movie:
            save_movie(fig, ts, update_args, file_name)
        else:
            save_image(ts[-1], update_args, file_name)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
