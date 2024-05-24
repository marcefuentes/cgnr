"""Tools for prettifying axes."""


def add_letters(ax, position, params, n):
    """add letters."""

    letter = chr(ord("a") + n % 26)
    if n >= 26:
        letter = letter + letter
    ax.text(
        *position,
        s=letter,
        **params,
        transform=ax.transAxes,
    )


def add_ticklabels_imshow(axs, c_min, c_max, r_min, r_max):
    """add tick labels for (nrows x ncols)."""

    y_params = [f"{r_max:.1f}", f"{(r_min + r_max)/2.:.1f}", f"{r_min:.1f}"]
    x_params = [f"{c_min:.0f}", f"{(c_min + c_max)/2.:.0f}", f"{c_max:.0f}"]

    for ax in axs[:, 0, 0, 0]:
        ax.set_yticklabels(y_params)
    for ax in axs[-1, :, 0, 0]:
        ax.set_xticklabels(x_params)


def add_ticklabels_line2d(axs, r_values, c_values):
    """add tick labels for (nrows x ncols x nr x nc)."""

    y_range = range(0, axs.shape[2], axs.shape[2] // 2)
    x_range = range(0, axs.shape[3], axs.shape[3] // 2)

    for i in range(axs.shape[0]):
        for k in y_range:
            axs[i, 0, k, 0].set_yticklabels([f"{r_values[k]:.1f}"])
    for j in range(axs.shape[1]):
        for m in x_range:
            axs[-1, j, -1, m].set_xticklabels([f"{c_values[m]:.0f}"])


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


def set_spines(ax, linewidth, color):
    """Prettify ax spines."""

    for spine in ax.spines.values():
        spine.set_linewidth(linewidth)
        spine.set_color(color)
