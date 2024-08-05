""" Initialize artists for plotting. """

from numpy import empty
from matplotlib.collections import LineCollection


def add_artists(data, image):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    axs = image["axs"]
    nrows, _, nr, nc = axs.shape
    data["budgets"] = empty((nrows, 1, nr, nc), dtype=object)
    data["icurves"] = empty((nrows, 1, nr, nc), dtype=object)
    data["icurves_grey"] = empty((nrows, 1, nr, nc, data["ic"].shape[2]), dtype=object)
    data["landscapes"] = empty((nrows, 1, nr, nc), dtype=object)

    for artist in ["budgets", "icurves", "icurves_grey", "landscapes"]:
        image[artist]["linewidth"] /= pow(image["fig_layout"]["nr"], 0.5)

    for i in range(nrows):
        for k in range(nr):
            for m in range(nc):
                for n in range(data["ic"].shape[2]):
                    data["icurves_grey"][i, 0, k, m, n] = axs[i, 0, k, m].plot(
                        data["x"], data["ic"][k, m, n], **image["icurves_grey"]
                    )[0]
                data["budgets"][i, 0, k, m] = axs[i, 0, k, m].plot(
                    data["x"], data["y"], **image["budgets"]
                )[0]
                data["icurves"][i, 0, k, m] = axs[i, 0, k, m].plot(
                    data["x"], data["y"], **image["icurves"]
                )[0]
                data["landscapes"][i, 0, k, m] = LineCollection([], **image["landscapes"])
                axs[i, 1, k, m].add_collection(data["landscapes"][i, 0, k, m])
