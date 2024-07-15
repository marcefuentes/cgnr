""" Adjust ax when there are 3 subplots """

from modules.add_ticks import add_ticklabels_ax


def adjust(axs, options, image, ticklabels_x, ticklabels_y):
    """Adjust plots"""

    if options["layout"] in ("m03", "m05", "m06", "m10", "m16r"):
        axs[1, 0, 0, 0].remove()
        ax = axs[0, 0, 0, 0]
        ax.set_axes_locator(None)

        if options["layout"] == "m03":
            width = 14.05
            height = 13.75
            n = 1
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)
        elif options["layout"] == "m05":
            width = 18.8
            height = 13.75
            n = 1
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)
        elif options["layout"] == "m06":
            width = 14.05
            height = 23.25
            n = 3
            add_ticklabels_ax(ax, ticklabels_y, ["", "", ""])
        elif options["layout"] == "m10":
            width = 18.8
            height = 23.25
            n = 3
            add_ticklabels_ax(ax, ticklabels_y, ["", "", ""])
        else:
            width = 28.3
            height = 23.25
            n = 3
            add_ticklabels_ax(ax, ticklabels_y, ["", "", ""])
        new_position = (2.5/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315)
                
        ax.set_position(new_position)
        ax.set_title(options["titles_columns"][0], fontsize=32, pad=214)

        if options["layout"] in ("m06", "m10", "m16r"):
            axs[2, 0, 0, 0].remove()
            ax = axs[3, 0, 0, 0]
            ax.set_axes_locator(None)
            n = 1
            new_position = (2.5/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315)
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)
            ax.set_position(new_position)

        if options["layout"] == "m16r":
            axs[1, 1, 0, 0].remove()
            ax = axs[0, 1, 0, 0]
            ax.set_axes_locator(None)
            n = 3
            ax.set_position(((2.5 + 4.0 + 0.75)/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315))
            ax.set_title(options["titles_columns"][1], fontsize=32, pad=214)
            axs[2, 1, 0, 0].remove()
            ax = axs[3, 1, 0, 0]
            ax.set_axes_locator(None)
            n = 1
            ax.set_position(((2.5 + 4.0 + 0.75)/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315))
            add_ticklabels_ax(ax, ["", "", ""], ticklabels_x)

