""" Adjust ax when there are 3 subplots """

from modules.axes_ticks import ticklabels_ax


def axes_adjust(data, image):
    """Adjust plots"""

    if data["ax_type"] != "AxesImage" or "adjust" not in data["layout"]:
        return

    distances = image["distances"]
    nrows = data["layout_i"]
    ncols = data["layout_j"]

    left_0 = image["margin_left"] / distances["width"]
    top_ax = (
        image["margin_bottom"]
        + (image["plot_size"] + image["margin_inner"]) * (nrows - 1.5)
    ) / distances["height"]

    image["axs"][1, 0, 0, 0].remove()
    ax = image["axs"][0, 0, 0, 0]
    ax.set_axes_locator(None)
    new_position = [
        left_0,
        top_ax,
        image["plot_size"] / distances["width"],
        image["plot_size"] / distances["height"],
    ]
    ax.set_position(new_position)
    ax.set_title(data["titles_columns"][0], fontsize=32, pad=214)

    if nrows == 2:
        ticklabels_ax(ax, image["ticklabels_y"], image["ticklabels_x"])
    else:
        image["axs"][2, 0, 0, 0].remove()
        ax = image["axs"][3, 0, 0, 0]
        ax.set_axes_locator(None)
        bottom_ax = (
            image["margin_bottom"] + (image["plot_size"] + image["margin_inner"]) * 0.5
        ) / distances["height"]
        new_position[1] = bottom_ax
        ax.set_position(new_position)

        if ncols == 5:

            left_1 = (
                left_0
                + (image["plot_size"] + image["margin_inner"]) / distances["width"]
            )

            image["axs"][2, 1, 0, 0].remove()
            ax = image["axs"][3, 1, 0, 0]
            ax.set_axes_locator(None)
            new_position[0] = left_1
            ax.set_position(new_position)

            image["axs"][1, 1, 0, 0].remove()
            ax = image["axs"][0, 1, 0, 0]
            ax.set_axes_locator(None)
            new_position[1] = top_ax
            ax.set_position(new_position)
            ax.set_title(data["titles_columns"][1], fontsize=32, pad=214)
