""" prettify axes. """

from modules.get_setting import get_setting as get


def add_letters(ax, letter_position, n):
    """add letters."""

    letter = chr(ord("a") + n % 26)
    if n >= 26:
        letter = letter + letter
    ax.text(
        0,
        letter_position,
        letter,
        fontsize=get("COMMON", "letter_label_size"),
        transform=ax.transAxes,
        weight="bold",
    )


def add_ticklabels(axes_args):
    """add tick labels for (nrows x ncols x nr x nc)."""

    nrows, ncols, nr, nc = axes_args["axs"].shape

    if nr == 1:
        add_ticklabels_imshow(axes_args)
        return

    for i in range(nrows):
        for k in range(0, nr, nr // 2):
            axes_args["axs"][i, 0, k, 0].set_yticklabels(
                [f"{axes_args['r_values'][k]:.1f}"]
            )
    for j in range(ncols):
        for m in range(0, nc, nc // 2):
            axes_args["axs"][-1, j, -1, m].set_xticklabels(
                [f"{axes_args['c_values'][m]:.0f}"]
            )


def add_ticklabels_imshow(axes_args):
    """add tick labels for (nrows x ncols)."""

    c_min = axes_args["c_values"][0]
    c_max = axes_args["c_values"][-1]
    r_min = axes_args["r_values"][-1]
    r_max = axes_args["r_values"][0]

    for ax in axes_args["axs"][:, 0, 0, 0]:
        ax.set_yticklabels(
            [f"{r_max:.1f}", f"{(r_min + r_max)/2.:.1f}", f"{r_min:.1f}"]
        )
    for ax in axes_args["axs"][-1, :, 0, 0]:
        ax.set_xticklabels(
            [f"{c_min:.0f}", f"{(c_min + c_max)/2.:.0f}", f"{c_max:.0f}"]
        )


def add_ticks(axes_args):
    """set ticks for (nrows x ncols x nr x nc)."""

    axs = axes_args["axs"]
    nrows, ncols, nr, nc = axs.shape

    if nr == 1:
        add_ticks_imshow(axes_args)
        return

    x_range = range(0, nr, nr // 2)
    y_range = range(0, nc, nc // 2)
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
    format_params = {
        "labelsize": get("COMMON", "tick_label_size"),
        "size": get("COMMON", "tick_size"),
        "color": get("COMMON", "tick_color"),
    }

    for i in range(nrows):
        for j in range(ncols):
            for k in x_range:
                axs[i, j, k, 0].set(**y_position_params)
                axs[i, j, k, 0].tick_params(axis="y", **format_params)
            for m in y_range:
                axs[i, j, -1, m].set(**x_position_params)
                axs[i, j, -1, m].tick_params(axis="x", **format_params)


def add_ticks_imshow(axes_args):
    """set ticks for (nrows x ncols) matrix."""

    c_min, c_max = 0, len(axes_args["c_values"]) - 1
    r_min, r_max = 0, len(axes_args["r_values"]) - 1
    position_params = {
        "xticks": [c_min, c_max / 2, c_max],
        "yticks": [r_min, r_max / 2, r_max],
        "xticklabels": [],
        "yticklabels": [],
    }
    format_params = {
        "axis": "both",
        "labelsize": get("COMMON", "tick_label_size"),
        "size": get("COMMON", "tick_size"),
        "color": get("COMMON", "tick_color"),
    }

    axs = axes_args["axs"]
    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            axs[i, j, 0, 0].set(**position_params)
            axs[i, j, 0, 0].tick_params(**format_params)


def add_title_column(ax, title):
    """add title."""

    ax.set_title(
        title,
        pad=get("COMMON", "plot_size") * get("COMMON", "title_padding"),
        fontsize=get("COMMON", "letter_label_size"),
    )


def add_title_row(ax, title):
    """add title."""

    ax.annotate(
        title,
        xy=(1, 0.5),
        xycoords="axes fraction",
        xytext=(get("COMMON", "plot_size") * get("COMMON", "title_padding") * 3.5, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        fontsize=get("COMMON", "letter_label_size"),
    )


def prettify_axes(axes_args):
    """prettify (nrows x ncols x nr x nc) matrix."""

    nrows, ncols, nr, nc = axes_args["axs"].shape
    letter_position = 1.0 + get("COMMON", "letter_padding") * nr

    for i in range(nrows):
        for j in range(ncols):
            add_letters(axes_args["axs"][i, j, 0, 0], letter_position, i * ncols + j)
            for k in range(nr):
                for m in range(nc):
                    set_spines(axes_args["axs"][i, j, k, m])
                    set_locator(
                        axes_args["axs"][i, j, k, m],
                        axes_args["divider"],
                        j * (nc + 1) + m + int(m / nc),
                        (nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
                    )
                    remove_ticks(axes_args["axs"][i, j, k, m])
                    set_limits(
                        axes_args["axs"][i, j, k, m],
                        axes_args["x_lim"],
                        axes_args["y_lim"],
                    )

    for j, title in enumerate(axes_args["column_titles"]):
        add_title_column(axes_args["axs"][0, j, 0, int(nc / 2)], title)
    for i, title in enumerate(axes_args["row_titles"]):
        add_title_row(axes_args["axs"][i, -1, int(nr / 2), -1], title)
    add_ticks(axes_args)
    add_ticklabels(axes_args)


def remove_ticks(ax):
    """remove ticks."""

    ax.set(xticks=[], yticks=[])


def set_limits(ax, xlim, ylim):
    """set limits."""

    ax.set(xlim=xlim, ylim=ylim)


def set_locator(ax, divider, nx, ny):
    """set locator."""

    ax.set_axes_locator(divider.new_locator(nx=nx, ny=ny))


def set_spines(ax):
    """set spines."""

    for spine in ax.spines.values():
        spine.set_linewidth(get("COMMON", "border_width"))
        spine.set_color(get("COMMON", "border_color"))
