""" Update data in artists. """

import re
import sys

import numpy as np

from matplotlib import colormaps

from settings_results.trait_map import trait_map
from settings_results.image import image
from modules_simple.get_zmatrix import get_zmatrix


def update_artists(t, update_args, options, dynamic_data):
    """Update artist data at time t."""

    if options["movie"]:
        dynamic_data["text"].set_text(t)

    if options["histogram"]:
        trait = trait_map[options["trait_set"]]["frq"]

    for i, row in enumerate(dynamic_data["dfs"]):
        for j, _ in enumerate(row):
            zmatrix = update_zmatrix(
                t,
                dynamic_data["dfs"][i, j],
                dynamic_data["dfs_control"][i, j],
                options["trait_set"],
            )
            artists = update_args["artists"][i, j]
            if options["fitness"] or options["histogram"]:
                artists = update_artists_line2d(artists, zmatrix)
                if options["histogram"]:
                    df = dynamic_data["dffrqs"][i, j]
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


def update_zmatrix(t, df, df_control, trait_in):
    """Return the updated zmatrix for a given time and trait."""

    if "nothing" in trait_in or df.empty:
        zmatrix = np.zeros((len(dynamic_data["alphas"]), len(dynamic_data["logess"])))
        return zmatrix

    if trait_in not in trait_map:
        print(f"Trait {trait_in} not in dictionary trait_map.py->trait_map.")
        sys.exit()
    trait = trait_map[trait_in]["mean"]
    zmatrix = get_zmatrix(t, df, trait) - get_zmatrix(t, df_control, trait)

    if "Grain" in trait:
        zmatrix = -zmatrix

    return zmatrix
