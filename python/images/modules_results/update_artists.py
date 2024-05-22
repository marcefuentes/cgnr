""" Update data in artists. """

import re
import sys

import numpy as np

from matplotlib import colormaps

from modules.get_setting import get_setting
from modules_results.trait_map import trait_map
from modules_results.get_zmatrix import get_zmatrix


def get_frq(update_args, i, j):
    """Return the dataframe and trait for a given grid."""

    if update_args["single_trait"]:
        df = update_args["dffrqs"][i][j]
        trait = trait_map[update_args["trait_set"]]["frq"]
    else:
        df = update_args["dffrqs"][i]
        trait = trait_map[update_args["columns"][j]]["frq"]
    return df, trait


def update_artists(t, update_args):
    """Update artist data at time t."""

    if update_args["movie"]:
        update_args["text"].set_text(t)

    for i, _ in enumerate(update_args["rows"]):
        for j, _ in enumerate(update_args["columns"]):
            zmatrix = update_zmatrix(t, update_args, i, j)
            artists = update_args["artists"][i, j]
            if update_args["fitness"] or update_args["histogram"]:
                artists = update_artists_line2d(artists, zmatrix)
                if update_args["histogram"]:
                    df, trait = get_frq(update_args, i, j)
                    if df.empty:
                        continue
                    df = df[df["Time"] == t]
                    artists = update_artists_histogram(
                        artists, df, update_args["alphas"], update_args["logess"], trait
                    )
            else:
                artists[0, 0].set_array(zmatrix)
    return update_args["artists"].flatten()


def update_artists_histogram(artists, df, alphas, logess, trait):
    """Update histograms."""

    for i, alpha in enumerate(alphas):
        for j, loges in enumerate(logess):
            d = df[(df["alpha"] == alpha) & (df["logES"] == loges)]
            freq_a = [col for col in d.columns if re.match(rf"^{trait}\d+$", col)]
            y = d.loc[:, freq_a].values[0].flatten()
            artists[i, j].set_ydata(y)
    return artists


def update_artists_line2d(artists, zmatrix):
    """Update background colors of plots."""

    nr, nc = zmatrix.shape

    for i in range(nr):
        for j in range(nc):
            bgcolor = colormaps[get_setting("COMMON", "color_map")](
                (zmatrix[i, j] + 1) / 2
            )
            artists[i, j].axes.set_facecolor(bgcolor)

    return artists


def update_zmatrix(t, update_args, i, j):
    """Return the updated zmatrix for a given time and trait."""

    if update_args["single_trait"]:
        trait_in = update_args["trait_set"]
        df = update_args["dfs"][i][j]
        df_none = update_args["df_none"][i][j]
        df_social = update_args["df_social"][i][j]
    else:
        trait_in = update_args["columns"][j]
        df = update_args["dfs"][i]
        df_none = update_args["df_none"]
        df_social = update_args["df_social"]

    none = bool(update_args["rows"][i] == "none" and update_args["trait_set"] != "none")

    if not update_args["single_folder"] and ("nothing" in trait_in or df.empty):
        zmatrix = np.zeros((len(update_args["alphas"]), len(update_args["logess"])))
        return zmatrix

    if trait_in not in trait_map:
        print(f"Trait {trait_in} not in dictionary trait_map.py->trait_map.")
        sys.exit()
    trait = trait_map[trait_in]["mean"]
    relative = trait_map[trait_in]["relative"]
    zmatrix = get_zmatrix(t, df, trait)

    if relative == "-none":
        zmatrix = zmatrix - get_zmatrix(t, df_none, trait)
    elif relative == "none-":
        if none:
            zmatrix = 0.5 - zmatrix
        else:
            zmatrix = get_zmatrix(t, df_none, trait) - zmatrix
    elif relative == "-social":
        zmatrix = zmatrix - get_zmatrix(t, df_social, trait)
    elif relative == "given":
        zmatrix = zmatrix * df.iloc[0]["Given"]
    elif relative == "neutral":
        zmatrix = zmatrix - get_zmatrix(t, df, f"Neutral{trait}")

    return zmatrix
