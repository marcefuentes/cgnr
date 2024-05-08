""" Prettify the figure. """

import os

from modules.get_setting import get_setting as get


def get_distances(nrows, ncols):
    """Calculate distances for figure."""

    inner_height = get("COMMON", "plot_size") * nrows + get("COMMON", "spacing") * (
        nrows - 1
    )
    inner_width = get("COMMON", "plot_size") * ncols + get("COMMON", "spacing") * (
        ncols - 1
    )
    width = get("COMMON", "left_margin") + inner_width + get("COMMON", "right_margin")
    height = get("COMMON", "top_margin") + inner_height + get("COMMON", "bottom_margin")
    distances = {
        "width": width,
        "height": height,
        "inner_width": inner_width,
        "inner_height": inner_height,
    }

    return distances


def prettify_fig(fig, distances, section, sm):
    """prettify the figure."""

    fig.set_size_inches(distances["width"], distances["height"])
    fig.supxlabel(
        t=get("COMMON", "x_label"),
        x=(get("COMMON", "left_margin") + distances["inner_width"] / 2)
        / distances["width"],
        y=get("COMMON", "bottom_margin") / 2.5 / distances["height"],
        fontsize=get("COMMON", "big_label_size"),
    )
    fig.supylabel(
        t=get("COMMON", "y_label"),
        x=get("COMMON", "left_margin") / 2.8 / distances["width"],
        y=(get("COMMON", "bottom_margin") + distances["inner_height"] / 2)
        / distances["height"],
        fontsize=get("COMMON", "big_label_size"),
    )

    cax = fig.add_axes(
        [
            (
                get("COMMON", "left_margin")
                + distances["inner_width"]
                + get("COMMON", "spacing") * get(section, "colorbar_right_position")
            )
            / distances["width"],
            (
                get("COMMON", "bottom_margin")
                + distances["inner_height"] / 2
                - get("COMMON", "plot_size") / 2
            )
            / distances["height"],
            (get("COMMON", "plot_size") / get(section, "colorbar_width"))
            / distances["width"],
            get("COMMON", "plot_size") / distances["height"],
        ]
    )  # [left, bottom, width, height]
    ticks = [-1, 0, 1]
    cbar = fig.colorbar(sm, cax=cax, ticks=ticks)
    cbar.ax.tick_params(
        labelsize=get("COMMON", "tick_label_size"),
        size=get("COMMON", "tick_size"),
        color=get("COMMON", "tick_color"),
    )
    cbar.outline.set_linewidth(get("COMMON", "border_width"))
    cbar.outline.set_edgecolor(get("COMMON", "border_color"))

    if get(section, "print_folder"):
        bottom_text = os.path.basename(os.getcwd())
    else:
        bottom_text = ""
    fig.text(
        x=(get("COMMON", "left_margin") + distances["inner_width"])
        / distances["width"],
        y=(get("COMMON", "bottom_margin") - get("COMMON", "x_label_size"))
        / distances["height"],
        s=bottom_text,
        fontsize=get("COMMON", "tick_label_size"),
        color="grey",
        ha="right",
    )
