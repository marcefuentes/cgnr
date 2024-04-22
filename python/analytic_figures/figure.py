#!/usr/bin/env python

""" Creates plots. """

import os
import time
import numpy as np

from modules.parse_args import parse_args
from modules.init_fig import init_fig
from modules.get_data import (
    get_data_single_trait,
    get_data_multitrait,
    get_rows_columns,
)
from modules.init_artists import init_imshow_artists, init_plot_artists
from modules.modes import all_traits
from modules.prettify_axes import prettify_axes_imshow, prettify_axes_plot
from modules.process_plt import process_plt, close_plt
import modules.settings as ss


def main(args):
    """Create the figure."""

    start_time = time.perf_counter()

    if args.mode_is_trait:
        dfs, df_none, df_social, dffrqs = get_data_single_trait(
            args.mode, args.histogram, args.movie
        )
        df = dfs[0][0]
    else:
        dfs, df_none, df_social, dffrqs = get_data_multitrait(
            args.mode, args.histogram, args.movie
        )
        df = df_none

    axes_args = {
        "y_values": np.sort(df["alpha"].unique())[::-1],
        "x_values": np.sort(df["logES"].unique()),
    }

    if args.histogram:
        axes_args["x_lim"] = [-2, ss.N_X_VALUES + 1]
        axes_args["y_lim"] = [0, 0.25]

    rows, axes_args["row_titles"], columns, axes_args["column_titles"] = (
        get_rows_columns(args.mode, args.mode_is_trait)
    )

    fig_args = {
        "nrows": len(rows),
        "ncols": len(columns),
        "nr": len(axes_args["y_values"]),
        "nc": len(axes_args["x_values"]),
        "nested": args.histogram,
    }

    fig, axes_args["axs"], axes_args["divider"] = init_fig(fig_args)

    update_args = {
        "mode": args.mode,
        "mode_is_trait": args.mode_is_trait,
        "columns": columns,
        "rows": rows,
        "dfs": dfs,
        "df_none": df_none,
        "df_social": df_social,
        "dffrqs": dffrqs,
        "movie": args.movie,
        "text": fig.texts[2],
    }

    file_name = os.path.basename(__file__).split(".")[0]
    if args.histogram:
        update_args["alphas"] = axes_args["y_values"]
        update_args["logess"] = axes_args["x_values"]
        prettify_axes_plot(axes_args)
        update_args["artists"] = init_plot_artists(axes_args["axs"])
        file_name += "_histogram"
    else:
        prettify_axes_imshow(axes_args)
        update_args["artists"] = init_imshow_artists(
            axes_args["axs"], fig_args["nr"], fig_args["nc"]
        )

    # Add data and save

    if args.mode == "all_traits":
        for trait in all_traits:
            update_args["mode"] = trait
            process_plt(fig, df.Time.unique(), update_args, f"{file_name}_{trait}")
    else:
        file_name += f"_{args.mode}"
        process_plt(fig, df.Time.unique(), update_args, file_name)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
