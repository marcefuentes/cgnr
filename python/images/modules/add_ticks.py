"""Format ticks."""


def add_ticklabels_ax(ax, ticklabels_y, ticklabels_x):
    """Add tick labels for a single line2d plot."""

    ax.set_xticklabels(ticklabels_x)
    ax.set_yticklabels(ticklabels_y)


def add_ticklabels_imshow(axs, ticklabels_y, ticklabels_x):
    """Add tick labels for (nrows x ncols)."""

    ticklabels_y = [f"{r:.1f}" for r in ticklabels_y]
    for ax in axs[:, 0, 0, 0]:
        ax.set_yticklabels(ticklabels_y)

    ticklabels_x = [f"{c:.0f}" for c in ticklabels_x]
    for ax in axs[-1, :, 0, 0]:
        ax.set_xticklabels(ticklabels_x)


def add_ticklabels_line2d(axs, ticklabels_y, ticklabels_x):
    """Add tick labels for (nrows x ncols x nr x nc)."""

    _range = range(0, axs.shape[2], axs.shape[2] // 2)
    for i in range(axs.shape[0]):
        for k, r_value in zip(_range, ticklabels_y):
            axs[i, 0, k, 0].set_yticklabels([f"{r_value:.1f}"])

    _range = range(0, axs.shape[3], axs.shape[3] // 2)
    for j in range(axs.shape[1]):
        for m, c_value in zip(_range, ticklabels_x):
            axs[-1, j, -1, m].set_xticklabels([f"{c_value:.0f}"])


def add_ticks_ax(ax, format_params):
    """Set ticks for a single line2d plot."""

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


def add_ticks_imshow(axs, nr, nc, format_params):
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


def ticks_imshow(axs, axes_args, format_params):
    """Format ticks for imshow plots."""

    add_ticks_imshow(axs, axes_args["nr"], axes_args["nc"], format_params)
    add_ticklabels_imshow(axs, axes_args["ticklabels_y"], axes_args["ticklabels_x"])


def ticks_line2d(axs, axes_args, format_params):
    """Format ticks for line2d plots."""

    add_ticks_line2d(axs, format_params)
    add_ticklabels_line2d(axs, axes_args["ticklabels_y"], axes_args["ticklabels_x"])


def ticks_ax(ax, axes_args, format_params):
    """Format ticks for a single line2d plot."""

    add_ticks_ax(ax, format_params)
    add_ticklabels_ax(ax, axes_args["ticklabels_y"], axes_args["ticklabels_x"])
