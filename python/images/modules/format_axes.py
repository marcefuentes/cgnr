""" Format axes. """

from modules.settings import SETTINGS as common
import modules.format_axes_tools as tools


def format_axes(axes_args):
    """format (nrows x ncols x nr x nc) matrix."""

    axs = axes_args["axs"]
    nrows, ncols, nr, nc = axs.shape

    # Format spines, reset ticks, set limits and position axes

    spine_params = {
        "linewidth": common["border_width"],
        "color": common["border_color"],
    }
    params = {
        "xticks": [],
        "yticks": [],
        "xlim": axes_args["x_lim"],
        "ylim": axes_args["y_lim"],
    }

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    ax = axs[i, j, k, m]
                    tools.format_spines(ax, **spine_params)
                    ax.set(**params)
                    ax.set(
                        axes_locator=axes_args["divider"].new_locator(
                            nx=j * (nc + 1) + m + int(m / nc),
                            ny=(nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
                        )
                    )

    # Add letters

    position = (0, 1.0 + common["letter_padding"] * nr)
    params = {
        "fontsize": common["letter_label_size"],
        "weight": "bold",
    }
    for i in range(nrows):
        for j in range(ncols):
            tools.add_letters(axs[i, j, 0, 0], position, params, i * ncols + j)

    # Add column titles

    params = {
        "pad": common["plot_size"] * common["title_padding"],
        "fontsize": common["letter_label_size"],
    }
    for j, title in enumerate(axes_args["column_titles"]):
        axs[0, j, 0, int(nc / 2)].set_title(title, **params)

    # Add row titles

    params = {
        "xy": (1, 0.5),
        "xycoords": "axes fraction",
        "xytext": (
            common["plot_size"] * common["title_padding"] * 3.5,
            0,
        ),
        "textcoords": "offset points",
        "va": "center",
        "ha": "left",
        "fontsize": common["letter_label_size"],
    }
    for i, title in enumerate(axes_args["row_titles"]):
        axs[i, -1, int(nr / 2), -1].annotate(title, **params)

    # Add ticks and tick labels

    params = {
        "labelsize": common["tick_label_size"],
        "size": common["tick_size"],
        "color": common["tick_color"],
    }
    if axs.shape[2] == 1:
        tools.add_ticks_imshow(axs, axes_args["nr"], axes_args["nc"], params)
        tools.add_ticklabels_imshow(axs, axes_args["r_values"], axes_args["c_values"])
    else:
        tools.add_ticks_line2d(axs, params)
        tools.add_ticklabels_line2d(axs, axes_args["r_values"], axes_args["c_values"])
