#!/usr/bin/env python

""" Creates plots. """

import os
import time
import numpy as np

from modules.get_setting import get_setting as get
from modules.init_fig import init_fig
from modules.make_image import make_image, close_plt
from modules.make_movie import make_movie
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
    file_name = os.path.basename(__file__).split(".")[0]

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
        "axs": None,
        "column_titles": [""],
        "divider": None,
        "file_name": file_name,
        "init_function": init_imshow_artists,
        "prettify_function": prettify_axes_imshow,
        "row_titles": [""],
        "x_lim": "None",
        "y_values": np.sort(df["alpha"].unique())[::-1],
        "y_lim": "None",
        "x_values": np.sort(df["logES"].unique()),
    }

    if args.histogram:
        axes_args["init_function"] = init_plot_artists
        axes_args["prettify_function"] = prettify_axes_plot
        axes_args["x_lim"] = [-2, get("file_name", "bins") + 1]
        axes_args["y_lim"] = [0, 0.25]

    rows, axes_args["row_titles"], columns, axes_args["column_titles"] = (
        get_rows_columns(args.mode, args.mode_is_trait)
    )

    fig_args = {
        "file_name": file_name,
        "nc": len(axes_args["x_values"]),
        "ncols": len(columns),
        "nested": args.histogram,
        "nr": len(axes_args["y_values"]),
        "nrows": len(rows),
        "sm": get_sm(),
    }

    update_args = {
        "artists": None,
        "mode": args.mode,
        "mode_is_trait": args.mode_is_trait,
        "columns": columns,
        "rows": rows,
        "dfs": dfs,
        "df_none": df_none,
        "df_social": df_social,
        "dffrqs": dffrqs,
        "movie": args.movie,
        "nc": len(axes_args["x_values"]),
        "nr": len(axes_args["y_values"]),
        "text": "",
        "update_function": update_artists,
    }

    if args.histogram:
        update_args["alphas"] = axes_args["y_values"]
        update_args["logess"] = axes_args["x_values"]
        file_name += "_histogram"
        update_args["text"] = fig.texts[2]

    fig, update_args = init_fig(fig_args, axes_args, update_args)

    if args.mode == "all_traits":
        for trait in all_traits:
            update_args["mode"] = trait
            make_image(df.Time.unique(), update_args, f"{file_name}_{trait}")
    else:
        file_name += f"_{args.mode}"
        if args.movie:
            make_movie(fig, df.Time.unique(), update_args, file_name)
        else:
            make_image(df.Time.unique(), update_args, file_name)
    close_plt(fig)

    print(f"\nTime elapsed: {(time.perf_counter() - start_time):.2f} seconds")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
