""" Initialize artists for plotting. """

from numpy import empty
from matplotlib.collections import LineCollection


def add_artists(data, axs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, _, nr, nc = axs.shape
    data["budgets"] = empty((nrows, 1, nr, nc), dtype=object)
    data["icurves"] = empty((nrows, 1, nr, nc), dtype=object)
    data["icurves_grey"] = empty((nrows, 1, nr, nc, data["ic"].shape[2]), dtype=object)
    data["landscapes"] = empty((nrows, 1, nr, nc), dtype=object)

    for i in range(nrows):
        for k in range(nr):
            for m in range(nc):
                for n in range(data["ic"].shape[2]):
                    data["icurves_grey"][i, 0, k, m, n] = axs[i, 0, k, m].plot(
                        data["x"], data["ic"][k, m, n]
                    )[0]
                data["budgets"][i, 0, k, m] = axs[i, 0, k, m].plot(
                    data["x"], data["y"]
                )[0]
                data["icurves"][i, 0, k, m] = axs[i, 0, k, m].plot(
                    data["x"], data["y"]
                )[0]
                data["landscapes"][i, 0, k, m] = LineCollection([])
                axs[i, 1, k, m].add_collection(data["landscapes"][i, 0, k, m])
