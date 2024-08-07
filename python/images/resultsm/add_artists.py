""" Initialize artists for plotting. """

from numpy import empty_like, ndindex


def add_artists(data, image):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    axs = image["axs"]
    artists = empty_like(axs, dtype=object)

    for idx in ndindex(axs.shape):
        ax = axs[idx]
        y = data["y"][idx]
        if data["ax_type"] == "AxesImage":
            artists[idx] = ax.imshow(y, **image["AxesImage"])
        elif data["ax_type"] == "Line2D":
            artists[idx] = ax.plot(data["x"], y, **image["Line2D"])[0]
        else:
            artists[idx] = ax.fill_between(data["x"], 0, y, **image["PolyCollection"])

    data["artists"] = artists
