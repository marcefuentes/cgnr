""" Fix positions for plots. """

from mpl_toolkits.axes_grid1 import Divider, Size

import modules.settings as ss


def create_divider(fig, measurements, layout):
    """Create divider."""

    nr = layout.get("nr", 1)
    nc = layout.get("nc", 1)

    spacing_fixed = Size.Fixed(ss.SPACING)
    plot_size_fixed = Size.Fixed(ss.PLOT_SIZE / nc)
    column_fixed = [plot_size_fixed] * nc + (
        [spacing_fixed] + [plot_size_fixed] * nc
    ) * (layout["ncols"] - 1)
    row_fixed = [plot_size_fixed] * nr + ([spacing_fixed] + [plot_size_fixed] * nr) * (
        layout["nrows"] - 1
    )
    divider = Divider(
        fig,
        (
            ss.LEFT_MARGIN / measurements["width"],
            ss.BOTTOM_MARGIN / measurements["height"],
            measurements["inner_width"] / measurements["width"],
            measurements["inner_height"] / measurements["height"],
        ),
        column_fixed,
        row_fixed,
        aspect=False,
    )

    return divider
