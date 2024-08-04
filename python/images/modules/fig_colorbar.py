""" Add colorbar to the figure """


def fig_colorbar(image, sm):
    """Add colorbar to the figure"""

    distances = image["distances"]

    cax = image["fig"].add_axes(
        [
            (
                image["margin_left"]
                + distances["width_inner"]
                + image["margin_inner"] * image["colorbar_position_right"]
            )
            / distances["width"],
            (
                image["margin_bottom"]
                + distances["height_inner"] / 2
                - image["colorbar_height"] / 2
            )
            / distances["height"],
            image["colorbar_width"] / distances["width"],
            image["colorbar_height"] / distances["height"],
        ]
    )  # [left, bottom, width, height]
    ticks = [-1, 0, 1]
    cbar = image["fig"].colorbar(sm, cax=cax, ticks=ticks)
    cbar.ax.tick_params(**image["ticks"])
    cbar.outline.set(**image["colorbar"])
