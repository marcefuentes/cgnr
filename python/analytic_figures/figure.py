#!/usr/bin/env python

""" Creates plots. """

import os
import re
import time
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import colormaps

import modules.settings as ss
import modules.modes as mm
from modules.add_colorbar import add_colorbar
from modules.argparse_utils import parse_args
from modules.create_fig import create_fig
from modules.init_artists import init_imshow_artists, init_plot_artists
from modules.prettify_axes import prettify_imshow_axes, prettify_plot_axes
from modules.prettify_fig import prettify_fig, create_measurements
from modules.update_zmatrix import update_zmatrix

def update(t, dict_update):
    """ Update the plot with the data at time t. """

    mode =                  dict_update["mode"]
    mode_is_single_trait =  dict_update["mode_is_single_trait"]
    columns =               dict_update["columns"]
    rows =                  dict_update["rows"]
    dfs =                   dict_update["dfs"]
    df_none =               dict_update["df_none"]
    df_social =             dict_update["df_social"]
    dffrqs =                dict_update["dffrqs"]
    movie =                 dict_update["movie"]
    text =                  dict_update["text"]
    artists =               dict_update["artists"]

    dict_z = {}
    dict_z["t"] = t

    if mode_is_single_trait:
        dict_z["trait"] = mode
    else:
        dict_z["df_none"] = df_none
        dict_z["df_social"] = df_social

    for r, row in enumerate(rows):
        if not mode_is_single_trait:
            dict_z["df"] = dfs[r]
        for c, column in enumerate(columns):
            if mode_is_single_trait:
                dict_z["df"] = dfs[r][c]
                dict_z["df_none"] = df_none[r][c]
                dict_z["df_social"] = df_social[r][c]
            else:
                dict_z["trait"] = column
            if row == "none" and mode != "none":
                dict_z["none"] = True
            else:
                dict_z["none"] = False
            zmatrix = update_zmatrix(dict_z)
            if dffrqs:
                if mode_is_single_trait:
                    column = mm.dict_traits[mode]["frq"]
                else:
                    column = mm.dict_traits[column]["frq"]
                for a, alpha in enumerate(dict_update["alphas"]):
                    for e, loges in enumerate(dict_update["logess"]):
                        d = dffrqs[r][
                            (dffrqs[r]["Time"] == t) \
                            & (dffrqs[r]["alpha"] == alpha) \
                            & (dffrqs[r]["logES"] == loges)
                        ]
                        freq_a = [col for col in d.columns if re.match(fr"^{column}\d+$", col)]
                        y = d.loc[:, freq_a].values[0].flatten()
                        artists[r, c, a, e].set_ydata(y)
                        bgcolor = colormaps[ss.COLOR_MAP]((zmatrix[a, e] + 1) / 2)
                        artists[r, c, a, e].axes.set_facecolor(bgcolor)
            else:
                artists[r, c].set_array(zmatrix)
    if movie:
        text.set_text(t)
    return artists.flatten()

def main(mode, histogram=False, movie=False, mode_is_single_trait=False):
    """ Create the figure. """

    start_time = time.perf_counter()
    this_script = os.path.basename(__file__)
    script_name = this_script.split(".")[0]

    # Get data

    if mode_is_single_trait:
        dfs, df_none, df_social, dffrqs = mm.get_data_single_trait(mode, histogram, movie)
        df = dfs[0][0]
    else:
        dfs, df_none, df_social, dffrqs = mm.get_data_multitrait(mode, histogram, movie)
        df = df_none

    ts = df.Time.unique()
    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())
    nr = len(alphas)
    nc = len(logess)
    titles = []

    if mode_is_single_trait:
        rows = mm.list_rows_single_trait
        columns = mm.dict_traits[mode]["columns"]
        for column in columns:
            titles.append(mm.dict_variants_all[column]["title"])
    else:
        if mode in mm.dict_multitrait_rows:
            rows = mm.dict_multitrait_rows[mode]
        else:
            rows = mm.dict_multitrait_rows["default"]
        columns = mm.dict_multitrait_modes[mode]
        for column in columns:
            titles.append(mm.dict_traits[column]["title"])
    nrows = len(rows)
    ncols = len(columns)
    measurements = create_measurements(nrows, ncols)

    if histogram:
        fig, axs, divider = create_fig(measurements, nrows, ncols, nc=nc, nr=nr)
        axs = prettify_plot_axes(
            axs,
            divider,
            alphas,
            logess,
            nrows,
            ncols,
            titles
        )
        artists = init_plot_artists(axs, nrows, ncols, nr, nc)
    else:
        fig, axs, divider = create_fig(measurements, nrows, ncols)
        axs = prettify_imshow_axes(
            axs,
            divider,
            alphas,
            logess,
            nrows,
            ncols,
            titles
        )
        artists = init_imshow_artists(axs, nrows, ncols, nr, nc)

    prettify_fig(fig, measurements)
    add_colorbar(fig, measurements, nc)

    # Add data and save

    name = f"{script_name}_{mode}"
    if histogram:
        name = f"{name}_histogram"

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
        "artists": artists
    }
    if histogram:
        dict_update["alphas"] = alphas
        dict_update["logess"] = logess

    if movie:
        dict_animation = {
            "fig": fig,
            "frames": ts,
            "func": update,
            "fargs": (dict_update,),
            "blit": True
        }
        ani = FuncAnimation(**dict_animation)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        if mode in ("all", "all_lang"):
            if mode == "all":
                traits = [
                    "ChooseGrain",
                    "MimicGrain",
                    "ImimicGrain",
                    "w_excess",
                    "qBSeen_excess"
                ]
            else:
                traits = [
                    "Choose_ltGrain",
                    "Imimic_ltGrain"
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
