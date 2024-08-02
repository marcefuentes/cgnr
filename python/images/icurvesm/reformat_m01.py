"""Format axes for layout m01."""

from modules.add_ax_labels import add_ax_labels
from modules.add_ticks import ticks_ax_line2d


def reformat_m01(image):
    """Format axes for layout m01."""

    add_ax_labels(
        image["axs"][0, 0, 0, 0],
        image["label_x_0"],
        image["label_y_0"],
        image["titles_columns_params"]["fontsize"],
        image["labelpad"],
    )
    add_ax_labels(
        image["axs"][0, 1, 0, 0],
        image["label_x_1"],
        image["label_y_1"],
        image["titles_columns_params"]["fontsize"],
        image["labelpad"],
    )
    image["ticklabels_x"] = [0.0, 0.5, 1.0]
    image["ticklabels_y"] = [0.0, 0.5, 1.0]
    ticks_ax_line2d(
        image["axs"][0, 0, 0, 0],
        image["ticklabels_y"],
        image["ticklabels_x"],
        image["ticks"],
    )
    ticks_ax_line2d(
        image["axs"][0, 1, 0, 0],
        image["ticklabels_y"],
        image["ticklabels_x"],
        image["ticks"],
    )
