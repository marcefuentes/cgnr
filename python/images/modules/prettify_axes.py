""" Prettify axes. """

from modules.get_setting import get_setting as get
import modules.prettify_axes_tools as tools


def prettify_axes(axes_args):
    """prettify (nrows x ncols x nr x nc) matrix."""

    axs = axes_args["axs"]
    nrows, ncols, nr, nc = axs.shape

    # Prettify spines, reset ticks, set limits and position axes

    params = {
        "linewidth": get("COMMON", "border_width"),
        "color": get("COMMON", "border_color"),
    }

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    tools.set_spines(axs[i, j, k, m], **params)
                    axs[i, j, k, m].set(
                        xticks=[],
                        yticks=[],
                        xlim=axes_args["x_lim"],
                        ylim=axes_args["y_lim"],
                        axes_locator=axes_args["divider"].new_locator(
                            nx=j * (nc + 1) + m + int(m / nc),
                            ny=(nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
                        )
                    )

    # Add letters

    position = (0, 1.0 + get("COMMON", "letter_padding") * nr)
    params = {
        "fontsize": get("COMMON", "letter_label_size"),
        "weight": "bold",
    }
    for i in range(nrows):
        for j in range(ncols):
            tools.add_letters(
                axs[i, j, 0, 0], position, params, i * ncols + j
            )

    # Add column titles

    params = {
        "pad": get("COMMON", "plot_size") * get("COMMON", "title_padding"),
        "fontsize": get("COMMON", "letter_label_size"),
    }
    for j, title in enumerate(axes_args["column_titles"]):
        axs[0, j, 0, int(nc / 2)].set_title(title, **params)

    # Add row titles

    params = {
        "xy": (1, 0.5),
        "xycoords": "axes fraction",
        "xytext": (
            get("COMMON", "plot_size") * get("COMMON", "title_padding") * 3.5,
            0,
        ),
        "textcoords": "offset points",
        "va": "center",
        "ha": "left",
        "fontsize": get("COMMON", "letter_label_size"),
    }
    for i, title in enumerate(axes_args["row_titles"]):
        axs[i, -1, int(nr / 2), -1].annotate(title, **params)

    # Add ticks and tick labels

    params = {
        "labelsize": get("COMMON", "tick_label_size"),
        "size": get("COMMON", "tick_size"),
        "color": get("COMMON", "tick_color"),
    }
    if axs.shape[2] == 1:
        tools.add_ticks_imshow(
            axs, len(axes_args["c_values"]), len(axes_args["r_values"]), params
        )
        tools.add_ticklabels_imshow(
            axs,
            axes_args["c_values"][0],
            axes_args["c_values"][-1],
            axes_args["r_values"][-1],
            axes_args["r_values"][0],
        )
    else:
        tools.add_ticks_line2d(axs, params)
        tools.add_ticklabels_line2d(axs, axes_args["r_values"], axes_args["c_values"])
