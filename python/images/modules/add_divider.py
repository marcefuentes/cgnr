""" Fix positions for plots. """

from mpl_toolkits.axes_grid1 import Divider, Size


def add_divider(image):
    """Create divider."""

    nrows = image["fig_layout"]["nrows"]
    ncols = image["fig_layout"]["ncols"]
    nr = image["fig_layout"]["nr"]
    nc = image["fig_layout"]["nc"]
    distances = image["distances"]

    spacing_fixed = Size.Fixed(image["margin_inner"])
    size_fixed = Size.Fixed(image["plot_size"] / nc)
    column_fixed = [size_fixed] * nc + (
        [spacing_fixed] + [size_fixed] * nc
    ) * (ncols - 1)
    row_fixed = [size_fixed] * nr + ([spacing_fixed] + [size_fixed] * nr) * (
        nrows - 1
    )
    image["divider"] = Divider(
        image["fig"],
        (
            image["margin_left"] / distances["width"],
            image["margin_bottom"] / distances["height"],
            distances["width_inner"] / distances["width"],
            distances["height_inner"] / distances["height"],
        ),
        column_fixed,
        row_fixed,
        aspect=False,
    )
