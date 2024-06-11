""" Prettify the figure. """

import os


def get_distances(nrows, ncols, image):
    """Calculate distances for figure."""

    inner_height = image["plot_size"] * nrows + image["spacing"] * (nrows - 1)
    inner_width = image["plot_size"] * ncols + image["spacing"] * (ncols - 1)
    width = image["left_margin"] + inner_width + image["right_margin"]
    height = image["top_margin"] + inner_height + image["bottom_margin"]
    distances = {
        "width": width,
        "height": height,
        "inner_width": inner_width,
        "inner_height": inner_height,
    }

    return distances


def format_fig(fig, distances, image, sm):
    """Format the figure."""

    fig.set_size_inches(distances["width"], distances["height"])
    fig.supxlabel(
        t=image["x_label"],
        x=(image["left_margin"] + distances["inner_width"] / 2) / distances["width"],
        y=image["bottom_margin"] / 2.5 / distances["height"],
        fontsize=image["suplabel_size"],
    )
    fig.supylabel(
        t=image["y_label"],
        x=image["left_margin"] / 2.8 / distances["width"],
        y=(image["bottom_margin"] + distances["inner_height"] / 2)
        / distances["height"],
        fontsize=image["suplabel_size"],
    )

    cax = fig.add_axes(
        [
            (
                image["left_margin"]
                + distances["inner_width"]
                + image["spacing"] * image["colorbar_right_position"]
            )
            / distances["width"],
            (
                image["bottom_margin"]
                + distances["inner_height"] / 2
                - image["colorbar_height"] / 2
            )
            / distances["height"],
            image["colorbar_width"] / distances["width"],
            image["colorbar_height"] / distances["height"],
        ]
    )  # [left, bottom, width, height]
    ticks = [-1, 0, 1]
    cbar = fig.colorbar(sm, cax=cax, ticks=ticks)
    cbar.ax.tick_params(**image["ticks"])
    cbar.outline.set(**image["colorbar"])

    if image["print_folder"]:
        bottom_text = os.path.basename(os.getcwd())
    else:
        bottom_text = ""
    fig.text(
        ha="right",
        s=bottom_text,
        x=(image["left_margin"] + distances["inner_width"]) / distances["width"],
        y=(image["bottom_margin"] - image["x_label_size"]) / distances["height"],
        **image["text"],
    )
