""" Fix positions for plots. """

from mpl_toolkits.axes_grid1 import Divider, Size

from modules.settings import SETTINGS as common


def create_divider(fig, layout, distances):
    """Create divider."""

    nr = layout["nr"]
    nc = layout["nc"]

    spacing_fixed = Size.Fixed(common["spacing"])
    plot_size_fixed = Size.Fixed(common["plot_size"] / nc)
    column_fixed = [plot_size_fixed] * nc + (
        [spacing_fixed] + [plot_size_fixed] * nc
    ) * (layout["ncols"] - 1)
    row_fixed = [plot_size_fixed] * nr + ([spacing_fixed] + [plot_size_fixed] * nr) * (
        layout["nrows"] - 1
    )
    divider = Divider(
        fig,
        (
            common["left_margin"] / distances["width"],
            common["bottom_margin"] / distances["height"],
            distances["inner_width"] / distances["width"],
            distances["inner_height"] / distances["height"],
        ),
        column_fixed,
        row_fixed,
        aspect=False,
    )

    return divider
