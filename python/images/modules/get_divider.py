""" Fix positions for plots. """

from mpl_toolkits.axes_grid1 import Divider, Size


def get_divider(image):
    """Create divider."""

    layout = image["fig_layout"]
    nr = layout["nr"]
    nc = layout["nc"]
    distances = image["distances"]

    spacing_fixed = Size.Fixed(image["margin_inner"])
    plot_size_fixed = Size.Fixed(image["plot_size"] / nc)
    column_fixed = [plot_size_fixed] * nc + (
        [spacing_fixed] + [plot_size_fixed] * nc
    ) * (layout["ncols"] - 1)
    row_fixed = [plot_size_fixed] * nr + ([spacing_fixed] + [plot_size_fixed] * nr) * (
        layout["nrows"] - 1
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
