""" Format axes. """

import numpy as np


def add_letters(ax, position, params, n):
    """Add letters."""

    params["s"] = chr(ord("a") + n % 26)
    if n >= 26:
        params["s"] = params["s"] + params["s"]
    params["transform"] = ax.transAxes
    ax.text(*position, **params)


def format_axes(axes_args, image):
    """format (nrows x ncols x nr x nc) matrix."""

    axs = axes_args["axs"]
    nrows, ncols, nr, nc = axs.shape

    # Position axes

    for i, j, k, m in np.ndindex(axs.shape):
        axs[i, j, k, m].set(
            axes_locator=axes_args["divider"].new_locator(
                nx=j * (nc + 1) + m + int(m / nc),
                ny=(nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
            )
        )

    # Format spines

    for ax in axs.flatten():
        for spine in ax.spines.values():
            spine.set(**image["spines"])

    # Set limits and reset ticks

    params = {
        "xlim": axes_args["lim_x"],
        "ylim": axes_args["lim_y"],
        "xticks": [],
        "yticks": [],
    }
    for ax in axs.flatten():
        ax.set(**params)

    # Add letters

    position = (0, 1.0 + image["padding_letter"] * nr)
    for i in range(nrows):
        for j in range(ncols):
            add_letters(axs[i, j, 0, 0], position, image["letters"], i * ncols + j)

    # Add column titles

    for j in range(ncols):
        axs[0, j, 0, int(nc / 2)].set_title(
            axes_args["titles_columns"][j], **image["titles_columns"]
        )

    # Add row titles

    for i in range(nrows):
        axs[i, -1, int(nr / 2), -1].annotate(
            axes_args["titles_rows"][i], **image["titles_rows"]
        )
