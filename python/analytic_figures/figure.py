#!/usr/bin/env python

""" Creates plots. """

import os
import time
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import modules.modes as mm
from modules.add_colorbar import add_colorbar
from modules.argparse_utils import parse_args
from modules.create_fig import create_fig
from modules.get_data import get_data_single_trait, get_data_multitrait
from modules.init_artists import init_imshow_artists, init_plot_artists
from modules.prettify_axes import prettify_imshow_axes, prettify_plot_axes
from modules.prettify_fig import prettify_fig, create_measurements
from modules.update import update

def main(mode, histogram=False, movie=False, mode_is_single_trait=False):
    """ Create the figure. """

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
    column_titles = []
    row_titles = []

    if mode_is_single_trait:
        rows = mm.dict_single_trait_rows_1.get(mode, mm.dict_single_trait_rows_1["default"])
        columns = mm.dict_traits[mode]["variants"]
        for column in columns:
            column_titles.append(mm.dict_variant_titles[column])
    else:
        rows = mm.dict_multitrait_rows.get(mode, mm.dict_multitrait_rows["default"])
        columns = mm.dict_multitrait_columns[mode]
        for column in columns:
            column_titles.append(mm.dict_traits[column]["title"])
    for row in rows:
        row_titles.append(mm.dict_row_titles[row])

    nrows = len(rows)
    ncols = len(columns)
    measurements = create_measurements(nrows, ncols)

    if histogram:
        fig, axs, divider = create_fig(
            measurements,
            nrows,
            ncols,
            nc=nc,
            nr=nr
        )
        axs = prettify_plot_axes(
            axs,
            divider,
            alphas,
            logess,
            row_titles,
            column_titles
        )
        artists = init_plot_artists(axs)
    else:
        fig, axs, divider = create_fig(
            measurements,
            nrows,
            ncols)
        axs = prettify_imshow_axes(
            axs,
            divider,
            alphas,
            logess,
            row_titles,
            column_titles
        )
        artists = init_imshow_artists(axs, nr, nc)

    prettify_fig(fig, measurements)
    add_colorbar(fig, measurements, nc)

    # Add data and save

    name = f"{script_name}_{mode}"
    if histogram:
        name = f"{name}_histogram"

    dict_update = {
        "mode":                 mode,
        "mode_is_single_trait": mode_is_single_trait,
        "columns":              columns,
        "rows":                 rows,
        "dfs":                  dfs,
        "df_none":              df_none,
        "df_social":            df_social,
        "dffrqs":               dffrqs,
        "movie":                movie,
        "text":                 fig.texts[2],
        "artists":              artists
    }
    if histogram:
        dict_update["alphas"] = alphas
        dict_update["logess"] = logess

    if movie:
        dict_animation = {
            "fig":      fig,
            "frames":   ts,
            "func":     update,
            "fargs":    (dict_update,),
            "blit":     True
        }
        ani = FuncAnimation(**dict_animation)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        if mode in ("all_lang_traits", "all_traits"):
            if mode == "all_lang_traits":
                traits = [
                    "Choose_ltGrain",
                    "Imimic_ltGrain"
                ]
            else:
                traits = [
                    "ChooseGrain",
                    "MimicGrain",
                    "ImimicGrain",
                    "w_excess",
                    "qBSeen_excess"
                ]
            for trait in traits:
                dict_update["mode"] = trait
                update(ts[-1], dict_update)
                plt.savefig(f"{script_name}_{trait}.png", transparent=False)
        else:
            update(ts[-1], dict_update)
            plt.savefig(f"{name}.png", transparent=False)
    plt.close()

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":
    args, is_trait = parse_args()
    main(
        mode=args.mode,
        histogram=args.histogram,
        movie=args.movie,
        mode_is_single_trait=is_trait
    )
