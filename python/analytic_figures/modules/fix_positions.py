
""" Fix positions for plots. """

from mpl_toolkits.axes_grid1 import Divider, Size

import modules.settings as ss

def create_divider(fig, measurements, nrows, ncols, nr=1, nc=1):
    """ Create divider. """

    spacing_fixed = Size.Fixed(ss.SPACING)
    plot_size_fixed = Size.Fixed(ss.PLOT_SIZE/nc)
    column_fixed = (
        [plot_size_fixed] * nc
        + ([spacing_fixed] + [plot_size_fixed] * nc) * (ncols - 1)
    )
    row_fixed = (
        [plot_size_fixed] * nr + ([spacing_fixed]
        + [plot_size_fixed] * nr) * (nrows - 1)
    )
    width = measurements["width"]
    height = measurements["height"]
    inner_width = measurements["inner_width"]
    inner_height = measurements["inner_height"]

    divider = Divider(
        fig,
        (ss.LEFT_MARGIN/width,
        ss.BOTTOM_MARGIN/height,
        inner_width/width,
        inner_height/height),
        column_fixed,
        row_fixed,
        aspect=False
    )

    return divider
