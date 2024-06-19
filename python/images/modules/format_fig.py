""" Prettify the figure. """

import os


def get_distances(nrows, ncols, image):
    """Calculate distances for figure."""

    height_inner = image["plot_size"] * nrows + image["margin_inner"] * (nrows - 1)
    width_inner = image["plot_size"] * ncols + image["margin_inner"] * (ncols - 1)
    width = image["margin_left"] + width_inner + image["margin_right"]
    height = image["margin_top"] + height_inner + image["margin_bottom"]
    distances = {
        "height": height,
        "height_inner": height_inner,
        "width": width,
        "width_inner": width_inner,
    }

    return distances


def format_fig(fig, distances, image):
    """Format the figure."""

    # Size

    fig.set_size_inches(distances["width"], distances["height"])

    # Sup labels

    fig.supxlabel(
        t=image["suplabel_x"],
        x=(image["margin_left"] + distances["width_inner"] / 2) / distances["width"],
        y=image["margin_bottom"] / 2.5 / distances["height"],
        fontsize=image["suplabel_size"],
    )
    fig.supylabel(
        t=image["suplabel_y"],
        x=image["margin_left"] / 2.8 / distances["width"],
        y=(image["margin_bottom"] + distances["height_inner"] / 2)
        / distances["height"],
        fontsize=image["suplabel_size"],
    )

    # Text

    if image["print_folder"]:
        bottom_text = os.path.basename(os.getcwd())
    else:
        bottom_text = ""
    fig.text(
        ha="right",
        s=bottom_text,
        x=(image["margin_left"] + distances["width_inner"]) / distances["width"],
        y=(image["margin_bottom"] - image["suplabel_size"])
        / distances["height"]
        / 18.0,
        **image["text"],
    )
