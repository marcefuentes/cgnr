""" Format axes. """

import numpy as np
import modules.format_axes_tools as tools


def format_axes(axes_args, image):
    """format (nrows x ncols x nr x nc) matrix."""

    axs = axes_args["axs"]
    nrows, ncols, nr, nc = axs.shape

    # Position axes

    for i, j, k, m in np.ndindex(axs.shape):
        axs[i, j, k, m].set(axes_locator = axes_args["divider"].new_locator(
            nx=j * (nc + 1) + m + int(m / nc),
            ny=(nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
        ))

    # Format spines

    params = {
        "linewidth": image["border_width"],
        "color": image["border_color"],
    }
    for ax in axs.flatten():
        tools.format_spines(ax, **params)

    # Set limits and reset ticks

    params = {
        "xlim": axes_args["x_lim"],
        "ylim": axes_args["y_lim"],
        "xticks": [],
        "yticks": [],
    }
    for ax in axs.flatten():
        ax.set(**params)

    # Add ticks and tick labels

    params = {
        "labelsize": image["tick_label_size"],
        "size": image["tick_size"],
        "color": image["tick_color"],
    }
    if axs.shape[2] == 1:
        tools.add_ticks_imshow(axs, axes_args["nr"], axes_args["nc"], params)
        tools.add_ticklabels_imshow(axs, axes_args["r_labels"], axes_args["c_labels"])
    else:
        tools.add_ticks_line2d(axs, params)
        tools.add_ticklabels_line2d(axs, axes_args["r_labels"], axes_args["c_labels"])

    # Add letters

    position = (0, 1.0 + image["letter_padding"] * nr)
    params = {
        "fontsize": image["letter_label_size"],
        "weight": "bold",
    }
    for i in range(nrows):
        for j in range(ncols):
            tools.add_letters(axs[i, j, 0, 0], position, params, i * ncols + j)

    # Add column titles

    params = {
        "pad": image["plot_size"] * image["title_padding"],
        "fontsize": image["letter_label_size"],
    }
    for j in range(ncols):
        axs[0, j, 0, int(nc / 2)].set_title(axes_args["column_titles"][j], **params)

    # Add row titles

    params = {
        "xy": (1, 0.5),
        "xycoords": "axes fraction",
        "xytext": (
            image["plot_size"] * image["title_padding"] * 3.5,
            0,
        ),
        "textcoords": "offset points",
        "va": "center",
        "ha": "left",
        "fontsize": image["letter_label_size"],
    }
    for i in range(nrows):
        axs[i, -1, int(nr / 2), -1].annotate(axes_args["row_titles"][i], **params)
