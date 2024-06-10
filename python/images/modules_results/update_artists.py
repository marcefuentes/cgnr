""" Update data in artists. """

import re
import numpy as np
from modules_results.get_zmatrix import get_zmatrix


def update_artists(t, update_args, options, dynamic_data):
    """Update artist data at time t."""

    for i, row in enumerate(dynamic_data["dfs"]):
        for j, _ in enumerate(row):
            zmatrix = update_zmatrix(t, dynamic_data, i, j)
            artists = update_args["artists"][i, j]
            if options["figure"] == "curves" or options["histogram"]:
                artists = update_artists_line2d(artists, zmatrix, update_args["cmap"])
                if options["histogram"]:
                    artists = update_artists_histogram(t, artists, dynamic_data, i, j)
            else:
                artists[0, 0].set_array(zmatrix)

    if options["movie"]:
        dynamic_data["text"].set_text(t)
        return artists.flatten()


def update_artists_histogram(t, artists, dynamic_data, i, j):
    """Update histograms."""

    df = dynamic_data["dffrqs"][i][j]
    if df.empty:
        return artists

    alphas = dynamic_data["alphas"]
    logess = dynamic_data["logess"]
    trait = dynamic_data["traits"][i][j]
    if "mean" in trait:
        trait = trait[:-4]

    df = df[df["Time"] == t]

    for i, alpha in enumerate(alphas):
        for j, loges in enumerate(logess):
            d = df[(df["alpha"] == alpha) & (df["logES"] == loges)]
            freq_a = [col for col in d.columns if re.match(rf"^{trait}\d+$", col)]
            y = d.loc[:, freq_a].values[0].flatten()
            artists[i, j].set_ydata(y)
    return artists


def update_artists_line2d(artists, zmatrix, cmap):
    """Update background colors of plots."""

    for i in range(zmatrix.shape[0]):
        for j in range(zmatrix.shape[1]):
            artists[i, j].axes.set_facecolor(cmap((zmatrix[i, j] + 1) / 2))

    return artists


def update_zmatrix(t, dynamic_data, i, j):
    """Return the updated zmatrix for a given time and trait."""

    df = dynamic_data["dfs"][i, j]
    df_control = dynamic_data["dfs_control"][i, j]
    trait = dynamic_data["traits"][i][j]

    if "nothing" in trait or df.empty:
        zmatrix = np.zeros((len(dynamic_data["alphas"]), len(dynamic_data["logess"])))
        return zmatrix

    if df_control.empty:
        zmatrix = get_zmatrix(t, df, trait)
        if "Grainmean" in trait:
            zmatrix = 1.0 - zmatrix
        return zmatrix

    zmatrix_treatment = get_zmatrix(t, df, trait)
    zmatrix_control = get_zmatrix(t, df_control, trait)

    if zmatrix_treatment.shape == zmatrix_control.shape:
        zmatrix = get_zmatrix(t, df, trait) - get_zmatrix(t, df_control, trait)
        if "Grainmean" in trait:
            zmatrix = -zmatrix
        return zmatrix

    print("\nData for one of the plots is incomplete.")
    zmatrix = np.zeros((len(dynamic_data["alphas"]), len(dynamic_data["logess"])))
    return zmatrix
