""" Update data in artists. """

import re
import sys

import numpy as np

from matplotlib import colormaps

from settings_results.image import image
from settings_results.trait_map import trait_map
from modules_results.get_zmatrix import get_zmatrix


def get_frq(options, dynamic_data, i, j):
    """Return the dataframe and trait for a given grid."""

    if options["single_trait"]:
        df = dynamic_data["dffrqs"][i][j]
        trait = trait_map[options["trait_set"]]["frq"]
    else:
        df = dynamic_data["dffrqs"][i]
        trait = trait_map[options["columns"][j]]["frq"]
    return df, trait


def update_artists(t, update_args, options, dynamic_data):
    """Update artist data at time t."""

    if options["movie"]:
        options["text"].set_text(t)

    for i, _ in enumerate(options["rows"]):
        for j, _ in enumerate(options["columns"]):
            zmatrix = update_zmatrix(t, options, dynamic_data, i, j)
            artists = update_args["artists"][i, j]
            if options["fitness"] or options["histogram"]:
                artists = update_artists_line2d(artists, zmatrix)
                if options["histogram"]:
                    df, trait = get_frq(options, dynamic_data, i, j)
                    if df.empty:
                        continue
                    df = df[df["Time"] == t]
                    artists = update_artists_histogram(
                        artists,
                        df,
                        dynamic_data["alphas"],
                        dynamic_data["logess"],
                        trait,
                    )
            else:
                artists[0, 0].set_array(zmatrix)

    return artists.flatten()


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

    cmap = colormaps.get_cmap(image["color_map"])

    for i in range(zmatrix.shape[0]):
        for j in range(zmatrix.shape[1]):
            artists[i, j].axes.set_facecolor(cmap((zmatrix[i, j] + 1) / 2))

    return artists


def update_zmatrix(t, options, dynamic_data, i, j):
    """Return the updated zmatrix for a given time and trait."""

    if options["single_trait"]:
        trait_in = options["trait_set"]
        df = dynamic_data["dfs"][i][j]
        df_none = dynamic_data["df_none"][i][j]
        df_social = dynamic_data["df_social"][i][j]
    else:
        trait_in = options["columns"][j]
        df = dynamic_data["dfs"][i]
        df_none = dynamic_data["df_none"]
        df_social = dynamic_data["df_social"]

    none = bool(options["rows"][i] == "none" and options["trait_set"] != "none")

    if not options["single_folder"] and ("nothing" in trait_in or df.empty):
        zmatrix = np.zeros((len(dynamic_data["alphas"]), len(dynamic_data["logess"])))
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
