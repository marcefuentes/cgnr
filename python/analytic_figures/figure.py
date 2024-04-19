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

def main(mode, histogram=False, movie=False, mode_is_single_trait=False):
    """Create the figure."""

    start_time = time.perf_counter()
    this_script = os.path.basename(__file__)
    script_name = this_script.split(".")[0]

    # Get data

    if mode_is_single_trait:
        dfs, df_none, df_social, dffrqs = get_data_single_trait(mode, histogram, movie)
        df = dfs[0][0]
    else:
        dfs, df_none, df_social, dffrqs = get_data_multitrait(mode, histogram, movie)
        df = df_none

    ts = df.Time.unique()
    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())
    nr = len(alphas)
    nc = len(logess)

    rows, row_titles, columns, column_titles = get_rows_columns(
        mode, mode_is_single_trait
    )

    nrows = len(rows)
    ncols = len(columns)
    measurements = create_measurements(nrows, ncols)

    if histogram:
        fig, axs, divider = create_fig(measurements, nrows, ncols, nc=nc, nr=nr)
        axs = prettify_plot_axes(
            axs, divider, alphas, logess, row_titles, column_titles
        )
        artists = init_plot_artists(axs)
    else:
        fig, axs, divider = create_fig(measurements, nrows, ncols)
        axs = prettify_imshow_axes(
            axs, divider, alphas, logess, row_titles, column_titles
        )
        artists = init_imshow_artists(axs, nr, nc)

    prettify_fig(fig, measurements)
    add_colorbar(fig, measurements, nc)

    # Add data and save

    if histogram:
        script_name += "_histogram"

    dict_update = {
        "mode": mode,
        "mode_is_single_trait": mode_is_single_trait,
        "columns": columns,
        "rows": rows,
        "dfs": dfs,
        "df_none": df_none,
        "df_social": df_social,
        "dffrqs": dffrqs,
        "movie": movie,
        "text": fig.texts[2],
        "artists": artists,
    }
    if histogram:
        dict_update["alphas"] = alphas
        dict_update["logess"] = logess

    process_plt(fig, ts, movie, dict_update, script_name)

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")


if __name__ == "__main__":
    args, is_trait = parse_args()
    main(
        mode=args.mode,
        histogram=args.histogram,
        movie=args.movie,
        mode_is_single_trait=is_trait,
    )
