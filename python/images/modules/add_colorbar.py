""" Add colorbar. """

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt

import modules.settings as ss


def add_colorbar(fig, kwargs, nc):
    """Add colorbar."""

    sm = ScalarMappable(cmap=ss.COLOR_MAP, norm=plt.Normalize(-1, 1))
    cax = fig.add_axes(
        [
            (ss.LEFT_MARGIN + kwargs["inner_width"] + ss.SPACING * 2.5) / kwargs["width"],
            (ss.BOTTOM_MARGIN + kwargs["inner_height"] / 2 - ss.PLOT_SIZE / 2) / kwargs["height"],
            (ss.PLOT_SIZE / nc) / kwargs["width"],
            ss.PLOT_SIZE / kwargs["height"],
        ]
    )  # [left, bottom, width, height]
    cbar = fig.colorbar(sm, cax=cax, ticks=[-1, 0, 1])
    cbar.ax.tick_params(
        labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE, color=ss.TICK_COLOR
    )
    cbar.outline.set_linewidth(ss.BORDER_WIDTH)
    cbar.outline.set_edgecolor(ss.BORDER_COLOR)
