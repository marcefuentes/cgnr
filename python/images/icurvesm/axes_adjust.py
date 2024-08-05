"""Format axes for layout m01."""

from modules.axes_labels import axes_labels
from modules.axes_ticks import ticks_ax_line2d


def axes_adjust(data, image):
    """Format axes for layout m01."""

    if data["layout"] != "m01":
        return

    axes_labels(
        image["axs"][0, 0, 0, 0],
        image["label_x_0"],
        image["label_y_0"],
        image["titles_columns_params"]["fontsize"],
        image["labelpad"],
    )
    axes_labels(
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
