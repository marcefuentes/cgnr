""" Adjust the positions of odd number of plots in a column """

from modules.axes_ticks import ticklabels_ax


def axes_adjust(data, image):
    """Adjust plots"""

    if data["ax_type"] != "AxesImage" or "adjust" not in data["layout"]:
        return

    nrows = data["layout_i"]
    ncols = data["layout_j"]

    plot_size = image["plot_size"]
    margin_inner = image["margin_inner"]
    margin_left = image["margin_left"]
    margin_bottom = image["margin_bottom"]

    left_pos = margin_left
    top_pos = margin_bottom + (plot_size + margin_inner) * (nrows - 1.5)

    # Adjust the main axis
    image["axs"][1, 0, 0, 0].remove()
    ax = image["axs"][0, 0, 0, 0]
    ax.set_axes_locator(None)
    new_position = [
        left_pos / image["distances"]["width"],
        top_pos / image["distances"]["height"],
        plot_size / image["distances"]["width"],
        plot_size / image["distances"]["height"]
    ]
    ax.set_position(new_position)
    ax.set_title(data["titles_columns"][0], fontsize=32, pad=214)

    if nrows == 2:
        ticklabels_ax(ax, image["ticklabels_y"], image["ticklabels_x"])
    else:
        # Adjust the bottom axis
        image["axs"][2, 0, 0, 0].remove()
        ax = image["axs"][3, 0, 0, 0]
        ax.set_axes_locator(None)
        bottom_pos = margin_bottom + (plot_size + margin_inner) * 0.5
        new_position[1] = bottom_pos / image["distances"]["height"]
        ax.set_position(new_position)

        if ncols == 5:
            left_1 = left_pos + (plot_size + margin_inner)

            # Adjust the top right axis
            image["axs"][1, 1, 0, 0].remove()
            ax = image["axs"][0, 1, 0, 0]
            ax.set_axes_locator(None)
            new_position[0] = left_1 / image["distances"]["width"]
            new_position[1] = top_pos / image["distances"]["height"]
            ax.set_position(new_position)
            ax.set_title(data["titles_columns"][1], fontsize=32, pad=214)

            # Adjust the bottom right axis
            image["axs"][2, 1, 0, 0].remove()
            ax = image["axs"][3, 1, 0, 0]
            ax.set_axes_locator(None)
            new_position[1] = bottom_pos / image["distances"]["height"]
            ax.set_position(new_position)
