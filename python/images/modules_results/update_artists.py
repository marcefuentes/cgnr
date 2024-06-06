""" Update data in artists. """

import re
import sys

import numpy as np

from matplotlib import colormaps

from settings_results.image import image
from modules_results.get_zmatrix import get_zmatrix


def update_artists(t, update_args, options, dynamic_data):
    """Update artist data at time t."""

    if options["movie"]:
        dynamic_data["text"].set_text(t)

    for i, row in enumerate(dynamic_data["dfs"]):
        for j, _ in enumerate(row):
            zmatrix = update_zmatrix(
                t,
                dynamic_data["dfs"][i, j],
                dynamic_data["dfs_control"][i, j],
                dynamic_data["traits"][i][j],
            )
            artists = update_args["artists"][i, j]
            if options["figure"] == "curves" or options["histogram"]:
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
                        dynamic_data["traits"][i][j],
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


def update_zmatrix(t, df, df_control, trait):
    """Return the updated zmatrix for a given time and trait."""

    if "nothing" in trait or df.empty:
        zmatrix = np.zeros((len(dynamic_data["alphas"]), len(dynamic_data["logess"])))
        return zmatrix

    if df_control.empty:
        zmatrix = get_zmatrix(t, df, trait)
        if "Grain" in trait:
            zmatrix = 1.0 - zmatrix
        return zmatrix

    zmatrix = get_zmatrix(t, df, trait) - get_zmatrix(t, df_control, trait)

    if "Grain" in trait:
        zmatrix = -zmatrix

    return zmatrix
