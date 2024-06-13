"""Format ticks."""


def add_ticklabels_imshow(axs, r_labels, c_labels):
    """Add tick labels for (nrows x ncols)."""

    r_labels = [f"{r:.1f}" for r in r_labels]
    for ax in axs[:, 0, 0, 0]:
        ax.set_yticklabels(r_labels)

    c_labels = [f"{c:.0f}" for c in c_labels]
    for ax in axs[-1, :, 0, 0]:
        ax.set_xticklabels(c_labels)


def add_ticklabels_line2d(axs, r_labels, c_labels):
    """Add tick labels for (nrows x ncols x nr x nc)."""

    _range = range(0, axs.shape[2], axs.shape[2] // 2)
    for i in range(axs.shape[0]):
        for k, r_value in zip(_range, r_labels):
            axs[i, 0, k, 0].set_yticklabels([f"{r_value:.1f}"])

    _range = range(0, axs.shape[3], axs.shape[3] // 2)
    for j in range(axs.shape[1]):
        for m, c_value in zip(_range, c_labels):
            axs[-1, j, -1, m].set_xticklabels([f"{c_value:.0f}"])


def add_ticklabels_unit(ax, r_labels, c_labels):
    """Add tick labels for a single line2d plot."""

    ax.set_xticklabels(c_labels)
    ax.set_yticklabels(r_labels)


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


def add_ticks_unit(ax, format_params):
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


def ticks_imshow(axs, axes_args, image):
    """Format ticks for imshow plots."""

    add_ticks_imshow(axs, axes_args["nr"], axes_args["nc"], image["ticks"])
    add_ticklabels_imshow(axs, axes_args["r_labels"], axes_args["c_labels"])


def ticks_line2d(axs, axes_args, image):
    """Format ticks for line2d plots."""

    add_ticks_line2d(axs, image["ticks"])
    add_ticklabels_line2d(axs, axes_args["r_labels"], axes_args["c_labels"])


def ticks_unit(axs, axes_args, image):
    """Format ticks for a single line2d plot."""

    add_ticks_unit(axs, image["ticks"])
    add_ticklabels_unit(axs, axes_args["r_labels"], axes_args["c_labels"])
