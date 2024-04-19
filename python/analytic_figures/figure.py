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
from modules.prettify_axes import prettify_imshow_axes, prettify_plot_axes
from modules.process_plt import process_plt


def main(args):
    """Create the figure."""

    start_time = time.perf_counter()

    # Get data

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

    dict_axs = {
        "y_values": np.sort(df["alpha"].unique())[::-1],
        "x_values": np.sort(df["logES"].unique()),
    }

    rows, dict_axs["row_titles"], columns, dict_axs["column_titles"] = get_rows_columns(
        args.mode, args.mode_is_trait
    )

    layout = {
        "nrows": len(rows),
        "ncols": len(columns),
        "nr" : len(dict_axs["y_values"]),
        "nc" : len(dict_axs["x_values"]),
        "histogram": args.histogram,
    }

    fig, dict_axs["axs"], dict_axs["divider"] = create_fig(layout)

    dict_update = {
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
        dict_update["alphas"] = dict_axs["y_values"]
        dict_update["logess"] = dict_axs["x_values"]
        prettify_plot_axes(dict_axs)
        dict_update["artists"] = init_plot_artists(dict_axs["axs"])
        file_name += "_histogram"
    else:
        prettify_imshow_axes(dict_axs)
        dict_update["artists"] = init_imshow_artists(dict_axs["axs"], layout["nr"], layout["nc"])

    # Add data and save

    process_plt(fig, df.Time.unique(), dict_update, file_name)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
