""" Fix positions for plots. """

from numpy import ndindex
from mpl_toolkits.axes_grid1 import Divider, Size


def axes_place(image):
    """Create divider."""

    nrows, ncols, nr, nc = image["axs"].shape
    distances = image["distances"]

    spacing = Size.Fixed(image["margin_inner"])
    size = Size.Fixed(image["plot_size"] / nc)
    column = [size] * nc + ([spacing] + [size] * nc) * (ncols - 1)
    row = [size] * nr + ([spacing] + [size] * nr) * (nrows - 1)

    divider = Divider(
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

    for i, j, k, m in ndindex(image["axs"].shape):
        image["axs"][i, j, k, m].set(
            axes_locator=divider.new_locator(
                nx=j * (nc + 1) + m + int(m / nc),
                ny=(nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
            )
        )
