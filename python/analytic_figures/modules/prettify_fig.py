""" Prettify the figure. """

import os

import modules.settings as ss


def create_measurements(nrows, ncols):
    """Create measurements for figure."""

    inner_height = ss.PLOT_SIZE * nrows + ss.SPACING * (nrows - 1)
    inner_width = ss.PLOT_SIZE * ncols + ss.SPACING * (ncols - 1)
    width = inner_width + ss.LEFT_MARGIN + ss.RIGHT_MARGIN
    height = inner_height + ss.TOP_MARGIN + ss.BOTTOM_MARGIN
    measurements = {
        "width": width,
        "height": height,
        "inner_width": inner_width,
        "inner_height": inner_height,
    }

    return measurements


def prettify_fig(fig, measurements):
    """Prettify the figure."""

    width = measurements["width"]
    height = measurements["height"]
    inner_width = measurements["inner_width"]
    inner_height = measurements["inner_height"]

    fig.supxlabel(
        t=ss.X_LABEL,
        x=(ss.LEFT_MARGIN + inner_width / 2) / width,
        y=(ss.BOTTOM_MARGIN - ss.X_LABEL_SIZE) / height,
        fontsize=ss.BIG_LABEL_SIZE,
    )
    fig.supylabel(
        t=ss.Y_LABEL,
        x=(ss.LEFT_MARGIN - ss.Y_LABEL_SIZE) / width,
        y=(ss.BOTTOM_MARGIN + inner_height / 2) / height,
        fontsize=ss.BIG_LABEL_SIZE,
    )

    if ss.PRINT_FOLDER:
        bottom_text = os.path.basename(os.getcwd())
    else:
        bottom_text = ""
    fig.text(
        x=(ss.LEFT_MARGIN + inner_width) / width,
        y=(ss.BOTTOM_MARGIN - ss.X_LABEL_SIZE) / height,
        s=bottom_text,
        fontsize=ss.TICK_LABEL_SIZE,
        color="grey",
        ha="right",
    )
