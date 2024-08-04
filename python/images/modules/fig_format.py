""" Prettify the figure. """

import os


def fig_format(image):
    """Format the figure."""

    fig = image["fig"]
    distances = image["distances"]

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

    # Text (folder name or movie time)

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
