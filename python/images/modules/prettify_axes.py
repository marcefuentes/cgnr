""" prettify axes. """

from modules.get_setting import get_setting as get


def add_letters(ax, position, fontsize, n):
    """add letters."""

    letter = chr(ord("a") + n % 26)
    if n >= 26:
        letter = letter + letter
    ax.text(
        0,
        position,
        letter,
        fontsize=fontsize,
        transform=ax.transAxes,
        weight="bold",
    )


def add_ticklabels_line2d(axs, r_values, c_values):
    """add tick labels for (nrows x ncols x nr x nc)."""

    y_range = range(0, axs.shape[2], axs.shape[2] // 2)
    x_range = range(0, axs.shape[3], axs.shape[3] // 2)

    for i in range(axs.shape[0]):
        for k in y_range:
            axs[i, 0, k, 0].set_yticklabels(
                [f"{r_values[k]:.1f}"]
            )
    for j in range(axs.shape[1]):
        for m in x_range:
            axs[-1, j, -1, m].set_xticklabels(
                [f"{c_values[m]:.0f}"]
            )


def add_ticklabels_imshow(axs, c_min, c_max, r_min, r_max):
    """add tick labels for (nrows x ncols)."""

    y_params = [f"{r_max:.1f}", f"{(r_min + r_max)/2.:.1f}", f"{r_min:.1f}"]
    x_params = [f"{c_min:.0f}", f"{(c_min + c_max)/2.:.0f}", f"{c_max:.0f}"]

    for ax in axs[:, 0, 0, 0]:
        ax.set_yticklabels(y_params)
    for ax in axs[-1, :, 0, 0]:
        ax.set_xticklabels(x_params)


def add_ticks_line2d(axs, format_params):
    """set ticks for (nrows x ncols x nr x nc)."""

    y_range = range(0, axs.shape[2], axs.shape[2] // 2)
    x_range = range(0, axs.shape[3], axs.shape[3] // 2)
    y_min, y_max = axs[0, 0, 0, 0].get_ylim()
    x_min, x_max = axs[0, 0, 0, 0].get_xlim()
    x_position_params = {
        "xticks": [(x_min + x_max) / 2],
        "xticklabels": [],
    }
    y_position_params = {
        "yticks": [(y_min + y_max) / 2],
        "yticklabels": [],
    }

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            for k in y_range:
                axs[i, j, k, 0].set(**y_position_params)
                axs[i, j, k, 0].tick_params(axis="y", **format_params)
            for m in x_range:
                axs[i, j, -1, m].set(**x_position_params)
                axs[i, j, -1, m].tick_params(axis="x", **format_params)


def add_ticks_imshow(axs, mc, mr, format_params):
    """set ticks for (nrows x ncols) matrix."""

    c_min, c_max = 0, mc - 1
    r_min, r_max = 0, mr - 1
    position_params = {
        "xticks": [c_min, c_max / 2, c_max],
        "yticks": [r_min, r_max / 2, r_max],
        "xticklabels": [],
        "yticklabels": [],
    }

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            axs[i, j, 0, 0].set(**position_params)
            axs[i, j, 0, 0].tick_params(axis="both", **format_params)


def prettify_axes(axes_args):
    """prettify (nrows x ncols x nr x nc) matrix."""

    axs = axes_args["axs"]
    nrows, ncols, nr, nc = axs.shape
    letter_position = 1.0 + get("COMMON", "letter_padding") * nr
    letter_size = get("COMMON", "letter_label_size")

    spine_linewidth = get("COMMON", "border_width")
    spine_color = get("COMMON", "border_color")

    for i in range(nrows):
        for j in range(ncols):
            add_letters(axs[i, j, 0, 0], letter_position, letter_size, i * ncols + j)
            for k in range(nr):
                for m in range(nc):
                    ax = axs[i, j, k, m]
                    for spine in ax.spines.values():
                        spine.set_linewidth(spine_linewidth)
                        spine.set_color(spine_color)
                    ax.set(xticks=[], yticks=[])
                    ax.set(xlim=axes_args["x_lim"], ylim=axes_args["y_lim"])
                    ax.set_axes_locator(axes_args["divider"].new_locator(
                        nx=j * (nc + 1) + m + int(m / nc),
                        ny=(nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
                    ))

    params = {
        "pad": get("COMMON", "plot_size") * get("COMMON", "title_padding"),
        "fontsize": get("COMMON", "letter_label_size"),
    }
    for j, title in enumerate(axes_args["column_titles"]):
        axs[0, j, 0, int(nc / 2)].set_title(
            title,
            **params,
        )

    params = {
        "xy": (1, 0.5),
        "xycoords": "axes fraction",
        "xytext": (get("COMMON", "plot_size") * get("COMMON", "title_padding") * 3.5, 0),
        "textcoords": "offset points",
        "va": "center",
        "ha": "left",
        "fontsize": get("COMMON", "letter_label_size"),
    }
    for i, title in enumerate(axes_args["row_titles"]):
        axs[i, -1, int(nr / 2), -1].annotate(title, **params)

    params = {
        "labelsize": get("COMMON", "tick_label_size"),
        "size": get("COMMON", "tick_size"),
        "color": get("COMMON", "tick_color"),
    }
    if axs.shape[2] == 1:
        add_ticks_imshow(axs, len(axes_args["c_values"]), len(axes_args["r_values"]), params)
        add_ticklabels_imshow(
            axs,
            axes_args["c_values"][0],
            axes_args["c_values"][-1],
            axes_args["r_values"][-1],
            axes_args["r_values"][0],
        )
    else:
        add_ticks_line2d(axs, params)
        add_ticklabels_line2d(axs, axes_args["r_values"], axes_args["c_values"])
