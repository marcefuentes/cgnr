""" Fix positions for plots. """

from mpl_toolkits.axes_grid1 import Divider, Size

from modules.get_setting import get_setting as get


def create_divider(fig, measurements, layout):
    """Create divider."""

    if layout["nested"]:
        nr = layout["nr"]
        nc = layout["nc"]
    else:
        nr = 1
        nc = 1

    spacing_fixed = Size.Fixed(get("COMMON", "spacing"))
    plot_size_fixed = Size.Fixed(get("COMMON", "plot_size") / nc)
    column_fixed = [plot_size_fixed] * nc + (
        [spacing_fixed] + [plot_size_fixed] * nc
    ) * (layout["ncols"] - 1)
    row_fixed = [plot_size_fixed] * nr + ([spacing_fixed] + [plot_size_fixed] * nr) * (
        layout["nrows"] - 1
    )
    divider = Divider(
        fig,
        (
            get("COMMON", "left_margin") / measurements["width"],
            get("COMMON", "bottom_margin") / measurements["height"],
            measurements["inner_width"] / measurements["width"],
            measurements["inner_height"] / measurements["height"],
        ),
        column_fixed,
        row_fixed,
        aspect=False,
    )

    return divider
