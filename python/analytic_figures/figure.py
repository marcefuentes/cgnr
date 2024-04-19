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

    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())

    rows, row_titles, columns, column_titles = get_rows_columns(
        args.mode, args.mode_is_trait
    )

    layout = {
        "nrows": len(rows),
        "ncols": len(columns),
        "nr" : len(alphas),
        "nc" : len(logess),
        "histogram": args.histogram,
    }

    fig, axs, divider = create_fig(layout)

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
        dict_update["alphas"] = alphas
        dict_update["logess"] = logess
        prettify_plot_axes(
            axs, divider, alphas, logess, row_titles, column_titles
        )
        dict_update["artists"] = init_plot_artists(axs)
        file_name += "_histogram"
    else:
        prettify_imshow_axes(
            axs, divider, alphas, logess, row_titles, column_titles
        )
        dict_update["artists"] = init_imshow_artists(axs, len(alphas), len(logess))

    # Add data and save

    process_plt(fig, df.Time.unique(), dict_update, file_name)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
