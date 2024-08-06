""" Initialize artists for plotting. """

from numpy import empty, ndindex
from matplotlib.collections import LineCollection


def add_artists(data, image):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    axs = image["axs"]
    nrows, _, nr, nc = axs.shape
    layout = (nrows, 1, nr, nc)
    data["budgets"] = empty(layout, dtype=object)
    data["icurves"] = empty(layout, dtype=object)
    data["icurves_grey"] = empty((*layout, data["ic"].shape[2]), dtype=object)
    data["landscapes"] = empty(layout, dtype=object)

    for artist in ["budgets", "icurves", "icurves_grey", "landscapes"]:
        image[artist]["linewidth"] /= pow(image["fig_layout"]["nr"], 0.5)

    for idx in ndindex(*layout):
        i, _, k, m = idx
        ax = axs[idx]
        for n in range(data["ic"].shape[2]):
            data["icurves_grey"][idx + (n,)] = ax.plot(
                data["x"], data["ic"][k, m, n], **image["icurves_grey"]
            )[0]
        data["budgets"][idx] = ax.plot(data["x"], data["y"], **image["budgets"])[0]
        data["icurves"][idx] = ax.plot(data["x"], data["y"], **image["icurves"])[0]
        data["landscapes"][idx] = LineCollection([], **image["landscapes"])
        axs[i, 1, k, m].add_collection(data["landscapes"][idx])
