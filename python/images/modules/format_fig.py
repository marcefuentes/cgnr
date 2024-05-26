""" Prettify the figure. """

import os

from modules.settings import SETTINGS as common


def get_distances(nrows, ncols):
    """Calculate distances for figure."""

    inner_height = common["plot_size"] * nrows + common["spacing"] * (
        nrows - 1
    )
    inner_width = common["plot_size"] * ncols + common["spacing"] * (
        ncols - 1
    )
    width = common["left_margin"] + inner_width + common["right_margin"]
    height = common["top_margin"] + inner_height + common["bottom_margin"]
    distances = {
        "width": width,
        "height": height,
        "inner_width": inner_width,
        "inner_height": inner_height,
    }

    return distances


def format_fig(fig, distances, exclusive, sm):
    """format the figure."""

    fig.set_size_inches(distances["width"], distances["height"])
    fig.supxlabel(
        t=common["x_label"],
        x=(common["left_margin"] + distances["inner_width"] / 2)
        / distances["width"],
        y=common["bottom_margin"] / 2.5 / distances["height"],
        fontsize=common["big_label_size"],
    )
    fig.supylabel(
        t=common["y_label"],
        x=common["left_margin"] / 2.8 / distances["width"],
        y=(common["bottom_margin"] + distances["inner_height"] / 2)
        / distances["height"],
        fontsize=common["big_label_size"],
    )

    cax = fig.add_axes(
        [
            (
                common["left_margin"]
                + distances["inner_width"]
                + common["spacing"] * exclusive["colorbar_right_position"]
            )
            / distances["width"],
            (
                common["bottom_margin"]
                + distances["inner_height"] / 2
                - common["plot_size"] / 2
            )
            / distances["height"],
            (common["plot_size"] / exclusive["colorbar_width"])
            / distances["width"],
            common["plot_size"] / distances["height"],
        ]
    )  # [left, bottom, width, height]
    ticks = [-1, 0, 1]
    cbar = fig.colorbar(sm, cax=cax, ticks=ticks)
    cbar.ax.tick_params(
        labelsize=common["tick_label_size"],
        size=common["tick_size"],
        color=common["tick_color"],
    )
    cbar.outline.set_linewidth(common["border_width"])
    cbar.outline.set_edgecolor(common["border_color"])

    if exclusive["print_folder"]:
        bottom_text = os.path.basename(os.getcwd())
    else:
        bottom_text = ""
    fig.text(
        x=(common["left_margin"] + distances["inner_width"])
        / distances["width"],
        y=(common["bottom_margin"] - common["x_label_size"])
        / distances["height"],
        s=bottom_text,
        fontsize=common["tick_label_size"],
        color="grey",
        ha="right",
    )
