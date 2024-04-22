""" Add colorbar. """

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt

import modules.settings as ss

def add_colorbar_icurves(axs):
    norm = Normalize(vmin=0, vmax=1)
    axins = inset_axes(axes_args["axs"][0, -1, -1],
        width="5%",
        height="100%",
        loc="upper right",
        bbox_to_anchor=(880, 200, 200, 200),
        borderpad=0)
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap="Reds"),
        cax=axins,
        ticks=[0, 0.5, 1])
    cbar.ax.tick_params(labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE, color=ss.TICK_COLOR)
    cbar.outline.set_linewidth(ss.LINE_WIDTH)

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
    cbar.ax.tick_params(labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE, color=ss.TICK_COLOR)
    cbar.outline.set_linewidth(ss.LINE_WIDTH)
