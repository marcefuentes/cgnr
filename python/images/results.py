#!/usr/bin/env python

""" Creates plots. """

import os
import time
import numpy as np

from common_modules.get_config import get_config
from modules.fix_positions import create_divider
from modules.get_setting import get_titles
from modules.init_fig import init_fig
from modules.save_image import save_image, close_plt
from modules.save_movie import save_movie
from modules.prettify_axes import prettify_axes
from modules.prettify_fig import get_distances, prettify_fig

from modules_results.get_data import (
    get_data_single_trait,
    get_data_multitrait,
    get_rows_columns,
)
from modules_results.get_sm import get_sm
from modules_results.init_artists import init_artists_imshow, init_artists_plot
from modules_results.modes import all_traits
from modules_results.parse_args import parse_args
from modules_results.update import update_artists


def main(args):
    """Main function"""

    start_time = time.perf_counter()
    file_name = os.path.basename(__file__).split(".")[0]

    update_args = {
        "alphas": None,
        "artists": None,
        "columns": None,
        "df_none": None,
        "df_social": None,
        "dffrqs": None,
        "dfs": None,
        "logess": None,
        "mode": args.mode,
        "mode_is_trait": args.mode_is_trait,
        "movie": args.movie,
        "rows": None,
        "text": "",
        "update_function": update_artists,
    }

    if args.mode_is_trait:
        (
            update_args["dfs"],
            update_args["df_none"],
            update_args["df_social"],
            update_args["dffrqs"],
            df,
        ) = get_data_single_trait(args.mode, args.histogram, args.movie, args.clean)
    else:
        (
            update_args["dfs"],
            update_args["df_none"],
            update_args["df_social"],
            update_args["dffrqs"],
            df,
        ) = get_data_multitrait(args.mode, args.histogram, args.movie, args.clean)

    (
        update_args["rows"],
        update_args["columns"],
    ) = get_rows_columns(args.mode, args.mode_is_trait)

    fig_layout = {
        "nc": 1,
        "ncols": len(update_args["columns"]),
        "nr": 1,
        "nrows": len(update_args["rows"]),
    }

    if args.histogram:
        fig_layout ["nc"] = len(axes_args["x_values"])
        fig_layout ["nr"] = len(axes_args["y_values"])

    fig, axs = init_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"])
    prettify_fig(fig, fig_distances, file_name, get_sm())
    update_args["text"] = fig.texts[2]

    axes_args = {
        "axs": axs,
        "column_titles": get_titles(update_args["columns"]),
        "divider": create_divider(fig, fig_layout, fig_distances),
        "row_titles": get_titles(update_args["rows"]),
        "x_lim": [None, None],
        "x_values": np.sort(df["logES"].unique()),
        "y_lim": [None, None],
        "y_values": np.sort(df["alpha"].unique())[::-1],
    }

    if args.histogram:
        update_args["artists"] = init_artists_plot(axs)
        update_args["alphas"] = axes_args["y_values"]
        update_args["logess"] = axes_args["x_values"]
        axes_args["x_lim"] = [-2, get_config("bins") + 1]
        axes_args["y_lim"] = [0, 0.25]
        file_name += "_histogram"
    else:
        update_args["artists"] = init_artists_imshow(
            axs, len(axes_args["y_values"]), len(axes_args["x_values"])
        )

    prettify_axes(axes_args)

    if args.mode == "all_traits":
        for trait in all_traits:
            update_args["mode"] = trait
            save_image(df.Time.unique()[-1], update_args, f"{file_name}_{trait}")
    else:
        file_name += f"_{args.mode}"
        if args.movie:
            save_movie(fig, df.Time.unique(), update_args, file_name)
        else:
            save_image(df.Time.unique()[-1], update_args, file_name)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
