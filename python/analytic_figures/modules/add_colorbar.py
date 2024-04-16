""" Add colorbar. """

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt

import modules.settings as ss


def add_colorbar(fig, measurements, nc):
    """Add colorbar."""

    width = measurements["width"]
    height = measurements["height"]
    inner_width = measurements["inner_width"]
    inner_height = measurements["inner_height"]

    sm = ScalarMappable(cmap=ss.COLOR_MAP, norm=plt.Normalize(-1, 1))
    cax = fig.add_axes(
        [
            (ss.LEFT_MARGIN + inner_width + ss.SPACING * 2.5) / width,
            (ss.BOTTOM_MARGIN + inner_height / 2 - ss.PLOT_SIZE / 2) / height,
            (ss.PLOT_SIZE / nc) / width,
            ss.PLOT_SIZE / height,
        ]
    )  # [left, bottom, width, height]
    cbar = fig.colorbar(sm, cax=cax, ticks=[-1, 0, 1])
    cbar.ax.tick_params(labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE)
    cbar.outline.set_linewidth(ss.LINE_WIDTH)
