""" Fix positions for plots. """

from mpl_toolkits.axes_grid1 import Divider, Size


def add_divider(image):
    """Create divider."""

    nrows = image["fig_layout"]["nrows"]
    ncols = image["fig_layout"]["ncols"]
    nr = image["fig_layout"]["nr"]
    nc = image["fig_layout"]["nc"]
    distances = image["distances"]

    spacing = Size.Fixed(image["margin_inner"])
    size = Size.Fixed(image["plot_size"] / nc)
    column = [size] * nc + ([spacing] + [size] * nc) * (ncols - 1)
    row = [size] * nr + ([spacing] + [size] * nr) * (nrows - 1)

    image["divider"] = Divider(
        image["fig"],
        (
            image["margin_left"] / distances["width"],
            image["margin_bottom"] / distances["height"],
            distances["width_inner"] / distances["width"],
            distances["height_inner"] / distances["height"],
        ),
        column,
        row,
        aspect=False,
    )
