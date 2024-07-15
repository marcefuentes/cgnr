""" Adjust ax when there are 3 subplots """

from modules.add_ticks import add_ticklabels_ax


def adjust(axs, layout, title, ticklabels_x, ticklabels_y):
    """Adjust plots"""

    if layout in ("m03", "m05", "m06", "m10"):
        axs[1, 0, 0, 0].remove()
        ax = axs[0, 0, 0, 0]
        ax.set_axes_locator(None)
        if layout == "m03":
            new_position = (0.1787, 0.3433, 0.283, 0.315)
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)
        elif layout == "m05":
            new_position = (0.133, 0.3433, 0.213, 0.315)
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)
        elif layout == "m06":
            new_position = (0.1787, 0.5473, 0.283, 0.315)
            add_ticklabels_ax(ax, ticklabels_y, ["", "", ""])
        else:
            new_position = (0.133, 0.5473, 0.213, 0.315)
            add_ticklabels_ax(ax, ticklabels_y, ["", "", ""])
        ax.set_position(new_position)
        ax.set_title(title, fontsize=32, pad=215)

        if layout in ("m06", "m10"):
            axs[3, 0, 0, 0].remove()
            ax = axs[2, 0, 0, 0]
            ax.set_axes_locator(None)
            if layout == "m06":
                ax.set_position((0.1787, 0.1373, 0.283, 0.315))
            else:
                ax.set_position((0.133, 0.1373, 0.213, 0.315))
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)
