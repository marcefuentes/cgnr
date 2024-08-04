"""Add distances to image."""


def add_distances(image):
    """Calculate distances for figure."""

    nrows = image["fig_layout"]["nrows"]
    ncols = image["fig_layout"]["ncols"]
    height_inner = image["plot_size"] * nrows + image["margin_inner"] * (nrows - 1)
    width_inner = image["plot_size"] * ncols + image["margin_inner"] * (ncols - 1)
    width = image["margin_left"] + width_inner + image["margin_right"]
    height = image["margin_top"] + height_inner + image["margin_bottom"]
    image["distances"] = {
        "height": height,
        "height_inner": height_inner,
        "width": width,
        "width_inner": width_inner,
    }


