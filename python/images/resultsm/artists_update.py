""" Update data in artists. """

import re
from resultsm.get_zmatrix import get_zmatrix


def artists_update(t, data):
    """Update artist data at time t."""

    if data["movie"]:
        data["text"].set_text(t)

    for i in range(data["layout_i"]):
        for j in range(data["layout_j"]):
            artists = data["artists"][i, j]
            zmatrix = update_zmatrix(t, data, i, j)
            if zmatrix is None:
                print(f"Insufficient data for plot [{i}, {j}].")
                if data["ax_type"] == "AxesImage" and data["layout"] != "theory":
                    data["artists"][i, j, 0, 0].set(cmap="Greys", clim=(0, 1))
            else:
                if data["ax_type"] == "Line2D" or data["ax_type"] == "PolyCollection":
                    artists = artists_update_line2d(artists, zmatrix, data["cmap"])
                    if data["histogram"]:
                        artists = artists_update_histogram(t, artists, data, i, j)
                else:
                    artists[0, 0].set_array(zmatrix)

    return artists.flatten()


def artists_update_histogram(t, artists, data, i, j):
    """Update histograms."""

    df = data["dffrqs"][i][j]
    if df.empty:
        return artists

    trait = data["traits"][i][j]
    if "mean" in trait:
        trait = trait[:-4]

    df = df[df["Time"] == t]

    for k, alpha in enumerate(data["alphas"]):
        for m, loges in enumerate(data["logess"]):
            d = df[(df["alpha"] == alpha) & (df["logES"] == loges)]
            freq_a = [col for col in d.columns if re.match(rf"^{trait}\d+$", col)]
            y = d.loc[:, freq_a].values[0].flatten()
            artists[k, m].set_ydata(y)
    return artists


def artists_update_line2d(artists, zmatrix, cmap):
    """Update background colors of plots."""

    for i in range(artists.shape[0]):
        for j in range(artists.shape[1]):
            artists[i, j].axes.set_facecolor(cmap((zmatrix[i, j] + 1) / 2))

    return artists


def update_zmatrix(t, data, i, j):
    """Return the updated zmatrix for a given time and trait."""

    df = data["dfs"][i, j]
    trait = data["traits"][i][j]

    if trait is None or df.empty:
        return None

    if trait not in df.columns:
        print(f"Trait {trait} does not exist.")
        return None

    zmatrix = get_zmatrix(
        t,
        df,
        trait,
        data["row_index"],
        data["column_index"],
    )

    df_control = data["dfs_control"][i, j]
    if df_control.empty:
        if "Grainmean" in trait:
            zmatrix = 1.0 - zmatrix
        return zmatrix

    zmatrix_control = get_zmatrix(
        t,
        df_control,
        data["traits_control"][i][j],
        data["row_index"],
        data["column_index"],
    )

    if zmatrix.shape == zmatrix_control.shape:
        zmatrix -= zmatrix_control
        if "Grainmean" in trait:
            zmatrix = 0.0 - zmatrix
        return zmatrix

    print(
        f"\nFocal zmatrix {zmatrix.shape} and control zmatrix {zmatrix_control.shape} "
        f"have different shapes."
    )
    return None
