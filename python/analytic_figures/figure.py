#!/usr/bin/env python

""" Creates plots. """

import os
import time
import numpy as np

from modules.add_colorbar import add_colorbar
from modules.argparse_utils import parse_args
from modules.create_fig import create_fig
from modules.get_data import (
    get_data_single_trait,
    get_data_multitrait,
    get_rows_columns,
)
from modules.init_artists import init_imshow_artists, init_plot_artists
from modules.prettify_axes import prettify_imshow_axes, prettify_plot_axes
from modules.prettify_fig import prettify_fig, create_measurements
from modules.process_plt import process_plt


def main(args):
    """Create the figure."""

    start_time = time.perf_counter()
    script_name = os.path.basename(__file__).split(".")[0]

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

    ts = df.Time.unique()
    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())
    nr = len(alphas)
    nc = len(logess)

    rows, row_titles, columns, column_titles = get_rows_columns(
        args.mode, args.mode_is_trait
    )

    nrows = len(rows)
    ncols = len(columns)
    measurements = create_measurements(nrows, ncols)
    layout = {
        "nrows": nrows,
        "ncols": ncols,
    }

    if args.histogram:
        layout["nr"] = nr
        layout["nc"] = nc
        fig, axs, divider = create_fig(measurements, layout)
        axs = prettify_plot_axes(
            axs, divider, alphas, logess, row_titles, column_titles
        )
        artists = init_plot_artists(axs)
    else:
        fig, axs, divider = create_fig(measurements, layout)
        axs = prettify_imshow_axes(
            axs, divider, alphas, logess, row_titles, column_titles
        )
        artists = init_imshow_artists(axs, nr, nc)

    prettify_fig(fig, measurements)
    add_colorbar(fig, measurements, nc)

    # Add data and save

    if args.histogram:
        script_name += "_args.histogram"

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
        "artists": artists,
    }
    if args.histogram:
        dict_update["alphas"] = alphas
        dict_update["logess"] = logess

    process_plt(fig, ts, dict_update, script_name)

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
