""" Format axes. """

import numpy as np
import modules.format_axes_tools as tools


def format_axes(axes_args, image):
    """format (nrows x ncols x nr x nc) matrix."""

    axs = axes_args["axs"]
    nrows, ncols, nr, nc = axs.shape

    # Format spines, reset ticks, set limits and position axes

    spine_params = {
        "linewidth": image["border_width"],
        "color": image["border_color"],
    }
    params = {
        "xticks": [],
        "yticks": [],
        "xlim": axes_args["x_lim"],
        "ylim": axes_args["y_lim"],
    }

    for i, j, k, m in np.ndindex(axs.shape):
        ax = axs[i, j, k, m]
        tools.format_spines(ax, **spine_params)
        params["axes_locator"] = axes_args["divider"].new_locator(
            nx=j * (nc + 1) + m + int(m / nc),
            ny=(nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
        )
        ax.set(**params)

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
    for j, title in enumerate(axes_args["column_titles"]):
        axs[0, j, 0, int(nc / 2)].set_title(title, **params)

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
    for i, title in enumerate(axes_args["row_titles"]):
        axs[i, -1, int(nr / 2), -1].annotate(title, **params)

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
