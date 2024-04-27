#!/usr/bin/env python

""" Creates plots of results. """

import os
import time

from common_modules.get_config import get_config
from modules.fix_positions import create_divider
from modules.get_setting import get_titles
from modules.init_fig import init_fig
from modules.prettify_axes import prettify_axes
from modules.prettify_fig import get_distances, prettify_fig
from modules.save_image import save_image, close_plt
from modules.save_movie import save_movie

from modules_results.get_update_args import get_update_args, get_rows, get_columns
from modules_results.get_sm import get_sm
from modules_results.init_artists import init_artists_imshow, init_artists_plot
from modules_results.modes import all_traits
from modules_results.parse_args import parse_args
from modules_results.update import update_artists, update_histogram


def main(args):
    """Main function"""

    start_time = time.perf_counter()
    file_name = os.path.basename(__file__).split(".")[0]

    update_args = {
        "alphas": None,
        "artists": None,
        "columns": get_columns(args.mode_is_trait, args.mode),
        "df_none": None,
        "df_social": None,
        "dffrqs": None,
        "dfs": None,
        "logess": None,
        "mode": args.mode,
        "mode_is_trait": args.mode_is_trait,
        "movie": args.movie,
        "rows": get_rows(args.mode_is_trait, args.mode),
        "text": "",
        "update_curve_function": update_histogram,
        "update_function": update_artists,
    }

    update_args, ts = get_update_args(update_args, args.histogram, args.clean)

    fig_layout = {
        "nc": len(update_args["logess"]) if args.histogram else 1,
        "ncols": len(update_args["columns"]),
        "nr": len(update_args["alphas"]) if args.histogram else 1,
        "nrows": len(update_args["rows"]),
    }

    fig, axs = init_fig(fig_layout)

    fig_distances = get_distances(fig_layout["nrows"], fig_layout["ncols"])
    prettify_fig(fig, fig_distances, file_name, get_sm())
    update_args["text"] = fig.texts[2]
    update_args["artists"] = (
        init_artists_plot(axs)
        if args.histogram
        else init_artists_imshow(
            axs, len(update_args["alphas"]), len(update_args["logess"])
        )
    )

    axes_args = {
        "axs": axs,
        "column_titles": get_titles(update_args["columns"]),
        "divider": create_divider(fig, fig_layout, fig_distances),
        "row_titles": get_titles(update_args["rows"]),
        "x_lim": [-2, get_config("bins") + 1] if args.histogram else [None, None],
        "x_values": update_args["logess"],
        "y_lim": [0, 0.25] if args.histogram else [None, None],
        "y_values": update_args["alphas"],
    }
    prettify_axes(axes_args)

    if args.histogram:
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
