"""Format ticks."""


def add_ticklabels_ax(ax, ticklabels_y, ticklabels_x):
    """Add tick labels for a single Line2D plot."""

    ax.set_xticklabels(ticklabels_x)
    ax.set_yticklabels(ticklabels_y)


def add_ticklabels_axesimage(axs, ticklabels_y, ticklabels_x):
    """Add tick labels for (nrows x ncols)."""

    for ax in axs[:, 0, 0, 0]:
        ax.set_yticklabels(ticklabels_y)

    for ax in axs[-1, :, 0, 0]:
        ax.set_xticklabels(ticklabels_x)


def add_ticklabels_line2d(axs, ticklabels_y, ticklabels_x):
    """Add tick labels for (nrows x ncols x nr x nc)."""

    _range = range(0, axs.shape[2], axs.shape[2] // 2)
    for i in range(axs.shape[0]):
        for k, r_value in zip(_range, ticklabels_y):
            axs[i, 0, k, 0].set_yticklabels([r_value])

    _range = range(0, axs.shape[3], axs.shape[3] // 2)
    for j in range(axs.shape[1]):
        for m, c_value in zip(_range, ticklabels_x):
            axs[-1, j, -1, m].set_xticklabels([c_value])


def add_ticks_ax_line2d(ax, format_params):
    """Set ticks for a single Line2D plot."""

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    position_params = {
        "xticks": [x_min, (x_min + x_max) / 2, x_max],
        "xticklabels": [],
        "yticks": [y_min, (y_min + y_max) / 2, y_max],
        "yticklabels": [],
    }

    ax.set(**position_params)
    ax.tick_params(axis="both", **format_params)


def add_ticks_axesimage(axs, nr, nc, format_params):
    """Set ticks for (nrows x ncols) matrix."""

    r_min, r_max = 0, nr - 1
    c_min, c_max = 0, nc - 1
    position_params = {
        "xticks": [c_min, c_max / 2, c_max],
        "yticks": [r_min, r_max / 2, r_max],
        "xticklabels": [],
        "yticklabels": [],
    }
    format_params["axis"] = "both"
    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            axs[i, j, 0, 0].set(**position_params)
            axs[i, j, 0, 0].tick_params(**format_params)


def add_ticks_line2d(axs, format_params):
    """Set ticks for (nrows x ncols x nr x nc)."""

    x_range = range(0, axs.shape[3], axs.shape[3] // 2)
    y_range = range(0, axs.shape[2], axs.shape[2] // 2)
    x_min, x_max = axs[0, 0, 0, 0].get_xlim()
    y_min, y_max = axs[0, 0, 0, 0].get_ylim()
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


def ticks_ax_line2d(ax, ticklabels_x, ticklabels_y, format_params):
    """Format ticks for a single Line2D plot."""

    add_ticks_ax_line2d(ax, format_params)
    add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)


def ticks_axesimage(image, format_params):
    """Format ticks for AxesImage plots."""

    add_ticks_axesimage(image["axs"], image["nr"], image["nc"], format_params)
    add_ticklabels_axesimage(
        image["axs"], image["ticklabels_y"], image["ticklabels_x"]
    )


def ticks_line2d(image, format_params):
    """Format ticks for Line2D plots."""

    add_ticks_line2d(image["axs"], format_params)
    add_ticklabels_line2d(
        image["axs"], image["ticklabels_y"], image["ticklabels_x"]
    )
