#!/usr/bin/env python

""" Creates plots. """

import os
import time
import numpy as np

from modules.argparse_utils import parse_args
from modules.create_fig import create_fig
from modules.get_data import (
    get_data_single_trait,
    get_data_multitrait,
    get_rows_columns,
)
from modules.init_artists import init_imshow_artists, init_plot_artists
from modules.modes import all_traits
from modules.prettify_axes import prettify_imshow_axes, prettify_plot_axes
from modules.process_plt import process_plt, close_plt
from modules.settings import BINS


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

    axes_data = {
        "y_values": np.sort(df["alpha"].unique())[::-1],
        "x_values": np.sort(df["logES"].unique()),
    }

    rows, axes_data["row_titles"], columns, axes_data["column_titles"] = (
        get_rows_columns(args.mode, args.mode_is_trait)
    )

    layout = {
        "nrows": len(rows),
        "ncols": len(columns),
        "nr": len(axes_data["y_values"]),
        "nc": len(axes_data["x_values"]),
        "nested": args.histogram,
    }

    fig, axes_data["axs"], axes_data["divider"] = create_fig(layout)

    update_data = {
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
        update_data["alphas"] = axes_data["y_values"]
        update_data["logess"] = axes_data["x_values"]
        prettify_plot_axes(axes_data)
        update_data["artists"] = init_plot_artists(axes_data["axs"], BINS)
        file_name += "_histogram"
    else:
        prettify_imshow_axes(axes_data)
        update_data["artists"] = init_imshow_artists(
            axes_data["axs"], layout["nr"], layout["nc"]
        )

    # Add data and save

    if args.mode == "all_traits":
        for trait in all_traits:
            update_data["mode"] = trait
            process_plt(fig, df.Time.unique(), update_data, f"{file_name}_{trait}")
    else:
        file_name += f"_{args.mode}"
        process_plt(fig, df.Time.unique(), update_data, file_name)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
